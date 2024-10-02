from cryptography.fernet import Fernet
import base64
import os
import time
import sys
import hashlib

def rensaterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#//////////////////////// Kryptera

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

#//////////////////////// Kryptera

file_name = "file.txt"

def read_list(password):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            encrypted_items = [row.strip() for row in f.readlines()] 
            decrypted_items = [decrypt_message(item, password) for item in encrypted_items] 
            return decrypted_items  
    else:
        print("Finns ingen fil")
        return []

def save_list(items, password):
    with open(file_name, 'w') as f:
        for sak in items:
            encrypted_item = encrypt_message(sak, password)  
            f.write(f"{encrypted_item}\n") 

def show_list(password):
    items = read_list(password)
    if items:
        print("Att-göra-lista:")
        for i, sak in enumerate(items, 1):
            print(f"{i}. {sak}")
    else:
        print("Listan är tom.")

def add_item(password):
    ny_sak = input("Skriv vad du vill lägga till: ")
    items = read_list(password)
    items.append(ny_sak)
    save_list(items, password)
    print(f"'{ny_sak}' har lagts till i listan.")

def remove_item(password):
    items = read_list(password)
    show_list(password)
    try:
        num = int(input("Ange numret på saken du vill ta bort: "))
        if 1 <= num <= len(items):
            borttagen_sak = items.pop(num-1)
            save_list(items, password)
            print(f"'{borttagen_sak}' har tagits bort från listan.")
        else:
            print("Ogiltigt nummer.")
    except ValueError:
        print("Ange ett giltigt nummer.")

# Fixa så man kan sortera utefrån prioritet, Email system (deadline), Kunna markera fördiga uppgifter, kunna redigera uppgifter, Kanse kunna grupptera uppgifter

def user_menu():
    password = input("Skriv in Lösenord: ") # Lägg till så man kan skapa lösenrod om inget är skrivet i filen
    rensaterminal()
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
        meny = input("Välj mellan (1/2/3/4): ")
        if meny == "1":
            rensaterminal()
            show_list(password)
            input("Gå tillbaka? Tryck på Enter.")
        elif meny == "2":
            rensaterminal()
            add_item(password)
            input("Gå tillbaka? Tryck på Enter.")
        elif meny == "3":
            rensaterminal()
            remove_item(password)
            input("Gå tillbaka? Tryck på Enter.")
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
            print("║ Du måste välja ett av numrena 1/2/3/4 ║")
            print("╚═════════════════════════════════════╝")
            time.sleep(3)

def main():
    user_menu()

if __name__ == "__main__":
    main()
