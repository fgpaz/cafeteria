# Cafeteria de Especialidad + Brunch - Guaymallen, Mendoza

## Proyecto

Propuesta comercial completa para una cafeteria de especialidad con brunch, orientada a presentar ante potenciales socios capitalistas. El objetivo es armar un documento profesional que cubra plan de negocio, proyecciones financieras, identidad de marca y presentacion ejecutiva.

## Concepto

- Cafe de especialidad a precio accesible para clase media
- Brunch con cocina fria + horno
- Dos locales simultaneos en Guaymallen, Mendoza
- Diferenciador: experiencia de servicio excepcional + identidad visual fuerte + comunidad
- Nombre de marca: a definir con el socio capitalista

## Socia operativa

- Gerente actual de 2 cafeterias de especialidad
- Head barista con experiencia en specialty coffee
- Aporta know-how operativo completo a cambio de porcentaje de sociedad
- No aporta capital; su contribucion es gestion, operacion y expertise

## Entregables

1. **Plan de negocio** (`01-Plan-de-Negocio/`): mercado, competencia, modelo, operaciones, marketing, legal
2. **Identidad de marca** (`02-Marca-y-Concepto/`): brand guidelines, identidad visual, tono, experiencia del cliente
3. **Proyecciones financieras** (`03-Proyecciones-Financieras/` + `financials/`): inversion, costos, ventas, escenarios, ROI
4. **Presentacion ejecutiva** (`04-Presentacion-Ejecutiva/`): deck para socios capitalistas con notas del presentador

## Formato y convenciones

### Obsidian

Este repositorio completo es un vault de Obsidian. Respetar estas convenciones:

- **Frontmatter YAML** en cada archivo .md:
  ```yaml
  ---
  title: Nombre del Documento
  status: pendiente | en-progreso | completo
  tags: [tag1, tag2]
  ---
  ```
- **Wikilinks** para referencias cruzadas: `[[Nombre-del-Archivo]]`
- **Callouts** para informacion destacada:
  ```markdown
  > [!info] Titulo
  > Contenido del callout
  ```
- **Placeholders de imagen** con callout `[!image]`:
  ```markdown
  > [!image] Foto: Descripcion
  > **Buscar en**: Unsplash, Pexels
  > **Keywords**: "palabras clave para buscar"
  > **Requisitos**: descripcion de la imagen necesaria
  > **Uso**: donde se usara esta imagen
  ```

### Imagenes y diagramas

| Tipo | Herramienta | Ubicacion |
|---|---|---|
| Organigramas, flujos, timelines | Mermaid (bloques ```mermaid en .md) | Inline en cada .md |
| Canvas, flujo de caja (complejos) | Mermaid (.mmd separados) | `assets/diagrams/` |
| Layout de locales, mapas conceptuales | Excalidraw (plugin Obsidian) | `assets/diagrams/` |
| Paleta, elementos graficos | SVG generado | `assets/images/` |
| Fotos de ambientacion, producto | Placeholders con instrucciones | Inline como callout [!image] |

### Planillas financieras

- Usar la skill `document-xlsx` para crear y editar archivos .xlsx
- Ubicacion: `financials/`
- Archivos esperados: `Inversion-Inicial.xlsx`, `Proyecciones-Mensuales.xlsx`, `Escenarios.xlsx`, `Dashboard-KPIs.xlsx`

## Idioma y estilo

- Espanol argentino
- Sin emojis
- Prosa clara y concisa
- Moneda principal: pesos argentinos (ARS)
- Moneda de referencia: dolares estadounidenses (USD) para la inversion total
- Usar formato de miles con punto (1.000.000) y decimales con coma (99,50)

## Sincronizacion

Dos computadoras trabajan en paralelo sobre este repositorio via GitHub (`fgpaz/cafeteria`).

- Hacer commits frecuentes con mensajes descriptivos
- Hacer `git pull` antes de empezar a trabajar
- No editar el mismo archivo en ambas computadoras a la vez
- `.obsidian/workspace.json` esta en `.gitignore` (es config local de cada maquina)
- `.claude/settings.local.json` esta en `.gitignore` (es config local de Claude Code)
- SIEMPRE al finalizar un trabajo, hacer commit y push de los cambios usando `gh` (GitHub CLI)

## Skills y flujo de trabajo

### Regla obligatoria: brainstorming al inicio

SIEMPRE que se inicie un chat o se reciba una tarea nueva, ejecutar primero la skill `brainstorming` antes de cualquier otra accion. El brainstorming refina la idea, identifica dependencias y genera un plan accionable. No se debe escribir codigo ni editar archivos sin pasar primero por brainstorming.

### Mapeo de skills por area

Cuando se trabaje en un area especifica, usar las skills asociadas segun esta tabla. Las skills se combinan: brainstorming siempre va primero, luego se aplican las skills del area correspondiente.

| Area | Carpeta | Skills principales | Skills complementarias |
|---|---|---|---|
| Plan de negocio | `01-Plan-de-Negocio/` | `business-plan-writer`, `hospitality-coordinator` | `marketing-strategy-pmm` (para Plan-de-Marketing.md), `chef-assistant` (para menu y oferta gastronomica) |
| Marca y concepto | `02-Marca-y-Concepto/` | `brand-strategist`, `brand-designer` | `writing-clearly-and-concisely` (para Tono-y-Voz.md y Brand-Story.md) |
| Proyecciones financieras | `03-Proyecciones-Financieras/` + `financials/` | `startup-financial-modeling`, `xlsx` | `business-plan-writer` (para narrativa del resumen financiero) |
| Presentacion ejecutiva | `04-Presentacion-Ejecutiva/` | `pitch-deck` | `brand-strategist` (para consistencia de mensaje), `docx` (si se genera documento) |
| Recursos e investigacion | `05-Recursos/` | `business-plan-writer` | `hospitality-coordinator` (para benchmarks del sector gastronomico) |
| Assets visuales | `assets/` | `brand-designer`, `obsidian` | - |
| Vault general | Raiz y estructura | `obsidian` | `writing-clearly-and-concisely` |

### Skills transversales (aplican a todas las areas)

- `brainstorming`: SIEMPRE primero, antes de cualquier tarea
- `writing-plans`: antes de tareas que requieran multiples pasos de implementacion
- `writing-clearly-and-concisely`: para toda prosa que se redacte en documentos
- `obsidian`: para cualquier operacion sobre el vault (crear notas, wikilinks, frontmatter)
- `dispatching-parallel-agents`: cuando haya 2 o mas tareas independientes que se puedan ejecutar en paralelo
- `executing-plans`: cuando exista un plan de implementacion listo para ejecutar

### Flujo de trabajo estandar

1. **Brainstorming**: refinar la idea, identificar el area y las skills necesarias
2. **Planificacion** (si aplica): usar `writing-plans` para tareas complejas
3. **Ejecucion**: aplicar las skills del area correspondiente
4. **Revision**: verificar que el resultado respete las convenciones del vault (frontmatter, wikilinks, callouts)
5. **Commit y push**: al finalizar, commit descriptivo y push con `gh`

## Estructura del vault

```
cafeteria/
├── CLAUDE.md
├── README.md
├── 01-Plan-de-Negocio/        # 8 archivos .md
├── 02-Marca-y-Concepto/       # 5 archivos .md
├── 03-Proyecciones-Financieras/  # 7 archivos .md
├── 04-Presentacion-Ejecutiva/ # 2 archivos .md
├── 05-Recursos/               # 3 archivos .md
├── financials/                # Planillas .xlsx
└── assets/
    ├── diagrams/              # .mmd y .excalidraw
    └── images/                # .svg y placeholders
```
