import requests
import json
from PIL import Image, ImageTk
import sys
from tkinter import Tk, Canvas, Frame, BOTH, NW
import csv
from csv import writer

# запрос к api
id_film = "683999"
token1 = "3bea7fb9ddb477b2230bb054ca5596aa"
response = requests.get('https://cloud-api.kinopoisk.dev/movies/all/page/1/token/' + token1)
if response.status_code == 200:
    print("успешно")
# print(response.headers)
# print(response.text)

x = response.text
y = json.loads(x)

#взятие фильма из листа
movie = y["movies"][5]

# вывод данных
"""
print(y["id"])
print(y["title"])
print(y["title_alternative"])
print(y["year"])
print(y["genres"])
print(y["rating_kinopoisk"])
if y["frames"] == 'null':
    if y["screenshots"] != 'null':
        print(y["screenshots"])
    else:
        print('NO')
else:
    print(y["frames"])
"""

# сохранение (вывод) 1 скриншота
"""
try:
    resp = requests.get(url_screen1, stream=True).raw
except requests.exceptions.RequestException as e:
    sys.exit(1)

try:
    img = Image.open(resp)
except IOError:
    print("Unable to open image")
    sys.exit(1)
# img.show()
img.save('sid.jpg', 'jpeg')
"""

# создание csv (первой строки)
"""
data = ["id", "title rus", "title eng", "year", "genres", "poster", "rating", "frames", "d_colours0","d_colours1","d_colours2","d_colours3","d_colours4","d_colours5","d_colours6","d_colours7","d_colours8","d_colours9"]

with open("data_f.csv", mode="w", encoding='cp1251') as w_file:
    file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
    file_writer.writerow(data)
"""

# проверка на наличие кадров
index1 = 0
if movie["frames"] is None:
    if movie["screenshots"] is None:
        index1 = 1   #нет кадров
    else:
        movie["frames"] = movie["screenshots"]
        # ограничение кадров до 10
        if len(movie["frames"]) > 10:
            del movie["frames"][10:len(movie["frames"])]

# проверка на жанры
index2 = 0
index3 = 0
for i in range(len(movie["genres"])):
    if movie["genres"][i] == 'Концерт' or movie["genres"][i] == 'Документальный':
        index2 = 1
    if movie["genres"][i] == 'Мультфильм':
        index3 = 1

# взятие палитры
if index1 == 0 and index2 == 0:
    d_colours = ['', '', '', '', '', '', '', '', '', '']
    framesNumber = len(movie["frames"])
    for i in range(framesNumber):
        url_screen1 = movie["frames"][i]
        url = "https://color-extractor-for-apparel-2.p.rapidapi.com/colors"
        url_screen = url_screen1

        querystring = {"image_url": url_screen}
        headers = {
            'x-rapidapi-host': "color-extractor-for-apparel-2.p.rapidapi.com",
            'x-rapidapi-key': "dc66b3f673msh9bfdaf8590f930ep18c4ccjsnd1ad3e7b46e0"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        x1 = response.text
        y1 = json.loads(x1)
        d_colours[i] = y1["dominant-colors"]

# запись в csv
if index2 == 1:   #"плохой" жанр
    print("жанр не подходит")
else:
    if index1 == 1:   #нет кадров
        print("картинок нет")
    else:
        list_data = [movie["id"], movie["title"], movie["title_alternative"], movie["year"], movie["genres"],
                     'https:' + movie["poster"],
                     movie["rating_kinopoisk"], movie["frames"], d_colours[0], d_colours[1], d_colours[2],
                     d_colours[3], d_colours[4],
                     d_colours[5], d_colours[6], d_colours[7], d_colours[8], d_colours[9]]
        if index3 == 1:   #если мультфильм
            with open('data_mf.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(list_data)
                f_object.close()
        else:
            with open('data_f.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(list_data)
                f_object.close()

#цвета
"""
colours = y1["dominant-colors"]
# colours = {'value': [34, 40, 40], 'weight': 0.792}, {'value': [108, 104, 95], 'weight': 0.1379}, {'value': [158, 152, 135], 'weight': 0.0672}, {'value': [130, 140, 128], 'weight': 0.0026}, {'value': [122, 131, 132], 'weight': 0.0003} #пример
rgb1 = colours[0]['value']
rgb2 = colours[1]['value']
rgb3 = colours[2]['value']
rgb4 = colours[3]['value']
rgb5 = colours[4]['value']

# RBG в HEX
hex1 = '%02x%02x%02x' % (rgb1[0], rgb1[1], rgb1[2])
hex2 = '%02x%02x%02x' % (rgb2[0], rgb2[1], rgb2[2])
hex3 = '%02x%02x%02x' % (rgb3[0], rgb3[1], rgb3[2])
hex4 = '%02x%02x%02x' % (rgb4[0], rgb4[1], rgb4[2])
hex5 = '%02x%02x%02x' % (rgb5[0], rgb5[1], rgb5[2])
"""
# вывод квадратов
"""
class Example(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Palette")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_rectangle(
            30, 10, 120, 80,
            outline="#000000", fill="#" + hex1
        )

        canvas.create_rectangle(
            150, 10, 240, 80,
            outline="#000000", fill="#" + hex2
        )

        canvas.create_rectangle(
            270, 10, 360, 80,
            outline="#000000", fill="#" + hex3
        )

        canvas.create_rectangle(
            390, 10, 480, 80,
            outline="#000000", fill="#" + hex4
        )

        canvas.create_rectangle(
            510, 10, 600, 80,
            outline="#000000", fill="#" + hex5
        )

        self.img = Image.open("sid.jpg")
        self.sid = ImageTk.PhotoImage(self.img)
        canvas.create_image(30, 100, anchor=NW, image=self.sid)

        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    ex = Example()
    root.geometry("700x700+1000+100")
    root.mainloop()


if __name__ == '__main__':
    main()
"""

