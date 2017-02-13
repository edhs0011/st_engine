import argparse
import zlib
import pandas as pd
from StringIO import StringIO
from util.preprocess import to_argus
from subprocess import Popen, PIPE, STDOUT
import logging.config
logging.config.fileConfig('etc/log/log.conf')
import logger

class Detection:
	def __init__(self, file_path):
		self.file_path = file_path
		self.read_input()

	def read_input(self):
		with open(self.file_path) as f:
			csv = f.read()
		stringIO = StringIO(zlib.decompress(csv))
		self.df = pd.read_csv(stringIO)

	def run(self):
		data = to_argus(self.df)
		# to call the detector by python slips.py
		p = Popen(['python', 'slips.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		stdout = p.communicate(input=data)[0]
		print stdout.decode()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file_path", help="the input of netflow file", type=str)
	args = parser.parse_args()

	detection = Detection(args.file_path)
	detection.run()

if __name__ == "__main__":
	main()