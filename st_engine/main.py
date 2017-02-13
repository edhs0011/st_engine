from util.preprocess import to_argus
import zlib
import pandas as pd
from StringIO import StringIO

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
		for data in to_argus(self.df):
			print data

def main():
	detection = Detection("/home/ehsieh/diamond-netflow/1486598402.csv.zlib")
	detection.run()

if __name__ == "__main__":
	main()