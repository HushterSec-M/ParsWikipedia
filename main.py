import json, requests
from bs4 import BeautifulSoup

def getNames():
    with open('russian_names.json', 'rt', encoding='utf-8-sig') as fh:
        data = json.load(fh)
    names = [i['Name'] for i in data]
    return names

def get_html(url):
    r = requests.get(url).text
    return r

def parse(name):
    url = 'https://ru.wikipedia.org/wiki/' + name
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', class_="infobox")
    key = table.find_all("th")
    value = table.find_all("td")
    dict = {}
    lkey, lval = len(key), len(value)
    # print(lkey, lval)
    for i in range(min(len(key), len(value))):
        try:
            if lkey == lval:
                dict[key[i].getText()] = value[i].getText()
            elif lkey > lval:
                dict[key[i].getText()] = value[i - (lkey - lval)].getText()
            elif lkey < lval:
                dict[key[i].getText()] = value[i + (lkey - lval)].getText()
        except:
            break
    dict = dict["Производ. формы"]
    dict = dict.replace("\n", "").replace("[", '').replace("]", '').replace("(", '').replace(")", '').replace(" ",
                                                                                                              '').replace(
        ".", '')
    for i in range(100):
        dict = dict.replace(str(i), '')
    dict = dict.split(",")
    dict.append(key[0].getText())
    return dict

import time
start_time = time.time()


names = getNames()
tname = "tname.json"
fname = "fname.json"


print("Wikipedia:")
i = 0
j = len(names)
ALL = int(j)
print(f"All names: {j}")
oneper = int(j/100)
print(f"1% names: {oneper}")

with open(fname, "w", encoding='utf-8-sig') as f:
    f.write("")
result = {}
print(f"{100}%")
for name in names:
    i+=1
    if (i % oneper == 0):
        print(f"{i}: {int(((j-oneper) * 100)/ALL)}%")
        j-=oneper
        print("--- %s seconds ---" % (time.time() - start_time))
    try:
        rName = []
        rName += parse(name)
        rName.append(name)
        result[name.lower()] = ", ".join(rName).lower()
    except:
        with open(fname, "a", encoding='utf-8-sig') as f:
            f.write(f"{name}\n")
with open(tname, "w", encoding='utf-8-sig') as f:
    f.write(str(result).replace("'", '"'))

print(f"DONE: [{i}:{int(((j-oneper) * 100)/ALL)}%]")






import winsound
print("--- TOTAL: %s seconds ---" % (time.time() - start_time))
duration = 500  # millisecond
freq = 500  # Hz
winsound.Beep(freq, duration)
