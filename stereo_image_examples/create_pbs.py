import os
import sys
import argparse
import re
from glob import glob

def replace_string(file_lines, key_str, replace_item):
  """replace instances of key within a file with replace_str"""
  # make sure replacement element is a string
  replace_str = str(replace_item)
  new_lines = [x.replace(key_str, replace_str) for x in file_lines]
  return new_lines

def save_changes(pbs_file, updated):
  """save the updated pbs file to the new path"""
  with open(pbs_file, 'w') as f:
    f.writelines(updated)
     

def main(args):
  """
  Creates the qsub scripts to run each individual job.
  Is modular, you specify the config file,
  the output directory, the data set, the path to the base
  run script and whether you want to plot the output of running
  each script, then you ware good to go.
  """
  # get a list of all the image_xx.txt files
  image_lists = glob('./image_*.txt')
  # convert to absolute path
  image_lists = [os.path.abspath(x) for x in image_lists]
  # read in the base file
  with open(args.base, 'r') as f:
    base_file = f.readlines()
  for i in range(len(image_lists)):
    print(i)
    print(image_lists[i])
    # now copy the base script over to the new run location
    #pbs_file = os.path.join(args.outdir, 'run_{:0>2d}.sh'.format(i))
    # now replace the necessary characters in that
    # pbs batch submission file to send everything
    # to the correct directories
    # for the config file, use absolute path and also need to escape
    # special characters so can be used by `sed`
    # my_cmd("sed -i \'s/<INDEX>/{}/g\' {}".format(i, pbs_file))
    # my_cmd("sed -i \'s/<IMAGELIST>/{}/g\' {}".format(image_lists[i], pbs_file))
    # my_cmd("sed -i \'s/<WALLTIME>/{}/g\' {}".format(args.walltime, pbs_file))
    # my_cmd("sed -i \'s/<MEMORY>/{}/g\' {}".format(args.mem, pbs_file))
    # my_cmd("sed -i \'s/<NCPUS>/{}/g\' {}".format(args.ncpus, pbs_file))
    updated = replace_string(base_file, '<INDEX>', i)
    updated = replace_string(updated, '<IMAGELIST>', image_lists[i])
    updated = replace_string(updated, '<WALLTIME>', args.walltime)
    updated = replace_string(updated, '<MEMORY>', args.mem)
    updated = replace_string(updated, '<NCPUS>', args.ncpus)
    # now save the updated changes in a new file
    pbs_file = os.path.join(args.outdir, 'run_{:0>2d}.sh'.format(i))
    save_changes(pbs_file, updated)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='pbs_batch',
                                   epilog=main.__doc__,
                                   formatter_class=
                                   argparse.RawDescriptionHelpFormatter)
  parser.add_argument('base', type=str,
                      help='path to the base script')
  parser.add_argument('outdir', type=str,
                      help='path to output the run files and directiories')
  parser.add_argument("--ncpus", type=int, default=1,
                      help="Number of CPU coes you are chasing")
  parser.add_argument("--walltime", type=str, default="00:10:00",
                      help="Max runtime in HH:MM:SS format")
  parser.add_argument("--mem", type=str, default="1GB",
                      help="Memory required, eg. 32GB, 500MB etc.")
  args = parser.parse_args(sys.argv[1:])
  # check that the absolute path is given for the config file path
  # and the output directory location. Is safer and easier to manage
  # then specifying local path
  for path_ in [args.base, args.outdir]:
    if(path_[0] not in ['~', '/']):
      raise(ValueError('need to specify abs path, error {}'.format(path_)))
  # check that the memory is supplied in correct format
  if(args.mem[-2:] not in  ['MB', 'GB']):
    raise(ValueError('Incorrect memory spec {}'.format(args.mem)))
  # now check that the wall time is correct
  walltime = re.compile('.*:.*:.*')
  if(walltime.match(args.walltime) is None):
    raise(ValueError('Incorrect walltime spec {}'.format(args.walltime)))

  #run the main program with these arguments parsed
  main(args)
