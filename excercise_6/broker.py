import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("num_federates", type = int)
parser.add_argument("comm_type", type = str)
parser.add_argument("root", type = str)
args = parser.parse_args()
#print(args.num_federates)
#print(args.broker_name)
#print(type(args.broker_name))

print("Starting Broker as follows : staff.init_broker({},{},{})".format(args.num_federates, args.comm_type, args.root))
staff.init_broker(args.num_federates, args.comm_type, args.root)

