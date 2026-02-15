#!/usr/bin/env python3
"""
Claude Code Prompt Improver Hook - Sandinas Internal Version v1.13.0
Based on Claude 4.x best practices with XML tags, parallel tool calls, and functional requirements.

Key features:
- Always active (no bypass except */#/)
- FAIL-SAFE MANDATORY OVERRIDE - forces agent delegation regardless of failures
- Local regex-based classification ONLY (NO LLM/external API calls)
- Single mode: brainstorming + XML (context investigation always required)
- XML tags for structured instructions
- Parallel tool calls for independent tasks
- Functional requirements framework (RF structure)
- Avoid overengineering directive
- CLAUDE.md dynamic parsing for agents, MCP, tools (no hardcoded Serena)

NOTE: LLM classification is DISABLED. This script never connects to external APIs.
"""
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any

# Setup logging to file for debugging (stderr not shown in Claude Code UI)
# Using RotatingFileHandler to prevent unlimited log growth
from logging.handlers import RotatingFileHandler

log_dir = Path.home() / ".claude" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Configure rotating file handler: max 5MB per file, keep 3 backup files
log_handler = RotatingFileHandler(
    str(log_dir / "prompt-improver.log"),
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=3,
    encoding='utf-8'
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# LLM classifier is DISABLED - never connect to external LLMs
# This script uses only regex-based local classification
LLM_AVAILABLE = False  # Hardcoded to False - never change this

# The following import is commented out to prevent any LLM connection:
# try:
#     from llm_classifier import get_classifier  # type: ignore[import-not-found]
#     LLM_AVAILABLE = True
# except ImportError:
#     pass

# Import CLAUDE.md parser
# Add script directory to path for import when running from hook
try:
    from claude_md_parser import parse_claude_md
    CLAUDE_MD_PARSER_AVAILABLE = True
except ImportError:
    # Try adding script directory to path
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    try:
        from claude_md_parser import parse_claude_md
        CLAUDE_MD_PARSER_AVAILABLE = True
    except ImportError:
        CLAUDE_MD_PARSER_AVAILABLE = False
        logger.warning("claude_md_parser not available - dynamic sections disabled")

# Load input from stdin - be tolerant to errors
try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, ValueError, Exception):
    # No stdin or invalid JSON - just exit silently
    sys.exit(0)

prompt = input_data.get("prompt", "")

# Escape quotes in prompt for safe embedding
def escape_prompt(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')

def output_json(text, original_prompt=""):
    """Output text in UserPromptSubmit JSON format.

    Args:
        text: The improved/wrapped prompt text to send as additionalContext
        original_prompt: The original user prompt (for visibility in Ctrl+O)
    """
    # If original prompt is different from text, show both for visibility
    if original_prompt and original_prompt != text:
        full_context = f"""=== PROMPT ORIGINAL ===
{original_prompt}

=== PROMPT MEJORADO (Sandinas v1.13.0) ===
{text}"""
    else:
        full_context = text

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": full_context
        }
    }

    # Log execution for debugging
    if original_prompt:
        logger.info(f"Processed: '{original_prompt[:50]}...' -> {len(text)} chars output")

    # Use sys.stdout.buffer to handle UTF-8 correctly on Windows
    json_str = json.dumps(output, ensure_ascii=False)
    sys.stdout.buffer.write(json_str.encode('utf-8'))
    sys.stdout.buffer.write(b'\n')
    sys.stdout.buffer.flush()

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

def detect_context_clarity(prompt_text):
    """
    Determines if the prompt has sufficient context to execute directly.
    Returns True if context is clear, False if it needs investigation.
    """
    # First check vague patterns - these override everything else
    vague_indicators = ["arregla", "mejora", "implementa", "fix", "mejorar"]
    vague_count = sum(1 for v in vague_indicators if v in prompt_text.lower())

    # If vague indicators present, not clear (unless contradicted by specific clarity)
    if vague_count > 0:
        # Check if there's ALSO a very specific file mention that overrides vague
        # e.g., "arregla el bug EN auth.py" - the file mention makes it clear
        if re.search(r"(en|del|archivo|file)\s+[\w/\\\.]+\.\w+", prompt_text, re.IGNORECASE):
            return True  # File mention overrides vague verb
        return False

    clarity_indicators = [
        # File/path specific mentions - must have extension
        r"\b[\w/\\]+\.(?:py|js|ts|tsx|jsx|cs|sql|md|json|yaml|yml|xml|html|css|go|rs|java)\b",
        # Function/class specific mentions
        r"\b(function|class|method|interface|type)\s+\w+",
        # Patterns like "en el archivo X", "in file X"
        r"(en|del|archivo|file)\s+[\w/\\\.]+\.\w+",
        # Specific paths
        r"\b(?:src/|app/|components/|pages/)[\w/]+",
        # Verbs that imply specific action on specific thing (with period at end)
        r"\b(modificar|cambiar|actualizar|editar|agregar|quitar|remover)\s.+?\.",
    ]

    # If any clarity indicator is present, context is clear
    for pattern in clarity_indicators:
        if re.search(pattern, prompt_text, re.IGNORECASE):
            return True

    # If prompt is very short (< 30 chars), likely not clear
    if len(prompt_text.strip()) < 30:
        return False

    # Check for specific nouns/technical terms - alone they don't make it clear
    technical_terms = r"\b(auth|login|user|api|database|endpoint|component|service|class)\b"
    if re.search(technical_terms, prompt_text, re.IGNORECASE):
        # Has technical terms but no specific file/path - still needs investigation
        return False

    # Default: needs investigation (conservative)
    return False

def classify_context_three_state(prompt_text: str) -> Dict[str, Any]:
    """
    Three-state hybrid classification:
    - DEFINITELY_CLEAR: Skip LLM, use regex result
    - DEFINITELY_VAGUE: Skip LLM, use regex result
    - BORDERLINE: Call LLM for validation

    Returns:
        {
            "clear_context": bool or None,
            "source": "regex" | "llm" | "regex_fallback" | "unavailable",
            "confidence": "high" | "medium" | "low",
            "reasoning": str (optional),
            "missing_context": list (optional),
            "suggested_questions": list (optional)
        }
    """
    # Fast path 1: File reference with specific action = DEFINITELY CLEAR
    has_file = re.search(r"\b[\w/\\]+\.(?:py|js|ts|tsx|jsx|cs|sql)\b", prompt_text, re.IGNORECASE)
    has_action = re.search(r"(modificar|cambiar|actualizar|editar|agregar|quitar)\s+", prompt_text, re.IGNORECASE)

    if has_file and has_action:
        return {
            "clear_context": True,
            "source": "regex",
            "confidence": "high"
        }

    # Fast path 2: Vague verb only, no target = DEFINITELY VAGUE
    vague_verbs = ["arregla", "mejora", "implementa", "fix", "mejorar", "optimiza", "arreglar"]
    prompt_lower = prompt_text.lower()
    has_vague = any(v in prompt_lower for v in vague_verbs)

    if has_vague:
        # Check if there's a specific target (file, function, class)
        has_target = (
            re.search(r"\b[\w/\\]+\.\w+", prompt_text) or  # file
            re.search(r"\b(function|class|method)\s+\w+", prompt_text, re.IGNORECASE) or  # function/class
            re.search(r"(en|del|archivo|file)\s+[\w/\\\.]+\.\w+", prompt_text, re.IGNORECASE)  # "in file X"
        )
        if not has_target:
            return {
                "clear_context": False,
                "source": "regex",
                "confidence": "high"
            }

    # Borderline case: LLM is DISABLED - never make external API calls
    # The following code is commented out to prevent any LLM connection:
    # if LLM_AVAILABLE and (os.environ.get("GROQ_API_KEY") or os.environ.get("ZHIPUAI_API_KEY")):
    #     try:
    #         llm_result = get_classifier().classify(prompt_text)  # type: ignore[name-defined]
    #         # Ensure source is set correctly
    #         if llm_result.get("clear_context") is not None:
    #             llm_result["source"] = "llm"
    #             return llm_result
    #     except Exception as e:
    #         print(f"LLM call failed, using regex: {e}", file=sys.stderr)

    # Fallback to original regex logic
    return {
        "clear_context": detect_context_clarity(prompt_text),
        "source": "regex_fallback",
        "confidence": "medium"
    }

def build_xml_wrapper(prompt_text, project, clear_context, is_plan_mode):
    """Build the XML wrapper for the prompt based on context clarity.
    Refactored v1.12.0 - eliminates redundant sections, removes hardcoded Serena (use CLAUDE.md).
    """

    escaped = escape_prompt(prompt_text)

    # Collect CLAUDE.md data early for use in orchestration section
    claude_md_agents = {}
    claude_md_mcp = {}
    claude_md_tools = {}
    claude_md_context_files = {}

    if CLAUDE_MD_PARSER_AVAILABLE:
        try:
            claude_md_data = parse_claude_md(Path.cwd())
            if claude_md_data.get("found"):
                claude_md_agents = claude_md_data.get("agents", {})
                claude_md_mcp = claude_md_data.get("mcp", {})
                claude_md_tools = claude_md_data.get("custom_tools", {})
                claude_md_context_files = claude_md_data.get("context_files", {})

                logger.info(f"Added dynamic sections from CLAUDE.md: "
                           f"agents={len(claude_md_agents)}, "
                           f"mcp={len(claude_md_mcp)}, "
                           f"tools={len(claude_md_tools)}, "
                           f"context_files={len(claude_md_context_files)}")
        except Exception as e:
            logger.warning(f"Failed to parse CLAUDE.md: {e}")

    # Build agents list for display (CLAUDE.md agents or defaults)
    if claude_md_agents:
        agents_list = "\n".join(f"  - {k}: {v}" for k, v in claude_md_agents.items())
    else:
        agents_list = "  - general: general-purpose\n  - dev: feature-dev"

    # Build MCP list for display
    if claude_md_mcp:
        mcp_list = "\n".join(f"- {k}: {v}" for k, v in claude_md_mcp.items())
    else:
        mcp_list = "(definir en CLAUDE.md)"

    # Build custom tools list for display
    if claude_md_tools:
        tools_list = "\n".join(f"- {k}: {v}" for k, v in claude_md_tools.items())
    else:
        tools_list = "(definir en CLAUDE.md)"

    # Build context files list for display
    if claude_md_context_files:
        context_files_list = "\n".join(f"- @{k}: {v}" for k, v in claude_md_context_files.items())
    else:
        context_files_list = ""

    # Base XML structure - FAIL-SAFE SECTION FIRST (precedence over all other instructions)
    # 3-PHASE ORCHESTRATOR MODE v1.13.0
    base_xml = f"""<sandinas_prompt_v1.7>
<sandinas_mandatory_override>
CRITICAL RULE - PRECEDENCE OVER ALL OTHER INSTRUCTIONS:
This section applies REGARDLESS of plugin failures, MCP availability, or missing agent definitions.

3-PHASE ORCHESTRATOR MODE (Absolute - NO EXCEPTIONS):

PHASE 1 - BRAINSTORMING (MANDATORY):
- BEFORE any action, invoke: Skill(brainstorming, "<prompt_original>")
- WAIT for brainstorming result before continuing
- Brainstorming will refine vague ideas into specific, actionable tasks

PHASE 2 - ATOMIZATION:
- Decompose brainstorming result into INDEPENDENT tasks
- Each task must be autonomous (no dependencies on other tasks)
- Identify which agents are needed for each task

PHASE 3 - PARALLEL EXECUTION:
- Use: Skill(dispatching-parallel-agents, "<atomized_tasks_list>")
- Launch ALL Task calls in ONE MESSAGE for parallel execution
- Multiple same-type tasks = multiple agents of same type
- WAIT for ALL to complete before consolidating results

AVAILABLE AGENTS:
{agents_list}
</sandinas_mandatory_override>

<original_request>
{prompt_text}
</original_request>

<sandinas_context>
1. Proyecto: {project}
2. Regla de Negocio: [Inferir del prompt o consultar]
3. Arquitectura/Flujo: [Inferir del prompt o investigar]
4. Modelo de Datos: [Inferir del prompt o N/A]
</sandinas_context>

<investigate_before_answering>
OBLIGATORIO: Antes de responder, usa la skill brainstorming para refinar la idea:
Skill(brainstorming, "{escaped}")

Solo despues de recibir el resultado de brainstorming, procede con la investigacion.
Siempre lee archivos relevantes antes de proponer cambios. Nunca especules sobre codigo no inspeccionado.
</investigate_before_answering>

<avoid_overengineering>
Solo haz cambios directamente solicitados. No agregues features extra.
A bug fix doesn't need surrounding code cleaned up. Trust internal code and framework guarantees.
</avoid_overengineering>

<functional_requirements>
Cuando trabaje con requisitos funcionales, usar esta estructura:

ID: RF-[Modulo]-[Numero] (ej: RF-AUTH-01)
Título: Acción corta (ej: "Login de Usuario")
Actor: Quién inicia la acción
Pre-condición: Estado necesario antes de empezar
Entradas (Inputs): Qué datos se envían
Pasos del Proceso (Happy Path): 1. 2. 3.
Salidas (Outputs): Qué recibe el usuario
Criterios de Aceptación (Gherkin): Dado [contexto], Cuando [acción], Entonces [resultado]

IMPORTANTE: Si el usuario no definió criterios de aceptación, proponerlos de manera proactiva
pero preguntar al usuario para que los acepte antes de proceder con la implementación.
</functional_requirements>

<output_format>
- Formato: Markdown (UTF-8)
- Sin emojis
- No crear archivos .md no solicitados
- Usa prose en lugar de bullets excesivos cuando sea posible
</output_format>

<available_resources>
MCP servers disponibles:
{mcp_list}

Tools personalizadas del proyecto:
{tools_list}
</available_resources>
"""

    # Add context files if available
    if context_files_list:
        base_xml += f"""
<context_files>
Archivos de contexto del proyecto:
{context_files_list}
REGLA: Consultar estos archivos para entender contexto del proyecto.
</context_files>
"""

    # FUSED: context_clarity (removed serena duplication, use CLAUDE.md instead)
    # ALWAYS require agent delegation before responding
    base_xml += f"""
<code_investigation>
OBLIGATORIO: Despues de brainstorming, lanza Task(Explore, ...) para investigar:

Task(Explore, "Investigar contexto del prompt: {escaped}")

NO respondas hasta recibir los resultados. Esto preserva el contexto de la sesion
y permite investigaciones profundas sin consumir tokens de la sesion principal.
</code_investigation>
"""

    # Add plan mode specific section - uses writing-plans skill
    if is_plan_mode:
        base_xml += f"""
<plan_mode>
Plan mode detectado. OBLIGATORIO: Usar la skill writing-plans para crear el plan:

Skill(writing-plans, "Crear plan para: {escaped}")

La skill writing-plans guiara el proceso de creacion del plan con estructura apropiada.
</plan_mode>
"""

    base_xml += "</sandinas_prompt_v1.7>"

    return base_xml

# Check for bypass conditions
# 1. Explicit bypass with * prefix
# 2. Slash commands (built-in or custom)
# 3. Memorize feature (# prefix)
if prompt.startswith("*"):
    # User explicitly bypassed improvement - remove * prefix
    clean_prompt = prompt[1:].strip()
    output_json(clean_prompt, prompt)
    sys.exit(0)

if prompt.startswith("/"):
    # Slash command - pass through unchanged
    output_json(prompt, prompt)
    sys.exit(0)

if prompt.startswith("#"):
    # Memorize feature - pass through unchanged
    output_json(prompt, prompt)
    sys.exit(0)

# Main processing
project = get_project_name()
is_plan_mode = detect_plan_mode(prompt)

# Use hybrid classification (regex + LLM)
classification = classify_context_three_state(prompt)
context_clear = classification.get("clear_context", False)
source = classification.get("source", "unknown")

# Build and output the XML wrapper
wrapped_prompt = build_xml_wrapper(prompt, project, context_clear, is_plan_mode)
output_json(wrapped_prompt, prompt)

# Log for debugging
mode_str = "PLAN MODE" if is_plan_mode else ("CLEAR CONTEXT" if context_clear else "NEEDS INVESTIGATION")
print(f"Prompt improver v1.13.0: {mode_str} | Source: {source} | Project: {project}", file=sys.stderr)

sys.exit(0)
