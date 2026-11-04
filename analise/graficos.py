from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Diretórios do projeto
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent
DIRETORIO = DIRETORIO_RAIZ / "resultados"

ARQUIVO_CSV = DIRETORIO / "resultados.csv"

COLUNAS_OBRIGATORIAS = ["implementacao", "leitores", "escritores", "rodada", "tempo_ms"]


def carregar_resultados(caminho=ARQUIVO_CSV):
    """
    Carrega e valida o CSV gerado pelo runner.py.
    """

    caminho = Path(caminho)

    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    try:
        dados = pd.read_csv(caminho)

    except pd.errors.EmptyDataError:
        raise ValueError("O arquivo CSV está vazio.")

    # Verificar colunas obrigatórias
    faltantes = [
        coluna for coluna in COLUNAS_OBRIGATORIAS if coluna not in dados.columns
    ]

    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {faltantes}")

    if dados.empty:
        raise ValueError("O CSV não possui registros.")

    # Verificar valores ausentes
    if dados[COLUNAS_OBRIGATORIAS].isna().any().any():
        raise ValueError("O CSV contém valores ausentes.")

    # Verificar implementações
    implementacoes = set(dados["implementacao"])

    if implementacoes != {"rw", "lock"}:
        raise ValueError(
            "O CSV deve conter as implementações 'rw' e 'lock', sem outros valores."
        )

    # Converter colunas numéricas
    colunas_numericas = ["leitores", "escritores", "rodada", "tempo_ms"]

    for coluna in colunas_numericas:
        try:
            dados[coluna] = pd.to_numeric(dados[coluna], errors="raise")

        except (ValueError, TypeError):
            raise ValueError(f"Valores não numéricos na coluna '{coluna}'.")

    # Verificar valores numéricos finitos
    if not np.isfinite(dados[colunas_numericas].to_numpy(dtype=float)).all():
        raise ValueError("O CSV contém valores numéricos inválidos.")

    # Verificar valores inteiros
    for coluna in ["leitores", "escritores", "rodada"]:
        if not (dados[coluna] % 1 == 0).all():
            raise ValueError(f"A coluna '{coluna}' deve conter inteiros.")

    # Verificar quantidade total de threads
    if not (dados["leitores"] + dados["escritores"] == 100).all():
        raise ValueError("Cada proporção deve possuir exatamente 100 threads.")

    # Verificar intervalos
    if not dados["leitores"].between(0, 100).all():
        raise ValueError("Quantidade de leitores fora do intervalo 0 a 100.")

    if not dados["escritores"].between(0, 100).all():
        raise ValueError("Quantidade de escritores fora do intervalo 0 a 100.")

    # Verificar tempos de execução
    if (dados["tempo_ms"] <= 0).any():
        raise ValueError("Os tempos de execução devem ser positivos.")

    # Verificar quantidade total de registros
    if len(dados) != 10100:
        raise ValueError(f"Esperados 10100 registros, mas encontrados {len(dados)}.")

    # Verificar rodadas duplicadas
    duplicados = dados.duplicated(
        subset=["implementacao", "leitores", "escritores", "rodada"]
    )

    if duplicados.any():
        raise ValueError("O CSV contém rodadas duplicadas.")

    # Aceitar rodadas numeradas de 0 a 49 ou de 1 a 50
    rodadas_encontradas = set(dados["rodada"])

    rodadas_validas = [set(range(50)), set(range(1, 51))]

    if rodadas_encontradas not in rodadas_validas:
        raise ValueError("As rodadas devem ser numeradas de 0 a 49 ou de 1 a 50.")

    # Verificar 50 rodadas por proporção
    contagem = dados.groupby(["implementacao", "leitores", "escritores"]).size()

    if not (contagem == 50).all():
        raise ValueError("Cada proporção deve possuir exatamente 50 rodadas.")

    # Verificar todas as 101 proporções
    for implementacao in ["rw", "lock"]:
        proporcoes = set(dados.loc[dados["implementacao"] == implementacao, "leitores"])

        if proporcoes != set(range(101)):
            raise ValueError(f"Proporções incompletas para '{implementacao}'.")

    print("CSV validado com sucesso!")

    return dados


def calcular_medias(dados):
    """
    Calcula o tempo médio das 50 rodadas
    para cada proporção e implementação.
    """

    medias = (
        dados.groupby(["implementacao", "leitores", "escritores"])["tempo_ms"]
        .mean()
        .reset_index()
    )

    return medias.rename(columns={"tempo_ms": "tempo_medio_ms"})


def criar_tabela_comparativa(medias):
    """
    Compara os tempos médios das implementações.
    """

    tabela = medias.pivot(
        index=["leitores", "escritores"],
        columns="implementacao",
        values="tempo_medio_ms",
    ).reset_index()

    tabela.columns.name = None

    tabela = tabela.rename(columns={"rw": "media_rw_ms", "lock": "media_lock_ms"})

    # Diferença absoluta
    tabela["diferenca_ms"] = tabela["media_lock_ms"] - tabela["media_rw_ms"]

    # Ganho percentual de Readers-Writers
    tabela["ganho_percentual"] = (
        tabela["diferenca_ms"] / tabela["media_lock_ms"]
    ) * 100

    return tabela.sort_values("leitores").reset_index(drop=True)


def grafico_tempos(tabela):
    """
    Gera o gráfico comparativo dos tempos médios.
    """

    plt.figure(figsize=(12, 6))

    plt.plot(
        tabela["leitores"], tabela["media_rw_ms"], label="Readers-Writers", linewidth=2
    )

    plt.plot(
        tabela["leitores"], tabela["media_lock_ms"], label="Bloqueio único", linewidth=2
    )

    plt.title("Comparação do tempo médio de execução")

    plt.xlabel("Quantidade de leitores (100 - leitores = escritores)")

    plt.ylabel("Tempo médio (ms)")
    plt.xticks(range(0, 101, 10))

    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(DIRETORIO / "comparacao_tempos.png", dpi=300)

    plt.close()


def grafico_ganho(tabela):
    """
    Gera o gráfico de ganho percentual.
    """

    plt.figure(figsize=(12, 6))

    plt.plot(tabela["leitores"], tabela["ganho_percentual"], linewidth=2, color="green")

    plt.axhline(y=0, color="black", linestyle="--")

    plt.title("Ganho percentual de Readers-Writers")

    plt.xlabel("Quantidade de leitores (100 - leitores = escritores)")

    plt.ylabel("Ganho percentual (%)")
    plt.xticks(range(0, 101, 10))

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(DIRETORIO / "ganho_percentual.png", dpi=300)

    plt.close()


def main():

    DIRETORIO.mkdir(parents=True, exist_ok=True)

    # Carregar e validar CSV
    dados = carregar_resultados()

    # Calcular médias
    medias = calcular_medias(dados)

    # Criar tabela comparativa
    tabela = criar_tabela_comparativa(medias)

    # Salvar tabela
    tabela.to_csv(DIRETORIO / "medias_por_proporcao.csv", index=False)

    # Gerar gráficos
    grafico_tempos(tabela)
    grafico_ganho(tabela)

    # Resumo
    print("\nAnálise concluída!")
    print(f"Proporções analisadas: {len(tabela)}")
    print(f"Rodadas processadas: {len(dados)}")

    print("\nArquivos gerados:")
    print("- medias_por_proporcao.csv")
    print("- comparacao_tempos.png")
    print("- ganho_percentual.png")


if __name__ == "__main__":
    main()
