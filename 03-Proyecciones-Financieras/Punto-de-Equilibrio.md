---
title: Punto de Equilibrio
status: en-progreso
tags: [financiero, break-even]
---

# Punto de Equilibrio

> [!info] Metodologia
> Break-even calculado con metodo de margen de contribucion. Costos fijos contra margen unitario variable.

## Datos de entrada

| Variable | Valor |
|---|---|
| Costos fijos mensuales por local | ~$10.960.000 |
| Costos variables como % de ventas | ~34% |
| Margen de contribucion | ~66% |
| Ticket promedio | $13.000 |

## Break-even por local

**En facturacion mensual:**

`Break-even = Costos fijos / Margen de contribucion`
`Break-even = $10.960.000 / 0,66 = $16.606.000/mes`

**En clientes por dia:**

`Clientes/dia = Break-even mensual / (30 dias x Ticket)`
`Clientes/dia = $16.606.000 / $390.000 = ~43 clientes/dia`

| Metrica | Valor |
|---|---|
| Facturacion minima mensual por local | **~$16.600.000** |
| Clientes minimos por dia por local | **~43** |
| % de capacidad a madurez (65 clientes) | **66%** |

## Break-even consolidado (2 locales)

| Metrica | Valor |
|---|---|
| Costos fijos mensuales (2 locales) | ~$21.900.000 |
| Facturacion minima mensual (2 locales) | **~$33.200.000** |
| Clientes minimos por dia (total) | **~85** (~43 por local) |

## Tiempo estimado para alcanzar el equilibrio

Segun la rampa de ventas proyectada:

| Mes | Clientes/dia/local | vs. Break-even (43) | Estado |
|---|---|---|---|
| 1 | 26 | -17 | Deficit |
| 2 | 33 | -10 | Deficit |
| 3 | 36 | -7 | Deficit |
| 4 | 39 | -4 | Deficit (cerca) |
| **5** | **46** | **+3** | **Break-even alcanzado** |
| 6 | 52 | +9 | Superavit |
| 7+ | 55-65 | +12 a +22 | Superavit creciente |

**El break-even operativo se alcanza en el mes 5** de operacion, cuando cada local supera los 43 clientes diarios.

> [!info] Lectura para inversor
> El negocio necesita operar al 66% de su capacidad de madurez para cubrir costos. El margen de seguridad una vez alcanzada la madurez (65 clientes vs. 43 necesarios) es de 34%, lo que da resiliencia ante caidas temporales de demanda.

## Deficit acumulado hasta break-even

| Mes | Ventas 2 locales | Costos totales (fijos + var.) | Resultado mensual | Acumulado |
|---|---|---|---|---|
| 1 | $20.280.000 | $28.795.000 | -$8.515.000 | -$8.515.000 |
| 2 | $25.740.000 | $30.652.000 | -$4.912.000 | -$13.427.000 |
| 3 | $28.080.000 | $31.447.000 | -$3.367.000 | -$16.794.000 |
| 4 | $30.420.000 | $32.243.000 | -$1.823.000 | -$18.617.000 |
| 5 | $35.880.000 | $34.099.000 | +$1.781.000 | -$16.836.000 |
| 6 | $40.560.000 | $35.690.000 | +$4.870.000 | -$11.966.000 |

> [!info] Capital de trabajo y deficit
> El deficit acumulado de ~$18,6M (pico en mes 4) es cubierto por el capital de trabajo incluido en la inversion inicial (~$45-66M para ambos locales). Hay margen de maniobra.

## Sensibilidad del break-even

| Variable | Cambio | Nuevo break-even (clientes/dia) | Efecto |
|---|---|---|---|
| Ticket sube 10% ($14.300) | +10% | 39 clientes/dia | Se alcanza 1 mes antes |
| Ticket baja 10% ($11.700) | -10% | 48 clientes/dia | Se alcanza 1 mes despues |
| COGS sube 5 p.p. (de 26% a 31%) | -5% contribucion | 50 clientes/dia | Se alcanza 2 meses despues |
| Se agrega 1 empleado/local | +$3M fijos | 48 clientes/dia | Se alcanza 1 mes despues |

---

**Documentos relacionados**: [[Costos-Fijos-y-Variables]] | [[Proyeccion-de-Ventas]] | [[Escenarios]] | [[ROI-y-Payback]]
