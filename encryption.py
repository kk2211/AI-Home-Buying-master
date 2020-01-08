from cryptography.fernet import Fernet
import os
import base64
import csv
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encryptPassword(password):
    pwd = password.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd))
    fernet = Fernet(key)
    encrypted = fernet.encrypt(pwd)

    return key.decode(), encrypted.decode()

def decryptPassword(key, password):
    key = key.encode()
    password = password.encode()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(password)
    return decrypted.decode()

def checkEmail(email):
    if not os.path.exists('user_details.csv'):
        return 1
    else:
        df = pd.read_csv('user_details.csv')
        flag = 1
        for i in range(len(df)):
            if df['email'].iloc[i] == email:
                flag = 0
                break
    return flag

def storeDetails(email, password, age, gender, businessman):
    key, password = encryptPassword(password)
    rows = []
    row = [email, key, password, age, gender, businessman]
    if not os.path.exists('user_details.csv'):
        rows.append(['email', 'key', 'password', 'age', 'gender', 'businessman'])
    rows.append(row)
    data = open('user_details.csv', 'a')
    writer = csv.writer(data)
    writer.writerows(rows)
    data.close()

def matchDetails(email, password):
    if not os.path.exists('user_details.csv'):
        return 0
    else:
        df = pd.read_csv('user_details.csv')
        flag = 0
        for i in range(len(df)):
            if df['email'].iloc[i]==email:
                key = df['key'].iloc[i]
                decrypted = df['password'].iloc[i]

                if decryptPassword(key, decrypted)==password:
                    flag = 1
                else:
                    flag = 0
                    break
    return flag


def getUserDetails(email):
    df = pd.read_csv('user_details.csv')
    df = df[df['email']==email]

    details = list(df.iloc[0])
    age = details[3]
    gender = details[4]
    bus = details[5]

    return [age, gender, bus]
