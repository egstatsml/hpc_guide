"""create_depth_map.py


taken largely from 
https://timosam.com/python_opencv_depthimage/#
"""
import numpy as np
from sklearn.preprocessing import normalize
import cv2
import argparse
import sys
import os

# first create the matchers
left_matcher = cv2.StereoSGBM_create(
  minDisparity=0,
  numDisparities=args.max_disparity,
  blockSize=args.block_size,
  P1=args.p1,    
  P2=args.p2,
  disp12MaxDiff=1,
  uniquenessRatio=15,
  speckleWindowSize=1000,
  speckleRange=2,
  mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
# create right matcher
right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
# create WLS filter
wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
wls_filter.setLambda(lmbda)
wls_filter.setSigmaColor(sigma)
# note here I am only sending parameters needed to this method, when before
# in the create_matchers method I sennt all the cmdline args.
# in general, the bottom 
wls_filter = create_wls_filter(left_matcher, args.lmbda, args.sigma)
# open the list of paths to image pairs to iterate over
with open(args.image_path_list) as f:
  image_pair_paths = f.readlines()
# going to strip and newline characters that might be hiding in there
image_pair_paths = [x.rstrip() for x in image_pair_paths]
# now want to iterate over these and compute disparity maps and then save them
for image_pair in image_pair_paths:
  # compute disparity map and apply wls filter
  # read images in and resize if needed
  left_im, right_im = read_resize_images(image_pair_path, im_height, im_width)
  # compute disparity maps for left and right images
  displ = left_matcher.compute(left_im, right_im)  # .astype(np.float32)/16
  dispr = right_matcher.compute(right_im, left_im)  # .astype(np.float32)/16
  #displ = np.int16(displ)
  #dispr = np.int16(dispr)
  filtered_im = wls_filter.filter(displ, left_im, disparity_map_right=dispr)
  print(np.max(displ))
  print(np.min(dispr))
  print(np.max(filtered_im))
  print(np.min(filtered_im))
  filtered_im = np.uint8(filtered_im)
  # now save it
  save_disparity_map(filtered_disp, image_pair)
