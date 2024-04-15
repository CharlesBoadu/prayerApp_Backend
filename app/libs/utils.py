import string;
import random;
import uuid;

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