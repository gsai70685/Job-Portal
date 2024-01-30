from passlib.context import CryptContext #It allows us to hash password using various algorithms
import secrets
import string
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
cwd = os.path.abspath(os.getcwd())
foldername = os.path.join(cwd, "media", "Logo")

async def hash_password(password:str) -> str:
    return pwd_context.hash(password)

async def verify_password(password:str, hash_password:str) -> bool:
    return pwd_context.verify(password, hash_password)

def generate_secret_key(length=32):
    """
    Generates a random secret key of the specified length.

    Parameters:
        length (int): Length of the secret key. Default is 32.

    Returns:
        str: Randomly generated secret key.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secrets_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secrets_key