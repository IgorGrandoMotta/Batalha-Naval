import random
from rich.console import Console
from rich.table import Table
import sys
sys.stdout.reconfigure(encoding='utf-8')

linhas = 10
colunas = 10
n_navios = 6

vazio = "🌊"
navios = "🛥️"
acerto = "💥"
erro = "💨"

def introducao():
    print("=" * 50)
    print("       Bem-vindo ao Batalha Naval!")
    print("=" * 50)
    print()
    print("Você vai enfrentar o computador em uma batalha no mar.")
    print("Cada jogador possui uma frota de 6 navios escondidos")
    print("em um tabuleiro 10x10.")
    print()
    print("Sua frota:")
    print("  1 - Destroyer         (1 célula)")
    print("  2 - Submarino         (2 células)")
    print("  3 - Contratorpedeiro A  (3 células)")
    print("  4 - Contratorpedeiro B  (3 células)")
    print("  5 - Navio-tanque      (4 células)")
    print("  6 - Porta-aviões      (5 células)")
    print()
    print("REGRAS:")
    print("  - Você e o computador atacam uma vez por turno.")
    print("  - Informe a linha e coluna que deseja atacar.")
    print("  - 💥 significa acerto, 💨 significa erro.")
    print("  - Um navio só afunda quando todas as suas células forem atingidas.")
    print("  - Vence quem afundar toda a frota inimiga primeiro.")
    print()
    print("Boa sorte, almirante!")
    print("=" * 50)

#CRIA UM TABULEIRO
def tabuleiro():
    return[[vazio] * colunas for o in range(linhas)]

#IMPRIME ALGUM TABULEIRO
def imprimir_tabuleiro(tab):
    console = Console()
    table = Table(show_header=False, padding=0)
    
    for _ in range(colunas):
        table.add_column(justify="center", width=5)
    
    for l in range(linhas):
        linha_cells = []
        for c in range(colunas):
            celula = tab[l][c]
            if celula == vazio:
                linha_cells.append("[blue] 🌊 [/blue]")
            elif celula == acerto:
                linha_cells.append("[red] 💥 [/red]")
            elif celula == erro:
                linha_cells.append("[yellow] 💨 [/yellow]")
            elif celula == 1:
                linha_cells.append("[green] ⚓ [/green]")
            elif celula == 2:
                linha_cells.append("[cyan] 🔱 [/cyan]")
            elif celula == 3:
                linha_cells.append("[yellow] 🔫 [/yellow]")
            elif celula == 4:
                linha_cells.append("[orange3] 🔰 [/orange3]")
            elif celula == 5:
                linha_cells.append("[magenta] ⛽ [/magenta]")
            elif celula == 6:
                linha_cells.append("[red] 🚀 [/red]")
        table.add_row(*linha_cells)
    console.print(table)

#VERIFICA SE HA NAVIOS
def verificar(tabuleiro, linha, coluna, tamanho, direcao):
    for i in range(tamanho):
        if direcao == 1:
            if coluna + i >= colunas or tabuleiro[linha][coluna + i] != vazio:
                return False
        elif direcao == 2: 
            if linha + i >= linhas or tabuleiro[linha + i][coluna] != vazio:
                return False
        else:
            print("Você digitou uma opção de direção invalida, use '1' ou '2'.")
            return False
    return True

#VERIFICA SE TODOS NAVIOS FORAM AFUNDADOS
def verificar_fim(tabuleiro):
    for l in range(linhas):
        for c in range(colunas): 
            if tabuleiro[l][c] != acerto and tabuleiro[l][c] != erro and tabuleiro[l][c] != vazio:
                return False
    return True
                        
#IMPLEMENTA OS NAVIOS NO TABULEIRO
def navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio):
    if verificar(tabuleiro, linha, coluna, tamanho, direcao):
        for _ in range(tamanho):
            if direcao == 1:
                    tabuleiro[linha][coluna + _] = navio
            elif direcao == 2:
                    tabuleiro[linha + _][coluna] = navio
        return True
    else:
        return False

#FROTA DE NAVIOS DO PLAYER
def frota_player(tabuleiro):
    print("Você deseja sortear a posição dos seus navios ou escolher manualmente?")
    print("1 - Sortear")
    print("2 - Escolher","\n")
    while True:
        try:
            opcao = int(input("Opção:"))
            if opcao != 1 and opcao != 2:
                continue
            else:
                break
        except ValueError:
            print("Entrada inválida!")
    if opcao == 1:
        tamanhos = [1,2,3,3,4,5]
        posicionados = []
        navio = 1
        while True:
            if navio >= 1 and navio <= 6:
                tamanho = tamanhos[navio - 1]
                direcao = random.randint(1,2)
                coluna = random.randint(0, 9)
                linha = random.randint(0, 9)
                if navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio):
                    posicionados.append(navio)
                    navio += 1
                    if len(posicionados) == 6:
                        break
        print("\n","Seu tabuleiro ficou assim:")
        imprimir_tabuleiro(tabuleiro)
        print("")
    else:
        print("Escolha qual navio posicionar:")
        print("1 - Destroyer      (1 célula)")
        print("2 - Submarino      (2 células)")
        print("3 - Contratorpedeiro A  (3 células)")
        print("4 - Contratorpedeiro B  (3 células)")
        print("5 - Navio-tanque   (4 células)")
        print("6 - Porta-aviões   (5 células)")
        tamanhos = [1,2,3,3,4,5]
        posicionados = []
        while True:
            try:   
                navio = int(input("Opção: "))
            except ValueError:
                print("Digite apenas opções de navios validas!")
            if navio >= 1 and navio <= 6:
                tamanho = tamanhos[navio - 1]
                direcao = int(input("Para horizontal Digite 1, para vertical digite 2:"))
                try:
                    coluna = int(input("Digite a coluna na qual seu navio irá estar/começar:"))
                    linha = int(input("Digite a linha na qual seu navio irá estar/começar:"))
                except ValueError:
                    print("\n","Digite apenas coordenadas validas! (0-9)")
                if navio in posicionados:
                    print("\n""Você ja atingiu o limite máximo deste tipo de navio. Digite a opção novamente.")
                    continue
                if navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio):
                    imprimir_tabuleiro(tabuleiro)
                    posicionados.append(navio)
                    if len(posicionados) == 6:
                        break
                else:
                    print("Posição inválida! Tente novamente.","\n")
                    continue
                    
            else:
                print("Posição inválida! O navio ultrapassa os limites do tabuleiro ou já existe um navio nessa posição. Tente novamente.","\n")

#FROTA DE NAVIOS DA CPU
def frota_cpu(tabuleiro):
    tamanhos = [1,2,3,3,4,5]
    posicionados = []
    navio = 1
    while True:
        if navio >= 1 and navio <= 6:
            tamanho = tamanhos[navio - 1]
            direcao = random.randint(1,2)
            coluna = random.randint(0, 9)
            linha = random.randint(0, 9)
            if navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio):
                posicionados.append(navio)
                navio += 1
                if len(posicionados) == 6:
                    break

#ATACA A UM LUGAR DO TABULEIRO
def ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, quem):
        if tabuleiro_adv[linha][coluna] == acerto or tabuleiro_adv[linha][coluna] == erro:
            print("Você ja atacou essa coordenada, tente outras coordenadas.")
        elif tabuleiro_adv[linha][coluna] == vazio:
            tabuleiro_adv[linha][coluna] = erro
            tabuleiro_visual[linha][coluna] = erro
            if quem == "player":
                print("Você errou!")
            else:
                print("Computador errou!","\n")
            return False
        elif tabuleiro_adv[linha][coluna] != vazio and tabuleiro_adv[linha][coluna] != erro and tabuleiro_adv[linha][coluna] != acerto:
            numero_navio = tabuleiro_adv[linha][coluna]
            tabuleiro_adv[linha][coluna] = acerto
            tabuleiro_visual[linha][coluna] = acerto
            if quem == "player":
                print("Você acertou!")
            else:
                print("Computador acertou!","\n")
            afundou = True
            for l in range(linhas):
                for c in range(colunas): 
                    if tabuleiro_adv[l][c] == numero_navio:
                        afundou = False
            if afundou:
                print("O navio afundou!","\n")
                return True

#PEDE ONDE O JOAGADOR QUER ATACAR
def turno_player(tabuleiro_adv,tabuleiro_visual):
    while True:
        try:
            linha = int(input("Digite a linha que deseja atacar:"))
            coluna = int(input("Digite a coluna que deseja atacar:"))
            print("")
            if linha < 0 or linha > 9 or coluna < 0 or coluna > 9:
                print("Valor fora do tabuleiro! Digite entre 0 e 9.","\n")
            else:
                ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, "player")
                break
        except ValueError:
            print("Entrada inválida! Digite apenas números.","\n")

#DEFINE ONDE O CPU VAI ATACAR
def turno_cpu(tabuleiro_adv,tabuleiro_visual):
    while True:
        linha = random.randint(0,9)
        coluna = random.randint(0,9)
        if tabuleiro_visual[linha][coluna] == vazio:
            ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, "cpu")
            break

#def tabuleiro; def imprimir_tabuleiro; def verificar; def navio_player; def frota_player; def frota_cpu; def ataque; def turno_player; def turno_cpu
######################################################################################################################################################
#ONDE IRA EXECUTAR O JOGO
def main():
    tabuleiro_player = tabuleiro()
    tabuleiro_cpu = tabuleiro()
    tabuleiro_p_visual = tabuleiro()
    tabuleiro_c_visual = tabuleiro()
    introducao()
    frota_player(tabuleiro_player)
    frota_cpu(tabuleiro_cpu)
    while True:
        turno_player(tabuleiro_cpu, tabuleiro_c_visual)
        if verificar_fim(tabuleiro_cpu) == True:
            print("Vitória! Você afundou todos os navios do seu inimigo.","\n")
            print("Obrigado por jogar o nosso jogo!")
            print("Feito por: Igor Motta, Caetano Chueri, Marco Mattos.")
            break

        turno_cpu(tabuleiro_player, tabuleiro_p_visual)
        if verificar_fim(tabuleiro_player) == True:
            print("O inimigo afundou todos os seus navios! Você perdeu.","\n")
            print("Obrigado por jogar o nosso jogo!")
            print("Feito por: Igor Motta, Caetano Chueri, Marco Mattos.")
            break
        print("Seu tabuleiro:")
        imprimir_tabuleiro(tabuleiro_p_visual)
        print("")
        print("Tabuleiro inimigo:")
        imprimir_tabuleiro(tabuleiro_c_visual)
        print("")
main()
