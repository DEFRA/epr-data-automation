import random
import string

def rand_suffix(length: int = 8) -> str:
    """
    Generate a random alphanumeric suffix.
    
    Args:
        length: Length of the suffix. Default is 8.
    
    Returns:
        A random string of alphanumeric characters.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

