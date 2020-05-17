from opensimplex import OpenSimplex
import math
import random
from direct.showbase.Loader import Loader
from panda3d.core import PNMImage


def generate(size, freq, height, terrace, filters):
    hmap = []
    for s in range(size):
        hmap.append([])
        for _ in range(size):
            hmap[s].append(None)

    tmp = OpenSimplex(random.randint(1, 100))
    percent = 0
    for i in range(size):
        for j in range(size):
            hmap[i][j] = tmp.noise2d(x=i/freq, y=j/freq)
            for f in range(filters):
                fac = math.pow(2, f+1)
                hmap[i][j] += abs(tmp.noise2d(x=i/(freq/fac), y=j/(freq/fac))/fac)
            hmap[i][j] *= height
            hmap[i][j] -= hmap[i][j]%terrace #TERRACING, UNCOMMENT FOR COOL EFFECT
            if int((i*size+j)/(size*size)*100) > percent:
                percent = int((i*size+j)/(size*size)*100)
                print("Calculating... " + str(percent) + "%")
    
    stuff = []
    tex_coordsone = (0,0, 1,0, 0,1)
    tex_coordstwo = (1,1, 1,0, 0,1)
    percent = 0
    for i in range(size - 1):
        for j in range(size - 1):
            vertsOne = (i,hmap[i][j],j, (i+1),hmap[i+1][j],j, i,hmap[i][j+1],(j+1))
            vertsTwo = ((i),hmap[i][j+1],j+1, i+1,hmap[i+1][j],(j), (i+1),hmap[i+1][j+1],(j+1))
            #Deciding which texture to use
            avgheight = (vertsOne[4]+vertsOne[7])/2
            plane = equation_plane(*vertsOne)
            norms = (-plane[0], -plane[1], -plane[2], -plane[0], -plane[1], -plane[2], -plane[0], -plane[1], -plane[2])
            xz = math.sqrt(plane[0]*plane[0]+plane[2]*plane[2]) #xz component of normal vector to plane
            if abs(xz) > 1 and avgheight > 10:
                tex = 0
            elif abs(xz) > 1 and avgheight <= 10:
                tex = 4
            elif avgheight <= 1:
                tex = 7
            elif avgheight >= 10:
                tex = 6
            else:
                tex = 2
            stuff.append([vertsOne, norms, tex_coordsone, tex])
            avgheight = (vertsTwo[1]+vertsTwo[4])/2
            plane = equation_plane(*vertsTwo)
            norms = (plane[0], plane[1], plane[2], plane[0], plane[1], plane[2], plane[0], plane[1], plane[2])
            xz = math.sqrt(plane[0]*plane[0]+plane[2]*plane[2])
            if abs(xz) > 1 and avgheight > 10:
                tex = 1
            elif abs(xz) > 1 and avgheight <= 10:
                tex = 5
            elif avgheight <= 1:
                tex = 8
            elif avgheight >= 10:
                tex = 6
            else:
                tex = 3
            stuff.append([vertsTwo, norms, tex_coordstwo, tex])
            if int((i*size+j)/(size*size)*100) > percent:
                percent = int((i*size+j)/(size*size)*100)
                print("Rendering... " + str(percent) + "%")
    
    return stuff

def equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):  
    a1 = x2 - x1 
    b1 = y2 - y1 
    c1 = z2 - z1 
    a2 = x3 - x1 
    b2 = y3 - y1 
    c2 = z3 - z1 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x1 - b * y1 - c * z1) 
    return (a, b, c, d)
    #Equation of plane is ax + by + cz + d= 0.