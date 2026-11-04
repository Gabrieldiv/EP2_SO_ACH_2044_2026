import threading


class EstrategiaRW:
    def __init__(self):
        self._leitores = 0  # Leitores na base
        self._trava_contador = threading.Lock()  # Lock protege contador
        self._acesso_base = threading.Lock()  # Lock controla acesso à base inteira

    def entrar_leitura(self):
        with self._trava_contador:
            self._leitores += 1
            if self._leitores == 1:  # Primeiro leitor
                self._acesso_base.acquire()

    def sair_leitura(self):
        with self._trava_contador:
            self._leitores -= 1
            if self._leitores == 0:  # Último leitor
                self._acesso_base.release()

    def entrar_escrita(self):
        self._acesso_base.acquire()

    def sair_escrita(self):
        self._acesso_base.release()
