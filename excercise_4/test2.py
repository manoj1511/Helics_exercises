import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("list", nargs = "+")
args = parser.parse_args()
print(args.name)
print(args.list)
print(type(args.list))
