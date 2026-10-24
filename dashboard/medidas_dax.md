# Medidas DAX del dashboard

> **Destino en el repositorio:** `dashboard/medidas_dax.md`
>
> Cada medida replica un KPI del notebook `05_kpis.ipynb`. **Después de crearlas, valida que den los valores de la tabla "Valores de referencia" del final** (vienen de `data/processed/kpis_referencia.csv`). Si una no coincide, el error está en la medida o en las relaciones, no en el notebook.
>
> Estas fórmulas siguen las tablas y columnas exactas de `data/processed/modelo_bi/`. Se escribieron siguiendo la lógica del notebook, pero hay que probarlas en Power BI Desktop: si alguna da error, corrige el nombre de la columna según tu modelo.

## Tablas del modelo

| Tabla | Archivo | Relación |
|---|---|---|
| `fact_lineas` | `modelo_bi/fact_lineas.parquet` | centro de la estrella |
| `dim_fecha` | `modelo_bi/dim_fecha.parquet` | `dim_fecha[fecha]` 1 → * `fact_lineas[fecha]` |
| `dim_producto` | `modelo_bi/dim_producto.parquet` | `dim_producto[codigo]` 1 → * `fact_lineas[codigo]` |
| `dim_cliente` | `modelo_bi/dim_cliente.parquet` | `dim_cliente[cliente_key]` 1 → * `fact_lineas[cliente_key]` |
| `dim_pais` | `modelo_bi/dim_pais.parquet` | `dim_pais[pais]` 1 → * `fact_lineas[pais]` |
| `rfm_clientes` | `rfm_clientes.parquet` | `dim_cliente[cliente_key]` 1 → 1 `rfm_clientes[cliente_id]` |

Todas las relaciones con dirección de filtro **única** (de la dimensión hacia los hechos), excepto la de `rfm_clientes`, que puede ser bidireccional.

> **Importante:** `dim_fecha` se marca como *tabla de fechas* (Herramientas de tabla → Marcar como tabla de fechas, columna `fecha`). `mes` se ordena por `mes_num` y `dia_semana` por `dia_semana_num`.

## Medidas base

```dax
Ventas Brutas =
CALCULATE ( SUM ( fact_lineas[importe] ), fact_lineas[tipo] = "Venta" )

Devoluciones =
-CALCULATE ( SUM ( fact_lineas[importe] ), fact_lineas[tipo] = "Devolucion" )

Ingresos Netos =
[Ventas Brutas] - [Devoluciones]

Pedidos =
CALCULATE ( DISTINCTCOUNT ( fact_lineas[factura] ), fact_lineas[tipo] = "Venta" )

Unidades Vendidas =
CALCULATE ( SUM ( fact_lineas[cantidad] ), fact_lineas[tipo] = "Venta" )
```

## KPIs

```dax
-- K1 · Ingresos netos  → usar la medida [Ingresos Netos]

-- K2 · Ticket promedio
Ticket Promedio =
DIVIDE ( [Ventas Brutas], [Pedidos] )

-- K3 · Tasa de devolución
Tasa Devolución =
DIVIDE ( [Devoluciones], [Ventas Brutas] )

-- K4 · Clientes activos (excluye invitados, cliente_key = -1)
Clientes Activos =
CALCULATE (
    DISTINCTCOUNT ( fact_lineas[cliente_key] ),
    fact_lineas[tipo] = "Venta",
    fact_lineas[cliente_key] <> -1
)

-- K5 · Tasa de recompra a 90 días (las banderas ya vienen calculadas en dim_cliente)
Clientes Observables 90d =
CALCULATE ( COUNTROWS ( dim_cliente ), dim_cliente[observable_90d] = TRUE () )

Clientes Recompran 90d =
CALCULATE ( COUNTROWS ( dim_cliente ), dim_cliente[recompra_90d] = TRUE () )

Tasa Recompra 90d =
DIVIDE ( [Clientes Recompran 90d], [Clientes Observables 90d] )

-- K6 · Concentración: % de las ventas que aporta el 20 % de clientes que más compran
Concentración Top 20 =
VAR Clientes =
    FILTER (
        VALUES ( dim_cliente[cliente_key] ),
        dim_cliente[cliente_key] <> -1 && [Ventas Brutas] > 0
    )
VAR K = ROUND ( COUNTROWS ( Clientes ) * 0.2, 0 )
VAR Top20 = TOPN ( K, Clientes, [Ventas Brutas], DESC )
RETURN
    DIVIDE ( SUMX ( Top20, [Ventas Brutas] ), SUMX ( Clientes, [Ventas Brutas] ) )

-- K7 · Crecimiento interanual comparable (enero–noviembre 2011 vs 2010)
Crecimiento Interanual =
VAR Ene_Nov_2011 =
    CALCULATE ( [Ingresos Netos], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = 2011, dim_fecha[mes_num] <= 11 )
VAR Ene_Nov_2010 =
    CALCULATE ( [Ingresos Netos], REMOVEFILTERS ( dim_fecha ), dim_fecha[anio] = 2010, dim_fecha[mes_num] <= 11 )
RETURN
    DIVIDE ( Ene_Nov_2011, Ene_Nov_2010 ) - 1
```

> **Por qué K7 fija los años:** compara el mismo periodo (ene–nov) de dos años para no sesgar con diciembre de 2011, que está incompleto. Es un KPI "de contexto": no cambia con los filtros de año.

## Medidas de apoyo para los visuales

```dax
-- Participación del mercado seleccionado frente al total
% Ventas del Mercado =
DIVIDE ( [Ventas Brutas], CALCULATE ( [Ventas Brutas], REMOVEFILTERS ( dim_pais ) ) )

-- Índice estacional del mes (1 = mes promedio) — para la página de estacionalidad
Índice Estacional =
VAR PromMes = AVERAGEX ( VALUES ( dim_fecha[anio_mes] ), [Ventas Brutas] )
VAR PromGlobal =
    CALCULATE (
        AVERAGEX ( VALUES ( dim_fecha[anio_mes] ), [Ventas Brutas] ),
        REMOVEFILTERS ( dim_fecha[mes], dim_fecha[mes_num] ),
        dim_fecha[mes_incompleto] = FALSE ()
    )
RETURN
    DIVIDE ( PromMes, PromGlobal )

-- Ventas acumuladas dentro del año (curva de Pareto/acumulado)
Ventas Acumuladas Año =
CALCULATE ( [Ventas Brutas], DATESYTD ( dim_fecha[fecha] ) )

-- Semáforo para la tasa de devolución (umbral de 3 %)
Color Devolución =
IF ( [Tasa Devolución] > 0.03, "#C0392B", "#3B8E5A" )

-- Texto dinámico para el título del dashboard ejecutivo
Titulo Ejecutivo =
"Ingresos netos £" & FORMAT ( [Ingresos Netos] / 1000000, "0.0" ) & " M · "
    & FORMAT ( [Pedidos], "#,0" ) & " pedidos · tasa de devolución " & FORMAT ( [Tasa Devolución], "0.0%" )
```

## Valores de referencia (sin filtros, para validar)

| KPI | Medida | Valor esperado |
|---|---|---|
| K1 | `[Ingresos Netos]` | **£18.929.108** |
| — | `[Ventas Brutas]` | £19.399.950 |
| — | `[Devoluciones]` | £470.842 |
| K2 | `[Ticket Promedio]` | **£491** (39.514 pedidos) |
| K3 | `[Tasa Devolución]` | **2,43 %** |
| K4 | `[Clientes Activos]` | **5.852** |
| K5 | `[Tasa Recompra 90d]` | **46,7 %** (2.457 de 5.256 clientes) |
| K6 | `[Concentración Top 20]` | **≈ 76,9 %** (ver nota) |
| K7 | `[Crecimiento Interanual]` | **+2,3 %** |

Con el filtro de mercado (`dim_pais[pais_grupo]`): Reino Unido → ticket £458, devolución 2,33 %; Exterior → ticket £853, devolución 2,97 %.

> **Nota K6:** el notebook y el DAX usan la misma definición (20 % de los clientes identificados con ventas), pero el redondeo de "el 20 %" puede diferir en una o dos unidades y mover el resultado unas décimas (76,9 % vs 76,8 %). Si la diferencia supera 1 punto, revisa el filtro `cliente_key <> -1`.
