# Marketplace Sandinas

Marketplace interno de plugins de Claude Code para Sandinas.

## Plugins Disponibles

### agent-dotnet-arquetipo
Agente especializado para crear proyectos .NET con el arquetipo CQRS de Sandinas.

**Características:**
- Agente experto que guía en la selección de templates
- Templates completos del arquetipo v4
- Documentación detallada
- Ejemplos de implementación

## Instalación del Marketplace

Para configurar el marketplace de Sandinas en Claude Code:

```bash
# 1. Agregar el marketplace de Sandinas
/plugin marketplace add /path/to/sandinas-marketplace

# 2. Listar plugins disponibles
/plugin marketplace list

# 3. Instalar el plugin deseado
/plugin install agent-dotnet-arquetipo@sandinas

# 4. Reiniciar Claude Code
```

## Uso de los Plugins

Una vez instalado el plugin `agent-dotnet-arquetipo`:

1. **Para crear nuevos componentes:**
   ```
   "Necesito crear un comando para registrar usuarios"
   "Quiero implementar una query con paginación"
   ```

2. **Para entender el arquetipo:**
   ```
   "Explícame cómo estructura el arquetipo CQRS"
   "Qué template uso para un handler de comandos"
   ```

El agente te hará preguntas para entender tu contexto y recomendará los templates específicos que necesitas.

## Agregar Nuevos Plugins

Para agregar un nuevo plugin al marketplace Sandinas:

1. Crea el directorio del plugin:
   ```bash
   mkdir sandinas-marketplace/plugins/mi-nuevo-plugin
   ```

2. Crea el archivo `.claude-plugin/plugin.json` con los metadatos

3. Agrega tu plugin al `marketplace.json` principal:
   ```json
   {
     "name": "mi-nuevo-plugin",
     "description": "Descripción del plugin",
     "version": "1.0.0",
     "source": "./plugins/mi-nuevo-plugin",
     "author": {
       "name": "Tu Nombre"
     }
   }
   ```

4. Desarrolla tus skills, commands o templates en los directorios correspondientes

## Estructura del Marketplace

```
sandinas-marketplace/
├── marketplace.json          # Configuración principal del marketplace
├── plugins/                  # Directorio de plugins
│   └── agent-dotnet-arquetipo/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       ├── templates/
│       ├── docs/
│       └── README.md
└── README.md                 # Este archivo
```

## Soporte

Para soporte sobre los plugins de Sandinas:
- Contacta al equipo de desarrollo
- Consulta la documentación interna
- Revisa los ejemplos en cada plugin