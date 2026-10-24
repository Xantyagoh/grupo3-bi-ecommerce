# Guía de construcción del dashboard (Power BI Desktop)

> **Destino en el repositorio:** `dashboard/GUIA_CONSTRUCCION.md` · Entregable: `dashboard/grupo3_ecommerce.pbix`
>
> Esta guía dice **qué** construir y **por qué**; el cómo (clics) está en la documentación de Power BI. Cada página responde una pregunta clave y se conecta con una hipótesis, para que lo que se muestra en el video coincida con lo que se dice (feedback de la entrega 2).

## 1. Cargar los datos

1. Power BI Desktop → **Obtener datos → Parquet** (o *Carpeta* si tu versión no trae el conector Parquet) → elegir los archivos de `data/processed/modelo_bi/` (5 archivos) y `data/processed/rfm_clientes.parquet`.
2. Importar también `data/processed/resumen_hipotesis.csv` (tabla `resumen_hipotesis`, para la página 6).
3. En **Vista de modelo**, crear las relaciones de la tabla de `medidas_dax.md` (todas 1 → *, filtro único). Comprobar que **no hay relaciones ambiguas**.
4. Marcar `dim_fecha` como tabla de fechas; ordenar `mes` por `mes_num` y `dia_semana` por `dia_semana_num`.
5. Ocultar las columnas llave (`cliente_key`, `codigo`, etc.) en la vista de informe.
6. Aplicar el tema: **Vista → Temas → Examinar temas →** `dashboard/tema_grupo3.json`.
7. Crear las medidas de `medidas_dax.md` en una tabla vacía llamada `_Medidas` y **validar contra los valores de referencia**.

## 2. Páginas

| # | Página | Pregunta / hipótesis | Visuales mínimos |
|---|---|---|---|
| 1 | **Resumen ejecutivo** | Estado general del negocio | 6 tarjetas KPI, línea de ingresos netos por mes, barras Top 5 países, anillo Reino Unido vs Exterior |
| 2 | **Ventas y estacionalidad** | P1 · H1 | Columnas por mes con temporada resaltada, matriz día × hora (mapa de calor), línea semanal, tarjeta del índice estacional |
| 3 | **Clientes y retención** | P3 · H4, H5, H6 | Treemap de segmentos RFM, dispersión frecuencia vs monetario, barras de recompra por captación y mercado, tabla de segmentos |
| 4 | **Mercados y devoluciones** | P4, P5 · H2, H3 | Mapa coroplético por país, barras de ticket por país, barras de tasa de devolución por mercado |
| 5 | **Productos** | P2 | Pareto (columnas + línea acumulada), Top 10 por ingreso y por unidades, matriz de detalle |
| 6 | **Hipótesis y decisiones** | Cierre / storytelling | Tabla `resumen_hipotesis` con formato condicional, 3 tarjetas de texto con las decisiones |

Total: **más de 10 tipos de visual distintos** (tarjeta, línea, columnas, barras, anillo, treemap, dispersión, mapa, matriz, tabla), por encima del mínimo de 5 que pide el enunciado.

### Página 1 — Resumen ejecutivo (el "dashboard ejecutivo")
- **Título dinámico** con la medida `[Titulo Ejecutivo]`.
- Fila de tarjetas: `Ingresos Netos`, `Ticket Promedio`, `Tasa Devolución` (color condicional con `[Color Devolución]`), `Clientes Activos`, `Tasa Recompra 90d`, `Crecimiento Interanual`.
- Línea: `Ingresos Netos` por `dim_fecha[anio_mes]`, con la leyenda `anio` para comparar 2010 vs 2011.
- Segmentadores sincronizados en todas las páginas: **Año**, **Mercado** (`dim_pais[pais_grupo]`) y **Temporada** (`dim_fecha[temporada]`).
- Regla ejecutiva: nada de tablas largas aquí; en 5 segundos se debe saber si el negocio va bien.

### Página 2 — Ventas y estacionalidad (H1)
- Columnas de `Ventas Brutas` por mes calendario coloreadas por `temporada`: se ve la temporada alta (sep–nov).
- Matriz `dia_semana` × `hora` con formato condicional de color (como el mapa de calor del notebook 03). El sábado debe verse casi vacío.
- Tarjeta con `[Índice Estacional]` (noviembre ≈ 1,8).
- **Título del gráfico que afirma el hallazgo:** "Septiembre–noviembre vende 1,7 veces más por semana" (H1).

### Página 3 — Clientes y retención (H4–H6)
- Usar `rfm_clientes[segmento]` en el treemap (tamaño = `monetario`).
- Barras: `Tasa Recompra 90d` por `dim_cliente[captacion]` (debe mostrar 40,5 % vs 48,2 %, H5) y por `dim_cliente[pais_grupo_cliente]` (46,2 % vs 46,8 %, H6).
- **Usar los filtros de `dim_cliente`**, no los de `dim_pais`: la recompra se calcula sobre `dim_cliente` y los filtros de `dim_pais` no llegan hasta ella.

### Página 4 — Mercados y devoluciones (H2, H3)
- Mapa por `dim_pais[pais]` (tamaño o color = `Ingresos Netos`). Si el mapa no carga, usar barras por país.
- Barras `Ticket Promedio` por país (Top 10); resaltar que **Exterior ≈ £853 vs Reino Unido ≈ £458** en promedio.
- Barras `Tasa Devolución` por `pais_grupo` (2,97 % vs 2,33 %) con la nota "diferencia pequeña (V de Cramér = 0,03)".

### Página 5 — Productos (P2)
- Pareto: columnas de ingreso por producto ordenado + línea con % acumulado. Mostrar que el 20 % de productos aporta ~78 %.
- **Drill-through** hacia una página oculta "Detalle de producto" (ventas mensuales y países del producto).

### Página 6 — Hipótesis y decisiones
- Tabla de `resumen_hipotesis` (hipótesis, p ajustado, efecto, magnitud, decisión) con formato condicional: verde = rechaza H0, gris = no rechaza.
- Tres tarjetas de texto con las decisiones propuestas (ver `docs/storytelling_y_decisiones.md`).

## 3. Interactividad (lo que pide el enunciado)

- **Segmentadores sincronizados** (Vista → Sincronizar segmentadores): Año, Mercado, Temporada.
- **Filtrado cruzado** entre visuales (por defecto) y *editar interacciones* para que las tarjetas del encabezado no se filtren con los gráficos de su misma fila.
- **Información sobre herramientas (tooltips) personalizada** en la línea de ingresos: mostrar pedidos, ticket y devolución del mes.
- **Marcadores + botones** para alternar entre "Ventas brutas" e "Ingresos netos" (parámetro de campo o marcadores).
- **Botones de navegación** entre páginas y botón de "Restablecer filtros".

## 4. Buenas prácticas de diseño (checklist)

- [ ] Una idea por página; máximo 6–8 visuales.
- [ ] Títulos que **dicen la conclusión**, no solo el nombre del campo.
- [ ] Misma paleta que los notebooks (el tema ya la trae): azul = base, naranja = destacar, gris = contexto.
- [ ] Ejes con unidades (£, %), sin decimales innecesarios; sin gráficos 3D; anillos con máximo 4 categorías.
- [ ] Alineación en cuadrícula y márgenes iguales; jerarquía: KPI arriba, detalle abajo.
- [ ] Texto alternativo en los visuales principales (accesibilidad).
- [ ] Verificar el dashboard con los 3 segmentadores en distintos valores (que ninguna tarjeta se vea vacía o en error).

## 5. Entrega

- Guardar como `dashboard/grupo3_ecommerce.pbix`.
- Exportar una captura por página en `dashboard/capturas/` (`01_resumen.png` … `06_hipotesis.png`).
- Si el `.pbix` pesa más de 100 MB, publicar sin los datos (Guardar como → *Plantilla .pbit*) y documentarlo en el README.
- **Plan B si no hay Power BI:** Tableau Public con las mismas 6 páginas; subir el `.twbx` a `dashboard/`.
