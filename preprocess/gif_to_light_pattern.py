#!/usr/bin/env python3.8

import PIL.Image, PIL.ImageDraw, PIL.ImageSequence
import math
import argparse
from collections import Counter


parser = argparse.ArgumentParser()
parser.add_argument("-f", dest='in_img', required=True)
parser.add_argument("-o", dest='out_img')
parser.add_argument("-l", dest='out_lua')
parser.add_argument("-d", dest='dim_factor', default=1, type=float)
parser.add_argument("-e", dest='edge_size', default=4, type=float)

args = parser.parse_args()

in_anim = PIL.Image.open(args.in_img)
img_x, img_y = in_anim.size
resize_x=400
resize_y=400
resize_to=(resize_x,resize_y)


ranks = [60, 48, 40, 32, 24, 16, 12, 8, 1]
num_ranks = len(ranks) - 1
diameter = (min(resize_x, resize_y) / 2) - float(args.edge_size)
frames = []
frames_txt = []
for in_img in PIL.ImageSequence.Iterator(in_anim):
    frame_txt = ''
    in_img = in_img.convert('RGB').resize(resize_to)
    ni = PIL.Image.new("RGB", in_img.size)
    img_x, img_y = in_img.size
    d = PIL.ImageDraw.Draw(ni)
    for rank, rank_size in enumerate(ranks):
        hypotenuse = (num_ranks - rank) * diameter/num_ranks
        for index in range(0,rank_size):
            rads = (index/rank_size)*(2*math.pi)
            x = -int(math.sin(rads) * hypotenuse - img_x/2)
            y = int(math.cos(rads) * hypotenuse + img_y/2)
            counter = Counter()
            for x_pix in range(x-3, x+3):
                for y_pix in range(y-3, y+3):
                    pix = in_img.getpixel((x_pix, y_pix))
                    counter['r'] += pix[0]
                    counter['g'] += pix[1]
                    counter['b'] += pix[2]
                    counter['t'] += 1
            red = int(counter['r']/counter['t']/args.dim_factor)
            green = int(counter['g']/counter['t']/args.dim_factor)
            blue = int(counter['b']/counter['t']/args.dim_factor)
            d.ellipse([(x-3,y-3),(x+3,y+3)], fill=(red,green,blue), width=1)
            # pixel order on star is G,R,B
            frame_txt += (f'\{green}\{red}\{blue}')
    frames_txt.append(frame_txt)
    frames.append(ni)

if args.out_img:
    frames[0].save(args.out_img, append_images=frames[1:], save_all=True , format='GIF', duration=100, loop=0)

if args.out_lua:
    with open(args.out_lua, 'w') as f:
        f.write('local f={}\n')
        for idx, line in enumerate(frames_txt):
            f.write(f'f[{idx}]=\'{line}\'\n')

        f.write('return f')
