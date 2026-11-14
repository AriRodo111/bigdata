# Actividad 1 — Exploración de NYC Open Data

**Fecha de consulta:** 13 de noviembre de 2026
**Portal:** https://www.nyc.gov/opendata (catálogo de datos en https://data.cityofnewyork.us)
**Cómo se consultó:** navegando el portal y usando la API pública del catálogo (Socrata). No se descargó ningún conjunto completo, solo metadatos y conteos.

## Qué es y para qué sirve

NYC Open Data es el portal donde las dependencias de la Ciudad de Nueva York publican sus datos gratis para que cualquiera los consulte, los descargue o los use por API. Existe porque una ley local (Local Law 11 de 2012) obliga a las agencias a publicar sus datos públicos. Sirve para hacer análisis, transparencia, periodismo, investigación y apps.

## Volumen y variedad (datos verificables, 13/11/2026)

| Medida | Valor | Fuente |
|---|---|---|
| Recursos en el catálogo (datasets, mapas, vistas, etc.) | 3,028 | API del catálogo, `domains=data.cityofnewyork.us` |
| De esos, conjuntos de tipo *dataset* | 2,410 | ídem, `only=dataset` |
| Resultados al buscar "taxi" | 106 | ídem, `q=taxi` |

**Recursos por categoría:** City Government 909 · Education 652 · **Transportation 373** · Environment 211 · Housing & Development 208 · Social Services 170 · Public Safety 141 · Recreation 105 · Health 77 · Business 68.

**Algunos datasets grandes (filas contadas con la API el 13/11/2026):**

| Dataset | Agencia | Filas | Enlace |
|---|---|---|---|
| 311 Service Requests from 2020 to Present | 311 | 23,125,617 | https://data.cityofnewyork.us/d/erm2-nwe9 |
| Motor Vehicle Collisions – Crashes | NYPD | 2,305,239 | https://data.cityofnewyork.us/d/h9gi-nx95 |
| 2023 Yellow Taxi Trip Data | TLC | 38,310,226 (conteo de no nulos en los metadatos) | https://data.cityofnewyork.us/d/4b4i-vvec |

Varios de estos se actualizan **a diario** (el 311 y Collisions mostraban actualización del 13/11/2026).

## Transporte y taxis

La TLC (Taxi and Limousine Commission) es de las agencias más consultadas del portal:

| Dataset | Para qué sirve | Enlace |
|---|---|---|
| 2023 Yellow Taxi Trip Data | Cada viaje de taxi amarillo: horas, distancia, tarifa, propina | https://data.cityofnewyork.us/d/4b4i-vvec |
| Yellow Taxi Trip Data 2014–2022 (uno por año) | Lo mismo, años anteriores (ej. 2019) | https://data.cityofnewyork.us/d/2upf-qytp |
| 2016 Green Taxi Trip Data | Viajes de taxis verdes (fuera de Manhattan centro) | https://data.cityofnewyork.us/d/hvrh-b6nb |
| NYC Taxi Zones | Mapa de las zonas `PULocationID`/`DOLocationID` del notebook | https://data.cityofnewyork.us/d/8meu-9t5y |
| For Hire Vehicles (FHV) – Active | Vehículos tipo Uber/Lyft con licencia vigente (el dataset más visto del portal: 3,964,659 vistas) | https://data.cityofnewyork.us/d/8wbx-tsch |
| Taxi and FHV Relief Stands (DOT) | Lugares donde taxis pueden detenerse | https://data.cityofnewyork.us/d/vqu8-xef9 |

**Relación con el notebook:** el Parquet que usamos (`yellow_tripdata_2025-01.parquet`) no viene de este portal, sino de la página de la TLC (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Solo enero de 2025 trae **3,475,226 viajes** en un archivo de **59 MB** (59,158,238 bytes, medido con una petición HEAD).

## Para comentarlo en la revisión

- Nueva York genera datos de casi todo: quejas al 311, choques, edificios, escuelas, nómina y taxis. Hay más de 3 mil recursos publicados.
- El volumen es de Big Data de verdad. El 311 pasa de 23 millones de filas, y un **solo año** de taxis amarillos tiene unos 38 millones. Un mes de taxis ya son 3.5 millones de filas.
- Además, los datos se actualizan seguido (varios a diario) y vienen en formatos distintos (tablas, mapas, archivos). Por eso tiene sentido usar Spark en lugar de pandas cuando se quiere procesar todo.
- En la práctica solo exploré el catálogo y conté filas con la API. No descargué nada pesado.
