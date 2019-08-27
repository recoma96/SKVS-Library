from SkvsClient.SkvsConnection import *
from time import *
a = SkvsConnection("user", "12345678", "127.0.0.1", 8000)

while True:
    a.open()
    a.close()