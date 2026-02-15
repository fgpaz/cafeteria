# Cafeteria de Especialidad + Brunch

Propuesta comercial para una cafeteria de especialidad con brunch en Guaymallen, Mendoza. Incluye plan de negocio, proyecciones financieras, identidad de marca y presentacion ejecutiva.

## Estructura

- `01-Plan-de-Negocio/` - Analisis de mercado, modelo de negocio, plan operativo, marketing, legal
- `02-Marca-y-Concepto/` - Brand guidelines, identidad visual, tono y voz, experiencia del cliente
- `03-Proyecciones-Financieras/` - Inversion, costos, ventas, escenarios, ROI
- `04-Presentacion-Ejecutiva/` - Deck para socios capitalistas
- `05-Recursos/` - Casos de exito, regulaciones, benchmarks
- `financials/` - Planillas Excel con proyecciones
- `assets/` - Diagramas (Mermaid, Excalidraw) e imagenes (SVG)

## Abrir como vault de Obsidian

Este repositorio completo es un vault de Obsidian. Para abrir:

1. Clonar el repositorio: `git clone https://github.com/fgpaz/cafeteria.git`
2. Abrir Obsidian
3. Seleccionar "Open folder as vault" y elegir la carpeta `cafeteria/`

## Setup en nueva computadora

1. Clonar el repositorio
2. Ejecutar el script de instalacion de skills:
   ```bash
   bash setup-skills.sh
   ```
3. Abrir como vault en Obsidian

## Sincronizacion entre computadoras

Se trabaja en dos computadoras via GitHub. Para sincronizar:

```bash
git pull                # Antes de empezar a trabajar
git add <archivos>      # Agregar cambios
git commit -m "mensaje" # Commitear
git push                # Subir al repo
```

No editar el mismo archivo en ambas computadoras a la vez para evitar conflictos.
