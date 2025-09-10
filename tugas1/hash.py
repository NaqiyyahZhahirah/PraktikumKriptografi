import hashlib
import hmac

filename = "fasilitas-mahasiswa-4.png"
key = b"kripto25"

with open(filename, "rb") as f:
    data = f.read()

print("MD5          :", hashlib.md5(data).hexdigest())
print("SHA1         :", hashlib.sha1(data).hexdigest())
print("HMAC-SHA256  :", hmac.new(key, data, hashlib.sha256).hexdigest())
