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
                dist = random.randint(min(x, abs(x-dist)), x)
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
                
                elif y - dist == 0: #Send to end:
                    pass #TODO: Find way to send to end without risk of jumping due to not allowed
                         #TODO: Make sure still checking allowed
                
                elif y + dist < size-1:
                    if Generate.allowed(((x, y), (x, y+dist))):
                        e_y = y + dist
                
                else:
                    i += 1
                    continue
                
                Generate.gen_ver(img, x, y, e_y)
                y = s_y
            
            i += 1
        
        
        img.save('imgs/' + str(size) * 2 + '.png')
        img.show()