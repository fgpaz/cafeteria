#!/usr/bin/env python3
"""
Claude Code Context Loader - Sandinas Internal Version
Loads session context after compactation (SessionStart hook).
Compatible with Windows, Linux, and macOS.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import glob

# Load input from stdin - be tolerant to errors
try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError, Exception) as e:
    # No stdin or invalid JSON - just exit silently
    # This happens when hook is called without JSON input
    sys.exit(0)

session_id = input_data.get("session_id", "")
source = input_data.get("source", "startup")  # startup, resume, clear, compact
hook_event_name = input_data.get("hook_event_name", "")

# Only process SessionStart events from compact
if hook_event_name != "SessionStart" or source != "compact":
    sys.exit(0)

# Context storage path - .docs/sesiones/ in current working directory
cwd = Path.cwd()
sessions_dir = cwd / ".docs" / "sesiones"

def find_most_recent_context():
    """Find the most recent Sandinas context file by modification time"""
    if not sessions_dir.exists():
        return None

    pattern = str(sessions_dir / "sandinas-context-*.json")
    files = glob.glob(pattern)

    if not files:
        return None

    # Sort by modification time (most recently modified first)
    # This handles parallel sessions correctly - the active session is the most recently updated
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]

def load_context(file_path):
    """Load and format context from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract relevant information
        sandinas = data.get("sandinas_context", {})
        decisions = data.get("user_decisions", [])
        tech = data.get("technical_summary", {})

        # Build context summary
        context_parts = [
            "RESTORED CONTEXT (Sandinas)",
            "=" * 40,
        ]

        # 4-point Sandinas context
        if sandinas:
            context_parts.extend([
                f"1. Proyecto: {sandinas.get('project', 'Unknown')}",
                f"2. Regla de Negocio: {sandinas.get('business_rule', 'Unknown')}",
                f"3. Arquitectura/Flujo: {sandinas.get('architecture', 'Unknown')}",
                f"4. Modelo de Datos: {sandinas.get('data_model', 'N/A')}",
            ])

        # User decisions (prioritized)
        if decisions:
            context_parts.append("\nDecisiones del usuario:")
            for d in decisions[:5]:  # Max 5 decisions
                decision = d.get("decision", "")[:80]
                context_parts.append(f"  - {decision}")

        # Technical summary (brief)
        if tech:
            context_parts.append("\nResumen técnico:")
            if tech.get("key_files"):
                files_str = ", ".join(tech.get("key_files", [])[:5])
                context_parts.append(f"  Archivos: {files_str}")
            if tech.get("errors_resolved"):
                for err in tech.get("errors_resolved", [])[:3]:
                    context_parts.append(f"  - {err}")

        context_parts.append(f"\n(restoreado de sesion anterior: {data.get('created_at', 'unknown')})")

        return "\n".join(context_parts)

    except Exception as e:
        print(f"Warning: Could not load context: {e}", file=sys.stderr)
        return None

# Find and load context
context_file = find_most_recent_context()

if context_file:
    context = load_context(context_file)
    if context:
        # Return as additionalContext
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))
        print(f"Context loaded from: {context_file}", file=sys.stderr)
    else:
        print(f"Warning: Context file found but could not be parsed", file=sys.stderr)
else:
    print("No saved context found (first compact or context was cleared)", file=sys.stderr)

sys.exit(0)
