import folium
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def grafo_networkx(grafo_dict: dict) -> nx.Graph:
    G = nx.Graph()
    for u, vizinhos in grafo_dict.items():
        for v, w in vizinhos:
            G.add_edge(u, v, weight=w)
    return G

def plot_grafo_estatico(grafo_dict: dict, caminho_destaque: list = None, arquivo: str = "grafo_cenario.png") -> None:
    G = grafo_networkx(grafo_dict)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    
    nx.draw_networkx_nodes(G, pos, node_color="#f39c12", node_size=800)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    
    arestas = list(G.edges())
    cores = []
    larguras = []
    
    if caminho_destaque and len(caminho_destaque) >= 2:
        pares = set(zip(caminho_destaque[:-1], caminho_destaque[1:]))
        pares |= {(b, a) for (a, b) in pares}
        for u, v in arestas:
            if (u, v) in pares or (v, u) in pares:
                cores.append("#c0392b") # Vermelho para a rota escolhida
                larguras.append(3.0)
            else:
                cores.append("#bdc3c7")
                larguras.append(1.5)
    else:
        cores = ["#34495e"] * len(arestas)
        larguras = [1.5] * len(arestas)
        
    nx.draw_networkx_edges(G, pos, edgelist=arestas, edge_color=cores, width=larguras)
    labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    
    plt.title("Malha Logística e Roteamento", pad=20)
    plt.axis("off")
    out = Path.cwd() / arquivo
    plt.savefig(out, dpi=120)
    plt.close()

def gerar_mapa_folium(caminho: list, coords_dict: dict, arquivo: str = "mapa_cenario.html") -> folium.Map:
    """Gera o mapa interativo baseado nas coordenadas dinâmicas passadas."""
    if not caminho:
        return None
        
    lats = [coords_dict[s][0] for s in caminho if s in coords_dict]
    lons = [coords_dict[s][1] for s in caminho if s in coords_dict]
    
    centro = (sum(lats) / len(lats), sum(lons) / len(lons))
    m = folium.Map(location=centro, zoom_start=6, tiles="OpenStreetMap")

    # Desenha a rota
    for i in range(len(caminho) - 1):
        u, v = caminho[i], caminho[i+1]
        if u in coords_dict and v in coords_dict:
            folium.PolyLine(
                locations=[coords_dict[u], coords_dict[v]],
                color="#e74c3c",
                weight=5,
                opacity=0.8,
                tooltip=f"Trecho de Deslocamento"
            ).add_to(m)

    # Marca as cidades
    for id_mun in caminho:
        if id_mun in coords_dict:
            lat, lon = coords_dict[id_mun]
            folium.Marker(
                location=[lat, lon],
                popup=str(id_mun),
                icon=folium.Icon(color="darkgreen", icon="leaf")
            ).add_to(m)

    out = Path.cwd() / arquivo
    m.save(str(out))
    return m

def plot_bst(arvore, arquivo="bst_cenario.png"):
    if arvore.raiz is None:
        return
        
    G = nx.DiGraph()
    pos = {}
    
    def adicionar_arestas(nodo, x=0, y=0, espacamento=1.5):
        if nodo is not None:
            pos[nodo.dados[0]] = (x, y) 
            
            if nodo.esquerda:
                G.add_edge(nodo.dados[0], nodo.esquerda.dados[0])
                adicionar_arestas(nodo.esquerda, x - espacamento, y - 1, espacamento / 1.5)
                
            if nodo.direita:
                G.add_edge(nodo.dados[0], nodo.direita.dados[0])
                adicionar_arestas(nodo.direita, x + espacamento, y - 1, espacamento / 1.5)

    adicionar_arestas(arvore.raiz)
    
    plt.figure(figsize=(10, 6))
    
    # Busca manual simples para pegar o risco do nó e colocar no label
    labels = {}
    for no in G.nodes():
        # Faz uma busca em nível simples apenas para desenhar o gráfico
        fila = [arvore.raiz]
        risco_no = 0
        while fila:
            atual = fila.pop(0)
            if atual.dados[0] == no:
                risco_no = atual.risco
                break
            if atual.esquerda: fila.append(atual.esquerda)
            if atual.direita: fila.append(atual.direita)
        labels[no] = f"ID:{no}\nR:{risco_no}"
    
    nx.draw(G, pos, with_labels=False, node_size=1500, node_color="#2ecc71", edge_color="gray", arrows=False)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", labels=labels)
    
    plt.title("Árvore Binária de Busca (BST) - Índices de Risco", pad=20)
    plt.axis('off')
    plt.savefig(arquivo, dpi=120)
    plt.close()