import random

def z(v):
    for m in v:
        if m == v[-1]:
            v = v[0:-1]

gen = input("Введите пол (муж/жен)")
name = input("Введите имя")

glasn = set("ёуеыаоэяию")
woman = ["ь", "а", "ия"]
man = ["им", "ий", "иль", "ей"]
a = random.randint(0, 2)
b = random.randint(0, 3)

for i in glasn:
    if i == name[-1]:
        name = name[0:-1]
        z(name)

if gen == "муж":
    print(name + man[a])
else:
    print(name + woman[b])