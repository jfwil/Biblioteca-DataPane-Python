import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datapane as dp
import webbrowser

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=500)
df = pd.DataFrame(data, columns=["Valores"])

sns.histplot(df["Valores"], bins=30, kde=True)
plt.title("Distribución Normal")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("histograma.png")
plt.close()

report = dp.Report(
    dp.Text("Ejmp1"),
    dp.DataTable(df.head(10)),
    dp.Media(file="histograma.png")
)

report.save(path="reporte.html", open=False)
webbrowser.open("reporte.html")   