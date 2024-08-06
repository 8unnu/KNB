import jwt

secret_key = f"8unnu9"

ALGORITHM = 'HS256'

def create_jwt_token(data: dict):
    return jwt.encode(data, secret_key, algorithm=ALGORITHM)

def decode_jwt_token(jwt_token):
    try:
        payload = jwt.decode(jwt_token, secret_key, algorithms=ALGORITHM)
        return payload.get("sub")
    except jwt.exceptions.InvalidSignatureError:
        pass