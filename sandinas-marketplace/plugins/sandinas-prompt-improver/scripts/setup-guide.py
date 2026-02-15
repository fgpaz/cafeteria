#!/usr/bin/env python3
"""
Sandinas Prompt Improver - Setup Guide
Shows configuration instructions when plugin is first installed.
"""
import json
import os
import sys
from pathlib import Path


def check_llm_config():
    """Check if LLM is configured."""
    # Check if .env file exists
    plugin_root = Path(__file__).parent.parent
    env_file = plugin_root / ".env"

    if not env_file.exists():
        return {"configured": False, "reason": "no_env_file"}

    # Check if API key is set
    env_content = env_file.read_text(encoding="utf-8")
    if "ZHIPUAI_API_KEY" not in env_content:
        return {"configured": False, "reason": "no_api_key"}

    # Check if API key has a value (not just placeholder)
    for line in env_content.splitlines():
        if line.startswith("ZHIPUAI_API_KEY="):
            value = line.split("=", 1)[1].strip()
            if not value or value in ["your_api_key_here", "YOUR_API_KEY_HERE"]:
                return {"configured": False, "reason": "placeholder_key"}
            return {"configured": True, "reason": "ok"}

    return {"configured": False, "reason": "no_api_key"}


def check_zhipuai_installed():
    """Check if zhipuai package is installed."""
    try:
        import zhipuai
        return True
    except ImportError:
        return False


def output_setup_guide():
    """Output setup guide as additionalContext."""
    plugin_root = Path(__file__).parent.parent

    guide = f"""
<sandinas_setup_guide>
Sandinas Prompt Improver v1.5.0 - Configuración LLM
====================================================

Estado actual: LLM no configurado (usando modo regex-only)

¿Qué es el modo LLM?
- El modo LLM usa zhipu AI (glm-4-flash, GRATIS) para detectar mejor el contexto vago
- Sin LLM: clasificación basada solo en patrones regex (funciona bien para casos obvios)
- Con LLM: validación inteligente del contexto Sandinas (4 puntos)

Pasos para habilitar LLM:
========================

1. Instalar dependencia:
   pip install zhipuai
   # O con pipx:
   pipx inject claude-code zhipuai

2. Configurar API key:
   cd "{plugin_root}"
   cp .env.example .env

3. Obtener API key gratuita en:
   https://open.bigmodel.cn/

4. Editar .env y agregar:
   ZHIPUAI_API_KEY=tu_api_key_aqui

El modelo glm-4-flash-250414 es GRATIS - sin costo por uso.

¿Quieres configurar LLM ahora?
------------------------------
Si responds "si", te guiare paso a paso.
Si prefieres usar solo regex, responde "no" y el plugin funcionara normalmente.

Más info: Ver README.md del plugin
</sandinas_setup_guide>
"""

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": guide.strip()
        }
    }
    print(json.dumps(output))


def output_configured_status():
    """Output message when LLM is configured."""
    guide = """
<sandinas_setup_guide>
Sandinas Prompt Improver v1.5.0 - Listo
========================================

Estado: LLM configurado y activo

Modo híbrido activo:
- Regex fast path para casos obvios (claro/vago)
- LLM (zhipu AI) para casos borderline
- Clasificación en tiempo real de cada prompt

Logs de clasificación:
- Source: regex → Fast path, sin LLM
- Source: llm → Validación con LLM
- Source: regex_fallback → LLM no disponible, usando regex

¡Listo para trabajar!
</sandinas_setup_guide>
"""

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": guide.strip()
        }
    }
    print(json.dumps(output))


def main():
    """Main entry point."""
    llm_status = check_llm_config()
    zhipuai_installed = check_zhipuai_installed()

    # Only show guide if .env doesn't exist or API key not set
    if not llm_status["configured"]:
        output_setup_guide()
    elif zhipuai_installed:
        output_configured_status()
    else:
        # .env exists but zhipuai not installed - brief reminder
        output_configured_status()


if __name__ == "__main__":
    main()
