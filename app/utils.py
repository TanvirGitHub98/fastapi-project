from passlib.context import CryptContext #for hashing

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") #For hashing

def hash(password:str):
    return pwd_context.hash(password)


def verifyLogin(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)