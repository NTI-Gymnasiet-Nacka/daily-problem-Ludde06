import time
import requests
import base64
import hashlib
import os
import sys
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken

FILE_NAME = "data.txt"

# Encryption system
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()) 

def decrypt_message(encrypted_message: str, password: str) -> str:
    key = generate_key(password)  
    fernet = Fernet(key)  
    decrypted_message = fernet.decrypt(encrypted_message.encode())  
    return decrypted_message.decode()  
# Encryption system

def read_list(password: str):
    """
    Reads and decrypts items from a file if it exists.

    Args:
        password (str): The password for decryption.

    Returns:
        list: A list of decrypted items or an empty list if the file is missing.
    """
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            encrypted_items = [row.strip() for row in f.readlines()] 
            decrypted_items = [decrypt_message(item, password) for item in encrypted_items]  
            return decrypted_items
    else:
        print("Error - Filen är borttagen eller saknas")
        return []
    
def read_epost(password):
    """
    Reads and decrypts the first line of a file to extract an email address.

    Args:
        password: The password used for decryption.

    Returns:
        str: The extracted email address, or None if the file is missing or empty.
    """
    if os.path.exists(FILE_NAME) and os.stat(FILE_NAME).st_size > 0:
        with open(FILE_NAME, 'r') as f:
            encrypted_item = f.readline().strip()
            decrypted_item = decrypt_message(encrypted_item, password)
            
            email_part = decrypted_item.split('/')[1]
            return email_part
    else:
        print("Error - Filen är borttagen eller tom")

def send_api_request(subject: str, message: str, password):
    """
    Sends an email via an API request.

    Args:
        subject (str): The subject of the email.
        message (str): The content of the email.
        password: The password used to read the recipient's email.

    Returns:
        None
    """
    payload = {
        'token': "FJH35HGH457645JH", #Kommer raderas efter projektet är klart
        'from': "notis@metelius.nu",
        'to': read_epost(password),
        'subject': subject,
        'message': message
    }
    try:
        response = requests.get("https://metelius.nu/api-system/epost", params=payload)
        if response.status_code == 200:
            print(f"E-post skickat")
        else:
            print(f"Fel vid skickande av e-post: {response.status_code}")
    except requests.RequestException as e:
        print(f"Fel vid API-förfrågan: {e}")

def check_deadlines(password):
    """
    Checks for and warns about deadlines from a list.

    Args:
        password: The password used to read the list of items.

    Returns:
        None
    """
    warned_deadlines = set() #Saves all warnings

    while True:
        items = read_list(password)

        for item in items:
            if "{" in item and "}" in item:
                deadline_str = item.split("{")[-1].strip(" }")#Takes out the date
                
                try:
                    deadline_date_str, deadline_time_str = deadline_str.split(" ")
                    deadline_day, deadline_month = map(int, deadline_date_str.split("/"))
                    deadline_hour, deadline_minute = map(int, deadline_time_str.split(":"))

                    current_time = datetime.now()
                    current_day = current_time.day
                    current_month = current_time.month
                    current_hour = current_time.hour
                    current_minute = current_time.minute

                    if (deadline_month < current_month or
                        (deadline_month == current_month and deadline_day < current_day) or
                        (deadline_month == current_month and deadline_day == current_day and
                         (deadline_hour < current_hour or 
                          (deadline_hour == current_hour and deadline_minute <= current_minute)))):
                        
                        if deadline_str not in warned_deadlines:
                            subject = f"Deadlinen har passerats!"
                            message = f"Deadlinen för {item.split('{')[0].strip()} har nåtts eller passerats ({deadline_str})!"
                            print(f"{message}")
                            send_api_request(subject, message, password)
                            warned_deadlines.add(deadline_str)              
                except ValueError:
                    print(f"Felaktigt format på deadline: {deadline_str}")
        time.sleep(60) 

def main():
    attempts = 3 
    while attempts > 0:
        password = input("Ange ditt lösenord för att övervaka deadlines: ")
        try:
            _ = read_list(password) 
            print("Lösenord verifierat - deadline-övervakning startar.")
            break
        except InvalidToken:
            attempts -= 1
            if attempts > 0:
                print(f"Fel lösenord. Du har {attempts} försök kvar.")
            else:
                print("För många misslyckade försök. Filen raderas.")
                os.remove(FILE_NAME)
                sys.exit()

    check_deadlines(password)

if __name__ == "__main__":
    main()
