#!/usr/bin/env python3
"""
Claude Code Context Saver - Sandinas Internal Version
Saves session context before compactation (PreCompact hook).
Extracts 4-point Sandinas context + user decisions + technical summary.
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
trigger = input_data.get("trigger", "manual")  # PreCompact: "manual" or "auto"
hook_event_name = input_data.get("hook_event_name", "")

# Only process PreCompact events
if hook_event_name != "PreCompact":
    sys.exit(0)

# Context storage path - .docs/sesiones/ in current working directory
cwd = Path.cwd()
sessions_dir = cwd / ".docs" / "sesiones"
sessions_dir.mkdir(parents=True, exist_ok=True)

# Generate session_id as yyyyMMddhhmm
formatted_session_id = datetime.now().strftime("%Y%m%d%H%M")
context_file = sessions_dir / f"sandinas-context-{formatted_session_id}.json"

def read_transcript(transcript_path):
    """Read and parse the transcript JSONL file"""
    if not transcript_path or not os.path.exists(transcript_path):
        return []

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            return [json.loads(line) for line in f if line.strip()]
    except Exception as e:
        print(f"Warning: Could not read transcript: {e}", file=sys.stderr)
        return []

def extract_context_from_transcript(transcript):
    """
    Extract Sandinas context from transcript.
    Returns dict with 4 points + user decisions + technical summary.
    """
    # Build a summary from transcript for LLM extraction
    # Extract key events: user prompts, tool uses, askUserQuestion responses
    key_events = []

    for entry in transcript:
        if isinstance(entry, dict):
            # User messages/prompts
            if entry.get("role") == "user":
                content = entry.get("content", "")
                if content and not content.startswith("PROMPT EVALUATION"):
                    key_events.append(f"USER: {content[:200]}...")

            # Assistant messages with tool calls or decisions
            elif entry.get("role") == "assistant":
                content = entry.get("content", "")
                if content:
                    # Look for AskUserQuestion or important decisions
                    if "AskUserQuestion" in str(entry.get("toolCalls", [])):
                        key_events.append(f"ASSISTANT: Asked user question")
                    # Look for tool uses
                    for tool_call in entry.get("toolCalls", []):
                        tool_name = tool_call.get("name", "")
                        key_events.append(f"TOOL: {tool_name}")

    # Create prompt for extraction (will be processed by hook runner)
    extraction_prompt = f"""
EXTRACT Sandinas context from this session summary:

Session Events:
{chr(10).join(key_events[-50:])}  # Last 50 events

Extract and return ONLY this JSON structure:
{{
  "sandinas_context": {{
    "project": "Project name or 'Unknown'",
    "business_rule": "Business rule/feature or 'Unknown'",
    "architecture": "Architecture/flow modified or 'Unknown'",
    "data_model": "Data model changes or 'N/A'"
  }},
  "user_decisions": [
    {{"timestamp": "approximate time", "decision": "what user decided", "context": "why"}}
  ],
  "technical_summary": {{
    "errors_resolved": ["error: solution (one line each)"],
    "todos_found": ["file:line - todo"],
    "key_files": ["path1", "path2", "path3"]
  }}
}}

Keep it SUPER CONCISE. Prioritize user decisions over technical details.
"""

    # Return the extraction prompt - this will be processed by the prompt-based hook
    return extraction_prompt

# Read transcript
transcript = read_transcript(transcript_path)

# Create context structure
context_data = {
    "session_id": formatted_session_id,
    "original_session_id": session_id,
    "trigger": trigger,
    "created_at": datetime.now().isoformat(),
    "transcript_entry_count": len(transcript),
    # The actual context will be extracted by prompt-based hook
    "extraction_prompt": extract_context_from_transcript(transcript)
}

# Save context to file
try:
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context_data, f, indent=2, ensure_ascii=False)
    print(f"Context saved to: {context_file}", file=sys.stderr)
except Exception as e:
    print(f"Error saving context: {e}", file=sys.stderr)
    sys.exit(1)

# Return additionalContext confirming save
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreCompact",
        "additionalContext": f"CONTEXT SAVED: Session context saved for restoration after compact. Session ID: {formatted_session_id}"
    }
}
print(json.dumps(output))
sys.exit(0)
