#!/usr/bin/env python3
"""
Claude Code Memory Reader Hook - Sandinas v1.3.0
Searches Serena for relevant project memories when plan mode is detected.
Provides context from previous sessions before creating a new plan.
Compatible with Windows, Linux, and macOS.
"""
import json
import sys
from pathlib import Path

# Load input from stdin - be tolerant to errors
try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError, Exception):
    # No stdin or invalid JSON - just exit silently
    sys.exit(0)

prompt = input_data.get("prompt", "")
hook_event_name = input_data.get("hook_event_name", "UserPromptSubmit")

# Only process UserPromptSubmit events
if hook_event_name != "UserPromptSubmit":
    # Pass through unchanged for other events
    output = {
        "hookSpecificOutput": {
            "hookEventName": hook_event_name,
            "additionalContext": prompt
        }
    }
    print(json.dumps(output))
    sys.exit(0)

def get_project_name():
    """Get project name from current working directory folder name."""
    return Path.cwd().name

def detect_plan_mode(prompt_text):
    """Detect if the user is entering plan mode."""
    plan_keywords = [
        "plan", "diseñar", "implementar", "arquitectura",
        "feature", "como hacer", "how to", "design"
    ]
    prompt_lower = prompt_text.lower()
    return any(keyword in prompt_lower for keyword in plan_keywords)

def output_json(text):
    """Output text in UserPromptSubmit JSON format"""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))

# Check bypass conditions
if prompt.startswith("*") or prompt.startswith("/") or prompt.startswith("#"):
    output_json(prompt)
    sys.exit(0)

project = get_project_name()

# Detect plan mode
if detect_plan_mode(prompt):
    # Wrap prompt with memory search request
    wrapped_prompt = f"""MEMORY READER REQUEST (Sandinas)
=================================
Project: {project}
Plan mode detected

The user is entering plan mode. Before creating the plan:

1. Search Serena MCP for memories related to project '{project}'
   - Use query: "{project}" sandinas
   - Look for tags: `sandinas`, `{project.lower()}`
   - No time limit - prioritize most recent memories

2. If memories are found, present them to the user:
   "He encontrado {{numero}} memorias previas del proyecto '{project}'. ¿Deseas agregar estas conclusiones al contexto del plan que estás creando?"

3. If user agrees, include the memories as additional context

4. Proceed with the original plan request after memory context is resolved

ORIGINAL USER REQUEST:
{prompt}

Remember: This memory search helps leverage previous learnings and decisions."""
    output_json(wrapped_prompt)
    print(f"Memory reader: Plan mode detected for project '{project}'", file=sys.stderr)
else:
    # Not plan mode - pass through original prompt
    output_json(prompt)

sys.exit(0)
