from PIL import Image
import random
import math

class Generate():

    def check_close(a, lst, abs_tol):

        for i in lst:
            if math.isclose(a, i, abs_tol=abs_tol):
                return True

        return False

    def gen_hor(size, ys, img):

        y = random.randint(1, size-2)

        while Generate.check_close(y, ys, 1):
            y=random.randint(1, size-2)

        hor_s_x = random.randint(1, size-3)
        hor_e_x = random.randint(1+hor_s_x, size-2)

        for x in range(hor_s_x, hor_e_x):
            img.putpixel((x, y), (255, 255, 255))

        return y

    def gen_vert(size, xs, img):
        pass

    def generate(size):
        img = Image.new('RGB', [size] * 2)
        s_pos = random.randrange(size)
        e_pos = random.randrange(size)
        img.putpixel((s_pos, 0), (255, 255, 255))
        img.putpixel((s_pos, 1), (255, 255, 255))
        img.putpixel((e_pos, size-1), (255, 255, 255))
        img.putpixel((e_pos, size-2), (255, 255, 255))

        xs = []
        ys = []
        curr_y = size - 2 #-2 to ensure one up
        while curr_y != 0: #generate conns
            if random.random() > .5:
                ys.append(Generate.gen_hor(size, ys, img))

            else:
                xs.append(Generate.gen_vert(size, xs, img))

        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()