#!/usr/bin/python3
import sys
import oiffile
import glob
from PIL import Image
import numpy as np
import os
import itertools

def Red_Green(img, fileprename, Green, Gray, i, ii, threshold):
    Red_Green = Image.new(mode = "RGB", size = (img.size[0], img.size[1]))
    Red_Green_pixels = Red_Green.load()
    if Green:
        for X in range(img.size[0]):
            for Y in range(img.size[1]):
                if img.getpixel((X,Y)) > threshold:
                    Red_Green_pixels[X,Y] = (0, img.getpixel((X,Y)), 0)
    elif Gray:
        for X in range(img.size[0]):
            for Y in range(img.size[1]):
                if img.getpixel((X,Y)) > threshold:
                    Red_Green_pixels[X,Y] = (img.getpixel((X,Y)), img.getpixel((X,Y)), img.getpixel((X,Y)))
    else:
        for X in range(img.size[0]):
            for Y in range(img.size[1]):
                if img.getpixel((X,Y)) > threshold:
                    Red_Green_pixels[X,Y] = (img.getpixel((X,Y)), 0, 0)
    Red_Green.save(fileprename + i + ii + '_.png')

def combine(fileprename):
    for Red_path, Green_path, Gray_path in zip(glob.glob(fileprename + '1*.png'), glob.glob(fileprename + '0*.png'), glob.glob(fileprename + '2*.png')):
        Green = Image.open(Green_path); Red = Image.open(Red_path); Gray = Image.open(Gray_path)
        print(Green_path)
        print(Red_path)
        print(Gray_path)

        #Red + Green
        print('\t Red + Green')
        Com = Image.new(mode = "RGB", size = (Red.size[0], Red.size[1]))
        Com_pixels = Com.load()
        for X in range(Red.size[0]):
            for Y in range(Red.size[1]):
                Com_pixels[X,Y] = (Red.getpixel((X,Y))[0], Green.getpixel((X,Y))[1], 0)
        if len(Green_path.split('_')) < 4:
            Com.save(fileprename + '01_.png')
        else:
            Com.save(fileprename + '01_' + Gray_path.split('_')[2] + '_.png')

        #Green + Gray
        print('\t Green + Gray')
        Com = Image.new(mode = 'RGB', size = (Red.size[0], Red.size[1]))
        Com_pixels = Com.load()
        for X in range(Red.size[0]):
            for Y in range(Red.size[1]):
                if Green.getpixel((X,Y))[1] > 0:
                    Com_pixels[X,Y] = (0, Green.getpixel((X,Y))[1], 0)
                else:
                    Com_pixels[X,Y] = (Gray.getpixel((X,Y)))
        if len(Green_path.split('_')) < 4:
            Com.save(fileprename + '02_.png')
        else:
            Com.save(fileprename + '02_' + Gray_path.split('_')[2] + '_.png')

        #Red + Gray
        print('\t Red + Gray')
        Com = Image.new(mode = 'RGB', size = (Red.size[0], Red.size[1]))
        Com_pixels = Com.load()
        for X in range(Red.size[0]):
            for Y in range(Red.size[1]):
                if Red.getpixel((X,Y))[0] > 0:
                    Com_pixels[X,Y] = (Red.getpixel((X,Y))[0], 0, 0)
                else:
                    Com_pixels[X,Y] = (Gray.getpixel((X,Y)))
        if len(Green_path.split('_')) < 4:
            Com.save(fileprename + '12_.png')
        else:
            Com.save(fileprename + '12_' + Gray_path.split('_')[2] + '_.png')

        #Red + Green + Gray
        print('\t Red + Green + Gray')
        Com = Image.new(mode = 'RGB', size = (Red.size[0], Red.size[1]))
        Com_pixels = Com.load()
        for X in range(Red.size[0]):
            for Y in range(Red.size[1]):
                if Red.getpixel((X,Y))[0] > 0 or Green.getpixel((X,Y))[1] > 0:
                    Com_pixels[X,Y] = (Red.getpixel((X,Y))[0], Green.getpixel((X,Y))[1], 0)
                else:
                    Com_pixels[X,Y] = (Gray.getpixel((X,Y)))
        if len(Green_path.split('_')) < 4:
            Com.save(fileprename + '012_.png')
        else:
            Com.save(fileprename + '012_' + Gray_path.split('_')[2] + '_.png')

def clear():
    for f in glob.glob('output/*png'):
        os.remove(f)

def Ultimate(Red_t, Green_t, Gray_t):
    clear()
    for f in glob.glob('input/*.oib'):
        print(f)
        fileprename ='output/' + f.split('.')[0].split('/')[1] + '_'
        im = oiffile.imread(f)
        imshape = im.shape
        print(imshape)
        if len(imshape) == 3:
            for i, x in enumerate(im):
                print('\t' + str(i))
                img = Image.fromarray(x, 'P')
                if i == 0:
                    Red_Green(img = img, fileprename = fileprename, Green = True, Gray = False, i = str(i), ii = '', threshold= Red_t)
                elif i == 1:
                    Red_Green(img = img, fileprename = fileprename, Green = False, Gray = False, i = str(i), ii = '', threshold= Green_t)
                else:
                    Red_Green(img = img, fileprename = fileprename, Green = False, Gray = True, i = str(i), ii = '', threshold= Gray_t)
        else:
            for i, y in enumerate(im):
                print(i)
                for ii, x in enumerate(y):
                    print('\t' + str(ii))
                    img = Image.fromarray(x, 'P')
                    if i == 0:
                        Red_Green(img = img, fileprename = fileprename, Green = True, Gray = False, i = str(i), ii = '_' + str(ii), threshold= Red_t)
                    elif i == 1:
                        Red_Green(img = img, fileprename = fileprename, Green = False, Gray = False, i = str(i), ii = '_' + str(ii), threshold= Green_t)
                    else:
                        Red_Green(img = img, fileprename = fileprename, Green = False, Gray = True, i = str(i), ii = '_' + str(ii), threshold= Gray_t)
        combine(fileprename = fileprename)
        print()

def check():
    if not os.path.exists('input/'):
        os.mkdir('input')
    if not os.path.exists('output/'):
        os.mkdir('output')
    for f in glob.glob('*.oib'):
        os.rename(f, 'input/' + f)

def Help():
    print('[-h, -u RED GREEN GRAY, -d]')

def main(opt):
    check()
    if len(opt) > 0:
        if opt[0] == '-h':
            Help()
        elif opt[0] == '-u':
            if len(opt) == 4:
                Ultimate(int(opt[1]), int(opt[2]), int(opt[3]))
            else:
                print(opt)
                Help()
        elif opt[0] == '-d':
            clear()
        sys.exit()
    else:
        Help()
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])