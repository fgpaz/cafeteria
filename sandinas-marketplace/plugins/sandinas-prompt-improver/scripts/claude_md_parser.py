#!/usr/bin/env python3
"""
CLAUDE.md Parser for prompt-improver plugin.

Extracts custom agents, MCP tools, and custom tools from CLAUDE.md files.
Supports both simplified format (key:value) and verbose markdown tables.
"""

import re
from pathlib import Path
from typing import Dict, Optional


def parse_simple_claude_md(content: str) -> Dict:
    """
    Parse simplified CLAUDE.md format with key:value pairs.

    Format:
        ## Agents
        backend: sandinas-dotnet-backend
        frontend: react-editor-pro

        ## MCP
        postgres: local DB queries
        serena: code navigation

        ## Custom Tools
        kill-backend: taskkill dotnet

        ## Context Files
        spec.md: Especificación del proyecto
        architecture.md: Documentación de arquitectura
    """
    result = {"agents": {}, "mcp": {}, "custom_tools": {}, "context_files": {}}
    current_section = None

    for line in content.splitlines():
        line = line.strip()

        # Skip empty lines and headers (but keep section headers)
        if not line:
            continue
        if line.startswith("#") and not line.startswith("##"):
            continue

        # Detect section headers
        if line == "## Agents" or line == "## Agentes":
            current_section = "agents"
        elif line == "## MCP" or line == "## Mcp" or line == "## mcp":
            current_section = "mcp"
        elif line == "## Custom Tools" or line == "## CustomTools" or line == "## Herramientas":
            current_section = "custom_tools"
        elif line == "## Context Files" or line == "## ContextFiles" or line == "## context files" or line == "## Archivos de Contexto":
            current_section = "context_files"
        elif line.startswith("##") and current_section:
            # Different section - reset
            current_section = None
        elif ":" in line and current_section:
            # Parse key: value pairs
            key, value = line.split(":", 1)
            result[current_section][key.strip()] = value.strip()

    return result


def parse_verbose_claude_md(content: str) -> Dict:
    """
    Parse verbose CLAUDE.md format with markdown tables.

    Extracts from tables like:
    | MCP | Uso | Cuando usarlo |
    |-----|-----|---------------|
    | postgres | Queries | Debugging |
    """
    result = {"agents": {}, "mcp": {}, "custom_tools": {}, "context_files": {}}

    lines = content.splitlines()
    i = 0

    # Find and parse markdown tables
    while i < len(lines):
        line = lines[i].strip()

        # Look for table start (header row with pipes)
        if not line.startswith("|"):
            i += 1
            continue

        # Check if next line is separator
        if i + 1 < len(lines) and "---" in lines[i + 1]:
            # This is a table header
            headers = [h.strip().lower() for h in line.split("|")[1:-1]]

            # Skip separator line
            i += 2

            # Determine table type based on headers
            is_agents_table = any(kw in " ".join(headers) for kw in ["agente", "agent", "tarea", "task"])
            is_mcp_table = any(kw in " ".join(headers) for kw in ["mcp", "herramienta", "tool"])

            # Find which column has the values (backtick patterns)
            value_col_idx = -1
            desc_col_idx = -1

            if is_agents_table or is_mcp_table:
                # Find column with backtick content or key names
                for idx, h in enumerate(headers):
                    if any(kw in h for kw in ["agente", "agent", "mcp", "tool"]):
                        value_col_idx = idx
                    elif any(kw in h for kw in ["uso", "descripcion", "desc", "cuando"]):
                        desc_col_idx = idx

            # Read data rows
            while i < len(lines):
                row_line = lines[i].strip()
                if not row_line.startswith("|"):
                    break

                cells = [c.strip() for c in row_line.split("|")[1:-1]]

                # Skip empty rows or separators
                if not cells or all(c in ["", ""] for c in cells):
                    i += 1
                    continue

                # Extract based on table type
                if is_agents_table and len(cells) > value_col_idx:
                    value_cell = cells[value_col_idx] if value_col_idx >= 0 else cells[-1]
                    desc_cell = cells[desc_col_idx] if desc_col_idx >= 0 and desc_col_idx < len(cells) else cells[0]

                    # Extract agent name from backticks
                    agent_match = re.search(r"`([^`]+)`", value_cell)
                    if agent_match:
                        agent_name = agent_match.group(1)
                        result["agents"][agent_name] = desc_cell[:100] if desc_cell else "Especialista"

                elif is_mcp_table and len(cells) >= 2:
                    # First non-header column usually has MCP name
                    for cell in cells:
                        # Look for MCP names (bold, italic, or plain text)
                        mcp_match = re.search(r"\*?\*?([a-zA-Z][a-zA-Z0-9-]+)\*?\*?", cell)
                        if mcp_match:
                            mcp_name = mcp_match.group(1)
                            # Skip common header words
                            if mcp_name.lower() not in ["uso", "cuando", "descripcion", "herramienta", "mcp"]:
                                # Get description from another cell or rest of cell
                                desc = re.sub(r"\*?\*?[a-zA-Z][a-zA-Z0-9-]+\*?\*?", "", cell).strip()
                                desc = re.sub(r"\s+", " ", desc)
                                if not desc:
                                    # Try to get description from another cell
                                    for other_cell in cells:
                                        if other_cell and other_cell != cell:
                                            desc_candidate = re.sub(r"`[^`]+`", "", other_cell).strip()
                                            if desc_candidate and desc_candidate != mcp_name:
                                                desc = desc_candidate[:100]
                                                break
                                result["mcp"][mcp_name] = desc[:100] if desc else "MCP tool"
                                break

                i += 1
        else:
            i += 1

    # Also look for section headers with bullet lists
    current_section = None
    for line in lines:
        line_stripped = line.strip()

        if "### Agentes Especializados" in line_stripped or "## Uso OBLIGATORIO" in line_stripped:
            current_section = "agents"
        elif "### Herramientas MCP" in line_stripped or "## Herramientas MCP" in line_stripped:
            current_section = "mcp"
        elif line_stripped.startswith("###") or line_stripped.startswith("##"):
            if "Agent" not in line_stripped and "MCP" not in line_stripped:
                current_section = None

        # Parse bullet points with colon pattern
        if current_section and line_stripped.startswith("-"):
            bullet_content = line_stripped[1:].strip()
            # Look for patterns like: `- postgres: description`
            match = re.match(r"^(`?[\w-]+`?):\s*(.+)$", bullet_content)
            if match:
                key = match.group(1).strip("`")
                value = match.group(2).strip()
                result[current_section][key] = value

    return result


def parse_claude_md(cwd: Path, filename: str = "CLAUDE.md") -> Dict:
    """
    Main parser function. Reads CLAUDE.md from current directory.

    Args:
        cwd: Current working directory
        filename: Name of the file to read (default: CLAUDE.md)

    Returns:
        Dictionary with keys: agents, mcp, custom_tools, context_files
    """
    claude_md_path = cwd / filename

    if not claude_md_path.exists():
        return {"agents": {}, "mcp": {}, "custom_tools": {}, "context_files": {}, "found": False}

    try:
        content = claude_md_path.read_text(encoding="utf-8")
    except Exception:
        return {"agents": {}, "mcp": {}, "custom_tools": {}, "context_files": {}, "found": False}

    # Try simplified format first
    result = parse_simple_claude_md(content)

    # If simplified didn't find much, try verbose parsing
    total_found = len(result["agents"]) + len(result["mcp"]) + len(result["custom_tools"]) + len(result["context_files"])
    if total_found == 0:
        verbose_result = parse_verbose_claude_md(content)
        # Merge results
        for key in ["agents", "mcp", "custom_tools", "context_files"]:
            result[key].update(verbose_result[key])

    result["found"] = True
    return result


def build_agents_xml(agents: Dict[str, str]) -> Optional[str]:
    """Build XML section for custom agents."""
    if not agents:
        return None

    lines = ["<custom_agents>", "Para este proyecto, usar agentes especializados:"]
    for key, desc in agents.items():
        lines.append(f"- {key}: {desc}")
    lines.append("REGLA: Usar el agente correspondiente antes de editar codigo directamente.")
    lines.append("</custom_agents>")
    return "\n".join(lines)


def build_mcp_xml(mcp: Dict[str, str]) -> Optional[str]:
    """Build XML section for MCP tools."""
    if not mcp:
        return None

    lines = ["<available_mcp_tools>", "MCP servers disponibles:"]
    for key, desc in mcp.items():
        lines.append(f"- {key}: {desc}")
    lines.append("</available_mcp_tools>")
    return "\n".join(lines)


def build_tools_xml(tools: Dict[str, str]) -> Optional[str]:
    """Build XML section for custom tools."""
    if not tools:
        return None

    lines = ["<custom_tools>", "Tools personalizadas del proyecto:"]
    for key, desc in tools.items():
        lines.append(f"- {key}: {desc}")
    lines.append("</custom_tools>")
    return "\n".join(lines)


def build_context_files_xml(context_files: Dict[str, str]) -> Optional[str]:
    """Build XML section for context files."""
    if not context_files:
        return None

    lines = ["<context_files>", "Archivos de contexto del proyecto:"]
    for key, desc in context_files.items():
        lines.append(f"- {key}: {desc}")
    lines.append("REGLA: Consultar estos archivos para entender contexto del proyecto.")
    lines.append("</context_files>")
    return "\n".join(lines)


def build_parallel_strategy_xml(agents: Dict[str, str], mcp: Dict[str, str]) -> Optional[str]:
    """Build XML section for parallel execution strategy based on detected capabilities."""
    has_backend = any(k in str(agents).lower() for k in ["backend", "dotnet", ".net", "api"])
    has_frontend = any(k in str(agents).lower() for k in ["frontend", "react", "next", "ui", "tsx"])
    has_multiple_mcp = len(mcp) > 1

    if not (has_backend and has_frontend) and not has_multiple_mcp:
        return None

    lines = ["<parallel_execution_strategy>", "Para tareas largas o multi-componente:"]

    if has_backend and has_frontend:
        lines.append("- Si hay tareas backend + frontend: lanzar agentes en paralelo")
    if has_multiple_mcp:
        lines.append("- Si hay múltiples MCP queries: ejecutar en paralelo")
    lines.append("- Sincronizar resultados antes de presentar al usuario")
    lines.append("</parallel_execution_strategy>")
    return "\n".join(lines)


def build_orchestration_xml(agents: Dict[str, str] = None) -> str:
    """Build XML section with orchestration strategy for parallel agent execution.

    ALWAYS returns XML - if no specific agents defined, uses default agents.
    """
    # Use default agents if none provided
    if not agents:
        agents = {
            "general": "general-purpose",
            "dev": "feature-dev"
        }

    # Build list of agent types available
    agent_list = "\n".join([f"  - {k}: {v}" for k, v in agents.items()])

    return f"""<orchestration_strategy>
ERES EL ORQUESTADOR. Tu sesion principal coordina, los sub-agentes ejecutan.

REGLAS DE PARALELIZACION:
-------------------------
1. Lanzar TODAS las Task calls en UN SOLO MENSAJE para ejecucion en paralela
2. Si hay multiples tareas del MISMO tipo, lanzar multiples agentes de ese tipo
3. Cada tarea independiente = un agente paralelo
4. Esperar a que TODOS terminen antes de consolidar resultados

AGENTES DISPONIBLES:
{agent_list}

EJEMPLO DE UN MENSAJE CON MULTIPLES AGENTES (MISMO TIPO):
-----------------------------------------------------------
Si el usuario pide "crear 5 componentes de UI", lanza:

Task(frontend, "Crear ComponentA")
Task(frontend, "Crear ComponentB")
Task(frontend, "Crear ComponentC")
Task(frontend, "Crear ComponentD")
Task(frontend, "Crear ComponentE")

(5 agentes del mismo tipo en UN SOLO MENSAJE = paralelo)

NO HAGAS:
- No lanzar agentes secuencialmente (uno, esperar, siguiente)
- No agrupar tareas no relacionadas en el mismo agente
</orchestration_strategy>"""


if __name__ == "__main__":
    import sys

    # Test parser with sample content or file argument
    if len(sys.argv) > 1:
        # Parse file from argument
        test_file = Path(sys.argv[1])
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            result = parse_simple_claude_md(content)

            # If simple format didn't find much, try verbose
            total_found = len(result["agents"]) + len(result["mcp"]) + len(result["custom_tools"])
            if total_found == 0:
                result = parse_verbose_claude_md(content)

            print(f"Found: {total_found + len(result.get('agents', {})) + len(result.get('mcp', {})) + len(result.get('custom_tools', {}))} items")
            print("Agents:", result.get("agents", {}))
            print("MCP:", result.get("mcp", {}))
            print("Custom Tools:", result.get("custom_tools", {}))

            # Show XML output
            print()
            print("=== XML Output ===")
            if result.get("agents"):
                print(build_agents_xml(result["agents"]))
            if result.get("mcp"):
                print(build_mcp_xml(result["mcp"]))
            if result.get("custom_tools"):
                print(build_tools_xml(result["custom_tools"]))
            if result.get("agents") or result.get("mcp"):
                print(build_parallel_strategy_xml(result.get("agents", {}), result.get("mcp", {})))
            if result.get("agents"):
                print(build_orchestration_xml(result["agents"]))
        else:
            print(f"File not found: {test_file}")
    else:
        # Default test with sample content
        sample = """
# Test Project

## Agents
backend: sandinas-dotnet-backend
frontend: react-editor-pro

## MCP
postgres: local DB
serena: code nav

## Custom Tools
kill-backend: taskkill dotnet
"""
        result = parse_simple_claude_md(sample)
        print("Agents:", result["agents"])
        print("MCP:", result["mcp"])
        print("Custom Tools:", result["custom_tools"])
