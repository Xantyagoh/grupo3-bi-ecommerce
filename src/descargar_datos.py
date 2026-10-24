"""Descarga el dataset Online Retail II (UCI) y lo deja listo en data/raw/.

Fuente : https://archive.ics.uci.edu/dataset/502/online+retail+ii  (CC BY 4.0)
DOI    : 10.24432/C5CG6D
Uso    : python src/descargar_datos.py

Genera dos archivos en data/raw/ (ignorados por git por su tamano):
  - online_retail_II.xlsx : el original (2 hojas, una por periodo)
  - online_retail_II.csv  : las 2 hojas unidas; es el que leen los notebooks
"""
import io
import zipfile
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
DESTINO = Path(__file__).resolve().parents[1] / "data" / "raw"


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    xlsx = DESTINO / "online_retail_II.xlsx"
    csv = DESTINO / "online_retail_II.csv"

    if not xlsx.exists():
        print("Descargando (~45 MB)...")
        with urlopen(URL) as r:
            datos = r.read()
        with zipfile.ZipFile(io.BytesIO(datos)) as z:
            z.extractall(DESTINO)
        print(f"Descargado: {xlsx}")

    if not csv.exists():
        print("Convirtiendo a CSV (tarda ~1-2 minutos)...")
        hojas = pd.read_excel(xlsx, sheet_name=None, engine="openpyxl")
        df = pd.concat(hojas.values(), ignore_index=True)
        df.to_csv(csv, index=False)
        print(f"Listo: {csv} ({len(df):,} filas)")
    else:
        print(f"Ya existe {csv}")


if __name__ == "__main__":
    main()
