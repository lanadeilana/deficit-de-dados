# Ed008 · Empregado e negativado

Em setembro de 2026, o Brasil teve 84,2 milhões de negativados (recorde da Serasa) e desemprego de 5,2% (menor taxa para o 3º trimestre desde 2012).

- Peça interativa: https://lanadeilana.github.io/deficit-de-dados/ed008-empregado-e-negativado/
- Edição no Substack: https://lanadeilana.substack.com/

## Arquivos

| Arquivo | O que faz |
|---|---|
| `index.html` | Gráfico 2022–2026 e simulador da fatia de negativados que está empregada |
| `reproduzir_ed008.py` | Baixa inadimplência e endividamento das famílias (Banco Central, SGS) e desemprego (IBGE, SIDRA 4099) |
| `graficos_ed008.py` | Gera `img/ed008_grafico_substack.png` e `img/ed008_grafico_quadrado.png` a partir de `dados/` |
| `dados/serasa_negativados_setembro.csv` | Negativados em setembro de cada ano (Serasa, sem API) |
| `dados/desemprego_3tri.csv` | Taxa de desocupação no 3º trimestre (IBGE, PNAD Contínua) |

## Fontes

- Serasa, [Mapa da Inadimplência](https://www.serasa.com.br/limpa-nome-online/blog/mapa-da-inadimplencia-e-renogociacao-de-dividas-no-brasil/)
- IBGE, PNAD Contínua, tabela 4099 no SIDRA
- Banco Central, Estatísticas Monetárias e de Crédito (API SGS)

## Limitações

A Serasa conta pessoas de 18 anos ou mais e a PNAD conta a partir de 14, então a comparação do simulador é aproximada. Nenhuma base pública cruza emprego e inadimplência na mesma pessoa, e essa é a variável que o simulador deixa o leitor escolher.
