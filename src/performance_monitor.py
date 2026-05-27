import time
import tracemalloc
import random
import matplotlib.pyplot as plt
import networkx as nx
from typing import Callable, Any, Tuple, Dict, List

operacoes_dijkstra = 0
operacoes_forca_bruta = 0

def gerar_grafo_aleatorio(n_vertices: int, probabilidade_aresta: float = 0.4) -> Dict[int, List[Tuple[int, float]]]:
    """Gera um grafo aleatório ponderado para testes de escalabilidade."""
    grafo_nx = nx.erdos_renyi_graph(n_vertices, probabilidade_aresta, seed=42, directed=False)
    if not nx.is_connected(grafo_nx):
        grafo_nx = nx.fast_gnp_random_graph(n_vertices, 0.8, seed=42)
        
    grafo_dict = {i: [] for i in range(n_vertices)}
    for u, v in grafo_nx.edges():
        peso = round(random.uniform(10.0, 100.0), 1)
        grafo_dict[u].append((v, peso))
        grafo_dict[v].append((u, peso))
    return grafo_dict

def plot_gap_otimalidade(func_forca_bruta, func_guloso_simples):
    """Gera o gráfico de diferença percentual entre a solução Ótima e a Gulosa Ingênua."""
    tamanhos_n = [5, 6, 7, 8, 9, 10, 11, 12]
    gaps = []
    
    for n in tamanhos_n:
        grafo = gerar_grafo_aleatorio(n)
        origem, destino = 0, n - 1
        
        custo_fb, _ = func_forca_bruta(grafo, origem, destino)
        custo_guloso, _ = func_guloso_simples(grafo, origem, destino)
        
        if custo_fb > 0 and custo_fb != float('inf') and custo_guloso != float('inf'):
            gap_percentual = ((custo_guloso - custo_fb) / custo_fb) * 100
            gaps.append(gap_percentual)
        else:
            gaps.append(0)
            
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_n, gaps, marker='s', color='#e74c3c', linewidth=2)
    plt.title("Gap de Otimalidade: Força Bruta vs Guloso Simples", fontsize=14)
    plt.xlabel("Número de Vértices (N)", fontsize=12)
    plt.ylabel("Diferença Percentual do Custo (%)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig("gap_otimalidade.png", dpi=120)
    plt.close()

def run_benchmark_e_plotar(func_dijkstra: Callable, func_forca_bruta: Callable):
    """
    Executa a bateria de testes pedida na rubrica e plota o gráfico.
    Tamanhos: N = 5, 8, 10, 12, 20, 50, 100
    """
    tamanhos_n = [5, 8, 10, 12, 20, 50, 100]
    
    tempos_dijkstra = []
    tempos_fb = []
    
    print(f"{'N':<5} | {'Algoritmo':<15} | {'Tempo (ms)':<15} | {'Memória (MB)':<15} | {'Operações'}")
    print("-" * 75)
    
    for n in tamanhos_n:
        grafo = gerar_grafo_aleatorio(n)
        origem, destino = 0, n - 1
        
        # --- TESTE: DIJKSTRA (GULOSO) ---
        global operacoes_dijkstra
        operacoes_dijkstra = 0 
        
        tracemalloc.start()
        t0 = time.perf_counter()
        _ = func_dijkstra(grafo, origem, destino) # Executa
        t1 = time.perf_counter()
        mem_dijkstra = tracemalloc.get_traced_memory()[1] / (1024 * 1024) # MB
        tracemalloc.stop()
        
        tempo_ms_dijkstra = (t1 - t0) * 1000
        tempos_dijkstra.append(tempo_ms_dijkstra)
        
        print(f"{n:<5} | {'Dijkstra':<15} | {tempo_ms_dijkstra:<15.4f} | {mem_dijkstra:<15.6f} | {operacoes_dijkstra} relaxamentos")
        
        # --- TESTE: FORÇA BRUTA ---
        if n <= 12:
            global operacoes_forca_bruta
            operacoes_forca_bruta = 0
            
            tracemalloc.start()
            t0 = time.perf_counter()
            _ = func_forca_bruta(grafo, origem, destino) 
            t1 = time.perf_counter()
            mem_fb = tracemalloc.get_traced_memory()[1] / (1024 * 1024) 
            tracemalloc.stop()
            
            tempo_ms_fb = (t1 - t0) * 1000
            tempos_fb.append(tempo_ms_fb)
            print(f"{n:<5} | {'Força Bruta':<15} | {tempo_ms_fb:<15.4f} | {mem_fb:<15.6f} | {operacoes_forca_bruta} chamadas")
        else:
            tempos_fb.append(None) 
            print(f"{n:<5} | {'Força Bruta':<15} | {'TIMEOUT (Estouro)':<15} | {'-':<15} | > 10^6 chamadas")
            
    # --- GERAÇÃO DO GRÁFICO (Matplotlib) ---
    plt.figure(figsize=(10, 6))
    
    # Plota Dijkstra (N de 5 a 100)
    plt.plot(tamanhos_n, tempos_dijkstra, marker='o', color='blue', label='Dijkstra (O(E log V))', linewidth=2)
    
    # Plota Força Bruta (Somente até N=12)
    n_validos_fb = [n for n in tamanhos_n if n <= 12]
    tempos_validos_fb = [t for t in tempos_fb if t is not None]
    plt.plot(n_validos_fb, tempos_validos_fb, marker='x', color='red', label='Força Bruta (O(N!))', linewidth=2, linestyle='--')
    
    plt.title("Escalabilidade Empírica: Tempo de Execução vs Tamanho do Grafo (N)", fontsize=14)
    plt.xlabel("Número de Vértices (Municípios)", fontsize=12)
    plt.ylabel("Tempo de Execução (milissegundos)", fontsize=12)
    plt.yscale('log') # Escala Logarítmica para evidenciar a explosão combinatória
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=12)
    
    # Salva e exibe
    plt.savefig("escalabilidade_comparativa.png", dpi=120)
    print("\nGráfico 'escalabilidade_comparativa.png' gerado com sucesso!")
    plt.show()