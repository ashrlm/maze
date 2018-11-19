from PIL import Image
import random

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
                if conn[0][0] in Generate.allowed_ys:
                    for x in range(conn[0][1]-1, conn[0][1]+2):
                        try:
                            Generate.allowed_xs.remove(x)
                        except ValueError:
                            pass
                    return True

            elif conn[0][1] == conn[1][1]:
                if conn[0][1] in Generate.allowed_xs:
                    for y in range(conn[0][1]-1, conn[0][1]+2):
                        try:
                            Generate.allowed_ys.remove(y)
                        except ValueError:
                            pass
                    return True

        except AttributeError:
            Generate.allowed_xs = [x for x in range(1, Generate.size)]
            Generate.allowed_ys = [y for y in range(1, Generate.size)]
            return Generate.allowed(conn)

    def generate(size):

        # BUG: Potential for infinite loops
        # BUG: Disallowed connections existing - AFAIK all vertical
        # BUG: Connection jumping
        # BUG: Multiple (>2) nodes where y in (0, size-1) - Likely linked to above

        Generate.size = size

        img = Image.new('RGB', [size] * 2)
        s_pos = random.randint(1, size-2)
        e_pos = random.randint(1, size-2)
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

                elif x + dist < size - 1:
                    if Generate.allowed(((x, y), (x+dist, y))):
                        e_x = x + dist

                else:
                    i += 1
                    continue

                Generate.gen_hor(img, y, x, e_x)
                x = e_x

            elif i % 2 != 0:
                dist = random.randint(2, size-y)
                if y - dist > 0:
                    if Generate.allowed(((x, y), (x, y-dist))):
                        e_y = y-dist

                    else:
                        continue

                elif y - dist == 0: #Send to end:
                    if s_pos != x:
                        if Generate.allowed(((x, y), (s_pos, y))):
                            Generate.gen_hor(img, y, x, s_pos)
                            x = s_pos

                        else:
                            mv_up = True
                            tmp = 0 #Remove later
                            while not Generate.allowed(((x, y), (s_pos, y))):
                                if tmp > 100: #Due to the chance of not being allowed to get to s_pos anywhere on curr y-axis
                                    print("Sorry - Entered infinite loop. This will be fixed soon")
                                    print("Terminating now")
                                    quit(

                                    )
                                if mv_up:
                                    if y == 1:
                                        mv_up = False
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
                        continue

                else:
                    continue

                Generate.gen_ver(img, x, y, e_y) #BUG: e_y sometimes undefined - Due to
                y = e_y

            i += 1

        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()