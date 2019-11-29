#!/usr/bin/env python3.8

import PIL.Image, PIL.ImageDraw, PIL.ImageSequence
import math
import argparse
from collections import Counter


parser = argparse.ArgumentParser()
parser.add_argument("-f", dest='in_img', required=True)
parser.add_argument("-o", dest='out_img')
parser.add_argument("-l", dest='out_lua')

args = parser.parse_args()

in_anim = PIL.Image.open(args.in_img)
img_x, img_y = in_anim.size
dim_factor=20


ranks = {1: 60, 2: 48, 3: 40, 4: 32, 5: 24, 6: 16, 7: 12, 8: 8, 9: 1}
num_ranks = 9
diameter = (min(img_x, img_y) / 2)
frames = []
frames_txt = []
for in_img in PIL.ImageSequence.Iterator(in_anim):
    frame_txt = ''
    in_img = in_img.convert('RGB')
    ni = PIL.Image.new("RGB", in_anim.size)
    d = PIL.ImageDraw.Draw(ni)
    for rank, size in ranks.items():
        hypotenuse = (num_ranks - rank) * diameter/num_ranks
        #hypotenuse = diameter - (rank-1) * (diameter/num_ranks)
        for index in range(0,size):
            rads = (index/size)*(2*math.pi)
            x = -int(math.sin(rads) * hypotenuse - img_x/2)
            y = -int(math.cos(rads) * hypotenuse - img_y/2)
            counter = Counter()
            for x_pix in range(x-3, x+3):
                for y_pix in range(y-3, y+3):
                    pix = in_img.getpixel((x_pix, y_pix))
                    counter['r'] += pix[0]
                    counter['g'] += pix[1]
                    counter['b'] += pix[2]
                    counter['t'] += 1
            red = int(counter['r']/counter['t']/dim_factor)
            green = int(counter['g']/counter['t']/dim_factor)
            blue = int(counter['b']/counter['t']/dim_factor)
            d.ellipse([(x-5,y-5),(x+5,y+5)], fill=(red,green,blue), width=2)
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
