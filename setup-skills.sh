#!/bin/bash
# Setup de skills para el proyecto Cafeteria
# Ejecutar en cualquier computadora despues de hacer git pull
# Uso: bash setup-skills.sh

echo ""
echo "Instalando skills del proyecto cafeteria..."
echo ""

# Skills imprescindibles del proyecto
echo "--- Skills imprescindibles ---"

npx skills add wshobson/agents@startup-financial-modeling -g -y
npx skills add borghei/claude-skills@brand-strategist -g -y
npx skills add daffy0208/ai-dev-standards@brand-designer -g -y
npx skills add julianobarbosa/claude-code-skills@obsidian -g -y
npx skills add "jmsktm/claude-settings@Business Plan Writer" -g -y
npx skills add alirezarezvani/claude-skills@marketing-strategy-pmm -g -y

echo ""
echo "--- Skills recomendadas ---"

npx skills add "jmsktm/claude-settings@Hospitality Coordinator" -g -y
npx skills add ailabs-393/ai-labs-claude-skills@pitch-deck -g -y
npx skills add lyndonkl/claude@chef-assistant -g -y

echo ""
echo "--- Skills de uso general ---"

npx skills add anthropics/skills@xlsx -g -y

echo ""
echo "====================================="
echo "Skills instaladas."
echo "====================================="
echo ""
echo "INSTALACION MANUAL REQUERIDA:"
echo ""
echo "Los siguientes plugins de Claude Code deben instalarse manualmente:"
echo "  - sandinas-prompt-improver (incluye brainstorming, writing-clearly-and-concisely, dispatching-parallel-agents)"
echo ""
echo "Para instalar plugins, consultar la documentacion de Claude Code plugins."
echo ""
