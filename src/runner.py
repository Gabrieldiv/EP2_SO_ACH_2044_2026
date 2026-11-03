import csv
from pathlib import Path

from src.experimento import rodar_experimento
from src.strategy_lock import EstrategiaLock
from src.strategy_rw import EstrategiaRW


RODADAS = 50
TOTAL_THREADS = 100
ARQUIVO_RESULTADOS = (
    Path(__file__).resolve().parent.parent / "resultados" / "resultados.csv"
)


def executar_experimentos(
    funcao_experimento=rodar_experimento,
    rodadas=RODADAS,
    caminho_resultados=ARQUIVO_RESULTADOS,
):
    """Executa todas as proporções e grava seus tempos em CSV.

    ``funcao_experimento`` pode ser substituída por uma função falsa nos testes,
    desde que aceite (n_leitores, n_escritores, classe_estrategia) e devolva o
    tempo em milissegundos.
    """
    caminho_resultados = Path(caminho_resultados)
    caminho_resultados.parent.mkdir(parents=True, exist_ok=True)

    with caminho_resultados.open("w", newline="", encoding="utf-8") as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(
            ["implementacao", "leitores", "escritores", "rodada", "tempo_ms"]
        )

        estrategias = (
            ("rw", EstrategiaRW),
            ("lock", EstrategiaLock),
        )

        for implementacao, classe_estrategia in estrategias:
            for n_leitores in range(TOTAL_THREADS + 1):
                n_escritores = TOTAL_THREADS - n_leitores

                for rodada in range(rodadas):
                    tempo_ms = funcao_experimento(
                        n_leitores,
                        n_escritores,
                        classe_estrategia,
                    )
                    escritor_csv.writerow(
                        [
                            implementacao,
                            n_leitores,
                            n_escritores,
                            rodada,
                            tempo_ms,
                        ]
                    )

    return caminho_resultados


def main():
    executar_experimentos()


if __name__ == "__main__":
    main()
