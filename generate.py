#!/usr/bin/env python3

from PIL import Image
import random
import math

class Generate():

    def gen_hor(img, y, sx, ex):

        if sx > ex:
            sx, ex = ex, sx

        for x in range(sx, ex+1):
            img.putpixel((x, y), (255, 255, 255))

    def gen_ver(img, x, sy, ey):

        if sy > ey:
            sy, ey = ey, sy

        for y in range(sy, ey+1):
            img.putpixel((x, y), (255, 255, 255))

    def allowed(conn):
        # NOTE: conn = ((sx, sy), (ex, ey))

        try:
            if conn[0][0] == conn[1][0]:
                if conn[0][0] in Generate.allowed_xs:
                    for x in (conn[0][0]-1, conn[0][0]+1):
                        try:
                            Generate.allowed_xs.remove(x)
                        except ValueError:
                            pass

                    return True

                else:
                    return False

            elif conn[0][1] == conn[1][1]:
                if conn[0][1] in Generate.allowed_ys:
                    for y in (conn[0][1]-1, conn[0][1]+1):
                        try:
                            Generate.allowed_ys.remove(y)
                        except ValueError:
                            pass

                    return True

                else:
                    return False

        except AttributeError:
            Generate.allowed_xs = [x for x in range(1, Generate.size) if not (math.isclose(x, Generate.s_pos, abs_tol=1) or math.isclose(x, Generate.e_pos, abs_tol=1))]
            Generate.allowed_ys = [y for y in range(1, Generate.size)]
            return Generate.allowed(conn)

    def generate(size):

        # BUG: Infinite loop - Very Very common

        Generate.size = size

        img = Image.new('RGB', [size] * 2)
        s_pos = random.randint(1, size-2)
        e_pos = random.randint(1, size-2)
        Generate.s_pos = s_pos
        Generate.e_pos = e_pos
        img.putpixel((s_pos, 0), (255, 255, 255))
        img.putpixel((s_pos, 1), (255, 255, 255))
        img.putpixel((e_pos, size-1), (255, 255, 255))
        img.putpixel((e_pos, size-2), (255, 255, 255))

        x = e_pos
        y = size - 2
        i = 0

        while y != 0:
            if i % 2 == 0 and x not in (1, size-2): #XCONN
                dist = random.randint(2, size)
                if x-dist > 0:
                    if Generate.allowed(((x, y), (x-dist, y))):
                        e_x = x - dist
                    else:
                        i += 1
                        continue

                elif x + dist < size - 1:
                    if Generate.allowed(((x, y), (x+dist, y))):
                        e_x = x + dist
                    else:
                        i += 1
                        continue

                else:
                    i += 1
                    continue

                Generate.gen_hor(img, y, x, e_x)
                x = e_x

            elif i % 2 != 0:
                dist = random.randint(2, size-y)
                if y - dist > 0:
                    if Generate.allowed(((x, y), (x, y-dist))):
                        e_y = y - dist

                    else:
                        i += 1
                        continue

                elif y - dist == 0: #Send to end
                    if s_pos != x:
                        if Generate.allowed(((x, y), (s_pos, y))):
                            Generate.gen_hor(img, y, x, s_pos)
                            x = s_pos

                        else:
                            mv_up = True
                            tmp = 0 #Remove later
                            while not Generate.allowed(((x, y), (s_pos, y))):
                                if tmp > 1.5 * size: #Due to the chance of not being allowed to get to s_pos anywhere on curr y-axis
                                    print("Sorry - Entered infinite loop. This will be fixed soon")
                                    print("Terminating now")
                                    quit()
                                if mv_up:
                                    if y == 1:
                                        mv_up = False
                                        tmp += 1
                                        continue
                                    y-=1

                                else:
                                    if y == size-2:
                                        pass #Do something else - If this occurs, no way of getting from pos to s_pos
                                             #Maybe try going 1 forward and re-doing this??
                                    y += 1

                                tmp += 1

                            Generate.gen_hor(img, y, x, s_pos)

                    Generate.gen_ver(img, x, y, 0)
                    break

                elif y + dist < size-1:
                    if Generate.allowed(((x, y), (x, y+dist))):
                        e_y = y + dist

                    else:
                        i += 1
                        continue

                else:
                    i += 1
                    continue

                Generate.gen_ver(img, x, y, e_y)
                y = e_y

            i += 1
            print(i)

        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()
