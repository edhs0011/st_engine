import argparse
import zlib
import multiprocessing
import os
import pandas as pd
import logging.config
logging.config.fileConfig('etc/log/log.conf')
import logger
from StringIO import StringIO
from util.preprocess import to_argus
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Queue
from slips import Tuple, Processor
from datetime import timedelta
from modules.markov_models_1 import __markov_models__
from context import Context

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="the input folder of netflow file", type=str)
    parser.add_argument('-a', '--amount', help='Minimum amount of flows that should be in a tuple to be printed.', action='store', required=False, type=int, default=-1)
    parser.add_argument('-v', '--verbose', help='Amount of verbosity.', action='store', default=1, required=False, type=int)
    parser.add_argument('-w', '--width', help='Width of the time slot used for the analysis. In minutes.', action='store', default=5, required=False, type=int)
    parser.add_argument('-d', '--datawhois', help='Get and show the whois info for the destination IP in each tuple', action='store_true', default=False, required=False)
    parser.add_argument('-D', '--dontdetect', help='Dont detect the malicious behavior in the flows using the models. Just print the connections.', default=False, action='store_true', required=False)
    parser.add_argument('-f', '--folder', help='Folder with models to apply for detection.', action='store', required=False, default='models')
    parser.add_argument('-o', '--output', help='Folder for the output result.', action='store', required=False, default='output', type=str)
    args = parser.parse_args()

    # Global shit for whois cache. The tuple needs to access it but should be shared, so global
    whois_cache = {}

    if args.dontdetect:
        logging.warn('Warning: No detections will be done. Only the behaviors are printed.')
        # If the folder with models was specified, just ignore it
        args.folder = False

    # Read the folder with models if specified
    if args.folder:
        onlyfiles = [f for f in os.listdir(args.folder) if os.path.isfile(os.path.join(args.folder, f))]
        logging.info('Detecting malicious behaviors with the following models:')
        for file in onlyfiles:
            __markov_models__.set_model_to_detect(os.path.join(args.folder, file))

    return args

def read_input(file_path):
    for file in os.listdir(file_path):
        with open(os.path.join(file_path, file)) as f:
            csv = f.read()
        stringIO = StringIO(zlib.decompress(csv))
        _df = pd.read_csv(stringIO)
        try:
            df.append(_df, ignore_index=True)
        except:
            df = _df
    return df

def main():
    args = parse()
    queue = Queue()
    df = read_input(args.file_path)
    processorThread = Processor(queue, args.output, timedelta(minutes=args.width), args.datawhois, args.verbose, args.amount, args.dontdetect)
    processorThread.start()

    data = to_argus(df)
    for line in data.strip().split("\n"):
        queue.put(line)
    queue.put('stop')

if __name__ == "__main__":
    main()