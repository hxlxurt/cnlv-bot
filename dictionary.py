d = {}

with open('dictionary.txt', 'r', encoding='UTF-8') as file:
    for line in file:
        key, value = line.strip().split('=')
        d[key] = value