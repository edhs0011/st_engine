import argparse
import zlib
import pandas as pd
from StringIO import StringIO
from util.preprocess import to_argus
from subprocess import Popen, PIPE, STDOUT
import logging.config
logging.config.fileConfig('etc/log/log.conf')
import logger
import os

class Detection:
	def __init__(self, file_path):
		self.file_path = file_path
		self.read_input()

	def read_input(self):
		for file in os.listdir(self.file_path):
			with open(os.path.join(self.file_path, file)) as f:
				csv = f.read()
			stringIO = StringIO(zlib.decompress(csv))
			df = pd.read_csv(stringIO)
			try:
				self.df.append(df, ignore_index=True)
			except:
				self.df = df

	def run(self):
		data = to_argus(self.df)
		# to call the detector by python slips.py
		p = Popen(['python', 'slips.py', '-w', str(args.width)], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
		stdout = p.communicate(input=data)[0]
		print stdout.decode()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("file_path", help="the input folder of netflow file", type=str)
	parser.add_argument('-w', '--width', help='Width of the time slot used for the analysis. In minutes.', action='store', default=5, required=False, type=int)
	global args
	args = parser.parse_args()

	detection = Detection(args.file_path)
	detection.run()

if __name__ == "__main__":
	main()