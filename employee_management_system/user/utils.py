import hashlib

def getMd5Hash(string):
    md5_hash = hashlib.md5(string.encode()).hexdigest()
    return md5_hash