import sqlite3
import random
import string
import getpass

# Database Setup

def setup_database():
    conn = sqlite3.connect('password_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            security_question TEXT,
            security_answer TEXT
        )''')
    conn.commit()
    conn.close()

# Function to Register New Users
def register_user():
    conn = sqlite3.connect('password_system.db')
    cursor = conn.cursor()
    
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    security_question = input("Enter a security question: ")
    security_answer = input("Enter the answer to your security question: ")
    
    cursor.execute('''INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)''', (username, password, security_question, security_answer))
    
    conn.commit()
    conn.close()

# Level 1: Username and Password Verification
def level_1(username, password):
    conn = sqlite3.connect('password_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT password FROM users WHERE username = ?''', (username,))
    
    record = cursor.fetchone()
    conn.close()
    
    if record and record[0] == password:
        return True
    else:
        return False

# Level 2: Captcha Verification
def generate_captcha():
    captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return captcha

def level_2(captcha):
    user_input = input(f"Enter the CAPTCHA [{captcha}]: ")
    return user_input == captcha

# Level 3: Security Question Verification
def level_3(username):
    conn = sqlite3.connect('password_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT security_question, security_answer FROM users WHERE username = ?''', (username,))
    
    record = cursor.fetchone()
    conn.close()
    
    if record:
        security_question, correct_answer = record
        user_answer = input(f"{security_question}: ")
        return user_answer == correct_answer
    return False

# Authentication
def authenticate():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    if level_1(username, password):
        print("Level 1: Username and Password Verification Successful")
        
        captcha = generate_captcha()
        if level_2(captcha):
            print("Level 2: CAPTCHA Verification Successful")
            
            if level_3(username):
                print("Level 3: Security Question Verification Successful")
                print("Access Granted!")
            else:
                print("Level 3: Security Question Verification Failed. Access Denied!")
        else:
            print("Level 2: CAPTCHA Verification Failed. Access Denied!")
    else:
        print("Level 1: Username and Password Verification Failed. Access Denied!")

# Run the system
setup_database()
# register_user()
register_user()
# Authenticate()
authenticate()
