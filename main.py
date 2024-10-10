import base64
import os
import time
import sys
import hashlib
from cryptography.fernet import Fernet, InvalidToken

FILE_NAME = "data.txt"

# Encryption system
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message: str, password: str) -> str:
    key = generate_key(password)  
    fernet = Fernet(key)  
    encrypted_message = fernet.encrypt(message.encode())  
    return encrypted_message.decode() 

def decrypt_message(encrypted_message: str, password: str) -> str:
    key = generate_key(password)  
    fernet = Fernet(key) 
    decrypted_message = fernet.decrypt(encrypted_message.encode()) 
    return decrypted_message.decode() 
# Encryption system

def clear_terminal():
    """
    Clears the terminal screen.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def create_new_user():
    """
    Creates a new user by collecting username, email, and password.

    Returns:
        str: The password for the newly created user.
    """
    clear_terminal()
    print("╔═══════════════════════════════╗")
    print("║    Välkommen ny användare!    ║")
    print("╚═══════════════════════════════╝")
    while True:
        print()
        username = str(input("Skapa ett användarnamn: "))
        if validate_username(username):
            break 
    while True:
        print()
        email = str(input("Skriv in din epost (Deadline notifikation): "))
        if validate_email(email):
            break 
    while True:
        print()
        password = input("Skapa ett lösenord (minst 4 tecken, inga blanksteg): ")
        if validate_password(password):
            break

    username_data = [(username + "/" + email)]  
    save_list(username_data, password)
    return password

def validate_username(username: str) -> bool:
    """
    Validates the provided username.

    Args:
        username (str): The username to validate.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if len(username) == 0 or ' ' in username:
        print("Användarnamnet får inte vara tomt eller innehålla blanksteg")
        return False
    return True

def validate_email(email: str) -> bool:
    """
    Validates the provided email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if "@" in email:
        return True
    print("Måste finnas ett '@' i eposten")
    return False

def validate_password(password: str) -> bool:
    """
    Validates the provided password.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if len(password) < 4 or ' ' in password:
        print("Lösenordet måste vara minst 4 tecken långt och får inte innehålla blanksteg")
        return False
    return True

def check_file_exists_or_empty():
    """
    Checks if the specified file exists and is not empty.

    Returns:
        bool: True if the file exists and is not empty, False otherwise.
    """
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        return False
    return True

def unhide_file():
    """
    Unhides a file on Windows by removing its hidden attribute.

    Returns:
        None
    """
    if os.name == 'nt':
        os.system(f'attrib -h {FILE_NAME}') 

def hide_file():
    """
    Hides a file on Windows by setting its hidden attribute.

    Returns:
        None
    """
    if os.name == 'nt':
        os.system(f'attrib +h {FILE_NAME}')

def read_user(password):
    """
    Reads and decrypts the first line of a file to extract the username.

    Args:
        password: The password used for decryption.

    Returns:
        str: The extracted username, or None if the file is missing or empty.
    """
    if os.path.exists(FILE_NAME) and os.stat(FILE_NAME).st_size > 0:
        with open(FILE_NAME, 'r') as f:
            encrypted_item = f.readline().strip()
            decrypted_item = decrypt_message(encrypted_item, password)
            
            user_part = decrypted_item.split('/')[0]
            return user_part
    else:
        print("Error - Filen är borttagen eller tom")

def change_email(email, password):
    """
    Changes the user's email address and updates it in the file.

    Args:
        email (str): The new email address to be set.
        password: The password used for decryption and encryption.

    Returns:
        None
    """
    if os.path.exists(FILE_NAME) and os.stat(FILE_NAME).st_size > 0:
        with open(FILE_NAME, 'r') as f:
            encrypted_item = f.readline().strip()
            decrypted_item = decrypt_message(encrypted_item, password)
            
            user_part = decrypted_item.split('/')[0]
            
            new_data = f"{user_part}/{email}"
            
            encrypted_new_data = encrypt_message(new_data, password)
        with open(FILE_NAME, 'w') as f:
            f.write(encrypted_new_data)
    else:
        print("Error - Filen är borttagen eller tom")

def read_list(password):
    """
    Reads and decrypts items from a file if it exists.

    Args:
        password: The password used for decryption.

    Returns:
        list: A list of decrypted items or an empty list if the file is missing.
    """
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            encrypted_items = [row.strip() for row in f.readlines()] 
            decrypted_items = [decrypt_message(item, password) for item in encrypted_items] 
            return decrypted_items  
    else:
        print("Error - Filen är borttagen")
        return []

def save_list(items, password):
    """
    Encrypts and saves a list of items to a file.

    Args:
        items (list): The list of items to be saved.
        password: The password used for encryption.

    Returns:
        None
    """
    with open(FILE_NAME, 'w') as f:
        for item in items:
            encrypted_item = encrypt_message(item, password)  
            f.write(f"{encrypted_item}\n") 

def show_list(password):
    """
    Displays the list of items to the user.

    Args:
        password: The password used to decrypt the items.

    Returns:
        None
    """
    items = read_list(password)
    if items:
        print("╔══════════════════════╗")
        print("║    Att Göra Lista    ║")
        print("╚══════════════════════╝")
        print()
        for i, sak in enumerate(items[1:], 1):
            print(f"{i}. {sak}")
    else:
        print("\nListan är tom")

def add_item(password):
    """
    Prompts the user to add an item to the list.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the item was added successfully, False if canceled.
    """
    new_item = input("Vad vill du lägga till - (A)vbryt: ")
    if new_item.lower() == "a":
        return False
    else:
        items = read_list(password)
        items.append(new_item)
        save_list(items, password)
        print(f"'{new_item}' har lagts till i listan")
        return True

def remove_item(password):
    """
    Prompts the user to remove an item from the list.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the item was removed successfully, False if canceled.
    """
    items = read_list(password)
    show_list(password)
    print()
    while True:
        try:
            number = int(input("Ange numret på saken du vill ta bort - (0) Avbryt: "))
            if number == 0:
                return False
            else:
                number += 1
                if 1 <= number <= (len(items)):
                    remove_item = items.pop(number - 1)
                    save_list(items, password)
                    print(f"'{remove_item}' har tagits bort från listan")
                    return True
                else:
                    print("\nOgiltigt nummer")
                    print()
        except ValueError:
            print("Ange ett giltigt nummer")

def edit(password):
    """
    Prompts the user to edit an existing item in the list.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the item was edited successfully, False if canceled.
    """
    items = read_list(password)
    show_list(password)
    print()
    while True:
        try:
            number = int(input("Ange numret på saken du vill redigera - (0) Avbryt: "))
            if number == 0:
                return False
            else:
                if 1 <= number <= (len(items) - 1):
                    clear_terminal()
                    print(f"Redigera: '{items[number]}'")
                    new_text = input("Vad vill du ändra det till - (A)vbryt: ")
                    if new_text.lower() == "a":
                        return False
                    else:
                        items[number] = new_text
                        save_list(items, password)
                        print(f"\nObjektet har uppdaterats till: '{new_text}'")
                        return True
                else:
                    print("Ogiltigt nummer\n")
        except ValueError:
            print("Ange ett giltigt nummer")

def finished(password):
    """
    Marks an item in the list as completed or uncompleted.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the item's status was changed successfully, False if canceled.
    """
    items = read_list(password)
    show_list(password)
    print()
    while True:
        try:
            number = int(input("Ange numret på saken du vill marekar som klar - (0) Avbryt: "))
            if number == 0:
                return False
            else:
                if 1 <= number <= (len(items) - 1):
                    clear_terminal()
                    if items[number].startswith("(") and items[number].endswith(")"):
                        items[number] = items[number][1:-1]
                        print(f"\nObjektet är nu avmarkerat som klart: '{items[number]}'")
                    else:
                        items[number] = "(" + items[number] + ")"
                        print(f"\nObjektet är nu markerat som klart: '{items[number]}'")
                    save_list(items, password)
                    return True
                else:
                    print("Ogiltigt nummer\n")
        except ValueError:
            print("Ange ett giltigt nummer")

def prio(password):
    """
    Sets or updates the priority of an item in the list.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the priority was set or updated successfully, False if canceled.
    """
    items = read_list(password)
    while True:
        try:
            clear_terminal()
            show_list(password)
            print()
            number = int(input("Ange numret på saken du vill prioritera - (0) Avbryt: "))
            if number == 0:
                return False
            elif 1 <= number <= (len(items) - 1):
                clear_terminal()
                current_item = items[number]
                current_priority = ""
                
                if '[' in current_item and ']' in current_item:
                    current_priority = current_item[current_item.index('['):]
                    current_item = current_item[:current_item.index('[')].strip()
                
                print(f"Prioritera: '{current_item}'")
                prio_choice = input("Ange prioritet (+, ++, +++) - (tryck Enter för att ta bort prioritet) - (A)vbryt: ")
                
                if prio_choice.lower() == "a":
                    return False
                elif prio_choice == "":
                    items[number] = current_item
                    save_list(items, password)
                    print(f"\nPrioriteten är borttagen: '{items[number]}'")
                    return True
                elif prio_choice in ['+', '++', '+++']:
                    if current_priority != f"[{prio_choice}]":
                        items[number] = f"{current_item} [{prio_choice}]"
                        save_list(items, password)
                        print(f"\nPrioriteten är uppdaterad: '{items[number]}'")
                    else:
                        print(f"\nIngen ändring gjordes, prioriteten är redan '{prio_choice}'")
                    return True
                else:
                    print("Ogiltig prioritet: Välj +, ++ eller +++\n")
                    time.sleep(1)
            else:
                print("Ogiltigt nummer\n")
        except ValueError:
            print("Ange ett giltigt nummer")

def deadline(password):
    """
    Adds or removes a deadline for an item in the list.

    Args:
        password: The password used for accessing the item list.

    Returns:
        bool: True if the deadline was set or removed successfully, False if canceled.
    """
    items = read_list(password)
    while True:
        try:
            clear_terminal()
            show_list(password)
            print()
            number = int(input("Ange numret på saken du vill lägga till eller ta bort en deadline på - (0) Avbryt: "))
            if number == 0:
                return False
            elif 1 <= number <= (len(items) - 1):
                clear_terminal()
                current_item = items[number]
                print(f"Nuvarande sak: '{current_item}'")
                
                deadline_input = input("Ange deadline (format: dd/mm hh:mm) eller tryck Enter för att ta bort deadline - (A)vbryt: ")
                
                if deadline_input.lower() == "a":
                    return False
                elif deadline_input == "":
                    if "{" in current_item and "}" in current_item:
                        current_item = current_item.split("{")[0].strip() 
                        items[number] = current_item
                        save_list(items, password)
                        print(f"\nDeadlinen har tagits bort från '{current_item}'")
                    else:
                        print("\nIngen deadline att ta bort")
                    return True
                
                try:
                    time.strptime(deadline_input, "%d/%m %H:%M")
                    
                    if "{" in current_item and "}" in current_item:
                        current_item = current_item.split("{")[0].strip() 
                
                    items[number] = f"{current_item} {{{deadline_input}}}"
                    save_list(items, password)
                    print(f"\nDeadlinen '{deadline_input}' har lagts till på '{current_item}'")
                    return True
                except ValueError:
                    print("Felaktigt format: Ange datum och tid som dd/mm hh:mm\n")
                    time.sleep(2)
            else:
                print("Ogiltigt nummer\n")
        except ValueError:
            print("Ange ett giltigt nummer")

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
            unhide_file()
            time.sleep(1)
            break
        except InvalidToken:
            attempts -= 1
            if attempts > 0:
                print(f"Fel lösenord: Du har {attempts} försök kvar")
                print()
            else:
                print("För många misslyckade försök, Filen raderas...")
                os.remove(FILE_NAME)
                sys.exit()  
    while True:
        clear_terminal()
        user = read_user(password)
        size = len(user) + 18
        print("╔" + "═" * (size - 2) + "╗")
        print(f'║  Användaren: {user}  ║')
        print("╚" + "═" * (size - 2) + "╝")
        print("\n╔════════════════════════╗")
        print("║     Att Göra Lista     ║")
        print("╠════════════════════════╣")
        print("║     1. Vissa lista     ║")
        print("║      2. Lägg till      ║")
        print("║       3. Ta bort       ║")
        print("║      4. Redigera       ║")
        print("║                        ║")
        print("║  5. Markera (Färdigt)  ║")
        print("║    6. Prio-ordning     ║")
        print("║      7. Deadline       ║")
        print("║                        ║")
        print("║                        ║")
        print("║     'fabricreset'      ║")
        print("║     'change_email'     ║")
        print("║                        ║")
        print("║       (A)vsluta        ║")
        print("╚════════════════════════╝")
        print()
        print()
        meny = input("Välj mellan (1/2/3/4/5/6/7), inställningar eller A: ")
        if meny == "1":
            clear_terminal()
            show_list(password)
            input("\nGå tillbaka? (Tryck på Enter)")
        elif meny == "2":
            clear_terminal()
            tillagd = add_item(password)
            print()
            if tillagd:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "3":
            clear_terminal()
            remove = remove_item(password)
            print()
            if remove:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "4":
            clear_terminal()
            remove = edit(password)
            print()
            if remove:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "5":
            clear_terminal()
            remove = finished(password)
            print()
            if remove:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "6":
            clear_terminal()
            remove = prio(password)
            print()
            if remove:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny == "7":
            clear_terminal()
            remove = deadline(password)
            print()
            if remove:
                input("Gå tillbaka? (Tryck på Enter)")
        elif meny.lower() == "a":
            clear_terminal()
            print("╔══════════════════════════════════════════╗")
            print("║ - Du kommer nu att stänga av programet - ║")
            print("╚══════════════════════════════════════════╝")
            hide_file() 
            time.sleep(2)
            sys.exit()
        elif meny == "fabricreset":
            clear_terminal()
            print("╔══════════════════════╗")
            print("║ - Datan är raderad - ║")
            print("╚══════════════════════╝")
            time.sleep(2)
            os.remove(FILE_NAME)
            sys.exit()  
        elif meny == "change_email":
            clear_terminal()
            print("╔═════════════════╗")
            print("║ - Ändra Email - ║")
            print("╚═════════════════╝")
            print()
            while True:
                print()
                email = input("Skriv in din nya epost: ")
                if validate_email(email):
                    print()
                    print("Epost ändrad!")
                    change_email(email, password)
                    break
            time.sleep(2)
        else:
            clear_terminal()
            print("╔══════════════════════════════════════╗")
            print("║ Du måste välja 1/2/3/4/5/6/7 eller A ║")
            print("╚══════════════════════════════════════╝")
            time.sleep(2)


if __name__ == "__main__":
    main()