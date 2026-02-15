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
