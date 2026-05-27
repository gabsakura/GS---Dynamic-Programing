import sys
import os
from collections import deque
from typing import List, Tuple, Dict

# 1. PRIMEIRO: Arrumamos o caminho do sistema para o Python enxergar a pasta raiz
caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if caminho_raiz not in sys.path:
    sys.path.append(caminho_raiz)

# 2. SEGUNDO: Agora sim fazemos a importação do nosso arquivo que está na outra pasta
from data.processed.datasets import obter_cenario

class SistemaRoteamento:
    """Classe gerenciadora que acopla o cenário escolhido às estruturas de dados."""
    
    def __init__(self, nome_cenario: str):
        # Carrega os dados reais do arquivo datasets.py
        self.dados_brutos = obter_cenario(nome_cenario)
        self.nome = self.dados_brutos["nome_cenario"]
        self.fontes = self.dados_brutos["fontes"]
        
        self.municipios = self.dados_brutos["municipios"]
        self.grafo = self.dados_brutos["grafo"]
        self.coords = self.dados_brutos["coords"]
        
        # Inicializa e popula a BST automaticamente
        self.arvore_risco = ArvoreRiscoBST()
        for dados_mun in self.municipios.values():
            self.arvore_risco.inserir(dados_mun)

# ==========================================
# ÁRVORE BINÁRIA DE BUSCA (BST)
# ==========================================
class NodoBST:
    def __init__(self, dados_municipio: Tuple[int, str, float, float, int]):
        self.dados = dados_municipio
        self.risco = dados_municipio[2] # Indice 2 (INPE/DETER ou INMET)
        self.esquerda = None
        self.direita = None

class ArvoreRiscoBST:
    def __init__(self):
        self.raiz = None

    def inserir(self, dados: Tuple[int, str, float, float, int]):
        if self.raiz is None:
            self.raiz = NodoBST(dados)
        else:
            self._inserir_recursivo(self.raiz, dados)

    def _inserir_recursivo(self, atual: NodoBST, dados: Tuple):
        if dados[2] < atual.risco:
            if atual.esquerda is None:
                atual.esquerda = NodoBST(dados)
            else:
                self._inserir_recursivo(atual.esquerda, dados)
        else:
            if atual.direita is None:
                atual.direita = NodoBST(dados)
            else:
                self._inserir_recursivo(atual.direita, dados)

    def buscar(self, r_min: float, r_max: float) -> List[Tuple]:
        resultados = []
        self._buscar_intervalo(self.raiz, r_min, r_max, resultados)
        return resultados

    def _buscar_intervalo(self, atual: NodoBST, r_min: float, r_max: float, resultados: List[Tuple]):
        if atual is None:
            return
        if atual.risco > r_min:
            self._buscar_intervalo(atual.esquerda, r_min, r_max, resultados)
        if r_min <= atual.risco <= r_max:
            resultados.append(atual.dados)
        if atual.risco < r_max:
            self._buscar_intervalo(atual.direita, r_min, r_max, resultados)

    def percurso_in_order(self) -> List[Tuple]:
        resultados = []
        self._in_order(self.raiz, resultados)
        return resultados

    def _in_order(self, atual: NodoBST, resultados: List[Tuple]):
        if atual:
            self._in_order(atual.esquerda, resultados)
            resultados.append(atual.dados)
            self._in_order(atual.direita, resultados)