"""Déficit de Dados, Ed008 (Empregado e negativado): reprodução dos dados principais.

Baixa do Banco Central (API SGS) a inadimplência das famílias e o endividamento,
e do IBGE (API SIDRA, tabela 4099) a taxa de desocupação da PNAD Contínua.
A série de negativados da Serasa não tem API e foi copiada das divulgações mensais.

Uso:  pip install requests pandas matplotlib
      python reproduzir_ed008.py
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Códigos SGS que precisam ser conferidos em https://www3.bcb.gov.br/sgspub
# O script compara a última leitura com o número publicado e avisa se não bater.
SGS = {
    "inadimplencia_pf_livre": (21112, 8.1),   # % da carteira PF com recursos livres, atraso > 90 dias (set/2026: 8,1)
    "endividamento_familias": (29037, 50.1),  # % da renda acumulada em 12 meses (ago/2026: 50,1)
}

# Serasa, Mapa da Inadimplência: milhões de negativados em setembro de cada ano
SERASA_SET = {2022: 68.39, 2023: 71.82, 2024: 72.64, 2025: 79.1, 2026: 84.2}


def sgs(codigo, inicio="01/03/2011"):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
    r = requests.get(url, params={"formato": "json", "dataInicial": inicio}, timeout=60)
    r.raise_for_status()
    df = pd.DataFrame(r.json())
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = df["valor"].astype(float)
    return df.set_index("data")["valor"]


def desocupacao():
    # tabela 4099 (trimestral), variável 4099 = taxa de desocupação
    url = "https://apisidra.ibge.gov.br/values/t/4099/n1/all/v/4099/p/all"
    dados = requests.get(url, timeout=60).json()[1:]
    df = pd.DataFrame(dados)[["D3C", "V"]]
    df.columns = ["trimestre", "taxa"]
    df["taxa"] = pd.to_numeric(df["taxa"], errors="coerce")
    df["ano"] = df["trimestre"].str[:4].astype(int)
    df["tri"] = df["trimestre"].str[-1].astype(int)
    return df


series = {}
for nome, (codigo, publicado) in SGS.items():
    s = sgs(codigo)
    series[nome] = s
    ultimo = s.iloc[-1]
    ok = "ok" if abs(ultimo - publicado) < 0.15 else "NÃO BATE, conferir o código"
    print(f"{nome}: SGS {codigo}, último {s.index[-1]:%m/%Y} = {ultimo:.1f} | publicado {publicado} -> {ok}")

pnad = desocupacao()
t3 = pnad[pnad["tri"] == 3].set_index("ano")["taxa"]
print("\nDesemprego no 3º trimestre:")
print(t3.loc[2022:].to_string())

# Quanto dos negativados os desocupados explicariam, no limite
desocupados_mi, negativados_mi = 5.63, 84.2
print(f"\nTeto do que os desocupados explicam: {desocupados_mi / negativados_mi:.1%} dos negativados")

fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4))
inad = series["inadimplencia_pf_livre"]
a.plot(inad.index, inad.values, color="#FF6B35")
a.set_title("Inadimplência das famílias, crédito livre (%)")
b.plot(t3.index, t3.values, color="#6E6862", marker="o")
b.set_title("Desemprego, 3º trimestre (%)")
for ax in (a, b):
    ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("ed008_series.png", dpi=150)
print("\nGráfico salvo em ed008_series.png")
