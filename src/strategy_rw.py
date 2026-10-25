class EstrategiaRW:

    def __init__(self):
        # Guarda o estado compartilhado: um contador de leitores dentro da base (começa em 0),
        # um lock que protege esse contador e um lock/semáforo que controla o acesso à base inteira.
        pass

    def entrar_leitura(self):
        # Leitores entram juntos. Só espera se houver um escritor dentro da base agora;
        # escritores que apenas aguardam a vez não bloqueiam o leitor (prioridade a leitores).
        # O primeiro leitor a entrar trava o acesso para os escritores; os seguintes só aumentam o contador.
        pass

    def sair_leitura(self):
        # Diminui o contador de leitores. Se era o último (contador chegou a 0),
        # libera o acesso à base para os escritores que estão esperando.
        pass

    def entrar_escrita(self):
        # Só entra quando não há nenhum leitor dentro da base e nenhum outro escritor. Espera se houver.
        pass

    def sair_escrita(self):
        # Libera o acesso à base para quem estiver esperando (leitor ou escritor).
        pass