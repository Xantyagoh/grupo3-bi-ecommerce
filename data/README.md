# Datos

## Fuente

**Online Retail II** — UCI Machine Learning Repository (id 502)
- Página: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- DOI: https://doi.org/10.24432/C5CG6D
- Autor: Daqing Chen (donado el 20/09/2019) · Licencia **CC BY 4.0**
- Contenido: 1.067.371 líneas de factura de una tienda en línea del Reino Unido (sin local físico) entre el 01/12/2009 y el 09/12/2011. Vende regalos y muchos de sus clientes son mayoristas.

## Cómo obtener los datos crudos

Los datos crudos pesan ~45 MB (xlsx) y ~96 MB (csv), por eso **no se suben al repositorio** (`data/raw/` está en `.gitignore`). Se descargan con un comando:

```bash
python src/descargar_datos.py
```

Crea `data/raw/online_retail_II.xlsx` (original) y `data/raw/online_retail_II.csv` (las dos hojas unidas; lo leen los notebooks). Tarda 1–2 minutos la primera vez.

## Carpetas

| Carpeta | Contenido | ¿En git? |
|---|---|---|
| `data/raw/` | Datos originales descargados | No |
| `data/processed/lineas_limpias.parquet` | Resultado del notebook 02 (limpio, 1.021.326 líneas) | Sí |
| `data/processed/modelo_bi/` | Modelo en estrella para Power BI (hechos + 4 dimensiones) | Sí |
| `data/processed/rfm_clientes.parquet` | Segmentos RFM por cliente (notebook 03) | Sí |
| `data/processed/resumen_hipotesis.csv` | Resultados de las 6 pruebas (notebook 04) | Sí |
| `data/processed/kpis_referencia.csv` | Valores de los 7 KPIs para validar el dashboard (notebook 05) | Sí |

## Diccionario de datos original

| Variable | Significado |
|---|---|
| `Invoice` | Número de factura (6 dígitos). Si empieza por **C**, es una cancelación/devolución |
| `StockCode` | Código de producto (5 dígitos; hay códigos especiales que no son producto) |
| `Description` | Nombre del producto |
| `Quantity` | Unidades por línea (negativa en cancelaciones) |
| `InvoiceDate` | Fecha y hora de la transacción |
| `Price` | Precio unitario en libras (£) |
| `Customer ID` | Identificador del cliente (5 dígitos); ~23 % de las líneas no lo tienen |
| `Country` | País de residencia del cliente |
