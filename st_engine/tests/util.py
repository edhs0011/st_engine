import unittest2 as unittest
import StringIO
import inspect
import os
import json
import pandas as pd
import numpy as np

class GoldenTestCase(unittest.TestCase):
    @classmethod
    def ckeckGolden(cls, obj, file, force=False):
        if force:
            _dir = os.path.join(os.path.dirname(inspect.getfile(cls)), "fixtures",
                            cls.__name__)
        else:
            _dir = os.path.join(os.path.dirname(inspect.getfile(cls)), "expected_results",
                            cls.__name__)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if isinstance(obj, dict) or isinstance(obj, list):
            _file = os.path.join(_dir, file + ".json")
            if force:
                os.remove(_file)
            contents = obj
            try:
                expected_results = json.load(open(_file))
            except IOError:
                json.dump(obj, open(_file, "w"))
                raise MakingGolden((_file,json.dumps(obj)))
        elif isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series) or isinstance(obj, np.ndarray) :
            if isinstance(obj, pd.Series):
                obj = obj.to_frame()
            if isinstance(obj, np.ndarray):
                obj = pd.DataFrame(obj)
            output = StringIO.StringIO()
            _file = os.path.join(_dir, file + ".csv")
            if force:
                os.remove(_file)
            obj.to_csv(output)
            contents = output.getvalue()
            try:
                expected_results = open(_file).read()
            except IOError:
                open(_file, "w").write(contents)
                raise MakingGolden((_file, contents))
        else:
            raise Exception("Unknown Type %s ", obj.__class__)
        return contents, expected_results, _file

    def df(self, file, index_col=None, keep=False, csvSrc=False):
        if keep:
            _dir = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "expected_results",
                                self.__class__.__name__)
        else:
            _dir = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "fixtures",
                                self.__class__.__name__)
        _file = os.path.join(_dir, file + ".csv")
        if csvSrc:
            return _file
        return pd.read_csv(_file, index_col=index_col)
        
    def assertGolden(self, obj, file):
        contents, expected_results, _file = self.ckeckGolden(obj, file)
        self.assertEquals(contents, expected_results, "At %s" % _file)