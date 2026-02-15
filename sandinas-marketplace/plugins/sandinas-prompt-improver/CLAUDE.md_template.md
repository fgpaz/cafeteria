# [Nombre Proyecto]

## Agents
backend: sandinas-dotnet-backend
frontend: react-editor-pro
ts: typescript-pro

## MCP
postgres: local DB queries
postgres-vps: production DB (172.238.197.75)
shadcn: UI components
serena: code navigation (priority #1)

## Custom Tools
kill-backend: taskkill /F /IM dotnet.exe

---
# FORMATO SIMPLIFICADO CLAUDE.md
#
# Este formato minimalista usa pocos tokens y es facil de mantener.
#
# Secciones:
# ## Agents - Lista agentes especializados (key: nombre_agente)
# ## MCP - Lista servidores MCP disponibles (key: uso)
# ## Custom Tools - Tools personalizadas del proyecto (key: comando)
#
# Ejemplo completo:
#
# ## Agents
# backend: sandinas-dotnet-backend    # Para .NET/C#
# frontend: react-editor-pro          # Para React/Next.js
# ts: typescript-pro                  # Para TypeScript
#
# ## MCP
# postgres: local DB queries          # Queries base local
# serena: code navigation (priority #1) # Navegacion codigo
#
# ## Custom Tools
# kill-backend: taskkill dotnet       # Detener backend
