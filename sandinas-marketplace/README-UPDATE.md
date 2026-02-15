# Configuración de Actualización Automática para Plugins Sandinas

## Repositorio Azure DevOps

**URL:** `git@ssh.dev.azure.com:v3/soluciones-desarrollo/GDD/Sandinas.Assets`

## Pasos para configurar

### 1. Preparar el repositorio

```bash
# En la carpeta actual
cd C:\repos\sandinas\sandinas-marketplace

# Inicializar repositorio (si no está hecho)
git init

# Agregar remoto de Azure DevOps
git remote add origin git@ssh.dev.azure.com:v3/soluciones-desarrollo/GDD/Sandinas.Assets

# Crear .gitignore si no existe
echo ".DS_Store" > .gitignore
echo "Thumbs.db" >> .gitignore
```

### 2. Estructura recomendada en el repositorio

```
Sandinas.Assets/
├── claude-plugins/          # Carpeta principal para plugins
│   ├── marketplace.json     # Configuración del marketplace
│   └── plugins/
│       ├── sandinas-prompt-improver/
│       │   ├── .claude-plugin/
│       │   │   └── plugin.json
│       │   ├── scripts/
│       │   ├── skills/
│       │   └── README.md
│       └── agent-dotnet-arquetipo/
│           ├── .claude-plugin/
│           └── ...
└── [otros assets de la empresa]
```

### 3. Para los desarrolladores

Instalar el marketplace desde Azure DevOps:

```bash
# Opción 1: HTTPS
claude plugin marketplace add https://dev.azure.com/soluciones-desarrollo/GDD/_git/Sandinas.Assets?path=claude-plugins

# Opción 2: SSH (requiere configuración de SSH)
claude plugin marketplace add git@ssh.dev.azure.com:v3/soluciones-desarrollo/GDD/Sandinas.Assets?path=claude-plugins

# Opción 3: Descargar y usar localmente
git clone git@ssh.dev.azure.com:v3/soluciones-desarrollo/GDD/Sandinas.Assets
claude plugin marketplace add ./Sandinas.Assets/claude-plugins
```

### 4. Flujo de actualización

**Para el equipo de desarrollo:**

```bash
# Actualizar marketplace (trae cambios del repositorio)
claude plugin marketplace update sandinas

# Actualizar plugins instalados
claude plugin update

# O actualizar todo en un comando
claude plugin marketplace update && claude plugin update
```

### 5. Script de actualización automática (Windows)

Crear `update-plugins.bat`:

```batch
@echo off
echo Actualizando plugins de Sandinas...

echo 1. Actualizando marketplace...
claude plugin marketplace update sandinas

echo 2. Actualizando plugins...
claude plugin update

echo 3. Plugins actualizados!
echo Reinicia Claude Code para aplicar los cambios.
pause
```

### 6. Versionamiento

Cuando actualices un plugin:

1. Modifica el archivo `.claude-plugin/plugin.json`
2. Incrementa la versión:
   ```json
   {
     "version": "1.1.0"  // De 1.0.0 a 1.1.0
   }
   ```
3. Commit y push:
   ```bash
   git add .
   git commit -m "Actualizado prompt-improver v1.1.0: nueva funcionalidad"
   git push origin main
   ```

### 7. Actualización automática periódica

**Opción A: Script programado en Windows**

Crear tarea programada que ejecute `update-plugins.bat` diariamente.

**Opción B: Hook en Git**

Crear `.git/hooks/post-merge`:
```bash
#!/bin/sh
echo "Plugins actualizados desde repositorio"
claude plugin marketplace update
```

### 8. Configuración en VS Code

Para facilitar actualizaciones, agregar a `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Actualizar Plugins Sandinas",
            "type": "shell",
            "command": "claude",
            "args": [
                "plugin",
                "marketplace",
                "update",
                "sandinas"
            ],
            "group": "build"
        }
    ]
}
```