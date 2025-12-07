import readline
import sys
from colors import console
from languages import languages

def delete_last_lines(count):
    if count < 1:
        return
    global lines_to_clean
    lines_to_clean -= count
    for _ in range(count):
        sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')

    sys.stdout.flush()

lines_to_clean = 0
litter = 0

text_color = "white"
place_missed_color = "#8b583e"
right_color = "#226c10"
idiot_color = "red"
warning_color = "#5b5b5b"



lang = languages[0]

terminal = [l["quit"] for l in languages]

rounds = []
symbs = ['❌', '✅']

def upd_head():
    global lines_to_clean
    lines_to_clean += 1
    clean_all()
    pprint(lang["start"] if (len(rounds) == 0) else
           f"{lang["stat"]}: {sum(rounds)}/{len(rounds)} {"".join(list(map(lambda x: symbs[x] + ' ', rounds)))}")
    lines_to_clean -= 1
def print_head():
    global lines_to_clean
    pprint(lang["start"])
    lines_to_clean -= 1
def pprint(*text):
    global litter
    global lines_to_clean
    delete_last_lines(litter)
    litter = 0
    lines_to_clean += 1
    console.print(*text)

def iinput(*args) -> str:
    global lines_to_clean
    resp = input(*args)
    lines_to_clean += 1
    return resp

def clean_all():
    global lines_to_clean
    t = lines_to_clean
    delete_last_lines(t)
def main():
    global lines_to_clean
    global litter
    going = True
    print_head()
    while going:
        upd_head()
        pprint(
            f"{lang["ask_word"][0]} '{lang["quit"]}', {lang["ask_word"][1]}")
        target = iinput()
        if target in terminal:
            going = False
            continue
        n = len(target)
        clean_all()
        pprint(
            f"{lang["guess"][0]} [bold white]{str(n)}[/bold white] {lang["guess"][1]} '{lang["quit"]}'{lang["guess"][2]}[{warning_color}]")
        users = ""
        gave_up = False
        while users != target:
            users = iinput()
            delete_last_lines(1)
            if users in terminal:
                gave_up = True
                break
            if len(users) != len(target):
                pprint(f"[{idiot_color}]{users}[/{idiot_color}]")
                pprint(f"[{idiot_color}]{lang["wrong len"]}[/{idiot_color}]")
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
            pprint("")
            rounds.append(0)
            pprint(f"{lang["ans"]}: {target}")
        else:
            pprint(lang["win"])
            pprint(lang["continue"])
            rounds.append(1)
            iinput()

if __name__ == "__main__":
    lang = languages[0]
    if len(sys.argv) > 1:
        lang_name = sys.argv[1].lower()
        for cur_lang in languages:
            if lang_name == cur_lang["name"] or lang_name == cur_lang["short"]:
                lang = cur_lang
    main()