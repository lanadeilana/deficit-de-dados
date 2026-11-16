# Déficit de Dados

Código, dados e peças interativas da newsletter [Déficit de Dados](https://lanadeilana.substack.com/), sobre dados, comportamento e saúde no Brasil.

Cada edição tem uma pasta própria com:

- `index.html`: peça interativa (gráfico histórico + simulador), publicada via GitHub Pages
- `reproduzir_*.py`: baixa o dado principal direto da fonte pública (API oficial)
- `graficos_*.py`: gera as imagens estáticas usadas no Substack e nas redes
- `dados/`: CSVs usados nos gráficos, com a fonte de cada linha
- `img/`: imagens geradas

| Edição | Tema | Peça interativa |
|---|---|---|
| Ed008 | Empregado e negativado | [abrir](https://lanadeilana.github.io/deficit-de-dados/ed008-empregado-e-negativado/) |

Para rodar qualquer edição:

```bash
cd ed008-empregado-e-negativado
pip install -r requirements.txt
python reproduzir_ed008.py   # confere o dado na fonte
python graficos_ed008.py     # gera as imagens em img/
```
