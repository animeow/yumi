import argparse
import os
import yumi.api as api

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--working-dir', help='working directory', action='store', dest='working_dir', default=os.getcwd())
parser.add_argument(help='Module name', dest='module', action='store', default='mls', nargs=argparse.OPTIONAL)
parser.add_argument(help='Module args', dest='module_args', action='store', nargs=argparse.REMAINDER)

args = parser.parse_args()

api.run(args.working_dir, args.module, args.module_args)
