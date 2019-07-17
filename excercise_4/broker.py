import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("num_federates", type = int)
parser.add_argument("broker_name", type = str)
args = parser.parse_args()
print(args.num_federates)
print(args.broker_name)
print(type(args.broker_name))

staff.init_broker(args.num_federates, args.broker_name)

