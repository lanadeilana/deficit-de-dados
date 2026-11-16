"""Déficit de Dados, Ed008: gera as imagens estáticas do gráfico a partir dos CSVs em dados/.

Saídas em img/:
  ed008_grafico_substack.png  1456x816, para o corpo do post no Substack
  ed008_grafico_quadrado.png  1080x1080, para LinkedIn e Instagram

Uso:  python graficos_ed008.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

AQUI = Path(__file__).parent
neg = pd.read_csv(AQUI / "dados/serasa_negativados_setembro.csv")
des = pd.read_csv(AQUI / "dados/desemprego_3tri.csv")

PRETO, LARANJA, CINZA, BRANCO, APOIO = "#0D0D0D", "#FF6B35", "#6E6862", "#F4F1EE", "#9C958F"
plt.rcParams["font.family"] = "DejaVu Sans"


def painel(ax, x, y, titulo, sufixo, ymin, ymax):
    ax.set_facecolor(PRETO)
    ax.plot(x, y, color=CINZA, lw=3, zorder=1)
    ax.scatter(x[:-1], y[:-1], color=CINZA, s=40, zorder=2)
    ax.scatter(x[-1:], y[-1:], color=LARANJA, s=120, zorder=3)
    for i, (xi, yi) in enumerate(zip(x, y)):
        ultimo = i == len(x) - 1
        ax.annotate(f"{yi:.1f}".replace(".", ",") + sufixo, (xi, yi), xytext=(0, 12),
                    textcoords="offset points", ha="center",
                    color=LARANJA if ultimo else BRANCO,
                    fontsize=15 if ultimo else 12, fontweight="bold" if ultimo else "normal")
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(x)
    ax.tick_params(colors=APOIO, length=0, labelsize=12)
    ax.set_yticks([])
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("#2B2826")
    ax.set_title(titulo, color=BRANCO, loc="left", fontsize=14, pad=14)


def figura(tamanho, arquivo, empilhado):
    fig = plt.figure(figsize=tamanho, dpi=100, facecolor=PRETO)
    grade = (2, 1) if empilhado else (1, 2)
    a = fig.add_subplot(*grade, 1)
    b = fig.add_subplot(*grade, 2)
    painel(a, neg["ano"], neg["negativados_milhoes"], "Negativados na Serasa, setembro (milhões)", "", 60, 90)
    painel(b, des["ano"], des["desemprego_pct"], "Desemprego, 3º trimestre (%)", "%", 0, 10)
    d = neg["negativados_milhoes"].iloc[-1] - neg["negativados_milhoes"].iloc[0]
    fig.suptitle("Desemprego no menor nível, negativados no maior", color=BRANCO,
                 fontsize=22, fontweight="bold", x=0.04, ha="left", y=0.97)
    fig.text(0.04, 0.905 if not empilhado else 0.925,
             f"2022 a 2026: +{d:.1f} milhões de negativados enquanto o desemprego caiu de 8,7% para 5,2%".replace(".", ","),
             color=APOIO, fontsize=13)
    fig.text(0.04, 0.02, "Fontes: Serasa, Mapa da Inadimplência · IBGE, PNAD Contínua   |   DÉFICIT DE DADOS",
             color=APOIO, fontsize=10)
    fig.subplots_adjust(left=0.04, right=0.97, top=0.78 if not empilhado else 0.84,
                        bottom=0.12 if not empilhado else 0.08, wspace=0.12, hspace=0.45)
    fig.savefig(AQUI / "img" / arquivo, facecolor=PRETO)
    plt.close(fig)


(AQUI / "img").mkdir(exist_ok=True)
figura((14.56, 8.16), "ed008_grafico_substack.png", empilhado=False)
figura((10.8, 10.8), "ed008_grafico_quadrado.png", empilhado=True)
print("Imagens salvas em img/")
