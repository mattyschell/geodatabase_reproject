import unittest
import os
from pathlib import Path

import filegeodatabasemanager

class FileGeodatabaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.tempdir = Path(os.environ['TEMP'])
        self.testdatadir = os.path.join(os.path.dirname(os.path.abspath(__file__))
                                       ,'testdata')
        self.testgdbpath = os.path.join(self.testdatadir
                                       ,'testsample.gdb')
        self.testgdb = filegeodatabasemanager.LocalGDB(self.testgdbpath)

    def tearDown(self):

        self.testgdb.clean()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_acreate(self):

        self.assertEqual(self.testgdb.name,'testsample.gdb')
        self.assertEqual(self.testgdb.path,self.testdatadir)
        self.assertEqual(self.testgdb.basename,'testsample')
        self.testgdb.create()
        self.assertTrue(self.testgdb.exists())

    def test_blocks(self):

        self.testgdb.create()
        self.assertFalse(self.testgdb.has_locks())

    def test_cclean(self):

        self.testgdb.create()
        self.testgdb.clean()
        self.assertFalse(self.testgdb.exists())



       


if __name__ == '__main__':
    unittest.main()