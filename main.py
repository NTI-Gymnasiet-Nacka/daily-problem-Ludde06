from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import time
import sys
import hashlib

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

file_name = "data.txt"

# - Encryption system

# Funktion för att generera en nyckel från ett lösenord
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())  # Generera en nyckel från lösenordet

# Funktion för att kryptera text
def encrypt_message(message: str, password: str) -> str:
    key = generate_key(password)  # Generera en nyckel från lösenordet
    fernet = Fernet(key)  # Skapa en Fernet-instans med nyckeln
    encrypted_message = fernet.encrypt(message.encode())  # Kryptera meddelandet
    return encrypted_message.decode()  # Returnera krypterad text som sträng

# Funktion för att dekryptera text
def decrypt_message(encrypted_message: str, password: str) -> str:
    key = generate_key(password)  # Generera en nyckel från lösenordet
    fernet = Fernet(key)  # Skapa en Fernet-instans med nyckeln
    decrypted_message = fernet.decrypt(encrypted_message.encode())  # Dekryptera meddelandet
    return decrypted_message.decode()  # Returnera dekrypterad text som sträng

# - Encryption system


def create_new_user():
    clear_terminal()
    print("╔═══════════════════════════════╗")
    print("║    Välkommen ny användare!    ║")
    print("╚═══════════════════════════════╝")
    while True:
        print()
        username = input("Skapa ett användarnamn: ")
        if validate_username(username):
            break 
    while True:
        print()
        password = input("Skapa ett lösenord (minst 4 tecken, inga blanksteg): ")
        if validate_password(password):
            break
    
    username_data = [username]  
    save_list(username_data, password)
    return password

def validate_username(username: str) -> bool:
    if len(username.strip()) == 0 or ' ' in username:
        print("Användarnamnet får inte vara tomt eller innehålla blanksteg.")
        return False
    return True

def validate_password(password: str) -> bool:
    if len(password) < 4 or ' ' in password:
        print("Lösenordet måste vara minst 4 tecken långt och får inte innehålla blanksteg.")
        return False
    return True



def check_file_exists_or_empty():
    if not os.path.exists(file_name) or os.stat(file_name).st_size == 0:
        return False
    return True

def unhide_file(file_name):
    if os.name == 'nt':
        os.system(f'attrib -h {file_name}') 

def hide_file(file_name):
    if os.name == 'nt':
        os.system(f'attrib +h {file_name}')



def read_user(password):
    if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
        with open(file_name, 'r') as f:
            encrypted_item = f.readline().strip()
            decrypted_item = decrypt_message(encrypted_item, password) 
            return decrypted_item 
    else:
        print("Error - Filen är borttagen eller tom.")

def read_list(password):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            encrypted_items = [row.strip() for row in f.readlines()] 
            decrypted_items = [decrypt_message(item, password) for item in encrypted_items] 
            return decrypted_items  
    else:
        print("Error - Filen är borttagen")
        return []

def save_list(items, password):
    with open(file_name, 'w') as f:
        for sak in items:
            encrypted_item = encrypt_message(sak, password)  
            f.write(f"{encrypted_item}\n") 

def show_list(password):
    items = read_list(password)
    if items:
        print("╔══════════════════════╗")
        print("║    Att Göra Lista    ║")
        print("╚══════════════════════╝")
        print()
        for i, sak in enumerate(items[1:], 1):
            print(f"{i}. {sak}")
    else:
        print()
        print("Listan är tom")

def add_item(password):
    ny_sak = input("Vad vill du lägga till - (A)vbryt: ")
    if ny_sak.lower() == "a":
        return False
    else:
        items = read_list(password)
        items.append(ny_sak)
        save_list(items, password)
        print(f"'{ny_sak}' har lagts till i listan.")
        return True

def remove_item(password):
    items = read_list(password)
    show_list(password)
    print()
    while True:
        try:
            num = int(input("Ange numret på saken du vill ta bort - (0) Avbryt: "))
            if num == 0:
                return False
            else:
                num += 1
                if 1 <= num <= len(items):
                    borttagen_sak = items.pop(num-1)
                    save_list(items, password)
                    print(f"'{borttagen_sak}' har tagits bort från listan.")
                    return True
                else:
                    print()
                    print("Ogiltigt nummer.")
                    print()
        except ValueError:
            print("Ange ett giltigt nummer.")

def edit(password):
    items = read_list(password)
    show_list(password)
    print()
    while True:
        try:
            num = int(input("Ange numret på saken du vill redigera - (0) Avbryt: "))
            if num == 0:
                return False
            else:
                if 1 <= num <= len(items):
                    clear_terminal()
                    print(f"Redigera: '{items[num]}'")
                    ny_text = input("Vad vill du ändra det till - (A)vbryt: ")
                    if ny_text.lower() == "a":
                        return False
                    else:
                        items[num] = ny_text
                        save_list(items, password)
                        print()
                        print(f"Objektet har uppdaterats till: '{ny_text}'")
                        return True
                else:
                    print("Ogiltigt nummer.\n")
        except ValueError:
            print("Ange ett giltigt nummer.")


# Fixa så man kan sortera utefrån prioritet, Email system (deadline), Kunna markera fördiga uppgifter, Kanse kunna grupptera uppgifter

def main():
    attempts = 3  
    while not check_file_exists_or_empty():
        password = create_new_user() 
        clear_terminal()
        break
    while check_file_exists_or_empty():  
        password = input("Skriv in Lösenord: ")
        try:
            _ = read_list(password)  
            print("Lösenord verifierat - välkommen!")
            unhide_file(file_name)
            time.sleep(1)
            break
        except InvalidToken:
            attempts -= 1
            if attempts > 0:
                print(f"Fel lösenord. Du har {attempts} försök kvar.")
                print()
            else:
                print("För många misslyckade försök. Filen raderas.")
                os.remove(file_name)
                sys.exit()  
    clear_terminal()
    while True:
        clear_terminal()
        user = read_user(password)
        size = len(user) + 18
        print("╔" + "═" * (size - 2) + "╗")
        print(f'║  Användaren: {user}  ║')
        print("╚" + "═" * (size - 2) + "╝")
        print()
        print("╔══════════════════════╗")
        print("║    Att Göra Lista    ║")
        print("╠══════════════════════╣")
        print("║    1. Vissa lista    ║")
        print("║     2. Lägg till     ║")
        print("║      3. Ta bort      ║")
        print("║     4. Redigera      ║")
        print("║                      ║")
        print("║      5. Avsluta      ║")
        print("╚══════════════════════╝")
        print()
        print()
        meny = input("Välj mellan (1/2/3/4): ")
        if meny == "1":
            clear_terminal()
            show_list(password)
            print()
            input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "2":
            clear_terminal()
            tillagd = add_item(password)
            print()
            if tillagd:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "3":
            clear_terminal()
            bortagen = remove_item(password)
            print()
            if bortagen:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "4":
            clear_terminal()
            bortagen = edit(password)
            print()
            if bortagen:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "5":
            clear_terminal()
            print("╔══════════════════════════════════════════╗")
            print("║ - Du kommer nu att stänga av programet - ║")
            print("╚══════════════════════════════════════════╝")
            hide_file(file_name) 
            time.sleep(2)
            sys.exit()
        else:
            clear_terminal()
            print("╔═══════════════════════════════════════╗")
            print("║ Du måste välja ett av numrena 1/2/3/4 ║")
            print("╚═══════════════════════════════════════╝")
            time.sleep(2)


if __name__ == "__main__":
    main()
