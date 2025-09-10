###
# Nama Program : hillcipher.py
# Nama         : Naqiyyah Zhahirah
# NPM          : 140810230039
# Deskripsi    : Program enkripsi, dekripsi, dan mencari kunci hill cipher
###

from math import gcd

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def text_to_nums(text):
    return [char_to_num(c) for c in text if c.isalpha()]

def nums_to_text(nums):
    return "".join(num_to_char(n) for n in nums)

def mat_mult(A, B, mod=26):
    n = len(A)
    m = len(B[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
            result[i][j] %= mod
    return result

def mat_det2(A):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % 26

def mat_adj2(A):
    return [[ A[1][1], -A[0][1]],
            [-A[1][0],  A[0][0]]]

def mod_inv(a, m=26):
    for x in range(1, m):
        if (a*x) % m == 1:
            return x
    return None

def mat_inv2(A, mod=26):
    det = mat_det2(A)
    det_inv = mod_inv(det, mod)
    if det_inv is None or gcd(det, 26) != 1:
        return None
    adj = mat_adj2(A)
    return [[(det_inv * adj[i][j]) % mod for j in range(2)] for i in range(2)]

def encrypt(plaintext, key):
    n = len(key)
    pt_nums = text_to_nums(plaintext)

    # padding kalau tidak habis
    while len(pt_nums) % n != 0:
        pt_nums.append(char_to_num('X'))

    ciphertext = []
    for i in range(0, len(pt_nums), n):
        block = [[x] for x in pt_nums[i:i+n]]
        cblock = mat_mult(key, block)
        ciphertext.extend([row[0] for row in cblock])
    return nums_to_text(ciphertext)

def decrypt(ciphertext, key):
    key_inv = mat_inv2(key)
    if key_inv is None:
        print("Kunci tidak valid untuk dekripsi")
        return None

    n = len(key)
    ct_nums = text_to_nums(ciphertext)
    plaintext = []
    for i in range(0, len(ct_nums), n):
        block = [[x] for x in ct_nums[i:i+n]]
        pblock = mat_mult(key_inv, block)
        plaintext.extend([row[0] for row in pblock])
    return nums_to_text(plaintext)

def find_key(plaintext, ciphertext, n):
    pt_nums = text_to_nums(plaintext)
    ct_nums = text_to_nums(ciphertext)

    # butuh minimal n*n huruf
    if len(pt_nums) < n*n or len(ct_nums) < n*n:
        print("Panjang plaintext/ciphertext kurang untuk cari kunci")
        return None

    # ambil n blok pertama
    P = [[pt_nums[i*n+j] for i in range(n)] for j in range(n)]
    C = [[ct_nums[i*n+j] for i in range(n)] for j in range(n)]

    P_inv = mat_inv2(P)
    if P_inv is None:
        print("Matriks plaintext tidak bisa diinvers")
        return None

    key = mat_mult(C, P_inv)
    return key

if __name__ == "__main__":
    # contoh kunci 2x2 (valid)
    key = [[7, 6],
           [2, 5]]

    plaintext = "PYTHON"
    print("Plaintext :", plaintext)

    # Enkripsi
    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)

    # Dekripsi
    decrypted = decrypt(ciphertext, key)
    print("Dekripsi  :", decrypted)

    # Cari kunci dari pasangan plaintext dan ciphertext
    P = "HELP"
    C = encrypt(P, key)
    found_key = find_key(P, C, 2)
    print("Kunci asli   :", key)
    print("Kunci ketemu :", found_key)
