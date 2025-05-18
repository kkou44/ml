import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

# === パラメータ設定 ===
N = 300
num_categories = 3  # ← カテゴリー数をここで自由に設定！

# === データ生成 ===
x = np.random.randn(N)
y = np.random.randn(N)
z = np.random.randn(N)
categories = np.random.choice(range(1, num_categories + 1), size=N)

# === カラーマップ設定 ===
cmap = plt.get_cmap('viridis', num_categories)
colors = [
    f'rgb({r * 255:.0f},{g * 255:.0f},{b * 255:.0f})'
    for r, g, b, _ in cmap(np.linspace(0, 1, num_categories))
]

# === Plotlyで3D散布図を作成 ===
fig = go.Figure()

for i, cat in enumerate(np.unique(categories)):
    idx = categories == cat
    print(i, cat)

    txt = ["破綻" if n%2 == 0 else "成立" for n in range(len(x[idx]))]
    fig.add_trace(go.Scatter3d(
        x=x[idx],
        y=y[idx],
        z=z[idx],
        mode='markers',
        name=f'Dataset {cat}\n identifier {i}',
        text=txt,
        marker=dict(
            size=5,
            color=colors[i % len(colors)],
            opacity=0.8
        )
    ))

# === レイアウト設定 ===
fig.update_layout(
    title=f"Interactive 3D Scatter Plot (Datasets 1–{num_categories})",
    legend_title="Datasets",
    legend=dict(itemsizing='constant')
)

import plotly.io as pio
pio.write_html(fig, file="scatter3d_plot.html", auto_open=False)
