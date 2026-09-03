# Big Data — Prácticas

Este repositorio contiene las **prácticas de la materia de Big Data**. Cada práctica es un
proyecto independiente, con sus propios datos, su propio notebook y su propia documentación,
de manera que se pueda revisar y ejecutar por separado y se conserve el registro de avance
mediante Git y GitHub.

## Materia

- **Materia:** Big Data
- **Autora:** Ariadna Gómez
- **Lenguaje de análisis:** Python

## Herramientas utilizadas

| Herramienta | Uso |
|-------------|-----|
| Python | Lenguaje con el que se realiza todo el análisis |
| pandas | Carga, filtrado y exploración de los conjuntos de datos |
| NumPy | Soporte numérico para los cálculos estadísticos |
| Jupyter Notebook | Entorno donde se documenta y ejecuta cada práctica |
| Git y GitHub | Control de versiones y publicación del repositorio |

## Organización del repositorio

El repositorio se organiza **por unidad y por práctica**. El nombre de cada carpeta sigue el
patrón `U<unidad>_<número de práctica>_<nombre>`:

```text
bigdata/
├── README.md                          # Este archivo: información general de la materia
├── .gitignore                         # Reglas de exclusión válidas para todas las prácticas
│
└── U1_1_probabilidad_estadistica/     # Práctica 1.1
    ├── README.md                      # Documentación de la práctica
    ├── requirements.txt               # Dependencias de la práctica
    ├── data/
    │   ├── raw/                       # Datos originales, sin modificar
    │   └── processed/                 # Datos transformados (vacía por ahora)
    ├── notebooks/                     # Notebooks del análisis
    └── src/                           # Scripts de apoyo
```

Cada carpeta de práctica repite siempre la misma estructura interna (`README.md`,
`requirements.txt`, `data/raw/`, `data/processed/`, `notebooks/` y `src/`), para que todas las
prácticas se lean y se ejecuten de la misma forma.

## Prácticas disponibles

| Práctica | Carpeta | Tema | Dataset | Notebook |
|----------|---------|------|---------|----------|
| Práctica 1.1 | [`U1_1_probabilidad_estadistica/`](U1_1_probabilidad_estadistica/) | Identificación de la fuente, exploración de datos y estadística descriptiva | *Annual change in population* (Our World in Data / UN WPP 2024) | `01_evolucion_poblacional.ipynb` |

### Descripción de cada práctica

**Práctica 1.1 — Evolución poblacional (`U1_1_probabilidad_estadistica/`)**
Análisis de la evolución de la población mundial a partir del indicador *Annual change in
population* de Our World in Data. La práctica documenta la fuente original de los datos, carga
y explora el archivo CSV con pandas (dimensiones, columnas, tipos de datos, valores faltantes y
número de entidades) y calcula las medidas de estadística descriptiva —media, mediana, varianza,
desviación estándar, mínimo y máximo— sobre la variable principal, tomando como subconjunto de
estudio a Granada entre 1983 y 2021.

## Cómo trabajar con una práctica

Cada práctica se ejecuta desde su propia carpeta y con su propio entorno virtual. Las
instrucciones detalladas (creación del entorno, instalación de dependencias y ejecución del
notebook) están en el `README.md` de cada práctica.
