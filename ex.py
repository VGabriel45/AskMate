import random


def find_pair(lst, n):
    for number in lst:
        for j in range(len(lst)-1):
            result = 0
            result += number + lst[j]
            if result == n:
                return f'{number} and {lst[j]}'
    return 'No valid pairs'


def generate_list():
    my_lsit = []
    for x in range(3):
        my_lsit.append(x)
    random.shuffle(my_lsit)
    return my_lsit


lst = generate_list()

print(find_pair([2,2], 0))
