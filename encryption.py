import hashlib

class Encryption:
    def convert(self,data):
        data = hashlib.md5(data.encode())
        data = data.hexdigest()
        return data