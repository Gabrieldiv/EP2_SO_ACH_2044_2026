import random
import threading
import time


class Leitor(threading.Thread):
    def __init__(self, base, estrategia):
        super().__init__()
        self.base = base
        self.estrategia = estrategia

    def run(self):
        self.estrategia.entrar_leitura()

        try:
            for i in range(1, 101):
                aleatorio = random.randrange(self.base.tamanho())
                self.base.ler(aleatorio)
            time.sleep(0.001)

        finally:
            self.estrategia.sair_leitura()


class Escritor(threading.Thread):
    def __init__(self, base, estrategia):
        super().__init__()
        self.base = base
        self.estrategia = estrategia

    def run(self):
        self.estrategia.entrar_escrita()

        try:
            for i in range(1, 101):
                aleatorio = random.randrange(self.base.tamanho())
                self.base.escrever(aleatorio, "MODIFICADO")
            time.sleep(0.001)

        finally:
            self.estrategia.sair_escrita()
