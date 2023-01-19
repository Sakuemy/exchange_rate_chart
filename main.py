import os, xmltodict, codecs, csv, math
import xml.etree.cElementTree as ET
from datetime import datetime
from progress.bar import IncrementalBar
from tkinter import *

outData = []
maxRate = 0
bar = IncrementalBar('Progress', max = len(os.listdir("files")))
for filename in os.listdir("files"):
    f = codecs.open(os.path.join("files", filename), 'r', 'utf_8_sig')
    root = xmltodict.parse(f.read())
    f.close()
    items = root['DailyExRates']
    date = datetime.strptime(items['@Date'], "%m/%d/%Y")
    for i in items['Currency']:
        if i['CharCode'] == 'USD':
            if date > datetime.strptime("06/30/2016", "%m/%d/%Y"):
                outData.append(list([date, str(round(float(i['Rate']) * 10000000))]))
            else:
                if date > datetime.strptime("12/31/1999", "%m/%d/%Y"):
                    outData.append(list([date, str(round(float(i['Rate']) * 1000))]))
                else:
                    outData.append(list([date, str(round(float(i['Rate'])))]))
    bar.next()

print("\nНачата сортировка")
outData.sort(key = lambda x: x[0])
print("Сортировка завершена")

outPrint = [["Курс USD", ""],["Date", "Rate"]] + outData

print('Запись в файл out.csv')
out = open('out.csv', 'w', newline='')
with out:
    writer = csv.writer(out, delimiter=";")
    writer.writerows(outPrint)
print("Запись в файл завершена")

for i in outData:
    if maxRate < int(i[1]):
        maxRate = int(i[1])

w = 900
h = 500

g = len(outData) / (w)
k = maxRate / (h - 100)
root = Tk()
c = Canvas(root, width=w + 50, height=h + 30, bg='white')
c.pack()

c.create_line(50, h - 30, 50, 0)
c.create_line(50, h - 30, w + 50, h - 30)

for i in range(20):
    c.create_line(47, (h - 30) - i * 30, 54, (h - 30) - i * 30)

for i in range(40):
    c.create_line(50 + (i * 30), h - 33, 50 + (i * 30), h - 26)

x = 50
u = 0
s = 0
ss = 0

for i in outData:
    if u < g:
        s = s + int(i[1])
        u = u + 1
    else:
        u = 0
        s = round(s / g / k)
        c.create_line(x, h - ss - 30, x + 1, h - s - 30, fill='red')
        if (x - 50) % 30 == 0:
            c.create_text(x, h - 10, text=str(i[0].day) + '\n' + str(i[0].month)\
            + '\n' + str(i[0].year), justify=CENTER,  font="Verdana 5")
            c.create_text(x + 20, h - s - 25, text=i[1], justify=CENTER,  font="Verdana 5")
        ss = s
        s = 0
        x = x + 1
c.create_text(x + 20, h - ss - 27, text=str(i[0].day) + '.' + str(i[0].month)\
    + '.' + str(i[0].year), justify=LEFT, font="Verdana 5", fill='red')
c.create_text(x + 20, h - ss - 35, text=i[1], justify=LEFT, font="Verdana 5", fill='red')
c.create_line(x, h - ss - 30, x, h - 30, fill='blue')
c.create_line(x, h - ss - 30, 50, h - ss - 30, fill='blue')
            
root.mainloop()











