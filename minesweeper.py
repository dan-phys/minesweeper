import random, colorama, platform, os, time

def magenta(text):
    return colorama.Fore.MAGENTA + text + colorama.Style.RESET_ALL

def init_box(*args):
    console_clear()
    bt = max(len(k) for k in args) + 6
    print(magenta(box["no"] + box["hor"]*bt + box["ne"]))
    for text in args:
        print(magenta(box["vert"]) + " "*3 + text + " "*(bt - len(text) - 3) + magenta(box["vert"]))
    print(magenta(box["vert"]) + " "*bt + magenta(box["vert"]))
    print(magenta(box["vert"]) + " "*(bt - 28) + "Aperte enter para continuar." + magenta(box["vert"]))
    print(magenta(box["so"] + box["hor"]*bt + box["se"]))
    input()
    console_clear()

def two_digits(num):
    if num < 10:
        return "0{}".format(num)
    else:
        return "{}".format(num)

def blue_back(dim,*args):
    div = round(dim/(2*len(args)))
    texts = []
    total_size = 0
    max_size = max(len(k) for k in args)
    for text in args:
        if len(text) < max_size:
            tws = " "*(max_size - len(text))
        tws = " "*(div - round(len(text)/2)) + text
        tws += " "*(2*div - len(tws))
        texts.append(tws)
        total_size += len(tws)
    if total_size < dim:
        texts[0] += " "*(dim - total_size)
    elif total_size > dim:
        texts[0] = texts[0][:dim - total_size]
    a = 0; b = 0
    while texts[0][a] == " ":
        a += 1
    while texts[-1][-1 + b] == " ":
        b -= 1
    b *= -1
    if a < b:
        texts[0] = " "*(b - a) + texts[0][0:-(b-a)]
    f_texts = "".join(k for k in texts)    
    print(colorama.Back.BLUE + f_texts + colorama.Style.RESET_ALL)

def console_clear():
    os_name = platform.system()
    if os_name == "Windows":
        os.system("cls")
        return
    os.system("clear")

def time_in_game():
    global end, start
    if end - start < 60:
        return "{} segundos".format(round(end - start))
    else:
        min = int((end - start)/60)
        sec = (end - start) - min*60
        if min == 1:
            if sec == 1:
                return "{} minuto e {} segundo".format(min, round(sec))
            else:
                return "{} minuto e {} segundos".format(min, round(sec))
        else:
            if sec == 1:
                return "{} minutos e {} segundo".format(min, round(sec))
            else:
                return "{} minutos e {} segundos".format(min, round(sec))

def draw(matriz):
    global dimension, num_bombs, num_marked, numbers, flags, num_open
    size = 3*(dimension + 1) + 1
    txt = "{} bombas".format(num_bombs)
    console_clear()
    blue_back(size, txt)
    for row in matriz:
        for el in row:
            if el in numbers:
                print(" {}".format(el), end = "")
            elif len(el.split()) >= 2: 
                if el.split()[1] == "h":
                    print("  {}".format(symbols["block"]), end = "")
                elif el.split()[1] == "o":
                    if el.split()[0] == "0":
                        print("   ", end = "")
                    elif el.split()[0] == "b":
                        print(" {}".format(symbols["bomb"]), end = "")
                    else:
                        print("  {}".format(el.split()[0]), end = "")
                elif el.split()[1] == "f":
                    print(" {}".format(symbols["flag"]), end = "")
        print()
    n_open = "{} abertos".format(num_open)
    marks = "{} marcados".format(num_marked)
    blue_back(size, marks, n_open)

def open_spaces(x,y):
    global numbers, matrix, num_open
    blank_spaces = []
    for k in range(x - 1, x + 2):
        for l in range(y - 1, y + 2):
            try:
                m = matrix[k][l].split()
            except IndexError:
                continue
            else:
                if len(m) == 2 and m[1] != "o":
                    matrix[k][l] = "{} {}".format(m[0],"o")
                    num_open += 1
                    if (k,l) != (x,y) and m[0] == "0":
                        blank_spaces.append([k,l]) 
                else:
                    continue
    if len(blank_spaces) > 0:
        for el in blank_spaces:
            open_spaces(el[0],el[1])

symbols = {"block": "\u25A0", "bomb": "\U0001F4A3", "flag": "\U0001F6A9"}
box = {"ne": "\u2557", "no": "\u2554", "so": "\u255a", "se": "\u255d", "vert": "\u2551", "hor": "\u2550"}

text1 = "Para jogar o campo minado são utilizados três comandos:"
text2 = "   - 'o linha coluna' para abrir uma posição. Ex.: 'o 2 3';"
text3 = "   - 'f linha coluna' para marcar ou desmarcar com uma bandeira. Ex.: 'f 10 5'; e"
text4 = "   - 'q' para sair do jogo."
init_box(text1, text2, text3,text4)

dimension = int(input("Digite a dimensão do campo minado (min 8): "))
if dimension < 8:
    while dimension < 8:
        console_clear()
        dimension = int(input("Digite um valor maior ou igual que 8: "))
console_clear()
prob = float(input("Digite a probabilidade de minas: "))
if prob >= 1 or prob <= 0:
    while prob >= 1 or prob <= 0:
        console_clear()
        prob = float(input("Digite um valor entre 0 e 1. "))
        
num_open = 0;       num_marked = 0;     num_bombs = 0;      flags = 0
matrix = [["0 h" for i in range(dimension + 1)] for j in range(dimension + 1)]
bombs = [] # posições das bombas
numbers = [] # Marcadores de posição
matrix[0][dimension] = "   " # Vértice que une os marcadores vertical e horizontal; não está sendo printado

for i in range(1, dimension + 1): 
    matrix[0][i - 1] = "{}".format(two_digits(i - 1)) # Adiciona os marcadores da horizontal
    matrix[i][dimension] = " {}".format(two_digits(i - 1)) # Adiciona os marcadores da vertical
    numbers.append(matrix[i][dimension])
    numbers.append(matrix[0][i - 1])
    for j in range(dimension):
        p = random.random()
        if p < prob: # Adiciona a posição das bombas
            bombs.append([i,j])
            num_bombs += 1
            matrix[i][j] = "b h"
            for k in range(i - 1, i + 2): # Adiciona os números ao redor das bombas
                for l in range(j - 1, j + 2):
                    if 1 <= k <= dimension and 0 <= l <= dimension - 1:
                        M = matrix[k][l].split()
                        if M[0] != "b":
                            matrix[k][l] = "{} {}".format(int(M[0]) + 1, "h")

game = True
start = time.time() # Printar, ao final, o tempo de jogo
while game:
    draw(matrix)
    command = input("Digite o comando: ")
    op = command.split() # Opções do comando
    if len(op) == 3:
        try:
            M = matrix[int(op[1]) + 1][int(op[2])].split()
        except IndexError:
            print("Digite uma posição válida.")
            time.sleep(2)
            continue
        if op[0].lower() == "o":
            if M[0] == "0": 
                open_spaces(int(op[1])+1,int(op[2]))
            elif M[0] == "b":
                for el in bombs:
                    matrix[el[0]][el[1]] = "{} {}".format("b", "o")
                end = time.time()
                draw(matrix)
                print("Infelizmente você perdeu o jogo em {}.".format(time_in_game()))
                game = False
            else:
                matrix[int(op[1]) + 1][int(op[2])] = "{} {}".format(M[0], "o")
                num_open += 1
        elif op[0].lower() == "f":
            if num_marked < num_bombs:
                if M[1] == "h":
                    matrix[int(op[1]) + 1][int(op[2])] = "{} {}".format(M[0],"f")
                    num_marked += 1
                elif M[1] == "f":
                    matrix[int(op[1]) + 1][int(op[2])] = "{} {}".format(M[0], "h")
                    num_marked -= 1
                else:
                    print("Marque uma posição válida.")
                    time.sleep(2)
            else:
                print("Você não pode inserir mais bandeiras.")
                time.sleep(2)
        else:
            print("Insira um comando válido.")
            time.sleep(2)
    else:
        if op[0].lower() == "q":
            exit()
        else:
            print("Insira um comando válido.")
            time.sleep(2)
    if num_marked + num_open == dimension**2:
        end = time.time()
        game = False
        draw(matrix)
        print("Parabéns! Você ganhou o jogo em {}.".format(time_in_game()))
