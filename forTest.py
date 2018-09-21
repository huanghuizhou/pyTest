a = ['aaa', 'bbb', 'ccc']
for index, x in enumerate(a):
    x = 'ddd'
    a[index] = x
    print(x)

print(a)
