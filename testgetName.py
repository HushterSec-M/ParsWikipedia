import json

with open('tname.json', 'r', encoding='utf-8-sig') as fh:
    data = json.load(fh)

res = data.keys()
print(", ". join(res))
print(len(res))
name = "артём"
for i in data:
    if (i == name) or (name in data[i].split(", ")):
        print(i)
        print(data[i])