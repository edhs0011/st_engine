import os
import inspect
import pandas as pd
import unittest2 as unittest
from ..util import to_argus
from util import GoldenTestCase

class TestPreprocess(GoldenTestCase):

    def test_trans_argus(self):
        df1 =  self.df("diamond_data_normal")
        self.assertGolden(to_argus(df1), "diamond_data_normal")

