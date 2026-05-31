# Projeto da GS🌍💧

Nosso projeto da GS é uma ferramenta computacional desenvolvida para o monitoramento e resposta a crises ambientais no Brasil. O sistema soluciona o desafio de otimização logística em cenários de desastre (seca na Caatinga e desmatamento na Amazônia), utilizando estruturas de dados avançadas para triagem de risco e algoritmos de grafos para cálculo de rotas de socorro. Os principais usuários são gestores de operações de órgãos ambientais e equipes de logística humanitária que necessitam de suporte à decisão rápido e eficiente.

## 🚀 Funcionalidades

* **Triagem de Risco (BST):** Classifica automaticamente municípios por nível de severidade utilizando uma Árvore Binária de Busca, permitindo buscas de intervalo otimizadas.
* **Roteamento Inteligente:** Implementa o algoritmo Guloso para encontrar rotas de menor custo logístico em redes complexas de rodovias e hidrovias.
* **Validação de Otimização:** Ferramenta de comparação que utiliza Busca em Profundidade (Força Bruta) para validar a qualidade das rotas geradas.
* **Monitoramento de Performance:** Benchmark em tempo real que rastreia consumo de memória e tempo de processamento, garantindo a escalabilidade do sistema.
* **Visualização Geoespacial:** Geração de mapas interativos via satélite e diagramas estáticos para suporte visual à tomada de decisão.

## 🛠 Tecnologias

As seguintes ferramentas e linguagens foram usadas na construção do projeto:

* **Python** (3.12+)
* **NetworkX** (3.6.1) - Construção e análise de grafos.
* **Folium** (0.15+) - Renderização de mapas interativos.
* **Matplotlib** (3.10.9) - Visualização de dados e estruturas.
* **Tracemalloc/Heapq** (Nativo) - Monitoramento de memória e filas de prioridade.

## 📦 Como rodar o projeto

Siga os passos abaixo para executar o projeto em sua máquina:

### Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

* **Git**
* **Python** (versão 3.8 ou superior)
* **Pip** (gerenciador de pacotes do Python)

### Passo a passo

```bash
# Clone este repositório
git clone https://github.com/gabsakura/GS---Dynamic-Programing.git

# Acesse a pasta do projeto
cd GS---Dynamic-Programing

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema para o cenário da Caatinga
python app.py

# Execute o sistema para o cenário da Amazônia
python appzonia.py

```

## 🤝 Contribuidores

* **[Gabriel Alexandre Fukushima Sakura]** - RM: 99522
* **[Henrique de Oliveira Gomes]** - RM: 566424
* **[Henrique Kolomyes Silveira]** - RM: 563467
* **[Lucas Henrique Viana Estevam Sena]** - RM: 566246
* **[Matheus Santos de Oliveira]** - RM: 561982