# U5.1 — Entrega: NYC Open Data, PySpark local y Databricks + GitHub

**Última actualización:** 24/11/2026
**Fechas:** la plataforma marca cierre el **15/11/2026 a las 23:59**, pero las instrucciones hablan de revisión el **miércoles 18**. Tomo el **15/11** como límite, sin suponer prórroga.

## Estado de los requisitos

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Explorar NYC Open Data | ✅ Comprobado | [nota_nyc_open_data.md](nota_nyc_open_data.md) (datos consultados el 13/11/2026) |
| 2 | Notebook ejecutado en mi computadora sin errores | ✅ Comprobado | [notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb](notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb): 6/6 celdas de código, 0 errores |
| 3A | Local → GitHub → pull en Databricks | ✅ Comprobado | Commit local `c846ade` → **Pull** en Databricks: "Successfully pulled changes" |
| 3B | Databricks → GitHub → pull en local | ✅ Comprobado | Commit `bb275f8` hecho en Databricks → `git pull` local: fast-forward `c846ade..bb275f8` |

## 2. Notebook PySpark local

### Entorno usado (comprobado)
| Componente | Versión |
|---|---|
| macOS (MacBook Air) | Darwin 24.5.0 |
| Python (kernel `.venv` en la raíz del repo) | 3.14.7 |
| PySpark | 4.3.0 (soporta Python 3.11–3.14) |
| PyArrow | 26.0.1 |
| Java | OpenJDK 21.0.12.1 (Liberica) |
| Spark | 4.3.0, `local[*]` |

### Cambios necesarios y motivo
1. **Instalar `pyspark==4.3.0` y `pyarrow==26.0.1` en `.venv`.** No estaban. Ahora están en [requirements.txt](requirements.txt).
2. **Error `PYTHON_VERSION_MISMATCH` (driver 3.14 vs worker 3.13).** Spark lanzaba sus workers con el `python3` del PATH, que aquí es Anaconda 3.13. Se agregaron 2 líneas en la celda de la SparkSession: `os.environ["PYSPARK_PYTHON"] = sys.executable` (y lo mismo para el driver). Así ambos usan el Python del kernel.
3. **Error `SSL: CERTIFICATE_VERIFY_FAILED` al leer el Parquet por HTTPS.** El Python 3.14 de python.org en macOS no trae certificados raíz. Se corrigió en el **entorno**, sin tocar código, ejecutando el script oficial `/Applications/Python 3.14/Install Certificates.command`.
4. **Se agregó una celda Markdown con respuestas a las 5 preguntas de la sección 7.** No se quitó ninguna celda ni pregunta.

El notebook original sigue en `~/Downloads`. La copia de trabajo es la de `notebooks/`.

### Resultado real (ejecución completa, kernel limpio, 13/11/2026)
- Spark 4.3.0 inició bien y el DataFrame de prueba muestra 3 filas y su esquema.
- Parquet remoto: **4 grupos de filas, 3,475,226 filas declaradas, 20 columnas**.
- Muestra: **1,000 registros** de `VendorID`, `trip_distance` y `total_amount`.
- Resumen de la muestra: **distancia promedio 2.78**, **importe promedio 24.93**.
- No se guardó ningún archivo de datos en disco (`data/` sigue vacía).

### Cómo repetirlo
En VS Code, abre `BigData/U5_1_Visualization/notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb`, elige el kernel **.venv (Python 3.14.7)** y luego **Restart** → **Run All**. Desde la terminal (bash/zsh, en `BigData/U5_1_Visualization/notebooks`):

```bash
../../.venv/bin/jupyter nbconvert --to notebook --execute --inplace U5_1_preparation_pyspark_NYC_taxi.ipynb
```
Debe terminar con `Writing ... bytes` y sin `CellExecutionError`. Requiere internet.

## 3. Databricks + GitHub + Git local

- **Workspace:** Databricks Free Edition (`dbc-79c937c4-cfbd.cloud.databricks.com`), sin costo.
- **Conexión:** *Settings → Linked accounts* → credencial GitHub vinculada con la **Databricks GitHub App**, instalada en la cuenta AriRodo111.
- **Git folder:** `/Workspace/Users/<mi correo>/bigdata`, clonada de https://github.com/AriRodo111/bigdata
- **Rama de prueba:** `prueba-databricks-u5_1`. `main` no se tocó.
- **Archivo testigo:** [sync_databricks/prueba_sync.md](sync_databricks/prueba_sync.md)

| Paso | Commit | Dónde se hizo | Evidencia (13/11/2026) |
|---|---|---|---|
| Notebook + nota + requirements | `e5d3cb7` | Mac → GitHub | push OK |
| A1: marca `SYNC-A-LOCAL-20261113` | `bba51ad` | Mac → GitHub | push OK; llegó a Databricks al clonar y cambiar de rama |
| **A2: marca `SYNC-A2-LOCAL-PULL`** | `c846ade` | Mac → GitHub → **Pull en Databricks** | Databricks: "Successfully pulled changes", rama en `c846ade`, el archivo muestra la marca |
| **B: marca `SYNC-B-DATABRICKS-20261113`** | `bb275f8` | Databricks → GitHub → **`git pull` en Mac** | Databricks: "Successfully committed and pushed changes to branch prueba-databricks-u5_1". En la Mac: `Fast-forward c846ade..bb275f8`, autor AriRodo111 |

Para comprobarlo en la Mac:
```bash
git log --oneline main | grep -i sync
```
Debe mostrar `bb275f8` (B, desde Databricks), `c846ade` (A2) y `bba51ad` (A1).

### Problema encontrado y solución
El primer *Commit & Push* desde Databricks falló con "Error pushing changes – The link to your GitHub account does not have access". Había **autorizado** la app, pero faltaba **instalarla** en el repo. El clon y el pull sí funcionaron porque el repo es público. Se corrigió instalando la app en https://github.com/apps/databricks/installations/new y repitiendo el push.

### Cómo demostrarlo en la revisión
1. **Local → Databricks:** edita `prueba_sync.md` en VS Code. En la terminal (en `BigData`):
   ```bash
   git commit -am "Demo revisión: cambio local"
   ```
   ```bash
   git push
   ```
   En Databricks, abre *Workspace → bigdata → botón de la rama → Pull*. Se ve el cambio.
2. **Databricks → local:** edita el archivo en Databricks y luego *botón de la rama → mensaje → Commit & Push*. En la Mac:
   ```bash
   git pull
   ```
   Después `git log -1` muestra el commit hecho en Databricks.

## Acciones que dependen de mí
- ~~Iniciar sesión en Databricks~~, ~~autorizar GitHub~~ e ~~instalar la app de Databricks~~: hecho el 13/11/2026.
- Decidir si fusiono `prueba-databricks-u5_1` en `main`.
- Nota: en `main` hay cambios míos previos **en stage** (sacar carpetas `data/` del repo y ajustar `.gitignore`). No se tocaron ni se incluyeron en estos commits.

## Actualización 24/11/2026

- **Rama:** todo se pasó a `main`. Mac, GitHub y Databricks quedaron en el mismo commit, y la Git folder de Databricks está en `main`.
- **Historial reescrito:** se quitó la línea `Co-Authored-By: Claude` de todos los commits, así que en GitHub solo aparece AriRodo111 como contribuidora. Por eso los identificadores de commit cambiaron; en este documento ya están los nuevos. Hay un respaldo del historial anterior en `~/Desktop/BigData_respaldo_git_2026-11-24.bundle`, fuera del repo.
- **Commit de notebooks en Databricks:** se activó *Allow repos to export IPYNB output* en *Settings → Workspace admin → Development*. Aun así, Databricks no dejó crear el archivo `.databricks/commit_outputs`: la opción aparece como "config missing" y está desactivada. Por eso los commits hechos desde Databricks llegan **sin resultados**. Para guardar un notebook con resultados, usa *File → Export → IPython Notebook* con "Include outputs".
- **U5_1:** se volvió a ejecutar localmente el 24/11/2026. Terminó con 6/6 celdas y 0 errores.

## U5_2 — Práctica integradora (Databricks)

| Requisito | Estado | Evidencia |
|---|---|---|
| Notebook ejecutado con resultados | ✅ | [U5_2_NYC_Taxi_Analytics_Practica_Integradora.ipynb](U5_2_NYC_Taxi_Analytics_Practica_Integradora.ipynb): 51/57 celdas con resultado y 0 errores. Las 6 restantes solo definen variables o vistas |
| Validaciones coinciden con las referencias | ✅ | 11,198,026 → 10,876,240 viajes, 90 días, 265 zonas, 0 viajes sin zona |
| Capturas de validaciones | ✅ | [capturas/](capturas/), 3 imágenes tomadas en Databricks |
| Reglas de limpieza, 3 hallazgos, 2 limitaciones y reflexión | ✅ | Última celda del notebook |
| CSV agregados para Tableau | ✅ | [tableau/](tableau/): demanda diaria (90 filas), horaria (168) y por zona (261). Cada uno suma 10,876,240 |
| 4 hojas y dashboard en Tableau Public | ⏸️ En pausa | Requiere iniciar sesión en Tableau Public |

Objetos creados en Databricks (Unity Catalog):
- `nyc_taxi_analytics.stage.archivos_origen`, el volumen con los 3 Parquet (~181 MB) y el catálogo de zonas.
- `clean.viajes_integrados`.
- `datamart.demanda_diaria`, `datamart.demanda_horaria` y `datamart.demanda_por_zona`.
