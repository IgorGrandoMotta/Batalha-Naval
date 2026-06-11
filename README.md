# ⚓ Batalha Naval

Jogo de Batalha Naval para dois jogadores (você vs. computador), rodando no terminal com interface visual colorida.

**Feito por:** Igor Motta, Caetano Chueri, Marco Mattos.

---

## 📋 Requisitos

- Python 3.8 ou superior
- Biblioteca **rich** (instalação abaixo)
- Sistema operacional **Windows** (necessário para os sons)

---

## 📦 Instalação da biblioteca

O jogo usa a biblioteca externa `rich` para exibir o tabuleiro colorido e os painéis no terminal. Para instalá-la, abra o terminal (Prompt de Comando ou PowerShell) e execute:

```
py -m pip install rich
```

Se o comando `py` não funcionar, tente:

```
python -m pip install rich
```

---

## 🔊 Configurando os arquivos de áudio

O jogo toca sons ao acertar ou errar um ataque. Para isso funcionar, você precisa:

**1.** Baixar (ou copiar do computador original) os dois arquivos de áudio:
- `explosion.wav` — toca quando um navio é acertado
- `waterexplosion.wav` — toca quando o ataque erra

**2.** Colocar os dois arquivos `.wav` na **mesma pasta** que o arquivo `batalha_naval.py`.

**3.** Abrir o arquivo `batalha_naval.py` e localizar as linhas abaixo (aparecem duas vezes no código):

```python
tocar_som(r"C:\Users\Marco Antonio\Documents\Batalha Naval\explosion.wav")
tocar_som(r"C:\Users\Marco Antonio\Documents\Batalha Naval\waterexplosion.wav")
```

**4.** Substituir o caminho pelo caminho real da pasta onde você salvou os arquivos. Por exemplo, se você salvou em `C:\Users\SeuNome\Desktop\BatalhaNaval\`, ficará assim:

```python
tocar_som(r"C:\Users\SeuNome\Desktop\BatalhaNaval\explosion.wav")
tocar_som(r"C:\Users\SeuNome\Desktop\BatalhaNaval\waterexplosion.wav")
```

> **Obs:** Se não quiser usar os sons, não precisa fazer nada — o jogo funciona normalmente sem eles, pois o código já trata esse caso automaticamente.

---

## ▶️ Como executar

Com o Python instalado e a biblioteca `rich` instalada, abra o terminal na pasta do jogo e execute:

```
py batalha_naval.py
```

ou

```
python batalha_naval.py
```

---

## 🎮 Como jogar

Ao iniciar, o jogo exibirá as regras completas na tela. Resumidamente:

- Você e o computador possuem frotas de **6 navios** escondidos em um tabuleiro **10x10**.
- No início, você escolhe se quer **posicionar seus navios manualmente** ou **deixar o jogo sortear** automaticamente.
- A cada turno, você informa a **linha e coluna** (de 0 a 9) que deseja atacar.
- O computador também ataca uma posição aleatória no seu tabuleiro a cada turno.
- **💥** indica acerto e **💨** indica erro.
- Um navio só afunda quando **todas as suas células** forem atingidas.
- Vence quem **afundar toda a frota inimiga** primeiro.

### Frota disponível

| Navio               | Tamanho   |
|---------------------|-----------|
| Destroyer           | 1 célula  |
| Submarino           | 2 células |
| Contratorpedeiro A  | 3 células |
| Contratorpedeiro B  | 3 células |
| Navio-tanque        | 4 células |
| Porta-aviões        | 5 células |

---

## 📁 Estrutura de arquivos esperada

```
BatalhaNaval/
│
├── batalha_naval.py      ← código principal
├── explosion.wav         ← som de acerto
├── waterexplosion.wav    ← som de erro
└── README.md             ← este arquivo
```

---

## 🧠 Explicação do código

### Variáveis globais

No topo do arquivo são definidas as configurações gerais do jogo:

```python
linhas = 10
colunas = 10
n_navios = 6
```

Definem o tamanho do tabuleiro (10x10) e a quantidade de navios. Também são definidos os emojis usados para representar cada estado de célula:

```python
vazio = "🌊"   # célula ainda não atacada
acerto = "💥"  # célula onde um navio foi atingido
erro = "💨"    # célula atacada mas sem navio
```

Os navios são representados por números de 1 a 6 dentro do tabuleiro.

---

### `tocar_som(arquivo)`

Toca um arquivo de áudio `.wav` usando o PowerShell do Windows. Usa `subprocess.Popen` para rodar o comando em segundo plano sem travar o jogo. Se der qualquer erro (arquivo não encontrado, sistema diferente), o `try/except` ignora silenciosamente e o jogo continua normalmente.

---

### `introducao()`

Exibe a tela inicial do jogo com:
- O título "BATALHA NAVAL" em um painel estilizado
- Uma tabela com todos os 6 navios, seus tamanhos e símbolos
- Um painel com as regras do jogo

Usa apenas funções da biblioteca `rich` para formatação visual no terminal.

---

### `tabuleiro()`

Cria e retorna um tabuleiro vazio: uma matriz (lista de listas) de 10x10 posições, onde todas as células começam com o valor `vazio` (🌊).

```python
return [[vazio] * colunas for o in range(linhas)]
```

Cada partida cria 4 tabuleiros: o real do jogador, o real da CPU, e um visual de cada um (o que é mostrado na tela).

---

### `imprimir_tabuleiro(tab, titulo, cor_titulo)`

Recebe um tabuleiro e o exibe no terminal de forma visual usando a biblioteca `rich`. Percorre cada célula da matriz e transforma o valor em um emoji colorido:

| Valor na matriz | Exibição |
|-----------------|----------|
| `vazio` (🌊) | 🌊 azul |
| `acerto` (💥) | 💥 vermelho |
| `erro` (💨) | 💨 ciano |
| `1` a `6` | emoji do navio correspondente com cor |

O título e a cor da borda são passados como parâmetros (verde para o tabuleiro do jogador, vermelho para o inimigo).

---

### `verificar(tabuleiro, linha, coluna, tamanho, direcao)`

Verifica se é possível posicionar um navio em determinada posição antes de colocá-lo. Checa duas condições para cada célula que o navio ocuparia:

- Se a posição não ultrapassa os limites do tabuleiro (0–9)
- Se a célula está vazia (sem outro navio)

Retorna `True` se o posicionamento é válido, ou `False` caso contrário. A direção `1` é horizontal (ocupa colunas) e `2` é vertical (ocupa linhas).

---

### `verificar_fim(tabuleiro)`

Percorre o tabuleiro inteiro verificando se ainda existe algum navio que não foi afundado. Um navio sobrevivente é qualquer célula que não seja `vazio`, `acerto` ou `erro` — ou seja, qualquer célula com valor de 1 a 6.

Retorna `True` se todos os navios foram destruídos (fim de jogo), ou `False` se ainda há navios restantes.

---

### `navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio)`

Efetivamente posiciona um navio no tabuleiro. Primeiro chama `verificar()` para checar se a posição é válida. Se for, percorre as células que o navio ocupa e grava o número do navio (1 a 6) em cada uma delas. Retorna `True` se conseguiu posicionar, `False` caso contrário.

---

### `frota_player(tabuleiro)`

Gerencia o posicionamento da frota completa do jogador. Oferece duas opções:

**Opção 1 — Automático:** sorteia aleatoriamente direção, linha e coluna para cada navio e tenta posicioná-lo. Repete até conseguir posicionar os 6 navios sem sobreposição.

**Opção 2 — Manual:** exibe um menu com os 6 navios e pede ao jogador que informe qual navio quer posicionar, a direção (1 = horizontal, 2 = vertical), a coluna inicial e a linha inicial. Valida cada entrada e exige que todos os 6 navios sejam posicionados antes de seguir.

---

### `frota_cpu(tabuleiro)`

Funciona igual à opção automática do `frota_player`, mas sem interação com o usuário. Posiciona os 6 navios da CPU de forma completamente aleatória no tabuleiro. O jogador nunca vê esse tabuleiro diretamente.

---

### `ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, quem)`

Processa um ataque em uma posição do tabuleiro adversário. Existem três casos possíveis:

- **Posição já atacada:** avisa que a coordenada já foi usada e não faz nada.
- **Posição vazia:** marca como `erro` nos dois tabuleiros (real e visual) e toca o som de água.
- **Posição com navio:** marca como `acerto`, toca o som de explosão e verifica se o navio inteiro foi afundado (se não restar nenhuma célula com o número daquele navio no tabuleiro).

O parâmetro `quem` indica se foi o jogador ou a CPU atacando, para exibir a mensagem correta.

---

### `turno_player(tabuleiro_adv, tabuleiro_visual)`

Gerencia o turno do jogador. Pede linha e coluna como entrada, valida se os valores estão entre 0 e 9, e chama `ataque()`. Se o jogador digitar algo inválido ou fora do intervalo, exibe uma mensagem de erro e pede novamente.

---

### `turno_cpu(tabuleiro_adv, tabuleiro_visual)`

Gerencia o turno do computador. Sorteia linha e coluna aleatoriamente em um loop `while True`, e só ataca quando encontrar uma posição que ainda não foi atacada (valor `vazio` no tabuleiro visual da CPU). Exibe as coordenadas escolhidas para o jogador acompanhar.

---

### `main()`

Função principal que orquestra todo o jogo. Ela:

1. Cria os 4 tabuleiros (real e visual de cada jogador)
2. Chama `introducao()` para exibir a tela inicial
3. Chama `frota_player()` e `frota_cpu()` para posicionar as frotas
4. Entra no loop principal do jogo:
   - Executa o turno do jogador
   - Verifica se o jogador venceu com `verificar_fim()`
   - Executa o turno da CPU
   - Verifica se a CPU venceu com `verificar_fim()`
   - Imprime os dois tabuleiros atualizados
5. Ao sair do loop, exibe a mensagem de vitória ou derrota
