from typing import List, Tuple, Dict

# =====================================================================
# BANCO DE DADOS GEOESPACIAIS (Fontes: IBGE, INPE, DNIT, ANA, INMET)
# Estrutura do Vértice: (ID_IBGE, Nome, Indice_Risco, Custo_Base, População)
# =====================================================================

CENARIOS = {
    "caatinga": {
        "nome_cenario": "Seca Extrema na Caatinga (Rota da Água)",
        "fontes": "ANA (Hidrologia), INMET (Seca Histórica), IBGE, DNIT",
        "municipios": {
            # Risco baseado na pluviometria (INMET/ANA)
            2611101: (2611101, 'Petrolina (Hub)', 1.2, 5000.0, 354317),
            2608750: (2608750, 'Lagoa Grande', 4.5, 2000.0, 25849),
            2603009: (2603009, 'Cabrobó', 5.8, 2500.0, 34503),
            2612208: (2612208, 'Salgueiro', 8.2, 4000.0, 61249),
            2610400: (2610400, 'Ouricuri', 9.8, 4500.0, 70000)
        },
        "grafo": {
            # Pesos baseados na malha viária do DNIT (km)
            2611101: [(2608750, 20.0), (2603009, 50.0)],
            2608750: [(2611101, 20.0), (2610400, 200.0)],
            2603009: [(2611101, 50.0), (2612208, 40.0)],
            2612208: [(2603009, 40.0), (2610400, 30.0)],
            2610400: [(2608750, 200.0), (2612208, 30.0)]
        },
        "coords": {
            2611101: (-9.3833, -40.5000),
            2608750: (-8.9950, -40.2700),
            2603009: (-8.5133, -39.3100),
            2612208: (-8.0744, -39.1194),
            2610400: (-7.8825, -40.0811)
        }
    },
    
    "amazonia": {
        "nome_cenario": "Rotas de Fiscalização (DETER/Amazônia)",
        "fontes": "INPE (PRODES/DETER), IBGE, DNIT (Rodovias/Fluvial)",
        "municipios": {
            # Risco baseado em alertas de desmatamento (INPE/DETER)
            1302603: (1302603, 'Manaus (Base Central)', 1.5, 0.0, 2063689),
            1500602: (1500602, 'Altamira', 8.9, 3500.0, 126279),
            1507300: (1507300, 'São Félix do Xingu', 9.5, 4200.0, 65418),
            1100205: (1100205, 'Porto Velho', 6.2, 2800.0, 460413),
            1505064: (1505064, 'Novo Progresso', 7.8, 3100.0, 34224)
        },
        "grafo": {
            # Pesos baseados em logística (DNIT Rodoviário + Hidrovias)
            1302603: [(1500602, 45.0), (1100205, 30.0)],
            1500602: [(1302603, 45.0), (1505064, 15.0)],
            1100205: [(1302603, 30.0), (1507300, 60.0)],
            1507300: [(1100205, 60.0), (1505064, 25.0)],
            1505064: [(1500602, 15.0), (1507300, 25.0)]
        },
        "coords": {
            1302603: (-3.1190, -60.0217),
            1500602: (-3.2033, -52.2064),
            1507300: (-6.6444, -51.9950),
            1100205: (-8.7619, -63.9039),
            1505064: (-7.1483, -55.4200)
        }
    }
}

def obter_cenario(nome_cenario: str) -> Dict:
    """Retorna os dados do cenário escolhido ('caatinga' ou 'amazonia')."""
    nome_cenario = nome_cenario.lower()
    if nome_cenario not in CENARIOS:
        raise ValueError(f"Cenário '{nome_cenario}' não encontrado. Escolha 'caatinga' ou 'amazonia'.")
    return CENARIOS[nome_cenario]