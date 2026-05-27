import heapq
from typing import Tuple, List, Dict

def algoritmo_guloso_dijkstra(grafo: Dict[int, List[Tuple[int, float]]], origem: int, destino: int) -> Tuple[float, List[int]]:
    """
    Implementação da Variante C (Dijkstra).
    Encontra o caminho de menor custo de um Hub para um município alvo.
    """
    
    # 1. Dicionário para manter custos acumulados e predecessores (Exigência da FIAP)
    # Inicializa todos os custos com "infinito", exceto a origem.
    custos_acumulados = {nodo: float('inf') for nodo in grafo}
    custos_acumulados[origem] = 0.0
    
    predecessores = {nodo: None for nodo in grafo}
    
    # 2. Conjunto para gerenciar os nós já fechados/visitados
    visitados = set()
    
    # 3. Heap (Fila de Prioridade) para gerenciar a fronteira de expansão (Exigência da FIAP)
    # Guarda tuplas no formato: (custo_acumulado, id_municipio)
    fronteira_heap = [(0.0, origem)]
    
    while fronteira_heap:
        # A abordagem GULOSA acontece aqui: sempre tira o de menor custo da fronteira
        custo_atual, atual = heapq.heappop(fronteira_heap)
        
        # Se já fechamos esse nó por um caminho mais rápido antes, ignoramos
        if atual in visitados:
            continue
            
        visitados.add(atual)
        
        # Condição de parada (Early exit): Achamos o destino
        if atual == destino:
            break
            
        # Expansão para os vizinhos
        for vizinho, peso_aresta in grafo.get(atual, []):
            if vizinho in visitados:
                continue
                
            novo_custo = custo_atual + peso_aresta
            
            # Relaxamento da aresta: se o novo caminho é melhor, atualizamos
            if novo_custo < custos_acumulados[vizinho]:
                custos_acumulados[vizinho] = novo_custo
                predecessores[vizinho] = atual
                
                # Adiciona na fila de prioridade para exploração futura
                heapq.heappush(fronteira_heap, (novo_custo, vizinho))
                
    # 4. Reconstruir e exibir o caminho ótimo (Exigência da FIAP)
    caminho_reconstruido = []
    passo = destino
    
    # Se o custo for infinito, significa que não há caminho possível
    if custos_acumulados[destino] == float('inf'):
        return float('inf'), []
        
    # Faz o caminho inverso usando o dicionário de predecessores
    while passo is not None:
        caminho_reconstruido.insert(0, passo)
        passo = predecessores[passo]
        
    return custos_acumulados[destino], caminho_reconstruido