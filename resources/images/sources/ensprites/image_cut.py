from PIL import Image

img = Image.open("all.png")
img.load()

x_count, y_count = 14, 5

w, h = 16, 16
dx, dy = 14, 14

index = 0
for j in range(y_count):
    for i in range(x_count):
        img.crop(((dx+w) * i, (dy+h) * j, (dx+w) * i + w, (dy+h) * j + h)).save("{}.png".format(index))
        index += 1
