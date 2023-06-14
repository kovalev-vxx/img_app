from images.models import Photo, Color, Keyword, Tone
import pandas as pd
import csv
import webcolors
import numpy as np
import requests
from colorthief import ColorThief
from io import BytesIO

tones = {
    "white": [255,255,255],
    "black": [0,0,0],
    "red": [255, 0,0],
    "green": [0,255,0],
    "blue": [0,0,255],
    "cyan": [0,255,255],
    "magenta": [255,0,255],
    "yellow": [255,255,0]
}

## Сделать таблицу ТОНА, где будут поля цветов выше и каждое фото как ключ. В полях цветов будет расстояние до этого цвета.
## Изначальный цвет фото взял из ColorThief
##потом при запросе какого либо тона сортировать по этому полю (расстоянию)
def get_tone(color):
    min_distance = None
    min_color = ""
    for tone in tones.items():
        # dis = np.sum(np.sqrt(np.array(color)-np.array(tone[1])))
        dis = np.linalg.norm(np.array(color)-np.array(tone[1]))
        if min_distance is None or dis < min_distance:
            min_distance=dis
            min_color = tone[0]
    return min_color

def rgb_to_hex(color):
  return ('{:X}{:X}{:X}').format(*color)

def run():
    photos = Photo.objects.all().exclude(photo_id__in=Tone.objects.all().values_list("pk"))
    n = 1
    for photo in photos:
        try:
            info = {}
            response = requests.get(photo.photo_image_url+"?w=100")
            color_thief = ColorThief(BytesIO(response.content))
            dominant_color = color_thief.get_color(quality=1)
            for tone in tones.items():
                dominant_color = np.array(dominant_color)
                t = np.array(tone[1])
                dis = np.linalg.norm(dominant_color - t)
                dis = (510 - dis) / 510
                info[tone[0]] = dis
            info["hex"] = rgb_to_hex(dominant_color)
            new_tone = Tone(white=info["white"],
                            black=info["black"],
                            red=info["red"],
                            green=info["green"],
                            blue=info["blue"],
                            cyan=info["cyan"],
                            magenta=info["magenta"],
                            yellow=info["yellow"],
                            hex=info["hex"],
                            photo=photo)
            new_tone.save()
            print(f"{n} из {len(photos)}")
            n+=1
        except:
            continue


# def run():
    # pass
    # keywords = Keyword.objects.all().values_list("keyword", flat=True)[:5]
    # print(keywords)
    # keywords = ["car"]
    # colors = ["cadetblue"]
    # print(Photo.objects.filter(keywords__keyword__iregex=(r'\b' + "car" + r"\b")).values_list("keywords__keyword"))
    # print(Photo.objects.filter(colors__color__in=["cadetblue"]))
    # df = pd.read_csv("scripts/colors.csv")
    # photo = Photo.objects.all().values_list()[0]
    # print(len(Keyword.objects.filter(photos__in=photo)))
    # keywords = list(set(df["keyword"].to_list()))
    # t = 1
    # for keyword in keywords:
    #     photo_ids = df["photo_id"][df["keyword"] == keyword].to_list()
    #     k = Color(color=keyword)
    #     k.save()
    #     for id in photo_ids:
    #         k.photos.add(Photo.objects.get(pk=id))
    #     print(f"{t} из {len(keywords)}")
    #     t += 1
