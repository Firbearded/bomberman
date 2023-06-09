from os.path import exists, join, splitext
from xml.etree import ElementTree

import pygame
from PIL import Image

from src.game.supporting.constants import Path

TEXTURE_FILENAMES = Path.TEXTURES
TEXTURE_DIR = Path.TEXTURES_DIR

SOUND_DIR = Path.SOUNDS_DIR
SOUND_FILENAMES = Path.SOUNDS

textures_len = 0
for k in TEXTURE_FILENAMES:
    textures_len += 1
sound_len = 0
for k in SOUND_FILENAMES.values():
    for j in k:
        sound_len += 1
TOTAL_NUMBER = textures_len + sound_len


def load_textures(game_object, directory=TEXTURE_DIR, filenames=TEXTURE_FILENAMES):
    """ Загрузка текстур """
    result = {}
    for filename in filenames:
        filename = filename.value
        game_object.loading.set_stage("textures '{}'".format(filename))

        data_filename = join(directory, filename + Path.TEXTURES_EXTENSION_LIST)
        png_filename = join(directory, filename + Path.TEXTURES_EXTENSION_PIC)

        flag = False
        for f in (data_filename, png_filename):
            if not exists(data_filename):
                print("TEXTURE LOADING: NOT EXISTS '{}'!".format(f))
                flag = True
        if flag: continue

        result[filename] = {}

        big_image = Image.open(png_filename)
        frames = frames_from_data(data_filename)

        for name, frame in frames:
            box = frame['box']
            rect_on_big = big_image.crop(box)
            real_sizelist = frame['real_sizelist']
            result_image = Image.new('RGBA', real_sizelist, (0, 0, 0, 0))
            result_box = frame['result_box']
            result_image.paste(rect_on_big, result_box, mask=0)
            if frame['rotated']:
                result_image = result_image.transpose(Image.ROTATE_90)

            mode = result_image.mode
            size = result_image.size
            data = result_image.tobytes()
            name = splitext(name)[0]

            result[filename][name] = pygame.image.fromstring(data, size, mode)

            print("TEXTURE LOADING: from '{}' loaded '{}' ".format(png_filename, name))

        game_object.loading.next()

    return result


def tree_to_dict(tree):  # Вспомогательные
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index + 1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index + 1].tag == 'integer':
                d[item.text] = int(tree[index + 1].text)
            elif tree[index + 1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index + 1])
    return d


def frames_from_data(data_filename):  # Вспомогательные
    root = ElementTree.fromstring(open(data_filename, 'r').read())
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{', '').replace('}', '').split(',')
    frames = plist_dict['frames'].items()
    for k, v in frames:
        frame = v
        if plist_dict["metadata"]["format"] == 3:
            frame['frame'] = frame['textureRect']
            frame['rotated'] = frame['textureRotated']
            frame['sourceSize'] = frame['spriteSourceSize']
            frame['offset'] = frame['spriteOffset']

        rectlist = to_list(frame['frame'])
        width = int(rectlist[3] if frame['rotated'] else rectlist[2])
        height = int(rectlist[2] if frame['rotated'] else rectlist[3])
        frame['box'] = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height
        )
        real_rectlist = to_list(frame['sourceSize'])
        real_width = int(real_rectlist[1] if frame['rotated'] else real_rectlist[0])
        real_height = int(real_rectlist[0] if frame['rotated'] else real_rectlist[1])
        real_sizelist = [real_width, real_height]
        frame['real_sizelist'] = real_sizelist
        offsetlist = to_list(frame['offset'])
        offset_x = int(offsetlist[1] if frame['rotated'] else offsetlist[0])
        offset_y = int(offsetlist[0] if frame['rotated'] else offsetlist[1])

        if frame['rotated']:
            frame['result_box'] = (
                int((real_sizelist[0] - width) / 2 + offset_x),
                int((real_sizelist[1] - height) / 2 + offset_y),
                int((real_sizelist[0] + width) / 2 + offset_x),
                int((real_sizelist[1] + height) / 2 + offset_y)
            )
        else:
            frame['result_box'] = (
                int((real_sizelist[0] - width) / 2 + offset_x),
                int((real_sizelist[1] - height) / 2 - offset_y),
                int((real_sizelist[0] + width) / 2 + offset_x),
                int((real_sizelist[1] + height) / 2 - offset_y)
            )
    return frames


def load_sounds(game_object, ):
    """ Загрузка звуков """
    result = {}
    ex = Path.SOUNDS_EXTENSION

    for dir2 in SOUND_FILENAMES:
        for filename in SOUND_FILENAMES[dir2]:
            filename = filename.value
            game_object.loading.set_stage("sounds '{}'".format(filename))

            path = join(dir2, filename + ex)

            sound = pygame.mixer.Sound(path)
            # sounds[splitext(filename)[0]] = sound
            result[splitext(filename)[0]] = sound
            print("SOUND LOADING: from '{}' loaded '{}'".format(path, sound))
            game_object.loading.next()

    return result
