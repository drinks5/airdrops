# encoding: utf-8

a = list(range(21))
length = len(a)
count = 0
print(a[::5])
for x in a[::5]:
    for i in range(int(length / 5)):
        index = a.index(x) + i
        if index < length:
            print(a[index])
