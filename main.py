from random import randint


def encrypt(m, n, g):
    """Takes in the message m, the generated prime product n, and the computed g value and returns the ciphertext as well as the
    selected r-value."""
    r = randint(0, n)
    gcdRandN = gcd(r, n)
    while gcdRandN != 1:
        r = randint(0, n)
        gcdRandN = gcd(r, n)
    ciphertext = (pow(g, m) * pow(r, n)) % pow(n, 2)
    return ciphertext, r


def decrypt(ciphertext, mu, n, lambda_value):
    """Takes in a ciphertext, mu, n, and a computed lambda value in order to return the plaintext."""
    first_result = pow(ciphertext, lambda_value) % (n * n)
    second_result = L(first_result, n) * mu
    message = second_result % n
    return message


def gcd(a, b):
    """Computes the greatest common divisor between two numbers"""
    if a == 0:
        return b
    return gcd(b % a, a)


def lcm(a, b):
    """Computes the least common multiple of two numbers"""
    return a * b // (gcd(a, b))


def L(x, n):
    """Function required for the crypto-system"""
    return (x - 1) // n


def product_of_two_ciphertexts(cipher1, cipher2, mu, n, lambda_value):
    """Demonstrate a property of the paililier cryptosystem that allows two ciphertexts to be multiplied,
    returning the sum of the two plaintexts"""
    product_of_ciphertext = (cipher1 * cipher2) % (n * n)
    sum_message = decrypt(product_of_ciphertext, mu, n, lambda_value)
    return sum_message


def product_of_ciphertext_and_plaint(cipher, plain, g, n, mu, lambda_val):
    """Demonstrate a property of the paililier cryptosystem that allows a ciphertext to be multiplied by the
    value g, raised to another plaintext, returns the sum of the two plaintexts."""
    intermediate_encryption = (cipher * pow(g, plain)) % (n * n)
    return decrypt(intermediate_encryption, mu, n, lambda_val), intermediate_encryption


def homomorphic_multiplication(cipher, m2, n, mu, l_val):
    """Demonstrate a property of the paililier cryptosystem that allows a ciphertext to be raised by a constant m2,
        returns the value of the plain text multiplied by the constant m2"""
    intermediate_encryption = pow(cipher, m2) % (n * n)
    return decrypt(intermediate_encryption, mu, n, l_val), intermediate_encryption


def main():

    p = 17
    q = 19
    m = 14
    n = p * q
    "Generate keys"
    lambda_value = (p - 1) * (q - 1)
    g = n + 1
    mu = pow(lambda_value, -1, n)
    "Generate a ciphertext and corresponding decryption"
    ciphertext, r = encrypt(m, n, g)
    message = decrypt(ciphertext, mu, n, lambda_value)

    "Generate a second ciphertext"
    m1 = 44
    ciphertext2, r2 = encrypt(m1, n, g)
    message2 = decrypt(ciphertext2, mu, n, lambda_value)
    sum_message = product_of_two_ciphertexts(ciphertext, ciphertext2, mu, n, lambda_value)

    print(f"The prime numbers we are choosing for this demonstration are p = {p} and q = {q}.")
    print("==========================")
    print(f"Our computed g value is {g} and our chosen r value is {r}")
    print("==========================")
    print(f"Public key (n,g): {n, g}")
    print(f"Private key (lambda, mu): {lambda_value, mu}")
    print("==========================")
    print(f"Message: {m}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Decrypted ciphertext: {message}")
    print("==========================")
    print(f"We will now show homomorphic addition of plaintexts.\nOur second message is m2 = {m1}")
    print(f"It's ciphertext is : {ciphertext2} and it's r-value is {r2}")
    print(f"We multiplied the ciphertexts to get {ciphertext * ciphertext2}")
    print(f"We decrypt this value to get {sum_message}, which is the sum of the plaintexts {m} and {m1}\n")

    message3, plaintext_raise_g = product_of_ciphertext_and_plaint(ciphertext, m1, g, n, mu, lambda_value)
    constant_k = 10
    message4, cipher_raise_plain = homomorphic_multiplication(ciphertext, constant_k, n, mu, lambda_value)
    print(f"We will show the product of a ciphertext and a plaintext raising our chosen g value {g}")
    print(f"The product of a ciphertext and a plaintext raising g is {plaintext_raise_g} ")
    print(f"The result is {message3}, which equal to the sum of our first message {m} and our second message {m1}")
    print("==========================")
    print(f"Now we will display the homomorphic multiplication properties of this system.")
    print(f"We will raise our first ciphertext {ciphertext} to a constant {constant_k}")
    print(f"The value of cipher raised with the plaintext is:  {cipher_raise_plain}")
    print(f"The value we get is then {message4}, which is the product of the plaintext {m} and the constant {constant_k}.")


if __name__ == '__main__':
    main()
