from typing import Tuple, List

def algoritmo_forca_bruta(grafo: dict, origem: str, destino: str, visitados: set = None, caminho_atual: list = None) -> Tuple[float, List[str]]:
    """Estratégia: Busca Exaustiva (DFS) testando todas as rotas para achar a globalmente ótima."""
    if visitados is None: visitados = set()
    if caminho_atual is None: caminho_atual = []

    visitados.add(origem)
    caminho_atual.append(origem)

    if origem == destino:
        return 0.0, list(caminho_atual)

    menor_custo = float('inf')
    melhor_caminho = []

    for vizinho, distancia in grafo.get(origem, []):
        if vizinho not in visitados:
            custo_restante, caminho_restante = algoritmo_forca_bruta(
                grafo, vizinho, destino, visitados.copy(), list(caminho_atual)
            )
            if custo_restante != float('inf'):
                custo_total = distancia + custo_restante
                if custo_total < menor_custo:
                    menor_custo = custo_total
                    melhor_caminho = caminho_restante

    return menor_custo, melhor_caminho