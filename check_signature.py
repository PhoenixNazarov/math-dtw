import json
import math
import os

from dtw import dtw


d = lambda x, y: (x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2

a = []
b = []

with open('data/signature_coord/true/8.json', 'r') as file:
    my_signature = json.loads(file.read())

print('Other :')
for i in os.listdir('data/signature_coord/false/'):
    with open('data/signature_coord/false/' + i, 'r') as file:
        check = json.loads(file.read())
    _dtw = dtw(my_signature, check, d=d)
    print(i, _dtw)
    a.append(_dtw)

print()

print('Signs :')
for i in os.listdir('data/signature_coord/true/'):
    with open('data/signature_coord/true/' + i, 'r') as file:
        my_signature2 = json.loads(file.read())
    if my_signature2 == my_signature:
        continue

    _dtw = dtw(my_signature, my_signature2, d=d)
    b.append(_dtw)
    print(i, _dtw)
print()

print('Avg:')
print('fake', sum(a) / len(a))
print('valid', sum(b) / len(b))
print('Correct', sum(a) / len(a) / (sum(b) / len(b)))
