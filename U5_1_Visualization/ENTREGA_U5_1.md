# U5.1 — Entrega: NYC Open Data, PySpark local y Databricks + GitHub

**Última actualización:** 13/11/2026
**Fechas:** la plataforma marca cierre el **15/11/2026 a las 23:59**, pero las instrucciones hablan de revisión el **miércoles 18**. Tomo el **15/11** como límite, sin suponer prórroga.

## Estado de los requisitos

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Explorar NYC Open Data | ✅ Comprobado | [nota_nyc_open_data.md](nota_nyc_open_data.md) (datos consultados el 13/11/2026) |
| 2 | Notebook ejecutado en mi computadora sin errores | ✅ Comprobado | [notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb](notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb): 6/6 celdas de código, 0 errores |
| 3A | Local → GitHub → pull en Databricks | ✅ Comprobado | Commit local `58b85dd` → **Pull** en Databricks: "Successfully pulled changes" |
| 3B | Databricks → GitHub → pull en local | ✅ Comprobado | Commit `3df2f26` hecho en Databricks → `git pull` local: fast-forward `58b85dd..3df2f26` |

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
| Notebook + nota + requirements | `1e35fb0` | Mac → GitHub | push OK |
| A1: marca `SYNC-A-LOCAL-20261113` | `6ecfeea` | Mac → GitHub | push OK; llegó a Databricks al clonar y cambiar de rama |
| **A2: marca `SYNC-A2-LOCAL-PULL`** | `58b85dd` | Mac → GitHub → **Pull en Databricks** | Databricks: "Successfully pulled changes", rama en `58b85dd`, el archivo muestra la marca |
| **B: marca `SYNC-B-DATABRICKS-20261113`** | `3df2f26` | Databricks → GitHub → **`git pull` en Mac** | Databricks: "Successfully committed and pushed changes to branch prueba-databricks-u5_1". En la Mac: `Fast-forward 58b85dd..3df2f26`, autor AriRodo111 |

Para comprobarlo en la Mac:
```bash
git log --oneline -4 prueba-databricks-u5_1
```
Debe mostrar `3df2f26`, `58b85dd`, `6ecfeea` y `1e35fb0`.

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
