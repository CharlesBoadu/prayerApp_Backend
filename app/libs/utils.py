import string;
import random;
import uuid;
import hashlib
import binascii

class Utilities:
    @staticmethod
    def gen_id():
        """
        Generate a random UUID and Convert
        UUID to a 32-character hexadecimal string
        """
        return uuid.uuid4().hex
    
    @staticmethod
    def get_random_string(length):
        # choose from all lowercase letter
        letters_lower = string.ascii_lowercase
        letters_upper = string.ascii_uppercase
        result_str = ''.join(random.choice(f"{letters_upper}{letters_lower}") for i in range(length))
        return result_str
    
    # Check hashed password validity
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password