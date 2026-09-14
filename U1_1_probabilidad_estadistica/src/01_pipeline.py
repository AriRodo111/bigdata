from pathlib import Path

import pandas as pd
import requests

# Carpeta raíz de la práctica: el script funciona igual si se ejecuta
# desde la raíz de la práctica, desde src/ o desde cualquier otra carpeta
RUTA_PRACTICA = Path(__file__).resolve().parent.parent

# ============================================================
# 1. EXTRACCIÓN — Fetch the data
# ============================================================

url_datos = "https://ourworldindata.org/grapher/life-expectancy.csv?v=1&csvType=full&useColumnShortNames=true"

df = pd.read_csv(
    url_datos,
    storage_options={
        "User-Agent": "Our World In Data data fetch/1.0"
    }
)

# ============================================================
# 2. EXTRACCIÓN — Fetch the metadata
# ============================================================

url_metadata = "https://ourworldindata.org/grapher/life-expectancy.metadata.json?v=1&csvType=full&useColumnShortNames=true"

metadata = requests.get(url_metadata, timeout=30).json()

# ============================================================
# 3. EXPLORACIÓN INICIAL
# ============================================================

print("Dimensiones del DataFrame:")
print(df.shape)

print("\nColumnas:")
print(df.columns.tolist())

print("\nTipos de datos:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

# ============================================================
# 4. LIMPIEZA
# ============================================================

# Eliminar registros que no tengan código de país
df = df.dropna(subset=["code"])

# Eliminar registros que no tengan esperanza de vida
df = df.dropna(subset=["life_expectancy_0"])

# Eliminar los agregados de OWID (continentes, grupos de ingreso y World),
# que sí tienen código (OWID_...) y no son países.
# Kosovo (OWID_KOS) y la URSS (OWID_USS) sí se conservan.
agregados = ["OWID_AFR", "OWID_ASI", "OWID_EUR", "OWID_OCE", "OWID_WRL",
             "OWID_HIC", "OWID_UMC", "OWID_LMC", "OWID_LIC"]
df = df[~df["code"].isin(agregados)]

# ============================================================
# 5. TRANSFORMACIÓN
# ============================================================

# Convertir el año a entero
df["year"] = df["year"].astype(int)

# ============================================================
# 6. FILTRADO
# ============================================================

# Trabajaremos únicamente con datos a partir del año 2000
df = df[df["year"] >= 2000]

# ============================================================
# 7. ANÁLISIS
# ============================================================

# Promedio de esperanza de vida por país,
# redondeado a dos decimales después de calcular la media
promedio_pais = (
    df.groupby("entity")["life_expectancy_0"]
      .mean()
      .round(2)
      .sort_values(ascending=False)
)

print("\nPromedio de esperanza de vida por país:")
print(promedio_pais.head(10))

# ============================================================
# 8. RESULTADO
# ============================================================
archivo_salida = RUTA_PRACTICA / "data" / "processed" / "promedio_esperanza_vida_por_pais.csv"

promedio_pais.to_csv(
    archivo_salida,
    header=["Average life expectancy"]
)

print("\nPipeline ejecutado correctamente.")
print(f"Archivo generado: {archivo_salida}")
