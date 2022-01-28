import hashlib


def hash_data(data: str) -> str:
  hashed = hashlib.sha512()
  hashed.update(data.encode('utf-8'))

  return hashed.hexdigest()
  