#!/usr/bin/env python3
"""
Claude Code Memory Writer Hook - Sandinas v1.3.0
Extracts session conclusions and writes to Serena MCP.
Runs after SubagentStop to capture learnings from completed work.
Compatible with Windows, Linux, and macOS.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Load input from stdin - be tolerant to errors
try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError, Exception):
    # No stdin or invalid JSON - just exit silently
    sys.exit(0)

session_id = input_data.get("session_id", "")
transcript_path = input_data.get("transcript_path", "")
hook_event_name = input_data.get("hook_event_name", "")

# Only process SubagentStop events
if hook_event_name != "SubagentStop":
    sys.exit(0)

def read_transcript(transcript_path):
    """Read and parse the transcript JSONL file"""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            return "\n".join(lines[-500:])  # Last 500 entries for context
    except Exception as e:
        print(f"Warning: Could not read transcript: {e}", file=sys.stderr)
        return ""

def get_project_name():
    """Get project name from current working directory folder name.

    Note: Using cwd folder name instead of git repo name because a project
    typically has multiple repos. The folder name better represents the
    project scope for memory management.
    """
    return Path.cwd().name

def extract_session_context(transcript_text):
    """
    Analyze transcript and extract key information.
    Returns a dict with project, context, conclusions, decisions, files.
    """
    # Create analysis prompt for the memory writer agent
    analysis_prompt = f"""Analyze this session transcript and extract Sandinas context:

TRANSCRIPT (last entries):
{transcript_text[:10000]}

Extract and return ONLY this JSON structure:
{{
  "project": "project name or 'Unknown'",
  "feature_type": "feature/fix/refactor/other",
  "feature_description": "brief description of what was worked on",
  "sandinas_context": {{
    "project": "Project name",
    "business_rule": "Business rule or feature",
    "architecture": "Architecture/flow modified",
    "data_model": "Data model changes or 'N/A'"
  }},
  "conclusions": [
    "key learning 1",
    "key learning 2"
  ],
  "decisions": [
    "technical decision 1 with reasoning"
  ],
  "key_files": [
    "path/to/file1",
    "path/to/file2"
  ],
  "tags": ["sandinas", "project", "feature-type", "component"]
}}

Be CONCISE. Focus on actionable conclusions and decisions."""
    return analysis_prompt

def format_memory_markdown(extracted_data):
    """Format extracted data as markdown for Serena memory"""
    now = datetime.now().strftime("%Y-%m-%d")
    project = extracted_data.get("project", "Unknown")
    feature_desc = extracted_data.get("feature_description", "Session")
    feature_type = extracted_data.get("feature_type", "other")

    title = f"{now} - {project} - {feature_desc}"

    md_parts = [
        f"# {title}",
        "",
        "## Contexto Sandinas",
    ]

    sandinas = extracted_data.get("sandinas_context", {})
    md_parts.extend([
        f"- **Proyecto:** {sandinas.get('project', 'Unknown')}",
        f"- **Regla de Negocio:** {sandinas.get('business_rule', 'Unknown')}",
        f"- **Arquitectura:** {sandinas.get('architecture', 'Unknown')}",
        f"- **Modelo de Datos:** {sandinas.get('data_model', 'N/A')}",
        "",
        "## Conclusiones",
    ])

    for conclusion in extracted_data.get("conclusions", []):
        md_parts.append(f"- {conclusion}")

    if extracted_data.get("decisions"):
        md_parts.extend(["", "## Decisiones Técnicas"])
        for decision in extracted_data.get("decisions", []):
            md_parts.append(f"- {decision}")

    if extracted_data.get("key_files"):
        md_parts.extend(["", "## Archivos Clave"])
        for file in extracted_data.get("key_files", []):
            md_parts.append(f"- `{file}`")

    tags = extracted_data.get("tags", [f"sandinas", project.lower(), feature_type])
    md_parts.extend([
        "",
        "## Tags",
        ", ".join(f"`{tag}`" for tag in tags),
    ])

    return title, "\n".join(md_parts)

# Main execution
transcript_text = read_transcript(transcript_path)

if not transcript_text:
    print("No transcript available for memory writing", file=sys.stderr)
    sys.exit(0)

project = get_project_name()
print(f"Memory writer: Processing session for project '{project}'", file=sys.stderr)

# The actual extraction and writing will be done by a parallel agent
# This script prepares the context and signals the intent
output = {
    "hookSpecificOutput": {
        "hookEventName": "SubagentStop",
        "additionalContext": f"""MEMORY WRITER REQUEST (Sandinas)
==============================
Project: {project}
Session: {session_id}

A memory writer agent should be launched in parallel to:
1. Analyze the completed session transcript
2. Extract Sandinas context, conclusions, and decisions
3. Write to Serena MCP using write_memory tool

The memory will be tagged with: sandinas, {project.lower()}, session-type

This runs in background and does not block the session flow."""
    }
}

print(json.dumps(output))
print(f"Memory writer request queued for project: {project}", file=sys.stderr)
sys.exit(0)
