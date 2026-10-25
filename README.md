# EP2 SO — Leitores e Escritores (ACH2044, 2026)

Experimento em Python: tempo médio de 100 threads (leitores e escritores) acessando uma base de
36.242 palavras (`data/bd.txt`), com e sem a solução de Leitores e Escritores.
Prazo de entrega: 08/11/2026.

## Arquivos e responsáveis
| Arquivo | Responsável |
|---|---|
| `src/base.py`, `src/workers.py`, `src/experimento.py`, relatório | Gabriel |
| `src/strategy_rw.py` (Leitores e Escritores, prioridade a leitores) | Marcus |
| `src/strategy_lock.py` (bloqueio único), `src/runner.py` | Vitor |
| `analise/graficos.py` (tabelas e gráficos) | Isac |

Cada um mexe só nos seus arquivos, em branch próprio.

## Como as peças se conectam
- `Base` (em `base.py`) guarda a lista de palavras em memória: `tamanho()`, `ler(i)`, `escrever(i, valor)`.
- Toda estratégia tem os mesmos quatro métodos: `entrar_leitura()`, `sair_leitura()`,
  `entrar_escrita()` e `sair_escrita()`.
- `rodar_experimento(n_leitores, n_escritores, classe_estrategia)` (em `experimento.py`)
  recebe a **classe** da estratégia, cria uma instância nova a cada chamada, monta as 100 threads
  embaralhadas e devolve o tempo em ms (do fim do povoamento até o último `join()`).

## Formato do CSV (`resultados/`)
Cabeçalho: `implementacao,leitores,escritores,rodada,tempo_ms`
- `implementacao` vale `rw` ou `lock`.
- Uma linha por rodada (50 rodadas por proporção, 101 proporções por implementação).