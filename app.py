import sys
import os
import time

# Garante que o Python encontre a pasta 'src'
caminho_raiz = os.path.abspath(os.path.dirname(__file__))
if caminho_raiz not in sys.path:
    sys.path.append(caminho_raiz)

from collections import deque
from src.data_structures import SistemaRoteamento
from src.greedy import algoritmo_guloso_dijkstra
from src.brute_force import algoritmo_forca_bruta
from src.visualization import plot_grafo_estatico, gerar_mapa_folium, plot_bst

def main():
    print("="*70)
    print("SISTEMA DE ROTEAMENTO E TRIAGEM AMBIENTAL - ROTA DA ÁGUA (CAATINGA)")
    print("="*70)

    # 1. Inicia o sistema
    print("\n[1] Inicializando o Sistema...")
    try:
        # Mudamos para 'caatinga' para ver o mapa do Nordeste!
        sistema = SistemaRoteamento("caatinga") 
        print(f"    [+] Cenário Carregado: {sistema.nome}")
        print(f"    [+] Fontes de Dados: {sistema.fontes}")
    except Exception as e:
        print(f"    [!] Erro ao carregar o sistema: {e}")
        return

    # 2. Triagem com Árvore Binária de Busca (BST)
    print("\n[2] Realizando Triagem (Árvore Binária de Busca)...")
    limite_risco = 8.0 # Seca extrema
    
    resultados_bst = sistema.arvore_risco.buscar(limite_risco, 100.0)
    resultados_bst.sort(key=lambda x: x[2], reverse=True) # Ordena pela pior seca
    fila_urgencia = deque(resultados_bst)

    print(f"    [!] Municípios em Seca Crítica (Índice >= {limite_risco}):")
    for dados in fila_urgencia:
        print(f"        -> {dados[1]} (Índice Seca: {dados[2]})")

    # 3. Preparação para o Roteamento
    if not fila_urgencia:
        print("\n    [✓] Nenhuma cidade em risco crítico encontrada no momento.")
        return

    origem_id = 2611101  # Petrolina (Hub de Água - Rio São Francisco)
    destino_id = fila_urgencia[0][0] # Ouricuri (Pior índice da fila)
    nome_destino = fila_urgencia[0][1]

    print(f"\n[3] Iniciando Batalha Algorítmica: Petrolina -> {nome_destino}...")

    # =======================================================
    # EXECUÇÃO 1: ALGORITMO GULOSO (DIJKSTRA)
    # =======================================================
    t0 = time.perf_counter()
    custo_guloso, rota_guloso = algoritmo_guloso_dijkstra(sistema.grafo, origem_id, destino_id)
    t_guloso = (time.perf_counter() - t0) * 1000 # em milissegundos
    rota_nomes_guloso = [sistema.municipios[node][1] for node in rota_guloso]

    # =======================================================
    # EXECUÇÃO 2: FORÇA BRUTA (BUSCA EXAUSTIVA DFS)
    # =======================================================
    t0 = time.perf_counter()
    custo_fb, rota_fb = algoritmo_forca_bruta(sistema.grafo, origem_id, destino_id)
    t_fb = (time.perf_counter() - t0) * 1000 # em milissegundos
    rota_nomes_fb = [sistema.municipios[node][1] for node in rota_fb]

    # 4. Análise de Resultados (O Veredito da FIAP)
    print("\n" + "="*70)
    print(f"ANÁLISE DE DESEMPENHO E OTIMALIDADE")
    print("="*70)
    
    print(f"[A] ALGORITMO GULOSO (Dijkstra c/ Heap)")
    print(f"    - Custo: {custo_guloso} km")
    print(f"    - Rota: {' -> '.join(rota_nomes_guloso)}")
    print(f"    - Tempo de Resolução: {t_guloso:.4f} ms")
    
    print(f"\n[B] FORÇA BRUTA (DFS / Backtracking)")
    print(f"    - Custo Ótimo Absoluto: {custo_fb} km")
    print(f"    - Rota: {' -> '.join(rota_nomes_fb)}")
    print(f"    - Tempo de Resolução: {t_fb:.4f} ms")

    print("\n[VEREDITO]")
    if custo_guloso == custo_fb:
        print(f"    -> O Guloso encontrou a rota matematicamente perfeita!")
        print(f"    -> Eficiência: O Guloso foi {t_fb / t_guloso:.2f}x mais rápido que a Força Bruta.")
    else:
        gap = ((custo_guloso - custo_fb) / custo_fb) * 100
        print(f"    -> O Guloso caiu em uma armadilha local (Gap de {gap:.1f}% em relação ao ótimo).")

    print("="*70)

    # 5. Geração de Visualizações (Output)
    print("\n[4] Gerando Arquivos Visuais do Cenário Caatinga...")

    # Usa a rota ótima para desenhar o mapa
    gerar_mapa_folium(rota_fb, sistema.coords, arquivo="mapa_operacao_caatinga.html")
    print("    [+] Mapa interativo gerado: mapa_operacao_caatinga.html")

    plot_grafo_estatico(sistema.grafo, caminho_destaque=rota_fb, arquivo="grafo_caatinga.png")
    print("    [+] Diagrama de rede gerado: grafo_caatinga.png")

    try:
        plot_bst(sistema.arvore_risco, arquivo="bst_caatinga.png")
        print("    [+] Diagrama da árvore gerado: bst_caatinga.png")
    except Exception as e:
        print(f"    [-] Aviso: Não foi possível gerar o diagrama da BST ({e})")

    print("\n[✓] Execução concluída! Abra o arquivo HTML para ver o mapa do Sertão.\n")

if __name__ == "__main__":
    main()