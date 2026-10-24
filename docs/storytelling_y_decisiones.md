# Storytelling, decisiones y limitaciones

> **Destino en el repositorio:** `docs/storytelling_y_decisiones.md`
> Todas las cifras salen de los notebooks 03–05 y del dashboard; si cambian al re-ejecutar, actualízalas aquí.

## 1. La historia en una frase

> **La tienda gana casi todo su dinero en tres meses (sep–nov) y de pocos clientes grandes, pero deja ir a la mitad de los clientes nuevos y, sobre todo, a los que capta justo en temporada alta. El crecimiento está en retener, no en vender más a los mismos.**

## 2. Estructura narrativa (situación → complicación → pregunta → respuesta → decisión)

| Paso | Qué decimos | Evidencia | Dónde se ve |
|---|---|---|---|
| **Situación** | Tienda mayorista en línea (£18,9 M netos en 2 años, 39.514 pedidos, ticket £491) | K1, K2 | Dashboard · Resumen ejecutivo |
| **Complicación 1** | Las ventas son muy estacionales: noviembre vende 1,8 veces el mes promedio | Índice estacional; H1: mediana semanal £261 k vs £155 k (×1,69), r = 0,76 | Página 2 |
| **Complicación 2** | Dependencia: el 20 % de los clientes (los *Campeones*) genera ~74 % del ingreso; el 80/20 se cumple en clientes (77 %) y productos (78 %) | Pareto, RFM, K6 | Páginas 3 y 5 |
| **Complicación 3** | El negocio está estancado (+2,3 % ene–nov) y 1 de cada 2 clientes nuevos no vuelve en 90 días | K5 = 46,7 %; K7 | Resumen ejecutivo |
| **Pregunta** | ¿Dónde se puede crecer y dónde se pierde dinero? | — | — |
| **Respuesta 1** | Los clientes captados en sep–nov recompran menos: 40,5 % vs 48,2 % (−7,6 pp) | H5, cohortes | Página 3 |
| **Respuesta 2** | Exterior: pedidos +43 % (mediana £421 vs £295) pero devuelve algo más (diferencia pequeña); misma recompra que el Reino Unido | H2, H3, H6 | Página 4 |
| **Respuesta 3** | Las devoluciones no son el problema: 2,4 % del valor vendido | K3 | Resumen ejecutivo |
| **Decisión** | Ver sección 3 | — | Página 6 |

## 3. Decisiones propuestas (basadas en evidencia)

| # | Decisión | Evidencia | KPI para monitorearla | Riesgo / cautela |
|---|---|---|---|---|
| **D1** | **Adelantar inventario y marketing a agosto–septiembre** y no dejar que se agote el stock en octubre–noviembre | H1 (efecto grande, r = 0,76); índice estacional nov = 1,82 | K1 ingresos netos de sep–nov | Solo dos temporadas observadas |
| **D2** | **Campaña de retención en diciembre–enero** dirigida a los clientes captados en sep–nov (meses de baja demanda: índice 0,66–0,76) | H5: −7,6 pp de recompra; cohortes sep–nov 2010 ≈ 8–14 % | K5 recompra a 90 días de la cohorte de temporada alta | El efecto es modesto (h = −0,15); probar con un grupo de control antes de escalar |
| **D3** | **Programa de cuenta clave para los *Campeones*** (≈ 1.190 clientes, 74 % del ingreso) y **reactivación de los clientes *En riesgo*** (1.446 clientes, 16,5 % del ingreso, 185 días sin comprar) | Segmentación RFM; K6 | Ingreso de Campeones; clientes En riesgo reactivados | La segmentación depende de la elección de k = 4 |
| **D4** | **Estrategia comercial propia para exportación** (pedidos mínimos/escalas de precio para clientes del Exterior), sin crear un programa de retención aparte | H2 (+43 % en el pedido mediano); H6 (misma recompra) | K2 ticket por mercado | El Exterior es el 15 % de las ventas |
| **D5** | **Mejorar la captura del `Customer ID` en el checkout**: el 22 % de las líneas (13 % del ingreso) no se puede seguir en el tiempo | Auditoría de calidad | % de líneas con cliente identificado | Requiere cambio en el sistema de ventas |
| **D6** | **No invertir (todavía) en reducir devoluciones por país**: la diferencia entre mercados es estadísticamente real pero trivial (V = 0,03) y el total es solo 2,4 % | H3; K3 | K3 tasa de devolución (vigilar > 3 %) | Falta saber el costo logístico de cada devolución |

## 4. Limitaciones

**Del dataset**
- **Una sola empresa y solo 2 años:** hay dos temporadas altas (2010 y 2011); la estacionalidad es consistente, pero no se puede asegurar que se mantenga.
- **Solo ingresos, sin costos ni márgenes:** un ingreso alto no implica una ganancia alta; las decisiones D1–D4 deberían validarse con rentabilidad por producto y cliente.
- **22 % de las líneas sin cliente:** el análisis por cliente (RFM, cohortes, recompra) ignora ~13 % del ingreso.
- **No hay categoría de producto ni canal de adquisición:** no se puede explicar *por qué* los captados en temporada alta recompran menos (¿promociones? ¿regalos de una sola vez?).
- **Las devoluciones no se vinculan al pedido original** (solo hay la factura "C"): no se sabe cuánto tardó la devolución ni cuál fue el motivo.
- **Diciembre de 2011 incompleto** (hasta el día 9): se excluye de los análisis temporales.

**De las decisiones de preparación**
- Se eliminaron duplicados exactos asumiendo que son errores de registro; si fueran líneas legítimas repetidas, las ventas estarían subestimadas en ~3 %.
- Se retiraron 2 pedidos gigantes cancelados a los minutos (R5); no cambian los ingresos netos pero sí la tasa de devolución (2,4 % vs 3,6 %).
- La cohorte de diciembre de 2009 mezcla clientes nuevos y antiguos (censura a la izquierda).

**Estadísticas**
- Las semanas consecutivas no son independientes (autocorrelación); Mann-Whitney la ignora. La conclusión de H1 es robusta por el tamaño del efecto, pero el p-valor exacto debe leerse con cautela.
- Seis pruebas: se aplicó la corrección de Holm, que no cambió ninguna decisión.
- **No rechazar H0 (H6) no demuestra igualdad:** el IC 95 % de la diferencia en recompra es −5,4 a +4,2 puntos; no se pueden descartar diferencias de hasta ~5 pp.
- Los análisis son **observacionales**: son asociaciones, no causas. Que los captados en temporada alta recompren menos no prueba que la temporada alta *cause* la menor recompra.
- Tamaño de muestra grande: casi cualquier diferencia sale significativa. Por eso se reporta siempre el **tamaño del efecto**.

## 5. Siguientes pasos

1. Incorporar costos para pasar de ingresos a **margen**.
2. Probar D2 con un **experimento controlado** (grupo con campaña vs grupo sin campaña).
3. Modelar la probabilidad de recompra con más variables (categoría del primer producto, canal).
4. Automatizar la actualización del dashboard con una conexión directa a la base de ventas.
