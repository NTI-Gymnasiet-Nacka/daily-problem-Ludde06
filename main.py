import os
import time
import sys

def rensaterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

file_name = "file.txt"

def read_list():
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            item = [row.strip() for row in f.readlines()]
            return item
    else:
        print("Finns ingen fil")
        return []

def save_list(item):
    with open(file_name, 'w') as f:
        for i, sak in enumerate(item, 1):
            f.write(f"{sak}\n")

def show_list():
    item = read_list()
    if item:
        print("Att-göra-lista:")
        for i, sak in enumerate(item, 1):
            print(f"{i}. {sak}")
    else:
        print("Listan är tom.")

def add_item():
    ny_sak = input("Skriv vad du vill lägga till: ")
    item = read_list()
    item.append(ny_sak)
    save_list(item)
    print(f"'{ny_sak}' har lagts till i listan.")

def remove_item():
    item = read_list()
    show_list()
    try:
        num = int(input("Ange numret på saken du vill ta bort: "))
        if 1 <= num <= len(item):
            borttagen_sak = item.pop(num-1)
            save_list(item)
            print(f"'{borttagen_sak}' har tagits bort från listan.")
        else:
            print("Ogiltigt nummer.")
    except ValueError:
        print("Ange ett giltigt nummer.")


def user_menu():
    while True: 
        rensaterminal()
        print("╔══════════════════════╗")
        print("║    Att Göra Lista    ║")
        print("╠══════════════════════╣")
        print("║    1. Vissa lista    ║")
        print("║   2. Lägg till sak   ║")
        print("║    3. Ta bort sak    ║")
        print("║      4. Avsluta      ║")
        print("╚══════════════════════╝")
        print("")
        meny = input("Välj mellan (1/2/3): ")
        if meny == "1":
            rensaterminal()
            show_list()
            print()
            goback = input("Gå tillbaka?")
            continue
        elif meny == "2":
            rensaterminal()
            add_item()
            print()
            goback = input("Gå tillbaka?")
        elif meny == "3":
            rensaterminal()
            remove_item()
            print()
            goback = input("Gå tillbaka?")
        elif meny == "4":
            rensaterminal()
            print("╔══════════════════════════════════════════╗")
            print("║ - Du kommer nu att stänga av programet - ║")
            print("╚══════════════════════════════════════════╝")
            time.sleep(3)
            sys.exit()
        else:
            rensaterminal()
            print("╔═════════════════════════════════════╗")
            print("║ Du måste välja ett av numrena 1/2/3 ║")
            print("╚═════════════════════════════════════╝")
            time.sleep(3)
            continue


def main():
    user_menu()


if __name__ == "__main__":
    main()