"""make_data_split.py

Makes a random split of data from the Holopix50 [1] dataset
so we can run some small demos on it.

# REFERENCES:
[1] Hua, Yiwen, et al. "Holopix50k: A Large-Scale In-the-wild Stereo
    Image Dataset." arXiv preprint arXiv:2003.11172 (2020).
"""
import os
from glob import glob
import argparse
import random
import sys
import shutil

def find_image_keys(source_dir):
  """Extract all the image keys from the filenames.

  Each image is stored as
  `-<image-key>_<left-or-right>.jpg`
  For example,
    `-LZzVudZ9Opy4fS11OBT_left.jpg`
    `-LTOTRvyDZJyxEiQUykH_left.jpg`
    `-LQ48NqbR1Y5JPiiwKKq_right.jpg`
    `-LQ48NqbR1Y5JPiiwKKq_left.jpg`
  Note the hyphen is before each image key.

  I just want to extract the image keys from here, as there
  should be an left and right image for each key.

  Args:
    source_dir (str):
      source directory with all the data
  
  Returns:
    list of all image keys

  Raises:
    IOError if the source directory is not valid
  """
  # check the source directory is valid
  # if it is valid, it should have two subdirectories named
  # `left` and `right`
  sub_dirs = os.listdir(source_dir)
  if ('left' not in sub_dirs) or ('right' not in sub_dirs):
    raise IOError('invalid source directory supplied: {}'.format(source_dir))
  # now lets find the image keys
  # they are the same across both left and right directories, so lets just
  # choose one
  abs_image_paths = glob('{}'.format(os.path.join(source_dir, 'left', '*.jpg')))
  # now lets get just the image key by getting rid of the absolute path info,
  # and then stripping the `left` suffix and file
  # extension and throw them away.
  # can do this by just getting rid of the last nine characters which
  # containt "_left.jpg"
  image_keys = [os.path.basename(x)[0:-9] for x in abs_image_paths]
  return image_keys


def copy_data(image_keys, source_dir, out_dir):
  """copy the selected images to new directories.
  
  am going to make the new directory structure be
  └── image_key
    ├── left.jpg
    └── right.jpg

  Args:
    image_keys (list(str)):
      image keys of images we want
    source_dir (str):
      path to the original data
    out_dir (str):
      path that will hold all the subdirectories
  
  Returns:
    NA

  Raises:
    IOError if either:
      1) source_dir doesn't exist (should actually be possible if we made it
      this far, but really in any function we should be running checks on 
      all the input arguments. 
     2) source_dir doesn't exist
     3) If some of the images don't exist (I won't raise this explicitly, this 
        will be raised by the `os` module if the corresponding images aren't
        valid
  """
  # check the source directory is valid
  # if it is valid, it should have two subdirectories named
  # `left` and `right`
  sub_dirs = os.listdir(source_dir)
  if ('left' not in sub_dirs) or ('right' not in sub_dirs):
    raise IOError('invalid source directory supplied: {}'.format(source_dir))
  # check the output dir exists
  if not os.path.isdir(out_dir):
    raise IOError('out directory supplied does not exist: {}'.format(out_dir))
  # now lets copy the data for the samples we will work on
  for image_key in image_keys:
    # create the corresponding sub directory
    os.mkdir(os.path.join(out_dir, image_key))
    # copy across
    for orientation in ['left', 'right']:
      src_path = os.path.join(source_dir,
                              orientation,
                              '{}_{}.jpg'.format(image_key, orientation))
      out_path = os.path.join(out_dir, image_key, '{}.jpg'.format(orientation))
      shutil.copy(src_path, out_path)
      

def main(args):
  # setting a random seed
  random.seed(1189998819991197253)
  # there are stereo images here, and the left and right images are
  # stored in two different subdirectories, but they have a common
  # key that is stored in the filename to link them.
  # Im going to find extract all the image keys and return it as a
  # list
  image_keys = find_image_keys(args.source_dir)
  # now lets get a random subsample of them
  subset_image_keys = random.sample(image_keys, args.num_samples)
  # now need to copy data to the a new directory
  copy_data(subset_image_keys, args.source_dir, args.out_dir)
  print(image_keys)
  print(subset_image_keys)
  
  
if __name__ == '__main__':
  """Loading in command line arguments.
  
  For a script like this, I might not actually use command line arguments,
  I might just hard code some paths here. I don't really need this code to be 
  modular; I am really only going to run it once. Mainly doing it here as
  another of how to use them.
  """
  parser = argparse.ArgumentParser(prog='main',
                                   epilog=main.__doc__,
                                   formatter_class=
                                   argparse.RawDescriptionHelpFormatter)
  default_source_dir = '/work/SAIVT/hpc_guide_data/stereo_images/holopix50k/data/val/Holopix50k/val/'
  default_out_dir = '/work/SAIVT/hpc_guide_data/stereo_images/holopix50k/data/small/'
  parser.add_argument('--source_dir', type=str, default=default_source_dir,
                      help='path to directory with the original data')
  parser.add_argument('--out_dir', type=str, default=default_out_dir,
                      help='path to directory with the output has been written')
  parser.add_argument('--num_samples', type=int, default=20,
                      help='number of samples to use')
  # parse in cmdline args
  args = parser.parse_args(sys.argv[1:])
  main(args)

