import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv("Nayarit_012.csv")

# Combinamos la fecha y la hora para tener un registro temporal exacto
df["fecha_completa"] = pd.to_datetime(
    df["fecha"] + " " + df["hora"].astype(str) + ":00:00", dayfirst=True)

#Filtrar por un contaminante para el análisis
contaminante = "Ozono"
df_filtrado = df[df["nombre_contaminante"] == contaminante].copy()

#Agrupar por día para obtener el promedio diario y suavizar la gráfica
df_diario = (
    df_filtrado.groupby(df_filtrado["fecha_completa"].dt.date)["valor"]
    .mean()
    .reset_index()
)
df_diario["fecha_completa"] = pd.to_datetime(df_diario["fecha_completa"])

#Calcular la línea de tendencia)
x_numerico = df_diario["fecha_completa"].map(pd.Timestamp.toordinal)
y_valores = df_diario["valor"]

#Ajuste polinomial de grado 1 (línea recta: y = mx + b)
pendiente, interseccion = np.polyfit(x_numerico, y_valores, 1)
linea_tendencia = pendiente * x_numerico + interseccion

#Graficar
plt.figure(figsize=(12, 6))

#Dibujar los promedios diarios
plt.plot(
    df_diario["fecha_completa"],
    y_valores,
    label="Promedio Diario",
    color="steelblue",
    alpha=0.7,
)

#Dibujar la línea de tendencia
plt.plot(
    df_diario["fecha_completa"],
    linea_tendencia,
    label="Línea de Tendencia",
    color="crimson",
    linestyle="--",
    linewidth=2,
)

# Personalización de la gráfica
plt.title(
    f"Tendencia Temporal de {contaminante} (Tepic, Nayarit)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Fecha", fontsize=12)
plt.ylabel(f"Concentración ({df_filtrado['unidades'].iloc[0]})", fontsize=12)
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(fontsize=11)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()