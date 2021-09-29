import re


a = '\n\t\t\t\tNo van a parar hasta machacarme,\nhasta hundirme\n\t\t\t'
finala  = re.sub(r'\n', '', a)
print("//", finala)
finala = re.sub(r'\t', '', finala)
print("//", finala)


