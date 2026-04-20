import os
import jwt
import schemas
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expire_minutes = os.getenv("TOKEN_EXPIRE_MINUTES", "30")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    # Create a copy of the data to be encoded in the token
    to_encode = data.copy()
    # Set the expiration time for the token
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(str(token_expire_minutes)))
    # Add the expiration time to the data to be encoded in the token
    to_encode.update({"exp": expire})
    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, secret_key, algorithms=[algorithm]) # type: ignore
        # Extract the user ID from the token payload
        id: str = payload.get("user_id") # type: ignore
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)