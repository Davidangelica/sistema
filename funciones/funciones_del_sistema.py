import bcrypt

def hash_contraseña (password:str):
    salt = bcrypt.gensalt()
    try:
        hash_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    except Exception:
        return {'error':'the password could not hashed'}
    
    return hash_password

def chequear_contraseña (pw1,pw2):
    try:
        chek = bcrypt.checkpw(pw1.encode('utf-8'),pw2.encode('utf-8'))
        return 'hola'
    except:
        return False