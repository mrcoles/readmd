import unittest
import os
import re
try: import cStringIO as StringIO
except: import StringIO

import readmd


def _markup(text, width=None):
    f = StringIO.StringIO(text)
    out = StringIO.StringIO()
    if width is None: width = 80
    readmd.readmd(f, width, out)
    return out.getvalue()

class SampleTestsMetaclass(type):
    def __new__(cls, name, bases, attrs):
        samples_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'sample-tests')

        # get all the test file names
        file_names = os.listdir(samples_dir)
        test_file_names = set()
        for name in file_names:
            if name.endswith('.sample') or name.endswith('.desired'):
                test_file_names.add('.'.join(name.split('.')[:-1]))

        # test logic function closure
        def get_fn(path):
            def fn(self):
                path = os.path.join(samples_dir, test_file_name)
                sample = open(path + '.sample')
                desired = open(path + '.desired') #TODO - IOError?
                sample_data = sample.read()
                desired_data = desired.read()
                sample.close()
                desired.close()
                self.assertEqual(_markup(sample_data), desired_data)
            return fn

        # run test on all test files
        _r_file_fn = re.compile('^[A-z][A-z0-9_\-]*$')
        for test_file_name in test_file_names:
            if _r_file_fn.match(test_file_name):
                attrs['test_%s' % test_file_name] = get_fn(test_file_name)

        return super(SampleTestsMetaclass, cls).__new__(cls, name, bases, attrs)


class TestReadMd(unittest.TestCase):
    __metaclass__ = SampleTestsMetaclass
    def setUp(self): pass
    def tearDown(self): pass


if __name__ == '__main__':
    unittest.main()
