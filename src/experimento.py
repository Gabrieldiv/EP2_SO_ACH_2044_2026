from src.base import Base
from src.workers import Leitor, Escritor
import random, time 
def rodar_experimento(n_leitores, n_escritores, classe_estrategia):
    # Cria a Base e uma estratégia nova (a partir da classe recebida), monta as 100 threads
    # (n_leitores leitores + n_escritores escritores) embaralhadas e inicia todas.
    # Mede só do fim do povoamento até o último join() e devolve esse tempo em milissegundos.
    base = Base("data/bd.txt")
    estrategia = classe_estrategia()
    threads = []
    for _ in range(n_leitores):
        threads.append(Leitor(base, estrategia))
    for _ in range(n_escritores):
        threads.append(Escritor(base, estrategia))
    random.shuffle(threads)
    inicio = time.perf_counter()
    for processo in threads:
        processo.start()
    for processo in threads:
        processo.join()
    fim = time.perf_counter()
    return ((fim - inicio) * 1000)
    