import random
import string


def passwordGenerator(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
