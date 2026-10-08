# Dashboard de Produção Agrícola no Brasil (2015–2024) (Tema 29).

## 1. Descrição do projeto

Este projeto apresenta uma **análise completa da produção agrícola no Brasil**, cobrindo todo o pipeline de dados: da importação do dado bruto até a publicação de um dashboard interativo.

 **Linguagem de Programação — Professor: Alexandre Neves Louzada**
 **Aluno: Rafael Rigo de Oliveira**

### Fluxo do Projeto

```
simulacao_producao_agricola_brasil.csv (dados brutos)
    ↓ Limpeza e engenharia de atributos (pandas)
prod_agricula.ipynb (análise e interpretação)
    ↓ Persistência (SQLite)
prod_agricula.db (banco SQLite)
    ↓ Dashboard (Streamlit)
app.py (aplicação web)
    ↓ Deploy
Streamlit Cloud (online)
```

---

## 2. Problema de negócio

O agronegócio é um dos principais setores da economia brasileira, e a análise de dados agrícolas ajuda a identificar padrões de produção, regiões mais produtivas e tendências do setor. O projeto busca responder:

- Quais estados apresentam maior produção agrícola?
- Quais culturas possuem maior produtividade?
- Quais culturas apresentam maior valor econômico?
- Houve crescimento da produção ao longo do tempo?
- Existe relação entre clima e produtividade?
- Quais regiões concentram maior área plantada?
- Existem períodos críticos de produção?

---

## 3. Tecnologias utilizadas

| Tecnologia | Função |
|------------|--------|
| Python | Linguagem principal |
| pandas | Manipulação e análise de dados |
| NumPy | Cálculos numéricos |
| plotly | Visualização interativa |
| SQLite | Persistência de dados |
| Streamlit | Dashboard interativo |
| Git/GitHub | Versionamento e publicação (GitHub Pages) |

---

## 4. Estrutura do projeto

```text
projeto-pratico/
|
|-- README.md                    # Este arquivo
|-- requirements.txt             # Dependências
|-- app.py                       # App Streamlit (dashboard)
|-- index.html                   # Página do projeto (GitHub Pages)
|
|-- dados/
|   |-- simulacao_producao_agricola_brasil.csv   # Dados brutos (4.440 registros)
|
|-- database/
|   |-- prod_agricula.db         # Banco SQLite (gerado pelo app)
|
|-- notebook/
|   |-- prod_agricula.ipynb      # Notebook de análise
|
|-- imagens/                     # Gráficos exportados
```

---

## 5. Como executar localmente

### 5.1 Clonar o repositório

```bash
git clone https://github.com/rafaelrig0/projeto-pratico.git
cd projeto-pratico
```

### 5.2 Instalar dependências

```bash
pip install -r requirements.txt
```

Conteúdo sugerido para o `requirements.txt`:

```text
pandas
numpy
plotly
streamlit
```

### 5.3 Executar o dashboard

```bash
streamlit run app.py
```

### 5.4 Executar o notebook

```bash
# Abrir no Jupyter/VSCode e executar célula por célula
jupyter notebook notebook/prod_agricula.ipynb
```

---

## 6. Base de dados

4.440 registros mensais (jan/2015 a dez/2024), 5 regiões, 20 estados e 7 culturas (Soja, Milho, Café, Algodão, Arroz, Feijão e Cana-de-açúcar).

| Coluna | Descrição |
|--------|-----------|
| `ano`, `mes`, `data` | Período de referência |
| `regiao`, `uf` | Região e estado |
| `cultura` | Cultura agrícola |
| `area_plantada_ha` | Área plantada (ha) |
| `producao_toneladas` | Produção total (t) |
| `produtividade` | Produção por hectare (t/ha) |
| `chuva_mm` | Volume de chuva (mm) |
| `temperatura_media` | Temperatura média (°C) |
| `valor_producao` | Valor econômico (R$) |
| `exportacoes` | Volume exportado |
| `nivel_produtividade` | Baixo, Médio, Alto ou Muito Alto |

---

## 7. KPIs utilizados

| KPI | Descrição |
|-----|-----------|
| Produção total | Soma de `producao_toneladas` |
| Cultura mais produzida | Cultura com maior produção acumulada |
| Estado mais produtivo | UF com maior média de `produtividade` |
| Área plantada total | Soma de `area_plantada_ha` |
| Valor econômico total | Soma de `valor_producao` |
| Média de produtividade | Média simples de `produtividade` (t/ha) |

Indicadores complementares: exportações totais, chuva média, temperatura média e correlações clima × produtividade.

---

## 8. Funcionalidades do dashboard (`app.py`)

- Filtros por **ano, mês, região, estado, cultura e nível de produtividade**
- KPIs dinâmicos
- **Visão Geral:** ranking de culturas, valor econômico, produtividade e distribuição por nível
- **Evolução Temporal:** linha anual, sazonalidade, produção por cultura e heatmap sazonal
- **Análise Regional:** ranking de estados, participação das regiões e tabela dinâmica estado × cultura
- **Clima e Exportações:** dispersão chuva × produtividade, temperatura × produtividade, correlações e evolução das exportações
- **Dados e Metodologia:** tabela interativa dos dados filtrados e conclusão executiva
- Persistência dos dados em banco SQLite (`database/prod_agricula.db`)

---

## 9. Notebook de análise

O notebook `prod_agricula.ipynb` documenta toda a análise:

| Seção | Conteúdo |
|-------|----------|
| 1. Introdução | Objetivos, perguntas orientadoras e tecnologias |
| 2. Contextualização do agronegócio | Importância econômica e fatores de produção |
| 3. Explicação da base | Dicionário de dados |
| 4. Leitura dos dados | Importação do CSV e primeira inspeção |
| 5. Limpeza e preparação | Nulos, duplicados, consistência, outliers e alertas de qualidade |
| 6. Engenharia de atributos | Trimestre, estação, valor por tonelada, taxa de exportação, faixas climáticas |
| 7. KPIs | Indicadores e filtros reutilizáveis |
| 8. Visualizações | Linha temporal, barras, heatmap, dispersão, tabela dinâmica, períodos críticos |
| 9. Interpretação | Leitura dos resultados e limitações |
| 10. Conclusão | Conclusão executiva e recomendações |

---

## 10. Principais insights

| Pergunta | Resultado na base simulada |
|----------|----------------------------|
| Maior produção (volume) | RJ, SP, ES e MG |
| Estado mais produtivo | MS (43,08 t/ha) |
| Cultura mais produzida | Feijão (≈ 167,4 mi t), quase empatada com Soja |
| Maior valor econômico | Soja (≈ R$ 166,2 bi) |
| Crescimento 2015→2024 | +5,8% (≈ 0,6% ao ano), com oscilações |
| Clima × produtividade | Sem relação detectável (r ≈ 0) |
| Maior área plantada | Sudeste (35,8% do total) |
| Períodos críticos | Pior ano: 2021; piores meses: mai–jun/2020 e mai/2021 |

### Limitações da base

- `produtividade` **não** equivale a `producao_toneladas ÷ area_plantada_ha`.
- `nivel_produtividade` não acompanha os valores de produtividade.
- O número de registros varia entre estados (120 a 480), o que influencia rankings baseados em soma.
- As diferenças entre culturas são pequenas e não foram testadas estatisticamente.

---

## 11. Publicação

| Etapa | Ferramenta | Status |
|-------|------------|--------|
| Versionamento | GitHub | Concluído |
| Página do projeto | GitHub Pages | Concluído |
| Dashboard | Streamlit Cloud | Concluído |

Links:

- Página do projeto: [https://rafaelrig0.github.io/projeto-pratico/](https://rafaelrig0.github.io/projeto-pratico/)
- Dashboard: [https://projeto-pratico-flmdsjp4abkfg6fekrwapn.streamlit.app/](https://projeto-pratico-flmdsjp4abkfg6fekrwapn.streamlit.app/)

---

## 12. Objetivo pedagógico

Este projeto demonstra como transformar uma base de dados em um produto analítico completo.

O foco não está apenas em gerar gráficos, mas em responder perguntas relevantes e apoiar a tomada de decisão.
