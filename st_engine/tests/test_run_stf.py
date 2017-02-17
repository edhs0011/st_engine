import os
import pandas as pd
import unittest2 as unittest
from st_engine.util import to_argus
from st_engine.slips import Processor
from util import GoldenTestCase
from testfixtures import Replacer, Replace
from Queue import Queue

class TestPreprocess(GoldenTestCase):

    def test_trans_argus(self):
        df1 = self.df("diamond_data_normal")
        self.assertGolden(to_argus(df1), "diamond_data_normal")

    def test_slips_processor(self):
        def _get_queue(queue, data):
            for line in data.strip().split("\n"):
                queue.put(line)
            queue.put('stop')

        def mock_print_data(slf):
            df = pd.DataFrame([i.strip().split(',') for i in slf.output_list])
            return df

        with Replace('st_engine.slips.Processor.print_output', mock_print_data):
            queue = Queue()
            args = {
                "width": 5,
                "verbose": 0,
                "amount": -1,
                "output": "temp_file"
            }
            df = self.df("diamond_data_normal", keep=True)
            df = df.to_csv(index=False)

            proc = Processor(queue, args["output"], args["width"], None, args["verbose"], args["amount"], None)
            _get_queue(queue, df)
            proc.run()
            self.assertGolden(proc.print_output(), "diamond_data_normal_pred")
            