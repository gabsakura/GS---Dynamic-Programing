import sys
import os

# Garante que o Python encontre a pasta 'src' independentemente de onde o script for rodado
caminho_raiz = os.path.abspath(os.path.dirname(__file__))
if caminho_raiz not in sys.path:
    sys.path.append(caminho_raiz)

from collections import deque
from src.data_structures import SistemaRoteamento
from src.greedy import algoritmo_guloso_dijkstra
from src.visualization import plot_grafo_estatico, gerar_mapa_folium, plot_bst

def main():
    print("="*60)
    print("SISTEMA DE ROTEAMENTO E TRIAGEM AMBIENTAL - AMAZÔNIA")
    print("="*60)

    # 1. Inicia o sistema
    print("\n[1] Inicializando o Sistema...")
    try:
        sistema = SistemaRoteamento("amazonia")
        print(f"    [+] Cenário Carregado: {sistema.nome}")
        print(f"    [+] Fontes de Dados: {sistema.fontes}")
    except Exception as e:
        print(f"    [!] Erro ao carregar o sistema: {e}")
        return

    # 2. Triagem com Árvore Binária de Busca (BST)
    print("\n[2] Realizando Triagem (Árvore Binária de Busca)...")
    limite_risco = 8.0
    fila_urgencia = deque()
    
    # Busca cidades com taxa de desmatamento >= 8.0
    sistema.arvore_risco.buscar_risco_critico(sistema.arvore_risco.raiz, limite_risco, fila_urgencia)

    print(f"    [!] Municípios em Risco Crítico (Desmatamento >= {limite_risco}):")
    for cidade_id, taxa in fila_urgencia:
        nome_cidade = sistema.municipios[cidade_id][1]
        print(f"        -> {nome_cidade} (Taxa: {taxa})")

    # 3. Execução do Roteamento (Dijkstra)
    if not fila_urgencia:
        print("\n    [✓] Nenhuma cidade em risco crítico encontrada no momento.")
        return

    origem_id = 1302603  # Manaus (Base Central)
    destino_id = fila_urgencia[0][0] # Pega o ID da primeira cidade da fila de triagem
    nome_destino = sistema.municipios[destino_id][1]

    print(f"\n[3] Calculando Rota Ótima (Dijkstra): Manaus -> {nome_destino}...")
    custo, rota = algoritmo_guloso_dijkstra(sistema.grafo, origem_id, destino_id)

    # Traduzindo IDs para Nomes para exibição no terminal
    rota_nomes = [sistema.municipios[node][1] for node in rota]

    print("\n" + "="*60)
    print(f"RESULTADO DO ROTEAMENTO GULOSO")
    print("="*60)
    print(f"Caminho: {' -> '.join(rota_nomes)}")
    print(f"Custo Logístico Total: {custo} (horas/km)")
    print("="*60)

    # 4. Geração de Visualizações (Output)
    print("\n[4] Gerando Arquivos Visuais...")

    # Mapa Folium (Interativo)
    gerar_mapa_folium(rota, arquivo="mapa_operacao_amazonia.html")
    print("    [+] Mapa interativo gerado: mapa_operacao_amazonia.html")

    # Grafo Estático (Matplotlib)
    plot_grafo_estatico(sistema.grafo, caminho_destaque=rota, arquivo="grafo_amazonia.png")
    print("    [+] Diagrama de rede gerado: grafo_amazonia.png")

    # Árvore BST
    try:
        plot_bst(sistema.arvore_risco, arquivo="bst_amazonia.png")
        print("    [+] Diagrama da árvore gerado: bst_amazonia.png")
    except Exception as e:
        print(f"    [-] Aviso: Não foi possível gerar o diagrama da BST ({e})")

    print("\n[✓] Execução do app.py concluída com sucesso!\n")

if __name__ == "__main__":
    main()