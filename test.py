from passlib.hash import bcrypt
from getpass import getpass



hasher = bcrypt.using(rounds=13)  # Make it slower

password = getpass()
hashed_password = hasher.hash(password)
print(hashed_password)
# $2b$13$H9.qdcodBFCYOWDVMrjx/uT.fbKzYloMYD7Hj2ItDmEOnX5lw.BX.
# \__/\/ \____________________/\_____________________________/
# Alg Rounds  Salt (22 char)            Hash (31 char)

print(hasher.verify(password, hashed_password))
# True
print(hasher.verify("not-the-password", hashed_password))
# False