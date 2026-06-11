# Batalha-Naval# ⚓ Batalha Naval

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
