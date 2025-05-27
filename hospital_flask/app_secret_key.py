import secrets

def generate_secret_key():
    return secrets.token_hex(32)
secret_key= generate_secret_key()
if __name__ == "__main__":
    print("Your secret key is:")
    print(generate_secret_key())
