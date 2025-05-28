import random
import time
from colorama import init, Fore, Style

init()

vida_jogador = 100
buff_ativo = False
inventario = []

deck = [
    {"nome": "Ataque Focado", "tipo": "ataque", "dano": 25},
    {"nome": "Golpe Rápido", "tipo": "ataque", "dano": 15},
    {"nome": "Barreira Divina", "tipo": "defesa", "cura": 20},
    {"nome": "Chama Sagrada", "tipo": "ataque", "dano": 30},
    {"nome": "Bênção", "tipo": "buff"},
    {"nome": "Ritual de Cura", "tipo": "cura", "cura": 25},
]

deuses = [
    {
        "nome": "Hercules Deus da Força",
        "vida": 80,
        "descricao": "O primeiro guardião...",
        "drop": {"nome": "Manoplas de Hércules", "efeito": "Aumenta o dano em 5"}
    },
    {
        "nome": "Atena Deusa da Sabedoria",
        "vida": 90,
        "descricao": "Ela controla o conhecimento...",
        "drop": {"nome": "Olho da Estratégia", "efeito": "Reduz o dano recebido em 5"}
    },
    {
        "nome": "Hades Deus das Sombras",
        "vida": 100,
        "descricao": "Mestre do engano...",
        "drop": {"nome": "Espada Sombria", "efeito": "Buffa muito o dano"}
    },
    {
        "nome": "Hécate Deusa da bruxaria",
        "vida": 120,
        "descricao": "O último e mais perigoso...",
        "drop": {"nome": "Cetro Maldito", "efeito": "Aumenta cura e buff juntos"}
    },
]

def narrar(texto, delay=1.5):
    print(Style.BRIGHT + texto + Style.RESET_ALL)
    time.sleep(delay)

def narrar_lento(texto, delay_char=0.06):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(delay_char)
    print()

def mostrar_status(vida_inimigo):
    print(f"\n{Fore.CYAN}Sua vida: {vida_jogador}  |  Vida do {Fore.YELLOW}{nome_deus}{Fore.CYAN}: {vida_inimigo}{Style.RESET_ALL}")
    itens_formatados = [item["nome"] if isinstance(item, dict) else item for item in inventario]
    print(f"{Fore.CYAN}Inventário: {', '.join(itens_formatados) if itens_formatados else 'Vazio'}{Style.RESET_ALL}\n")

def escolher_carta():
    print("Escolha sua ação:")
    for i, carta in enumerate(deck, 1):
        print(f"{i}. {carta['nome']} ({carta['tipo'].capitalize()})")
    print(f"{len(deck)+1}. Usar item do inventário")
    
    escolha = input("Digite o número da ação: ")
    
    if escolha == str(len(deck)+1):
        return usar_item()
    
    if escolha not in [str(x) for x in range(1, len(deck)+1)]:
        print(Fore.YELLOW + "Escolha inválida! Você perde a vez." + Style.RESET_ALL)
        return None
    return deck[int(escolha) - 1]

def usar_item():
    global vida_jogador
    if not inventario:
        print(Fore.YELLOW + "Inventário vazio!" + Style.RESET_ALL)
        return None

    print("Itens disponíveis:")
    for i, item in enumerate(inventario, 1):
        nome_item = item["nome"] if isinstance(item, dict) else item
        print(f"{i}. {nome_item}")
    escolha = input("Escolha um item para usar: ")

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(inventario):
        print("Escolha inválida.")
        return None

    item = inventario.pop(int(escolha) - 1)

    if isinstance(item, str) and item == "Poção de Vida":
        vida_jogador = min(vida_jogador + 30, 100)
        narrar(Fore.GREEN + "Você usou uma Poção de Vida e recuperou 30 de vida!" + Style.RESET_ALL)
    elif isinstance(item, str) and item == "Espada dos Deuses":
        narrar(Fore.MAGENTA + "Você empunhou a Espada dos Deuses!" + Style.RESET_ALL)
        return {"nome": "Espada dos Deuses", "tipo": "ataque", "dano": 50}
    else:
        inventario.append(item)  # Reinsere, pois o efeito é passivo
        print("Este item possui efeito passivo e já está em uso.")
    return None

def aplicar_buffs(item, carta, dano, cura):
    nome_item = item["nome"] if isinstance(item, dict) else ""

    if carta["tipo"] == "ataque":
        if nome_item == "Manoplas de Hércules":
            dano += 5
        elif nome_item == "Espada Sombria":
            dano = int(dano * 1.3)

    if carta["tipo"] in ["cura", "defesa"]:
        if nome_item == "Cetro Maldito":
            cura += 10

    return dano, cura

def usar_carta(carta, vida_inimigo):
    global vida_jogador, buff_ativo

    if carta is None:
        return vida_inimigo

    narrar(f"Você usou {Fore.MAGENTA}{carta['nome']}{Style.RESET_ALL}!")

    dano = carta.get("dano", 0)
    cura = carta.get("cura", 0)

    for item in inventario:
        if isinstance(item, dict):
            dano, cura = aplicar_buffs(item, carta, dano, cura)

    if carta["tipo"] == "ataque":
        if buff_ativo:
            dano = int(dano * 1.5)
            narrar(Fore.RED + "Seu ataque foi fortalecido pelo buff!" + Style.RESET_ALL)
            buff_ativo = False
        vida_inimigo -= dano
        narrar(Fore.RED + f"Você causou {dano} de dano ao {nome_deus}." + Style.RESET_ALL)

    elif carta["tipo"] == "defesa":
        vida_jogador += cura
        narrar(Fore.GREEN + f"Você criou uma barreira e curou {cura} de vida." + Style.RESET_ALL)

    elif carta["tipo"] == "buff":
        buff_ativo = True
        narrar(Fore.LIGHTBLUE_EX + "Você invocou uma bênção, seu próximo ataque será mais forte." + Style.RESET_ALL)

    elif carta["tipo"] == "cura":
        vida_jogador += cura
        narrar(Fore.GREEN + f"Você realizou um ritual de cura e recuperou {cura} de vida." + Style.RESET_ALL)

    return vida_inimigo

def ataque_deus():
    global vida_jogador
    dano = random.randint(15, 30)

    for item in inventario:
        if isinstance(item, dict) and item["nome"] == "Olho da Estratégia":
            dano = max(0, dano - 5)

    narrar(Fore.RED + f"{nome_deus} atacou você e causou {dano} de dano!" + Style.RESET_ALL)
    vida_jogador -= dano

def boss_final_inicial():
    global vida_jogador, nome_deus
    nome_deus = "Hécate Deusa da bruxaria - Versão Inicial"
    vida_inimigo = 150

    narrar(Fore.YELLOW + f"VOCÊ ENFRENTA A {nome_deus}!" + Style.RESET_ALL)
    narrar("Este é um combate impossível. Você está destinado a perder para aprender.", 2)

    while vida_jogador > 0 and vida_inimigo > 0:
        mostrar_status(vida_inimigo)
        carta = escolher_carta()
        vida_inimigo = usar_carta(carta, vida_inimigo)
        if vida_inimigo <= 0:
            break
        ataque_deus()
        if vida_jogador <= 0:
            narrar(Fore.RED + "Você foi derrotado por Hécate Deusa da bruxaria!" + Style.RESET_ALL)
            break
        time.sleep(1)

def iniciar_jogo():
    global vida_jogador
    vida_jogador = 100

    print()
    print(Fore.MAGENTA + "="*60 + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + "VOCÊ CONCLUIU OS REQUISITOS NECESSÁRIOS...".center(60) + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + "A MÃE ESTÁ DE OLHO EM VOCÊ, FILHOTE...".center(60) + Style.RESET_ALL)
    print(Fore.MAGENTA + "="*60 + Style.RESET_ALL)
    print()

    resposta = input("DESEJA INICIAR O SISTEMA? (sim/não): ").lower()
    if resposta == "sim":
        introducao_lore()
        for deus in deuses:
            batalha_deus(deus)
            if vida_jogador <= 0:
                narrar(Fore.RED + "Sua jornada termina aqui." + Style.RESET_ALL)
                return
            else:
                inventario.append("Poção de Vida")
                narrar(Fore.CYAN + "Você encontrou uma Poção de Vida no campo de batalha!" + Style.RESET_ALL)
                if deus["nome"] == "Hades Deus das Sombras":
                    inventario.append("Espada dos Deuses")
                    narrar(Fore.MAGENTA + "Você obteve a lendária Espada dos Deuses!" + Style.RESET_ALL)
                vida_jogador = min(vida_jogador + 30, 100)
                time.sleep(2)
        narrar(Fore.GREEN + "Você venceu todos os deuses e provou que é digno do poder supremo!" + Style.RESET_ALL)
    else:
        narrar("Jogo encerrado. Até a próxima!", 2)

def introducao_lore():
    print()
    narrar_lento("No início dos tempos, quando o mundo ainda era jovem,", 0.07)
    narrar_lento("deuses antigos governavam os destinos dos mortais,", 0.07)
    time.sleep(1)
    narrar_lento("detendo poderes além da imaginação humana.", 0.07)
    time.sleep(2)
    narrar_lento("\nUm desafiante surge, determinado a desafiar cada deus que controlar o equilíbrio do universo.", 0.06)
    narrar_lento("Sua coragem será testada e sua mente desafiada.", 0.06)
    time.sleep(2)
    print("\n" + "-"*60 + "\n")

def batalha_deus(deus):
    global vida_jogador, nome_deus
    nome_deus = deus["nome"]
    vida_inimigo = deus["vida"]

    narrar(Fore.YELLOW + f"Você se prepara para enfrentar {nome_deus}!" + Style.RESET_ALL)
    narrar(deus["descricao"])
    time.sleep(2)

    while vida_jogador > 0 and vida_inimigo > 0:
        mostrar_status(vida_inimigo)
        carta = escolher_carta()
        vida_inimigo = usar_carta(carta, vida_inimigo)

        if vida_inimigo <= 0:
            narrar(Fore.GREEN + f"Você derrotou {nome_deus}!" + Style.RESET_ALL)
            inventario.append(deus["drop"])
            narrar(Fore.MAGENTA + f"Você recebeu o item: {deus['drop']['nome']} - {deus['drop']['efeito']}" + Style.RESET_ALL)

        ataque_deus()

        if vida_jogador <= 0:
            narrar(Fore.RED + f"Você foi derrotado por {nome_deus}. Sua jornada termina aqui." + Style.RESET_ALL)
            break

        time.sleep(1)

def main():
    boss_final_inicial()
    iniciar_jogo()

if __name__ == "__main__":
    main()
