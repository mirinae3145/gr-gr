#!/usr/bin/env python3
"""Inspect, select, and safely update Graft v1 symbol summaries (stdlib only)."""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

PAYLOAD_VERSION = 1
SYMBOL_KINDS = {
    "function", "method", "class", "type", "interface", "enum", "struct",
    "trait", "variable", "constant", "module", "namespace",
}
STATES = {"pending", "stale", "ready"}
HASH = re.compile(r"[0-9a-f]{64}\Z")
SPAN = re.compile(r"L([1-9][0-9]*)(?:-L([1-9][0-9]*))?\Z")


class SummaryError(Exception):
    """A validation failure with no graph update."""


def require(condition, message):
    if not condition:
        raise SummaryError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    try:
        text = sys.stdin.read() if str(path) == "-" else Path(path).read_text(encoding="utf-8")
        return json.loads(text)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SummaryError("Cannot read JSON input: " + str(exc)) from exc


def atomic_json(path, value, mode=0o600, before_replace=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        if before_replace:
            before_replace()
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def emit(value, output=None):
    if output:
        atomic_json(output, value)
    else:
        print(json.dumps(value, ensure_ascii=False, indent=2))


def read_source(path):
    raw = path.read_bytes()
    require(not raw.startswith(b"\xfe\xff"), "UTF-16BE source is unsupported; no summary written.")
    # Match Graft's source reader, retaining UTF-8 BOMs and CRLF line endings.
    try:
        return raw[2:].decode("utf-16le") if raw.startswith(b"\xff\xfe") else raw.decode("utf-8")
    except UnicodeError as exc:
        raise SummaryError("Unsupported source encoding: " + str(path)) from exc


class Graph:
    def __init__(self, repo, graph="graft/.graph/wiring.json"):
        self.repo = Path(repo).resolve()
        self.path = (self.repo / graph).resolve()
        require(self.path.is_relative_to(self.repo), "Graph must be inside the target repository.")
        try:
            self.raw = self.path.read_bytes()
            self.data = json.loads(self.raw)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SummaryError("Cannot read Graft graph; use an existing structural index: " + str(exc)) from exc
        require(isinstance(self.data, dict), "Unsupported graph shape; inspect the installed schema.")
        require(isinstance(self.data.get("meta"), dict) and self.data["meta"].get("version") == 1,
                "Unsupported graph version; re-check compatibility before writing.")
        require(isinstance(self.data.get("nodes"), list) and isinstance(self.data.get("edges"), list),
                "Graph requires nodes and edges arrays.")
        self.nodes = {}
        self.files = {}
        self.sources = {}
        for node in self.data["nodes"]:
            require(isinstance(node, dict), "Invalid graph node.")
            for field in ("id", "name", "kind", "path", "body_hash"):
                require(isinstance(node.get(field), str), "Node is missing a string field: " + field)
            require(node["id"] not in self.nodes, "Duplicate graph node ID: " + node["id"])
            require(HASH.fullmatch(node["body_hash"]), "Unsupported body hash for " + node["id"])
            require(node.get("summary_state") in STATES, "Unsupported summary state for " + node["id"])
            require(node.get("summary") is None or isinstance(node["summary"], str), "Invalid stored summary.")
            self.nodes[node["id"]] = node
            if node["kind"] == "file":
                require(node["path"] not in self.files, "Ambiguous file metadata: " + node["path"])
                self.files[node["path"]] = node

    def source(self, relative):
        if relative not in self.sources:
            parts = PurePosixPath(relative)
            require(not parts.is_absolute() and ".." not in parts.parts, "Unsafe source path.")
            path = (self.repo / relative).resolve()
            require(path.is_relative_to(self.repo), "Source resolves outside the repository: " + relative)
            require(relative in self.files, "Missing file hash metadata: " + relative)
            text = read_source(path)
            require(digest(text.encode("utf-8")) == self.files[relative]["body_hash"],
                    "Source differs from its graph file hash; run graft build and select again: " + relative)
            self.sources[relative] = text
        return self.sources[relative]

    def span(self, node):
        span = node.get("span")
        require(isinstance(span, str), "Unsupported source span field: " + node["id"])
        match = SPAN.fullmatch(span)
        require(match is not None, "Unsupported source span: " + node["id"])
        start, end = int(match[1]), int(match[2] or match[1])
        require(start <= end <= len(self.source(node["path"]).split("\n")),
                "Source span is out of bounds: " + node["id"])
        return start, end

    def assert_unchanged(self):
        require(self.path.read_bytes() == self.raw, "Graph changed concurrently; select again.")
        for relative, original in self.sources.items():
            require(read_source(self.repo / relative) == original,
                    "Source changed concurrently; rebuild and select again: " + relative)


def validate_summary(summary):
    require(isinstance(summary, str) and bool(summary.strip()), "Every applied summary must be nonempty.")
    summary = summary.strip()
    require("\n" not in summary and "\r" not in summary and len(summary) <= 1200,
            "A summary must be one concise line of at most 1200 characters.")
    return summary


def selection(graph, ids=(), paths=(), all_dirty=False, include_ready=False, source=False):
    require(ids or paths or all_dirty, "Select explicit IDs/paths, or deliberately use --all-dirty.")
    for node_id in ids:
        require(node_id in graph.nodes, "Unknown node ID: " + node_id)
        require(graph.nodes[node_id]["kind"] in SYMBOL_KINDS, "Only source symbols may be selected: " + node_id)
    normalized = [p.replace("\\", "/").removeprefix("./").rstrip("/") for p in paths]
    require(all(p and p != "." and ".." not in PurePosixPath(p).parts for p in normalized),
            "Use a repository-relative file or directory prefix.")
    selected = []
    for node in graph.data["nodes"]:
        if node["kind"] not in SYMBOL_KINDS:
            continue
        if ids and node["id"] not in ids:
            continue
        if normalized and not any(node["path"] == p or node["path"].startswith(p + "/") for p in normalized):
            continue
        if node["summary_state"] == "ready" and not include_ready:
            continue
        start, end = graph.span(node)
        entry = {key: node[key] for key in ("id", "name", "kind", "path", "span", "body_hash")}
        entry.update(source_hash=graph.files[node["path"]]["body_hash"],
                     summary_before=node.get("summary"), state_before=node["summary_state"], summary=None)
        if source:
            entry["source"] = "\n".join(graph.source(node["path"]).split("\n")[start - 1:end])
        selected.append(entry)
    return {"format_version": PAYLOAD_VERSION, "repository": str(graph.repo),
            "graph": str(graph.path.relative_to(graph.repo)), "graph_version": 1, "symbols": selected}


def validate_payload(graph, payload, summaries=False, replace_ready=False):
    require(isinstance(payload, dict) and payload.get("format_version") == PAYLOAD_VERSION,
            "Unsupported payload format.")
    require(payload.get("repository") == str(graph.repo) and payload.get("graph_version") == 1,
            "Payload belongs to another checkout or graph version.")
    require(payload.get("graph") == str(graph.path.relative_to(graph.repo)), "Payload graph path differs.")
    require(isinstance(payload.get("symbols"), list), "Payload needs a symbols array.")
    seen = set()
    changes = []
    for entry in payload["symbols"]:
        require(isinstance(entry, dict) and isinstance(entry.get("id"), str), "Invalid symbol payload.")
        node_id = entry["id"]
        require(node_id not in seen, "Duplicate payload ID: " + node_id)
        seen.add(node_id)
        node = graph.nodes.get(node_id)
        require(node is not None and node["kind"] in SYMBOL_KINDS, "Unknown or out-of-scope symbol: " + node_id)
        for key in ("path", "span", "body_hash", "kind"):
            require(entry.get(key) == node.get(key), "Symbol identity changed; select again: " + node_id)
        graph.span(node)
        require(entry.get("source_hash") == graph.files[node["path"]]["body_hash"],
                "Source snapshot changed; select again: " + node_id)
        summary = validate_summary(entry.get("summary")) if summaries else None
        # A successfully applied, identical payload is an idempotent no-op.
        if summaries and node["summary_state"] == "ready" and node.get("summary") == summary:
            continue
        require("summary_before" in entry and "state_before" in entry, "Missing prior-state snapshot.")
        require(entry["summary_before"] == node.get("summary") and entry["state_before"] == node["summary_state"],
                "Summary changed since selection: " + node_id)
        if summaries:
            require(node["summary_state"] != "ready" or replace_ready,
                    "Ready summary replacement needs --replace-ready: " + node_id)
            changes.append((node_id, summary))
    return changes


def apply_payload(graph, payload, replace_ready=False):
    lock_path = graph.path.with_name(graph.path.name + ".gr-gr.lock")
    try:
        lock_fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise SummaryError("Another gr-gr writer may be active; inspect the lock before retrying: " + str(lock_path)) from exc
    try:
        os.close(lock_fd)
        graph.assert_unchanged()
        changes = validate_payload(graph, payload, summaries=True, replace_ready=replace_ready)
        result = copy.deepcopy(graph.data)
        by_id = {node["id"]: node for node in result["nodes"]}
        for node_id, summary in changes:
            node = by_id[node_id]
            if node["summary_state"] == "stale" and "crux" in node:
                node["crux"] = None
            node["summary"] = summary
            node["summary_state"] = "ready"
        if changes:
            mode = stat.S_IMODE(graph.path.stat().st_mode)
            atomic_json(graph.path, result, mode=mode, before_replace=graph.assert_unchanged)
        return {"updated": len(changes), "unchanged": len(payload["symbols"]) - len(changes),
                "rebuild_required": bool(changes)}
    finally:
        lock_path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "select", "apply"):
        command = commands.add_parser(name)
        command.add_argument("--repo", required=True)
        command.add_argument("--graph", default="graft/.graph/wiring.json")
        if name == "select":
            command.add_argument("--id", action="append", default=[])
            command.add_argument("--path", action="append", default=[])
            command.add_argument("--all-dirty", action="store_true")
            command.add_argument("--include-ready", action="store_true")
            command.add_argument("--source", action="store_true")
            command.add_argument("--output")
        elif name == "apply":
            command.add_argument("--input", required=True)
            command.add_argument("--replace-ready", action="store_true")
    args = parser.parse_args()
    try:
        graph = Graph(args.repo, args.graph)
        if args.command == "inspect":
            symbols = [n for n in graph.nodes.values() if n["kind"] in SYMBOL_KINDS]
            emit({"graph_version": 1, "supported": True, "symbol_count": len(symbols),
                  "states": {s: sum(n["summary_state"] == s for n in symbols) for s in sorted(STATES)},
                  "node_fields": sorted({key for n in symbols for key in n}),
                  "excluded": "file nodes and concept maps"})
        elif args.command == "select":
            emit(selection(graph, args.id, args.path, args.all_dirty, args.include_ready, args.source), args.output)
        else:
            emit(apply_payload(graph, read_json(args.input), args.replace_ready))
        return 0
    except (SummaryError, OSError) as exc:
        print("gr-gr: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
