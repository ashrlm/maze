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

        if sy > ey:
            sy, ey = ey, sy

        for y in range(sy, ey):
            img.putpixel((x, y), (255, 255, 255))

    def generate(size):

        # TODO: Ensure that connections overlap but are not adjacent
        #
        # Store list of connections as [[(s_x, s_y), (e_x, e_y)]]
        # When checking, loop over connections, and disallow if:
        # (math.isclose(s_x, e_x, abs_tol=1) and s_x != e_x) or (math.isclose(s_y, e_y, abs_tol=1) and s_y != e_y)

        img = Image.new('RGB', [size] * 2)
        s_pos = random.randrange(size)
        e_pos = random.randrange(size)
        img.putpixel((s_pos, 0), (255, 255, 255))
        img.putpixel((s_pos, 1), (255, 255, 255))
        img.putpixel((e_pos, size-1), (255, 255, 255))
        img.putpixel((e_pos, size-2), (255, 255, 255))

        x = e_pos
        y = size - 2
        i = 0

        while y != 0:
            if i % 2 == 0 and x not in (1, size-2): #XCONN - Ensure not on border
                dist = random.randint(2, size-3)
                x = random.randint(min(x, abs(x-dist)), x)
                if x - dist > 0:
                    e_x = x - dist

                elif x + dist < size:
                    e_x = x + dist

                else:
                    continue

                Generate.gen_hor(img, y, x, e_x)
                x = e_x

            elif i % 2 != 0:
                dist = random.randint(2, size-y)
                if y - dist > 0:
                    e_y = y - dist

                elif y - dist == 0: #Send to end
                    if s_pos != x:
                        Generate.gen_ver(img, x, y, y-dist+1) #Move nearly to top
                        y = 1 #Ensure at top
                        Generate.gen_hor(img, y, x, s_pos)

                    else:
                        Generate.gen_ver(img, x, y, y+dist)

                    break

                elif y + dist < size-1:
                    e_y = y + dist

                else:
                    i+=1
                    continue

                Generate.gen_ver(img, x, y, e_y)
                y = e_y

            i += 1

        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()