# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:55:39 2021

@author: juliu

Credit: Dave Babbitt on Stackoverflow
See https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python 
"""

import os
import imageio

png_dir = './images/'
images = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('./Veff.gif', images)
