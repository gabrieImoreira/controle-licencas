import re

email = "y@teste.com.br"
if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    print("invalid email")
else:
    print("valid email")
