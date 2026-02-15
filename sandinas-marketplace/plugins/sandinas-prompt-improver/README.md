# Sandinas Prompt Improver

Plugin interno de Claude Code para optimizar prompts con contexto especifico de Sandinas.

## Caracteristicas

- **Clasificacion hibrida**: Regex + LLM (Groq/ZhipuAI) para deteccion mejorada de contexto
- **Siempre activo**: Procesa todos los prompts con XML tags estructurados
- Basado en **Claude 4.x best practices**:
  - XML tags para instrucciones estructuradas
  - Paralelizacion de tareas independientes
  - Estructura de requisitos funcionales (RF)
  - Directiva "avoid overengineering"
  - Investigacion antes de responder
- **Integracion Serena MCP** para busqueda de contexto y memoria
- Compatible con Windows, Linux y macOS
- **Soporte multi-proveedor LLM**: Groq (primary) o ZhipuAI (fallback)

## Modos de Operacion

| Contexto | Comportamiento |
|----------|---------------|
| **Claro** | XML directo con instrucciones organizadas |
| **No claro** | Skill prompt-improver + XML + investigacion Serena |

## Instalacion

```bash
# 1. Agregar el marketplace de Sandinas
claude plugin marketplace add C:\repos\sandinas\sandinas-marketplace

# 2. Instalar el plugin
claude plugin install sandinas-prompt-improver@sandinas

# 3. Reiniciar Claude Code
```

## Configuracion LLM (Opcional)

El plugin funciona sin configuracion adicional (modo regex-only). Para habilitar la clasificacion LLM mejorada, puedes usar **Groq** (recomendado, free tier) o **ZhipuAI** (alternativa).

### Opcion 1: Groq (Recomendado - Free Tier)

**Paso 1: Instalar dependencia**

```bash
# Con pip (si Python esta instalado globalmente)
pip install groq

# Con pipx (si Claude Code usa pipx)
pipx inject claude-code groq
```

**Paso 2: Configurar API Key**

1. Crear archivo `.env` en el directorio del plugin:
```bash
cd C:\repos\sandinas\sandinas-marketplace\plugins\sandinas-prompt-improver
cp .env.example .env
```

2. Obtener API key gratuita en: https://console.groq.com/keys

3. Editar `.env` con tu API key:
```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_ENABLED=true
```

### Opcion 2: ZhipuAI (Alternativa - Requiere saldo)

**Paso 1: Instalar dependencia**

```bash
# Con pip
pip install zhipuai

# Con pipx
pipx inject claude-code zhipuai
```

**Paso 2: Configurar API Key**

1. Editar `.env` (creado en el paso anterior):
```
ZHIPUAI_API_KEY=your_api_key_here
ZHIPUAI_MODEL=glm-4.7
ZHIPUAI_ENABLED=true
```

2. Obtener API key en: https://open.bigmodel.cn/

### Prioridad de Proveedores

El plugin intentara usar los proveedores en este orden:
1. **Groq** (si `GROQ_API_KEY` esta configurada)
2. **ZhipuAI** (si `ZHIPUAI_API_KEY` esta configurada)
3. **Modo regex-only** (si ninguno esta configurado)

## Verificacion

```bash
# Test sin API key (funciona con regex)
echo '{"prompt": "arregla el bug"}' | python scripts/improve-prompt.py
# Output: Source: regex

# Test con API key Groq configurada
echo '{"prompt": "crear validacion"}' | python scripts/improve-prompt.py
# Output: Source: llm (si key configurada) o regex_fallback (sin key)
```

## Uso

El hook se ejecuta automaticamente en cada prompt. Los prompts se clasifican en tres categorias:

1. **Definitivamente claro** (file + accion) - Skip LLM, procesa directo
2. **Definitivamente vago** (verbo vago sin objetivo) - Skip LLM, pide aclaracion
3. **Borderline** - LLM valida contexto Sandinas (4 puntos)

### Contexto Sandinas (4 puntos)

1. **Proyecto**: ¿Que proyecto/codebase?
2. **Regla de Negocio**: ¿Que feature/requerimiento?
3. **Arquitectura/Flujo**: ¿Que parte del sistema?
4. **Modelo de Datos**: ¿Que entidades/campos?

## Ejemplos

### Prompt claro (file especifico + accion):
```
"modificar auth.py para agregar refresh token"
```
Output: `CLEAR CONTEXT | Source: regex`

### Prompt vago (verbo vago sin objetivo):
```
"arregla el bug"
```
Output: `NEEDS INVESTIGATION | Source: regex`

### Prompt borderline (requiere LLM si esta configurado):
```
"crear validacion de usuarios"
```
Output: `NEEDS INVESTIGATION | Source: llm` (con API key Groq/ZhipuAI) o `regex_fallback` (sin API key)

## Estructura

```
sandinas-prompt-improver/
├── .claude-plugin/
│   └── plugin.json          # Configuracion del plugin
├── scripts/
│   ├── improve-prompt.py    # Hook principal (clasificacion hibrida)
│   ├── llm-classifier.py    # Modulo LLM con Groq/ZhipuAI
│   ├── run_python.bat       # Wrapper para Windows
│   ├── memory-writer.py     # Guarda memorias en Serena
│   ├── memory-reader.py     # Carga memorias de Serena
│   ├── cleanup-sessions.py  # Limpia archivos de sesion antiguos
│   ├── context-saver.py     # Guarda contexto antes de compactar
│   ├── context-loader.py    # Carga contexto despues de compactar
│   └── test-hook.py         # Script de prueba
├── skills/
│   └── prompt-improver/     # Skill para mejora de prompts
├── hooks/
│   └── hooks.json           # Configuracion de hooks
├── .env.example             # Template para API keys (Groq/ZhipuAI)
└── README.md                # Este archivo
```

## Proveedores LLM Soportados

| Proveedor | Modelo | Cost | Estado |
|-----------|--------|------|--------|
| **Groq** | llama-3.3-70b-versatile | Free tier disponible | **Primary** |
| ZhipuAI | glm-4.7 | Requiere saldo | Fallback |
| (ninguno) | - | - | Regex-only |

## Troubleshooting

**LLM mode not working?**

1. Verificar que el SDK este instalado:
   ```bash
   pip show groq   # Para Groq
   pip show zhipuai   # Para ZhipuAI
   ```

2. Verificar que la API key existe:
   ```bash
   cat .env | grep API_KEY
   ```

3. Reiniciar Claude Code despues de configurar la API key

4. El plugin cae automaticamente a modo regex si LLM no esta disponible

## Mantenimiento y Limpieza

El plugin crea dos tipos de archivos que requieren mantenimiento:

### 1. Archivos de Sesion (.docs/sesiones/)

**Ubicacion**: `[proyecto]/.docs/sesiones/sandinas-context-YYYYMMDDhhmm.json`

El hook PreCompact guarda el contexto de la sesion antes de compactar. Estos archivos se acumulan con el tiempo.

### 2. Log de Actividad

**Ubicacion**: `~/.claude/logs/prompt-improver.log`

El log ahora usa **rotacion automatica**:
- Maximo 5 MB por archivo
- Mantiene hasta a 3 archivos de respaldo (.log.1, .log.2, .log.3)
- Rotacion automatica cuando se excede el tamaño

### Script de Limpieza

El script `cleanup-sessions.py` elimina archivos de sesion antiguos:

```bash
# Ver estadisticas sin borrar
python scripts/cleanup-sessions.py --stats

# Simular limpieza (dry-run)
python scripts/cleanup-sessions.py --days 30 --dry-run

# Limpiar archivos mayores a 30 dias
python scripts/cleanup-sessions.py --days 30

# Limpiar archivos mayores a 7 dias
python scripts/cleanup-sessions.py --days 7
```

**Automatizacion recomendada**:

# Windows (Task Scheduler)
# Agregar tarea programada que ejecute:
python C:\Users\fgpaz\.claude\plugins\cache\sandinas\sandinas-prompt-improver\1.6.1\scripts\cleanup-sessions.py --days 30

# Linux/macOS (cron)
# Agregar a crontab -e:
0 2 * * * cd /path/to/project && python ~/.claude/plugins/cache/sandinas/sandinas-prompt-improver/1.6.1/scripts/cleanup-sessions.py --days 30
