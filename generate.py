from PIL import Image
import random
import math

class Generate():

    def gen_hor(img, y, sx, ex):

        if sx > ex:
            sx, ex = ex, sx

        for x in range(sx, ex):
            img.putpixel((x, y), (255, 255, 255))

    def gen_ver(img, x, sy, ey):
        for y in range(sy, ey):
            img.putpixel((x, y), (255, 255, 255))

    def generate(size):
        img = Image.new('RGB', [size] * 2)
        s_pos = random.randrange(size)
        e_pos = random.randrange(size)
        img.putpixel((s_pos, 0), (255, 255, 255))
        img.putpixel((s_pos, 1), (255, 255, 255))
        img.putpixel((e_pos, size-1), (255, 255, 255))
        img.putpixel((e_pos, size-2), (255, 255, 255))

        x = e_pos
        y = size - 2

        while y != 0:
            if random.random() > .5 or x in (1, size-2): #XCONN - Ensure not on border
                dist = random.randint(2, size-3)
                s_x = random.randint(min(x, abs(x-dist)), x) #BUG - Check not going into negative
                if s_x - dist > 0:
                    e_x = s_x - dist

                elif s_x + dist < size:
                    e_x = s_x + dist

                else:
                    continue

                Generate.gen_hor(img, y, s_x, e_x)
                x = e_x

            else:
                pass # TODO: YCONN


        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()