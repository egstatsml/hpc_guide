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

def create_matchers(max_disparity, block_size, p1, p2):
  """create left and right stereo matchers.

  Note that some values here are hard-coded.
  I would deem this as acceptable if I have good reason to beleive they are
  never, ever, ever going to change.
  If the time comes when they need to be changed by myself for my own
  experimentation of if I need to search to find the most suitable one, I 
  would add it as a command line argument.
  
  Args:
    max_disparity (int):
      max disparity for matcher to search to
    block_size (int):
      size of the window for matcher
    p1 (float):
      smoothing param
    p2 (float):
      smoothing param

  Returns:
    left and right matcher

  Raises:
    NA, enough error checking should have been done before making it to here
    although it is generally best practice to perform error checking within
    every function.
  """
  # create left matcher
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
  return left_matcher, right_matcher


def create_wls_filter(left_matcher, lmbda, sigma):
  """create WLS filter from matcher instance and then set
  appropriate params

  Args:
    left_matcher (SGBM Matcher Object):
      left matcher for problem
    lmbda (float):
      parameter for regularisation when postprocessing
    sigma (float):
      sensitivity parameter for postprocessing
  
  Returns:
    wls filter instance

  Raises:
    NA
    """
  wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
  wls_filter.setLambda(lmbda)
  wls_filter.setSigmaColor(sigma)
  return wls_filter
  
def compute_disparity_and_filter(left_matcher, right_matcher,
                                 wls_filter, image_pair_path,
                                 im_height, im_width):
  """compute disparity map and then apply wls filter
  
  Will also reshape image to desired size beforehand.
  
  Args:
    left_matcher (SGBM matcher object):
      matcher for left image in stereo pair
    right_matcher (SGBM matcher object):
      matcher for right image in stereo pair
    wls_filter (WLS Filter Object):
      filter to post-process the disparity map
    image_pair_path (str):
      path to the image pair
    im_height (int):
      height of image to be resized to
    im_width (int):
      width of image to be resized to
    
  Returns:
    disparity map computed on resized image that was then filtered
  
  Raises:
    NA
  """
  # read images in and resize if needed
  left_im, right_im = read_resize_images(image_pair_path, im_height, im_width)
  # compute disparity maps for left and right images
  displ = left_matcher.compute(left_im, right_im)  # .astype(np.float32)/16
  dispr = right_matcher.compute(right_im, left_im)  # .astype(np.float32)/16
  #displ = np.int16(displ)
  #dispr = np.int16(dispr)
  filtered_im = wls_filter.filter(displ, left_im, disparity_map_right=dispr)
  #  filtered_im = cv2.normalize(src=filtered_im, dst=filtered_im,
  #                              beta=0.0, alpha=1.0, norm_type=cv2.NORM_MINMAX);
  print(np.max(displ))
  print(np.min(dispr))
  print(np.max(filtered_im))
  print(np.min(filtered_im))
  filtered_im = np.uint8(filtered_im)
  return filtered_im
  
  
def read_resize_images(image_pair_path, im_height, im_width):
  """read image pair from supplied path and resize if needed

  Args:
    image_pair_path (str):
      path to the image pair
    im_height (int):
      height of image to be resized to
    im_width (int):
      width of image to be resized to

  Returns:
    left and right images of correct size

  Raises:
    IOError if the path of an image is invalid
  """
  left_im = cv2.resize(cv2.imread(os.path.join(image_pair_path, 'left.jpg')),
                       (im_width, im_height))
  right_im = cv2.resize(cv2.imread(os.path.join(image_pair_path, 'right.jpg')),
                        (im_width, im_height))
  return left_im, right_im


def save_disparity_map(filtered_disp, image_pair):
  """save disparity map
  
  Will save it such that it is stored as,
  └── image_key
      ├── disp.jpg
      ├── left.jpg
      └── right.jpg
  
  where `image_key` is given as the base directory in the
  `image_pair` path.

  Args:
    filtered_disp (array):
      final disparity map
    image_pair (str):
      path to directory containing the two original images, which is where
      we will save this disparity map

  Returns:
    NA
  """
  cv2.imwrite(os.path.join(image_pair, 'disp.jpg'), filtered_disp)
  

def main(args):
  """Program for performing stereo matching and filtering
  to create depth maps from a stereo pair.
  Will first perform stereo matching using the SGBM
  method [1]. Will then apply the Weigted Least Squared postprocessing
  to tidy it up [2].

  Please refer to documenetion within these references for info. on what these
  params are which values are suitable for them.

  # REFERENCES
  [1] https://docs.opencv.org/3.4/d2/d85/classcv_1_1StereoSGBM.html
  [2] https://docs.opencv.org/3.4/d9/d51/classcv_1_1ximgproc_1_1DisparityWLSFilter.html
  """
  # first create the matchers
  left_matcher, right_matcher = create_matchers(args.max_disparity,
                                                args.block_size,
                                                args.p1, args.p2)
  # create WLS filter
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
    filtered_disp = compute_disparity_and_filter(left_matcher,
                                                 right_matcher,
                                                 wls_filter,
                                                 image_pair,
                                                 args.im_height,
                                                 args.im_width)
    # now save it
    save_disparity_map(filtered_disp, image_pair)
    

def check_cmdline_args(args):
  """check values for cmdline args are good
  
  Our params for the stereo matcher and filtering have some certain constraints.
  Want to check them all to make sure they are all valid before running any of
  them.
  
  Args:
    args (object):
      essentially a struct/struct with all our parsed cmdline args
  
  Returns:
    NA

  Raises:
    IOError if path for file list doesnt exist
    ValueError if a param is supplied is invalid
  """
  if not os.path.isfile(args.image_path_list):
    raise IOError(
      'Value for image paths does not exist: {}'.format(args.image_path_list))
  if (args.max_disparity <= 0) or ((args.max_disparity % 16) != 0):
    raise ValueError(
      'Invalid value for max disparity, must be integer > 0 that is divisible by 16: {}'.format(
        args.max_disparity))
  if (args.block_size < 3) or ((args.block_size % 2) == 0):
    raise ValueError(
      'Invalid value for block_size, must be odd integer >= 3: {}'.format(
        args.block_size))
  if args.p1 is None:
    # set to suggested value, which is
    # 8*number_of_image_channels*blockSize*blockSize
    args.p1 = int(8 * 3 * args.block_size**2.0)
  elif args.p1 < 0:
    raise ValueError(
      'Invalid value for p1, must be positive. If unsure leave as default. {}'.format(
        args.p1))
  if args.p2 is None:
    # set to suggested value, which is
    # 32*number_of_image_channels*blockSize*blockSize
    args.p2 = int(32 * 3 * args.block_size**2.0)
  elif args.p2 < 0:
    raise ValueError(
      'Invalid value for p2, must be positive. If unsure leave as default. {}'.format(
        args.p2))
  if args.p1 > args.p2:
    raise ValueError(
      'Invalid value for p1 and p2, p1 must be < p2: {} {}'.format(
        args.p1, args.p2))
  if (args.lmbda < 0):
    raise ValueError(
      'Invalid value for lmbda, must be > 0: {}'.format(
        args.lmbda))    
  if (args.sigma < 0):
    raise ValueError(
      'Invalid value for sigma, must be > 0: {}'.format(
        args.sigma))    
    

if __name__ == '__main__':
  """Loading in command line arguments.  
  """
  parser = argparse.ArgumentParser(prog='main',
                                   epilog=main.__doc__,
                                   formatter_class=
                                   argparse.RawDescriptionHelpFormatter)
  parser.add_argument('image_path_list',
                      type=str,
                      help='text file with path to images')
  parser.add_argument('--im_height', type=int, default=1080,
                      help='height of image to be reshaped to')
  parser.add_argument('--im_width', type=int, default=1920,
                      help='width of image to be reshaped to')
  parser.add_argument('--max_disparity', type=int, default=160,
                      help='maximum disparity for matcher to search to')
  parser.add_argument('--block_size', type=int, default=15,
                      help='block size for disparity matcher')
  parser.add_argument('--p1', type=int, default=None,
                      help='smoothness param')
  parser.add_argument('--p2', type=int, default=None,
                      help='smoothness param')
  parser.add_argument('--lmbda', type=int, default=8000,
                      help='parameter for regularisation when postprocessing')
  parser.add_argument('--sigma', type=int, default=1.2,
                      help='sensitivity parameter for postprocessing')
  # parse in cmdline args
  args = parser.parse_args(sys.argv[1:])
  # perform some checks on the command line arguments
  check_cmdline_args(args)
  main(args)

