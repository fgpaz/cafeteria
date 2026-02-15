# Guia de Desarrollo de Plugins - Sandinas

Guia para crear y mantener plugins de Claude Code en el ecosistema Sandinas.

## 1. Estructura Correcta de un Plugin

```
mi-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifesto obligatorio
├── commands/                # Slash commands (opcional)
│   └── comando.md
├── agents/                  # Agentes personalizados (opcional)
│   └── agente.md
├── skills/                  # Skills invocables por modelo (opcional)
│   └── mi-skill/
│       └── SKILL.md
├── hooks/                   # Event handlers (opcional)
│   └── hooks.json
├── .mcp.json               # Configuracion de servidores MCP (opcional)
└── README.md               # Documentacion del plugin
```

**IMPORTANTE:** Los directorios `commands/`, `agents/`, `skills/`, `hooks/` deben estar en la **RAIZ** del plugin, NO dentro de `.claude-plugin/`. Solo `plugin.json` va dentro de `.claude-plugin/`.

---

## 2. plugin.json - Campos Requeridos

Archivo ubicado en `.claude-plugin/plugin.json`:

| Campo | Tipo | Obligatorio | Descripcion |
|-------|------|-------------|-------------|
| `name` | string | Si | Identificador unico y namespace para comandos |
| `description` | string | Si | Descripcion mostrada en el plugin manager |
| `version` | string | Si | Version usando semver (ej: "1.0.0") |
| `author` | object | No | Objeto con `name` y `email` opcionales |

**Ejemplo minimo:**
```json
{
  "name": "sandinas-doc-auto",
  "description": "Generacion automatica de documentacion tecnica",
  "version": "1.0.0"
}
```

**Ejemplo completo:**
```json
{
  "name": "sandinas-doc-auto",
  "description": "Generacion automatica de documentacion tecnica al finalizar sesiones de Claude Code",
  "version": "1.0.0",
  "author": {
    "name": "Sandinas Dev Team",
    "email": "dev@sandinas.com"
  },
  "homepage": "https://github.com/sandinas/doc-auto",
  "license": "MIT"
}
```

---

## 3. Tipos de Componentes

### Commands (Slash Commands)
Archivos Markdown en `commands/`. El filename se convierte en el comando.

```
commands/
└── hola.md           # Crea /plugin-name:hola
```

**Formato:**
```markdown
---
description: Saluda al usuario
---

# Comando Hola

Saluda al usuario calurosamente con el nombre "$ARGUMENTS".
```

### Agents
Archivos Markdown en `agents/` que definen el comportamiento de agentes personalizados.

### Skills
Directorios en `skills/` que contienen `SKILL.md`. Son invocados automaticamente por Claude segun el contexto.

```
skills/
└── code-review/
    └── SKILL.md
```

### Hooks
Configuracion en `hooks/hooks.json` para reaccionar a eventos.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "npm run lint" }
        ]
      }
    ]
  }
}
```

### MCP Servers
Configuracion en `.mcp.json` para integrar servidores MCP.

---

## 4. Ejemplo Practico: Crear un Plugin Simple

Vamos a crear un plugin "Hola Sandinas" que saluda al usuario.

```bash
# 1. Crear estructura de directorios
mkdir -p hola-sandinas/.claude-plugin
mkdir hola-sandinas/commands

# 2. Crear plugin.json
cat > hola-sandinas/.claude-plugin/plugin.json << 'EOF'
{
  "name": "hola-sandinas",
  "description": "Plugin de ejemplo para saludar usuarios de Sandinas",
  "version": "1.0.0",
  "author": {
    "name": "Sandinas Dev Team"
  }
}
EOF

# 3. Crear comando
cat > hola-sandinas/commands/saludar.md << 'EOF'
---
description: Saluda al usuario por su nombre
---

# Comando Saludar

Saluda al usuario llamado "$ARGUMENTS" de parte del equipo de Sandinas.
EOF

# 4. Probar localmente
cd hola-sandinas
claude --plugin-dir .
```

Una vez iniciado Claude, ejecuta:
```
/hola-sandinas:saludar Juan
```

---

## 5. Validacion y Testing

### Probar localmente
```bash
claude --plugin-dir ./mi-plugin
```

### Verificar componentes
| Comando | Verifica |
|---------|----------|
| `/help` | Lista comandos disponibles |
| `/agents` | Lista agentes disponibles |
| `claude plugin list` | Lista plugins instalados |

### Checklist de validacion
- [ ] `plugin.json` tiene campos obligatorios (name, description, version)
- [ ] Directorios estan en la raiz, NO dentro de `.claude-plugin/`
- [ ] Commands tienen frontmatter con `description`
- [ ] Skills tienen `SKILL.md` con frontmatter valido

---

## 6. Publicacion en Marketplace Sandinas

### Pasos para agregar un plugin al marketplace

1. **Colocar plugin en el directorio del marketplace**
   ```bash
   cp -r mi-plugin /path/to/sandinas-marketplace/plugins/
   ```

2. **Actualizar marketplace.json**
   ```json
   {
     "name": "mi-plugin",
     "description": "Descripcion del plugin",
     "version": "1.0.0",
     "source": "./plugins/mi-plugin",
     "author": {
       "name": "Tu Nombre"
     }
   }
   ```

3. **Reinstalar marketplace**
   ```bash
   cd /path/to/sandinas-marketplace
   claude plugin marketplace remove sandinas
   claude plugin marketplace add ./
   ```

4. **Probar instalacion**
   ```bash
   claude plugin install mi-plugin@sandinas
   ```

---

## 7. Best Practices Especificas de Sandinas

### Nomenclatura
- Prefijo de plugins: `sandinas-` para plugins internos
- Nombres descriptivos en ingles para commands/agents
- Evitar abreviaturas ambiguas

### Versionamiento
- Usar Semantic Versioning (semver): `MAJOR.MINOR.PATCH`
- Incrementar `MAJOR` para cambios incompatibles
- Incrementar `MINOR` para funcionalidad nueva backward-compatible
- Incrementar `PATCH` para correcciones

### Estructura de directorios
- Mantener `commands/` organizado por funcionalidad
- Usar subdirectorios en `skills/` para Skills complejos
- Documentar hooks con comentarios en `hooks.json`

---

## 8. Troubleshooting Común

### Plugin no aparece en el marketplace
**Verifica:**
- Que el plugin este listado en `marketplace.json`
- Que la ruta `source` sea correcta relativa a la raiz del marketplace
- Que reinstalaste el marketplace despues de modificar `marketplace.json`

### Comando no funciona
**Verifica:**
- Que el archivo `.md` este en `commands/`, no en `.claude-plugin/commands/`
- Que el archivo tenga frontmatter valido con `description`
- Que usas el namespace correcto: `/plugin-name:command`

### Error de estructura
**Comun:** Poner directorios dentro de `.claude-plugin/`
```
INCORRECTO:
  .claude-plugin/
    plugin.json
    commands/        # MAL

CORRECTO:
  .claude-plugin/
    plugin.json
  commands/          # BIEN
```

---

## Referencias

- [Documentacion oficial de Claude Code - Plugins](https://code.claude.com/docs/en/plugins.md)
- [Plugins Reference - Especificacion completa](https://code.claude.com/docs/en/plugins-reference)
- [Slash Commands Documentation](https://code.claude.com/docs/en/slash-commands)
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)
