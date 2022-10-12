from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password):
    return bcrypt_context.hash(password)

def check_encrypted_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)
