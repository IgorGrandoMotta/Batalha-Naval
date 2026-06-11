import random
import subprocess
from playsound import playsound
import winsound
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import sys
sys.stdout.reconfigure(encoding='utf-8')

linhas = 10
colunas = 10
n_navios = 6
console = Console()

vazio = "🌊"
navios = "🛥️"
acerto = "💥"
erro = "💨"

#PARA TOCAR SOM
def tocar_som(arquivo):
    try:
        subprocess.Popen(['powershell', '-c', f'(New-Object Media.SoundPlayer "{arquivo}").PlaySync()'])
    except:
        pass
    
#MENU INTRODUTORIO
def introducao():
    console.print(Panel.fit(
        "[bold cyan]⚓  BATALHA NAVAL  ⚓[/bold cyan]",
        border_style="bold blue"
    ))
    console.print()
    console.print("[white]Você vai enfrentar o computador em uma batalha no mar.[/white]")
    console.print("[white]Cada jogador possui uma frota de 6 navios escondidos em um tabuleiro 10x10.[/white]")
    console.print()

    frota_table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
    frota_table.add_column("Nº", style="bold white", width=4)
    frota_table.add_column("Navio", style="cyan")
    frota_table.add_column("Tamanho", style="white")
    frota_table.add_column("Símbolo", justify="center")
    frota_table.add_row("1", "Destroyer",          "1 célula",  "⚓")
    frota_table.add_row("2", "Submarino",           "2 células", "🔱")
    frota_table.add_row("3", "Contratorpedeiro A",  "3 células", "🔫")
    frota_table.add_row("4", "Contratorpedeiro B",  "3 células", "🔰")
    frota_table.add_row("5", "Navio-tanque",        "4 células", "⛽")
    frota_table.add_row("6", "Porta-aviões",        "5 células", "🚀")
    console.print(frota_table)

    console.print(Panel(
        "[bold white]REGRAS[/bold white]\n"
        "[white]• Você e o computador atacam uma vez por turno.[/white]\n"
        "[white]• Informe a linha e coluna que deseja atacar (0-9).[/white]\n"
        "[white]• [red]💥[/red] = acerto   [cyan]💨[/cyan] = erro[/white]\n"
        "[white]• Um navio só afunda quando todas as suas células forem atingidas.[/white]\n"
        "[white]• Vence quem afundar toda a frota inimiga primeiro.[/white]",
        border_style="blue",
        title="[bold blue]Como jogar[/bold blue]"
    ))
    console.print()
    console.print("[bold yellow]Boa sorte, almirante! 🫡[/bold yellow]")
    console.print()

#CRIA UM TABULEIRO
def tabuleiro():
    return[[vazio] * colunas for o in range(linhas)]

#IMPRIME ALGUM TABULEIRO
def imprimir_tabuleiro(tab, titulo, cor_titulo):
    table = Table(
        show_header=False,
        padding=0,
        box=box.SIMPLE,
        title=f"[bold {cor_titulo}]{titulo}[/bold {cor_titulo}]"
    )
    
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
                linha_cells.append("[cyan] 💨 [/cyan]")
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
            console.print("[red]Direção inválida! Use 1 (horizontal) ou 2 (vertical).[/red]")
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
    console.print(Panel.fit(
        "[bold white]Como deseja posicionar seus navios?[/bold white]\n"
        "[cyan]1[/cyan] - Sortear automaticamente\n"
        "[cyan]2[/cyan] - Escolher manualmente",
        border_style="cyan"
    ))
    while True:
        try:
            opcao = int(input("\nOpção: "))
            if opcao != 1 and opcao != 2:
                console.print("[red]Opção inválida! Digite 1 ou 2.[/red]")
                continue
            else:
                break
        except ValueError:
            console.print("[red]Entrada inválida![/red]")

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
        console.print()
        imprimir_tabuleiro(tabuleiro, "Seu tabuleiro", "green")
        console.print()
    else:
        console.print(Panel.fit(
            "[bold white]Escolha qual navio posicionar:[/bold white]\n"
            "[cyan]1[/cyan] - Destroyer          ⚓  (1 célula)\n"
            "[cyan]2[/cyan] - Submarino           🔱  (2 células)\n"
            "[cyan]3[/cyan] - Contratorpedeiro A  🔫  (3 células)\n"
            "[cyan]4[/cyan] - Contratorpedeiro B  🔰  (3 células)\n"
            "[cyan]5[/cyan] - Navio-tanque        ⛽  (4 células)\n"
            "[cyan]6[/cyan] - Porta-aviões        🚀  (5 células)",
            border_style="cyan"
        ))
        tamanhos = [1,2,3,3,4,5]
        posicionados = []
        while True:
            try:   
                navio = int(input("\nOpção: "))
            except ValueError:
                console.print("[red]Digite apenas opções de navios válidas![/red]")
                continue
            if navio >= 1 and navio <= 6:
                tamanho = tamanhos[navio - 1]
                try:
                    direcao = int(input("Direção (1 = horizontal, 2 = vertical): "))
                    coluna = int(input("Coluna inicial (0-9): "))
                    linha = int(input("Linha inicial (0-9): "))
                except ValueError:
                    console.print("[red]Digite apenas coordenadas válidas! (0-9)[/red]")
                    continue
                if navio in posicionados:
                    console.print("[red]Você já posicionou esse navio! Escolha outro.[/red]")
                    continue
                if navio_player(tabuleiro, linha, coluna, tamanho, direcao, navio):
                    imprimir_tabuleiro(tabuleiro, "Seu tabuleiro", "green")
                    posicionados.append(navio)
                    if len(posicionados) == 6:
                        break
                else:
                    console.print("[red]Posição inválida! Tente novamente.[/red]")
                    continue
            else:
                console.print("[red]Opção inválida! Escolha entre 1 e 6.[/red]")

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
        console.print("[yellow]Você já atacou essa coordenada! Tente outra.[/yellow]")
    elif tabuleiro_adv[linha][coluna] == vazio:
        tabuleiro_adv[linha][coluna] = erro
        tabuleiro_visual[linha][coluna] = erro
        if quem == "player":
            console.print("[cyan]💨 Você errou! Nenhum navio atingido.[/cyan]")
            try:
                tocar_som(r"C:\Users\motta\Documents\TRABALHOS\Raciocinio Algoritimo\- Jogo Batalha Naval -\waterexplosion.wav")
            except:
                pass
        else:
            console.print("[cyan]💨 Computador errou![/cyan]")
        return False
    elif tabuleiro_adv[linha][coluna] != vazio and tabuleiro_adv[linha][coluna] != erro and tabuleiro_adv[linha][coluna] != acerto:
        numero_navio = tabuleiro_adv[linha][coluna]
        tabuleiro_adv[linha][coluna] = acerto
        tabuleiro_visual[linha][coluna] = acerto
        if quem == "player":
            console.print("[bold red]💥 Você acertou![/bold red]")
            try:
                tocar_som(r"C:\Users\motta\Documents\TRABALHOS\Raciocinio Algoritimo\- Jogo Batalha Naval -\explosion.wav")
            except:
                pass    
        else:
            console.print("[bold red]💥 Computador acertou![/bold red]")
        afundou = True
        for l in range(linhas):
            for c in range(colunas): 
                if tabuleiro_adv[l][c] == numero_navio:
                    afundou = False
        if afundou:
            console.print(Panel.fit(
                "[bold red]🔥 NAVIO AFUNDADO! 🔥[/bold red]",
                border_style="red"
            ))
            return True

#PEDE ONDE O JOAGADOR QUER ATACAR
def turno_player(tabuleiro_adv, tabuleiro_visual):
    console.print(Panel.fit("[bold green]🎯 SEU TURNO[/bold green]", border_style="green"))
    while True:
        try:
            linha = int(input("  Linha  (0-9): "))
            coluna = int(input("  Coluna (0-9): "))
            console.print()
            if linha < 0 or linha > 9 or coluna < 0 or coluna > 9:
                console.print("[red]Valor fora do tabuleiro! Digite entre 0 e 9.[/red]")
            else:
                ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, "player")
                break
        except ValueError:
            console.print("[red]Entrada inválida! Digite apenas números.[/red]")

#DEFINE ONDE O CPU VAI ATACAR
def turno_cpu(tabuleiro_adv, tabuleiro_visual):
    console.print(Panel.fit("[bold red]🤖 TURNO DO COMPUTADOR[/bold red]", border_style="red"))
    while True:
        linha = random.randint(0,9)
        coluna = random.randint(0,9)
        if tabuleiro_visual[linha][coluna] == vazio:
            console.print(f"  Computador atacou: linha [bold]{linha}[/bold], coluna [bold]{coluna}[/bold]")
            ataque(tabuleiro_adv, tabuleiro_visual, linha, coluna, "cpu")
            break

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
        if verificar_fim(tabuleiro_cpu):
            console.print()
            console.print(Panel(
                "[bold yellow]🏆 VITÓRIA! Você afundou todos os navios do inimigo! 🏆[/bold yellow]\n\n"
                "[white]Obrigado por jogar![/white]\n"
                "[cyan]Feito por: Igor Motta, Caetano Chueri, Marco Mattos.[/cyan]",
                border_style="yellow",
                title="[bold yellow]FIM DE JOGO[/bold yellow]"
            ))
            break

        turno_cpu(tabuleiro_player, tabuleiro_p_visual)
        if verificar_fim(tabuleiro_player):
            console.print()
            console.print(Panel(
                "[bold red]💀 DERROTA! O computador afundou todos os seus navios![/bold red]\n\n"
                "[white]Obrigado por jogar![/white]\n"
                "[cyan]Feito por: Igor Motta, Caetano Chueri, Marco Mattos.[/cyan]",
                border_style="red",
                title="[bold red]FIM DE JOGO[/bold red]"
            ))
            break

        console.print()
        imprimir_tabuleiro(tabuleiro_p_visual, "Seu tabuleiro", "green")
        console.print()
        imprimir_tabuleiro(tabuleiro_c_visual, "Tabuleiro inimigo", "red")
        console.print()

main()