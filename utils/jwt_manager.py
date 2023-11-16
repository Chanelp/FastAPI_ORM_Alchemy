from jwt import encode, decode
import os
#from dotenv import load_dotenv

#load_dotenv()

#SECRET_KEY = os.getenv('SECRET_KEY')

def create_token(data: dict):
    #token = encode(payload= data, key= SECRET_KEY, algorithm= "HS256")
    token = encode(payload= data, key="my_secret_key", algorithm= "HS256")
    return token

def validate_token(token: str) -> dict:
    #data: str = decode(token, key=SECRET_KEY, algorithms = ["HS256"])
    data: str = decode(token, key="my_secret_key", algorithms = ["HS256"])
    return data