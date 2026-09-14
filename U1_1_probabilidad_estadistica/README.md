# Práctica 1.1 — Análisis de la evolución poblacional mundial

## 1. Introducción

Práctica correspondiente a la materia de **Big Data**, dentro del bloque de **Probabilidad y
Estadística**.

El **objetivo** de la práctica es identificar correctamente la fuente de un conjunto de datos
real, cargarlo y explorarlo con Python, y calcular sobre él las principales medidas de
estadística descriptiva.

El **problema que se analiza** es cómo ha cambiado la población de las distintas entidades del
mundo a lo largo del tiempo: cuántas entidades y años cubre el conjunto de datos, qué valores
faltantes contiene, y qué magnitud y qué dispersión presenta el cambio poblacional, tanto a
nivel global como en un subconjunto concreto (Granada, 1983–2021).

El análisis se realiza con **Python**, utilizando:

- **pandas** — carga, filtrado y exploración del dataset.
- **NumPy** — soporte numérico para los cálculos.
- **Jupyter Notebook** — entorno donde se documenta y se ejecuta el análisis.

## 2. Fuente de los datos

- **Dataset:** *Annual change in population* (Cambio anual de la población).
- **Publicado por:** Our World in Data (OWID).
- **Fuente original:** United Nations — *World Population Prospects* (2024), procesado por
  Our World in Data.
- **URL:** <https://ourworldindata.org/grapher/annual-population-growth>
- **Datos originales:** <https://population.un.org/wpp/downloads/>
- **Fecha de descarga del paquete de datos:** 9 de agosto de 2026.

**Qué información contiene.** Cada fila es una observación de una entidad (país, región o
agregado) en un año determinado. La **variable principal**, `Annual change in population`,
representa el **cambio neto anual de la población**, calculado como la diferencia entre la
población al 1 de julio de dos años consecutivos. Al ser un cambio *neto*, refleja de forma
combinada los nacimientos, las defunciones y la migración. La unidad son **personas**.

**Entidades y periodo.** El archivo contiene **256 entidades** (países, regiones y agregados
como *World*) y cubre los años **1951 a 2100**. La serie de estimaciones históricas
(`Annual change in population`) abarca **1951–2023** y la serie de proyecciones bajo el escenario
medio de la ONU (`Annual population change (Projected)`) abarca **2024–2100**.

### Cita oficial de la fuente

> UN, World Population Prospects (2024) – processed by Our World in Data. “Annual change in
> population – UN WPP” [dataset]. United Nations, “World Population Prospects”; United Nations,
> “World Population Prospects - Interim Update” [original data].

### Dataset adicional descargado

En `data/raw/` se conserva también el paquete **`births-and-deaths-projected-to-2100`**
(*Births and deaths per year*, Our World in Data / UN WPP 2024). Se descargó junto con
el anterior, pero **todavía no se utiliza en ningún notebook** de esta práctica.

## 3. Variables utilizadas

Nombres reales de las columnas del archivo
`annual-population-growth.csv`:

| Variable | Descripción |
|----------|-------------|
| `Entity` | Nombre del país, región o agregado |
| `Code` | Código OWID de la entidad (normalmente el código ISO alpha-3; vacío en agregados) |
| `Year` | Año de la observación |
| `Annual change in population` | Cambio neto anual de la población, estimaciones 1951–2023 (personas) |
| `Annual population change (Projected)` | Cambio neto anual de la población, proyecciones 2024–2100 (personas) |

## 4. Estructura de la práctica

```text
U1_1_probabilidad_estadistica/
├── README.md                                     # Documentación de la práctica
├── requirements.txt                              # Dependencias necesarias
├── data/
│   ├── raw/                                      # Datos originales, sin modificar
│   │   ├── annual-population-growth/             # Dataset utilizado en el análisis
│   │   │   ├── annual-population-growth.csv
│   │   │   ├── annual-population-growth.metadata.json
│   │   │   └── readme.md                         # Documentación original de OWID
│   │   └── births-and-deaths-projected-to-2100/  # Dataset descargado, aún sin analizar
│   │       ├── births-and-deaths-projected-to-2100.csv
│   │       ├── births-and-deaths-projected-to-2100.metadata.json
│   │       └── readme.md
│   └── processed/                                # Datos generados por los pipelines de src/
├── notebooks/
│   ├── 01_evolucion_poblacional.ipynb            # Notebook con las cuatro actividades
│   └── 02_transformaciones.ipynb                 # Transformaciones con pandas (esperanza de vida)
└── src/
    ├── 01_pipeline.py                            # Pipeline ETL: promedio de esperanza de vida por país
    └── 02_pipeline_auto.py                       # Pipeline automatizado en una función: limpieza general
```

### Pipelines y transformaciones (esperanza de vida)

Estos archivos usan el dataset *Life expectancy* de Our World in Data, que se **descarga
directamente de internet** al ejecutarlos (no se guarda en `data/raw/`), por lo que requieren
conexión y la librería `requests`.

- **`notebooks/02_transformaciones.ipynb`** — descarga los datos, renombra las columnas al
  español (`Pais`, `Codigo`, `Anio`, `Esperanza de Vida`), filtra entidades por texto, localiza y
  elimina los registros sin código (agregados como *Americas*), obtiene los 10 países con menor
  esperanza de vida en 2020 y mide la memoria usada por el DataFrame.
- **`src/01_pipeline.py`** — pipeline por etapas (extracción, exploración, limpieza,
  transformación, filtrado desde el año 2000, análisis y resultado). Excluye también los agregados
  de OWID que sí tienen código (`OWID_WRL`, continentes y grupos de ingreso) y guarda
  `data/processed/promedio_esperanza_vida_por_pais.csv`.
- **`src/02_pipeline_auto.py`** — agrupa la exploración y la limpieza (eliminar nulos y
  duplicados) en la función `ejecutar_pipeline(df)` y guarda
  `data/processed/auto_resultado.csv`.

Los scripts se ejecutan desde cualquier carpeta, por ejemplo:

```bash
python src/01_pipeline.py
```

Los archivos de `data/raw/` **no se modifican nunca**. Cualquier archivo derivado o transformado
debe guardarse en `data/processed/`, para mantener siempre separados los datos originales de los
datos procesados.

## 5. Requisitos e instalación

Se utiliza **Python 3.14** (el entorno con el que se ejecutó esta práctica es 3.14.7) y un
entorno virtual propio para la práctica.

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

Después, con el entorno activado:

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt`:

```text
pandas==3.0.5
numpy==2.5.2
requests
jupyter
ipykernel
notebook
```

## 6. Cómo ejecutar el análisis

1. Activar el entorno virtual (`source .venv/bin/activate` en macOS/Linux o
   `.venv\Scripts\activate` en Windows).
2. Abrir Jupyter Notebook con el comando `jupyter notebook`.
3. Entrar a la carpeta `notebooks/`.
4. Abrir el archivo `01_evolucion_poblacional.ipynb`.
5. Seleccionar el kernel correspondiente al entorno `.venv`.
6. Ejecutar las celdas **en orden**, de arriba hacia abajo.
7. También puede utilizarse `Run All` (*Kernel → Restart Kernel and Run All Cells*) para
   ejecutar el notebook completo.

El notebook está preparado para ejecutarse **de principio a fin sin errores**. La ruta del CSV
está definida de forma relativa, por lo que funciona tanto si el notebook se ejecuta desde la
carpeta `notebooks/` como desde la raíz de la práctica.

## 7. Contenido del notebook

- **Actividad 1 — Identificación de la fuente:** documentación del productor original de los
  datos, de la organización que los procesa, de la cita oficial y del significado de la variable
  analizada.
- **Actividad 2 — Carga y exploración de datos:** carga del CSV con `pd.read_csv()`, revisión de
  las dimensiones, los nombres de las columnas, los tipos de datos, las primeras filas, las
  estadísticas descriptivas generales, los valores faltantes y el número de entidades distintas;
  además, filtrado de subconjuntos por año y por entidad.
- **Actividad 3 — Estadística descriptiva:** cálculo de la media, la mediana, la varianza, la
  desviación estándar, el mínimo y el máximo de la variable `Annual change in population` para
  Granada entre 1983 y 2021, y comparación con el mínimo y el máximo de todo el dataset.
- **Actividad 4 — Comprobación del entorno:** verificación de las versiones de Python, pandas y
  NumPy utilizadas.

Después de las actividades que producen resultados, el notebook incluye una celda de
**Interpretación** que explica qué significan los valores obtenidos.
