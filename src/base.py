class Base:

    def __init__(self, caminho):
        # Lê uma vez o arquivo passado e indexa suas linhas nas posições da lista
        self._frases = []

        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                self._frases.append(linha.strip("\n"))


    def tamanho(self):
        # devolve quantas posições lista tem (quantas linhas o arquivo possui)
        return len(self._frases)

    def ler(self, i):
        return self._frases[i]
        # devolve o texto da linha i da lista


    def escrever(self, i, valor):
        self._frases[i] = valor
        # escreve algo no linha i da lista, só em memória principal, sem disco
