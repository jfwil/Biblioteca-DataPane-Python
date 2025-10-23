import itertools
import pandas as pd
import matplotlib.pyplot as plt
import datapane as dp
import webbrowser
from math import comb, factorial
from itertools import combinations_with_replacement

#espacio muestral 
dados = [1, 2, 3, 4, 5, 6]
ordenados = list(itertools.product(dados, repeat=2))  # 6*6 = 36 elementos Permutacion
no_ordenados = list(combinations_with_replacement(dados, 2))  # 21 combos Combinacion

#DataFrame permutaciones para las graficas
df_ordenados = pd.DataFrame(ordenados, columns=["Dado1", "Dado2"])
df_ordenados["Suma"] = df_ordenados["Dado1"] + df_ordenados["Dado2"]
df_ordenados["SumaEsPar"] = df_ordenados["Suma"] % 2 == 0


total_permutaciones = len(df_ordenados) # 36
favorables_permutaciones = df_ordenados["SumaEsPar"].sum()  # 18
prob_permutaciones = favorables_permutaciones / total_permutaciones

#dataFrame combinaciuones (sumas y si suma es par)
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
plt.savefig("pares_barras.png")
plt.close()

#tabla resumen de resultados 
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
    dp.Text("Probabilidad: suma par lanzando 2 dados"),
    dp.Text("Tabla: resultados ordenados (primeros 10)"),
    dp.DataTable(df_ordenados.head(10)),
    dp.Text("Tabla: combinaciones no ordenadas (21 combos)"),
    dp.DataTable(df_combinaciones),
    dp.Text("Resumen"),
    dp.DataTable(df_resumen),
    dp.Media(file="pares_barras.png"),
)

#guardar el reporte en HTML
report.save(path="reporte_dados_pares.html", open=True)


