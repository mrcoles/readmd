import unittest
import os
try: import cStringIO as StringIO
except: import StringIO

import readmd


def _markup(text, width=None):
    f = StringIO.StringIO(text)
    out = StringIO.StringIO()
    if width is None: width = 80
    readmd.readmd(f, width, out)
    return out.getvalue()


class TestReadMd(unittest.TestCase):

    def setUp(self): pass
    def tearDown(self): pass

    def test_ul(self):
        samples_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'sample-tests')

        # get all the test file names
        file_names = os.listdir(samples_dir)
        test_file_names = set()
        for name in file_names:
            if name.endswith('.sample') or name.endswith('.desired'):
                test_file_names.add('.'.join(name.split('.')[:-1]))

        # run test on all test files
        for test_file_name in test_file_names:
            path = os.path.join('sample-tests', test_file_name)

            sample = open(path + '.sample')
            desired = open(path + '.desired') #TODO - do something if IOError?

            sample_data = sample.read()
            desired_data = desired.read()

            sample.close()
            desired.close()

            self.assertEqual(_markup(sample_data), desired_data)

    # def test_ol(self):
    #     self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
