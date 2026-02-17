---
title: Proyeccion de Ventas
status: en-progreso
tags: [financiero, ventas, forecast]
---

# Proyeccion de Ventas

> [!info] Supuestos base
> Ticket promedio: ~ARS 13.000. Capacidad a madurez: 65 clientes/dia por local. Dos locales. Febrero 2026.

## Parametros de proyeccion

| Variable | Valor |
|---|---|
| Ticket promedio | ARS 13.000 |
| Clientes/dia por local a madurez | 65 |
| Dias operativos por mes | 30 |
| Ventas mensuales por local a madurez | $25.350.000 |
| Ventas mensuales 2 locales a madurez | $50.700.000 |
| Ventas anuales 2 locales a madurez | $608.400.000 |

## Rampa de ventas - Ano 1 (escenario base)

Se asume una curva de crecimiento gradual. Los primeros meses tienen menor afluencia por ser locales nuevos, y se alcanza la madurez operativa entre el mes 6 y 8.

| Mes | % de madurez | Clientes/dia/local | Ventas/mes/local (ARS) | Ventas 2 locales (ARS) |
|---|---|---|---|---|
| 1 | 40% | 26 | $10.140.000 | $20.280.000 |
| 2 | 50% | 33 | $12.870.000 | $25.740.000 |
| 3 | 55% | 36 | $14.040.000 | $28.080.000 |
| 4 | 60% | 39 | $15.210.000 | $30.420.000 |
| 5 | 70% | 46 | $17.940.000 | $35.880.000 |
| 6 | 80% | 52 | $20.280.000 | $40.560.000 |
| 7 | 85% | 55 | $21.450.000 | $42.900.000 |
| 8 | 90% | 59 | $23.010.000 | $46.020.000 |
| 9 | 95% | 62 | $24.180.000 | $48.360.000 |
| 10 | 100% | 65 | $25.350.000 | $50.700.000 |
| 11 | 100% | 65 | $25.350.000 | $50.700.000 |
| 12 | 100% | 65 | $25.350.000 | $50.700.000 |
| **Total ano 1** | | | | **$470.340.000** |

> [!info] Lectura de la rampa
> La proyeccion de ano 1 (~ARS 470M) es ~77% de la capacidad a madurez anual ($608M). Esto es coherente con el SOM de ano 1 estimado en el [[Analisis-de-Mercado]] (~ARS 426M, que usaba 70% como referencia conservadora).

## Composicion de ventas por linea

| Linea de ingreso | % sobre ventas | Ingreso mensual a madurez (2 locales) |
|---|---|---|
| Cafe y bebidas calientes/frias | 45% | $22.815.000 |
| Brunch (platos salados y dulces) | 40% | $20.280.000 |
| Pasteleria y complementos | 10% | $5.070.000 |
| Eventos y talleres | 5% | $2.535.000 |
| **Total** | **100%** | **$50.700.000** |

## Estacionalidad aplicada

La rampa del primer ano ya incorpora la curva de crecimiento. A partir del ano 2, se aplica un ajuste estacional sobre la base de madurez.

| Trimestre | Ajuste sobre base | Logica |
|---|---|---|
| T1 (ene-mar) | -5% | Vacaciones, menor frecuencia laboral |
| T2 (abr-jun) | +5% | Retorno a rutina, otono-invierno temprano (mas cafe) |
| T3 (jul-sep) | +8% | Pico invernal, vacaciones de julio, consumo grupal |
| T4 (oct-dic) | -3% | Primavera-verano, menor consumo de bebidas calientes |

## Proyeccion anual resumida (3 anos)

| Ano | Ventas anuales (ARS) | Crecimiento | Supuesto |
|---|---|---|---|
| 1 | ~$470.340.000 | - | Rampa de apertura (77% de madurez promedio) |
| 2 | ~$608.400.000 | +29% | Madurez operativa plena |
| 3 | ~$650.000.000 | +7% | Crecimiento organico por comunidad y reputacion |

> [!info] Nota sobre inflacion
> Estas proyecciones son en pesos constantes de febrero 2026. En un contexto inflacionario, los valores nominales seran mayores, pero el volumen real (clientes x ticket real) es lo que importa para evaluar el modelo. Las planillas en `financials/` permitiran actualizar con indices de ajuste.

## Limites de la proyeccion

1. La rampa de 40% a 100% en 10 meses es un supuesto basado en experiencia operativa, no en datos historicos del proyecto.
2. El ticket promedio puede variar por estacionalidad y mix de productos.
3. El ano 3 asume crecimiento organico sin apertura de nuevos locales ni cambios de formato.

---

**Documentos relacionados**: [[Costos-Fijos-y-Variables]] | [[Punto-de-Equilibrio]] | [[Escenarios]] | [[Analisis-de-Mercado]]

Ver planilla detallada: `financials/Proyecciones-Mensuales.xlsx`
