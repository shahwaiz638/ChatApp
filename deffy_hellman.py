import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate

def generate_primitive_root(p):
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g

def diffie_hellman(p: int, g: int, a: int, b: int) -> int:
 
    # Checking if 'p' is a prime number
    if not is_prime(p):
        raise ValueError("'p' must be a prime number.")
 
    # Checking if 'g' is a primitive root modulo 'p'
    if not is_primitive_root(g, p):
        raise ValueError("'g' must be a primitive root modulo 'p'.")
 
    # Checking if 'a' and 'b' are positive integers
    if a < 0 or b < 0:
        raise ValueError("'a' and 'b' must be positive integers.")
 
    # Calculating the public keys for both parties
    A = pow(g, a, p)
    B = pow(g, b, p)
 
    # Calculating the shared secret key for both parties
    secret_key_a = pow(B, a, p)
    secret_key_b = pow(A, b, p)
 
    # Verifying that the shared secret keys match
    if secret_key_a != secret_key_b:
        raise ValueError("Shared secret keys do not match.")
 
    return secret_key_a
 
 
def is_prime(n: int) -> bool:
 
    if n <= 1:
        return False
 
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
 
    return True
 
 
def is_primitive_root(g: int, p: int) -> bool:
    """
    Checks if a number is a primitive root modulo 'p'.
 
    Parameters:
    - g: int
        The number to be checked.
    - p: int
        The modulus.
 
    Returns:
    - bool:
        True if the number is a primitive root modulo 'p', False otherwise.
    """
 
    if g <= 1 or g >= p:
        return False
 
    factors = factorize(p - 1)
 
    for factor in factors:
        if pow(g, (p - 1) // factor, p) == 1:
            return False
 
    return True
 
 
def factorize(n: int) -> list:
    """
    Factorizes a number into its prime factors.
 
    Parameters:
    - n: int
        The number to be factorized.
 
    Returns:
    - list:
        A list of prime factors of the number.
    """
 
    factors = []
 
    while n % 2 == 0:
        factors.append(2)
        n //= 2
 
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            n //= i
        else:
            i += 2
 
    if n > 1:
        factors.append(n)
 
    return factors
 
 
#Example usage of the diffie_hellman function:
# Generate a prime 'p' (e.g., 2048 bits)

def deffy_hellman(p1,p2):
    p = generate_prime(32)
    g = generate_primitive_root(p)

    print(f"Generated prime 'p': {p}")
    print(f"Generated primitive root 'g': {g}")

    # Get input for 'a' and 'b'
    a = p1
    b = p2
    
    try:
        shared_key = diffie_hellman(p, g, a, b)
        print(f"The shared secret key is: {shared_key}")
        return shared_key
    except ValueError as e:
        print(f"Error during Diffie-Hellman key exchange: {e}")
        return 0