import readline
import sys
from colors import console

def delete_last_lines(count):
    for _ in range(count):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')

    sys.stdout.flush()

termainal = ['й', 'q']

text_color = "white"
place_missed_color = "#8b583e"
right_color = "#226c10"
idiot_color = "red"
warning_color = "#5b5b5b"

lines_to_clean = 0
litter = 0


rounds = []
symbs = ['❌', '✅']

def print_head():
    pprint(f"Статистика {sum(rounds)}/{len(rounds)}{':' if len(rounds) else ""} {"".join(list(map(lambda x: symbs[x] + ' ', rounds)))}")

def pprint(text):
    global litter
    delete_last_lines(litter)
    litter = 0
    global lines_to_clean
    lines_to_clean += 1
    console.print(text)
def clean_all():
    global lines_to_clean
    delete_last_lines(lines_to_clean)
    lines_to_clean = 0
going = True
while going:
    clean_all()
    print_head()
    pprint(f"Введи слово или '{termainal[0]}', чтобы остановить игру [{warning_color}]\n(ввод слова будет скрыт)[/{warning_color}]")
    target = input()
    if target in termainal:
        going = False
        continue
    n = len(target)
    delete_last_lines(3)
    pprint(f"Отгадывай, там [bold white]{str(n)}[/bold white] букв или введи '{termainal[0]}', чтобы сдаться")
    users = ""
    gave_up = False
    while users != target:
        users = input()
        if users in termainal:
            gave_up = True
            break
        delete_last_lines(1)
        if len(users) != len(target):
            pprint(f"[{idiot_color}]{users}[/{idiot_color}]")
            pprint(f"[{idiot_color}]Алё, буквы считай[/{idiot_color}]")
            litter += 2
            continue
        copy_t = list(target)
        copy_u = list(users)
        resp = [' '] * len(users)
        for i in range(n):
            if copy_t[i] == copy_u[i]:
                resp[i] = 'x'
                copy_t[i] = "0"
                copy_u[i] = "9"
        for i in range(n):
            if copy_u[i].isdigit():
                continue
            if copy_t.count(copy_u[i]) != 0:
                resp[i] = '.'
                copy_t.remove(copy_u[i])
                copy_u[i] = "9"
        for i in range(n):
            if resp[i] == 'x':
                resp[i] = f"[{text_color} on {right_color}]{users[i]}[/{text_color} on {right_color}]"
            elif resp[i] == '.':
                resp[i] = f"[{text_color} on {place_missed_color}]{users[i]}[/{text_color} on {place_missed_color}]"
            else:
                resp[i] = f"[{text_color}]{users[i]}[/{text_color}]"
        pprint("".join(resp))
    if gave_up:
        pprint("Вы проиграли")
        rounds.append(0)
        pprint("Ответ: " + target)
    else:
        pprint("Ура, победа🎉🎉🎉")
        pprint("Тыкни enter, чтобы продолжить")
        rounds.append(1)
        input()