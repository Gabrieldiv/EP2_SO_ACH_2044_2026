import threading


class EstrategiaLock:

    def __init__(self):
        # Guarda um único lock que protege a base inteira. Não há contador de leitores,
        # porque aqui leitor e escritor são tratados igual: um de cada vez dentro da base.
        self._acesso_base = threading.Lock()

    def entrar_leitura(self):
        # Toma o lock. Se qualquer thread (leitor ou escritor) já estiver dentro, espera.
        self._acesso_base.acquire()

    def sair_leitura(self):
        # Libera o lock para quem estiver esperando.
        self._acesso_base.release()

    def entrar_escrita(self):
        # Toma o lock. Se qualquer thread (leitor ou escritor) já estiver dentro, espera.
        self._acesso_base.acquire()

    def sair_escrita(self):
        # Libera o lock para quem estiver esperando.
        self._acesso_base.release()
