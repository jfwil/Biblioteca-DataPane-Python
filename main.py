import itertools
import pandas as pd
import matplotlib.pyplot as plt
import datapane as dp
import webbrowser
from math import comb, factorial

#espacio muestral (permutaciones: pares ordenados)

dados = [1, 2, 3, 4, 5, 6]
ordenados = list(itertools.product(dados, repeat=2))  # 36 elementos (6*6)

#crear DataFrame con suma y paridad
df_ordenados = pd.DataFrame(ordenados, columns=["Dado1", "Dado2"])
df_ordenados["Suma"] = df_ordenados["Dado1"] + df_ordenados["Dado2"]
df_ordenados["SumaEsPar"] = df_ordenados["Suma"] % 2 == 0

#conteos
total_permutaciones = len(df_ordenados)                 # 36
favorables_permutaciones = df_ordenados["SumaEsPar"].sum()  # 18
prob_permutaciones = favorables_permutaciones / total_permutaciones

#casos no ordenados (combinaciones con reemplazo): (a,b) ~ (b,a)
from itertools import combinations_with_replacement
no_ordenados = list(combinations_with_replacement(dados, 2))  # 21 combos

#dataFrame combos no ordenados (sumas y si suma es par)
df_combinaciones = pd.DataFrame(no_ordenados, columns=["A", "B"])
df_combinaciones["Suma"] = df_combinaciones["A"] + df_combinaciones["B"]
df_combinaciones["SumaEsPar"] = df_combinaciones["Suma"] % 2 == 0

def multiplicidad(pair):
    a, b = pair
    return 1 if a == b else 2  # (x,x) aparece 1 vez en ordenados; (x,y) con x!=y aparece 2 veces (x,y) y (y,x)

df_combinaciones["Multiplicidad"] = df_combinaciones[["A", "B"]].apply(lambda r: multiplicidad(tuple(r)), axis=1)
df_combinaciones["CasosOrdenadosEquivalentes"] = df_combinaciones["Multiplicidad"]

n, k = 6, 2
combinaciones_formula = comb(n + k - 1, k) 
permutaciones_formula = n * n               

texto_explicativo = f"""
Cálculo combinatorio:

- Permutaciones (resultados ordenados) = 6 × 6 = {permutaciones_formula}
- Combinaciones con reemplazo (resultados no ordenados) = C(n + k - 1, k) = C(6+2-1, 2) = {combinaciones_formula}

Favorable (suma par) en permutaciones:
- (par, par) = 3 × 3 = 9
- (impar, impar) = 3 × 3 = 9
-> total favorables = {favorables_permutaciones}
Probabilidad (ordenado) = {favorables_permutaciones} / {total_permutaciones} = {prob_permutaciones:.4f}
"""

#grafico de barras
counts = df_ordenados["SumaEsPar"].value_counts().sort_index()
labels = ["Impar", "Par"]
values = [int(counts.get(False, 0)), int(counts.get(True, 0))]

plt.figure(figsize=(6,4))
plt.bar(labels, values)
plt.title("Conteo de sumas par vs impar (dos dados, resultados ordenados)")
plt.ylabel("Número de casos")
plt.xlabel("Paridad de la suma")
plt.tight_layout()
plt.savefig("paridad_barras.png")
plt.close()

#preparacion de tablas resumen
df_resumen = pd.DataFrame({
    "Concepto": [
        "Total permutaciones (ordenadas)",
        "Total combinaciones (no ordenadas)",
        "Favorables (suma par, permutaciones)",
        "Probabilidad (suma par, permutaciones)"
    ],
    "Valor": [
        permutaciones_formula,
        combinaciones_formula,
        int(favorables_permutaciones),
        f"{prob_permutaciones:.4f}"
    ]
})

#crear reporte con Datapane y guardarlo
report = dp.Report(
    dp.Text("# Probabilidad: suma par lanzando 2 dados"),
    dp.Text(texto_explicativo),
    dp.Text("## Tabla: resultados ordenados (primeros 10)"),
    dp.DataTable(df_ordenados.head(10)),
    dp.Text("## Tabla: combinaciones no ordenadas (21 combos)"),
    dp.DataTable(df_combinaciones),
    dp.Text("## Resumen"),
    dp.DataTable(df_resumen),
    dp.Media(file="paridad_barras.png"),
)

#guardar el reporte en HTML
report.save(path="reporte_dados_paridad.html", open=False)

print("Reporte guardado en: reporte_dados_paridad.html")
print("Abre ese archivo en tu navegador para ver el informe.")
