import hashlib


def is_admin(login):
    """Check if the login is administrator."""
    if login in admins:
        return True
    return False

def is_authenticated_admin(login, password):
    """Check if the user is *really* and authenticated administrator."""
    if is_admin(login) and check_auth(login, password):
        return True
    return False

def is_authenticated_user(login, password):
    """Check if the user is *really* and authenticated administrator."""
    if check_auth(login, password):
        return True
    return False

def can_login(login, password):
    """Check if the login and password are valid."""
    if login in accounts and accounts[login] == password:
        return True
    return False

def encrypt_password(password):
    """Encrypt user's password, with multiple secure hashes."""
    md5_hash = hashlib.md5(password).hexdigest()
    sha1_hash = hashlib.sha1(md5_hash).hexdigest()
    sha224_hash = hashlib.sha1(sha1_hash).hexdigest()
    return sha224_hash


def check_auth(login, password):
    """Check if credentials are valid."""
    if login in accounts:
        encrypted_password = encrypt_password(accounts[login])
        if password == encrypted_password:
            return True
    return False