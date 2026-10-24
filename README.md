# Análisis de E-commerce con Business Intelligence · Grupo 3

**Evento Evaluativo 3 · Análisis de Datos · Ingeniería de Sistemas · ITM 2026-2**
Docente: Daniel Alexis Nieto Mora · Proyecto asignado: **Equipo 3 — E-commerce**

| Integrante | Usuario de GitHub |
|---|---|
| Santiago Betancur | [@Xantyagoh](https://github.com/Xantyagoh) |
| Diego Alzate | [@DiegoA1123](https://github.com/DiegoA1123) |
| Carlos Mendez | [@carmarisx](https://github.com/carmarisx) |
| Sebastian Cadavid | [@Exmen9](https://github.com/Exmen9) |
| Daniel Martinez | [@danielmmnez](https://github.com/danielmmnez) |

---

## Objetivo

Convertir las transacciones de una tienda en línea mayorista en **información útil para la toma de decisiones**, mediante un modelo de datos, indicadores (KPIs), **pruebas de hipótesis** y un **dashboard en Power BI**, para responder:

1. ¿Cómo evolucionan las ventas y qué tan fuerte es la estacionalidad?
2. ¿Qué tan concentrados están los ingresos en pocos clientes, productos y países?
3. ¿Qué proporción de clientes vuelve a comprar y qué diferencia a quienes lo hacen?
4. ¿Qué tan grandes son las devoluciones y dónde se concentran?
5. ¿Los clientes del exterior se comportan distinto a los del Reino Unido?

## Dataset

**Online Retail II** (UCI Machine Learning Repository, id 502 · [DOI 10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D) · CC BY 4.0): 1.067.371 líneas de factura de una tienda en línea del Reino Unido entre dic-2009 y dic-2011. Más detalle en [`data/README.md`](data/README.md).

## Metodología

El proyecto sigue las 6 fases del enunciado; cada fase tiene su notebook o entregable:

| Fase | Qué se hace | Dónde |
|---|---|---|
| 1. Comprensión del problema | Contexto, problema de negocio, 5 preguntas clave, auditoría de calidad | `notebooks/01_comprension_problema.ipynb` |
| 3. Preparación y modelado | Limpieza con trazabilidad, atípicos, variables, modelo en estrella | `notebooks/02_preparacion_modelado.ipynb` |
| 1-2. Exploración | EDA univariado y multivariado, segmentación RFM, cohortes | `notebooks/03_eda.ipynb` |
| 2 y 6. Hipótesis y validación | 6 hipótesis (H0/H1), supuestos, pruebas, tamaño del efecto, corrección de Holm | `notebooks/04_hipotesis_validacion.ipynb` |
| 4. KPIs | 7 KPIs con fórmula, justificación e interpretación | `notebooks/05_kpis.ipynb` |
| 5. Dashboard | Power BI de 6 páginas (incluye dashboard ejecutivo) | `dashboard/` |
| 6. Storytelling | Narrativa, decisiones propuestas y limitaciones | `docs/storytelling_y_decisiones.md` |

## Estructura del repositorio

```
├── README.md
├── requirements.txt
├── data/
│   ├── README.md              fuente, licencia y diccionario de datos
│   ├── raw/                   datos originales (no se versionan)
│   └── processed/             datos limpios, modelo en estrella, RFM, resultados
├── src/descargar_datos.py     descarga el dataset desde la UCI
├── notebooks/                 01 a 05
├── dashboard/                 .pbix, medidas DAX, tema, guía y capturas
└── docs/                      figuras y storytelling
```

## Cómo reproducir

```bash
git clone https://github.com/Xantyagoh/grupo3-bi-ecommerce.git
cd grupo3-bi-ecommerce
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python src/descargar_datos.py    # descarga y convierte los datos (1-2 min)
jupyter notebook                 # ejecutar los notebooks 01 a 05 en orden (Restart & Run All)
```

El dashboard se abre con **Power BI Desktop** (`dashboard/grupo3_ecommerce.pbix`); si se pide actualizar datos, apuntar la carpeta `data/processed/modelo_bi/`.

## Video explicativo

_(se agrega el enlace al final del proyecto)_

## Referencias

- Chen, D. (2019). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D
