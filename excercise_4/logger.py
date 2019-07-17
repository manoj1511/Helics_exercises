import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("logger_file_name", type = str)
args = parser.parse_args()
print(args.logger_file_name)

staff.init_logger(args.logger_file_name)
