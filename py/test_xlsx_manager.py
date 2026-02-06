import unittest
import os
from pathlib import Path

import filegeodatabase_manager
import xlsx_manager

class XlsxManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.tempdir     = Path(os.environ['TEMP'])
        self.testdatadir = os.path.join(
            os.path.dirname(os.path.abspath(__file__))
           ,'testdata')
        # this geodatabase has one feature class nybb (borough) in 2263
        self.ingdbpath = os.path.join(self.testdatadir
                                     ,'sample.gdb')
        self.ingdb      = filegeodatabase_manager.LocalGDB(self.ingdbpath)
        self.testxlsxpath = os.path.join(self.tempdir
                                        ,'test.xlsx')        
        self.testgdbpath  = os.path.join(self.tempdir
                                        ,'test.gdb')
                
    def setUp(self):

        # will create and delete an excel file and a scratch gdb for each test
        self.testxlsx = xlsx_manager.ExcelFile(self.testxlsxpath)
        self.testxlsx.checkoutlicense()
        self.ingdb.copy(self.testgdbpath)
        self.testgdb  = filegeodatabase_manager.LocalGDB(self.testgdbpath)

    def tearDown(self):

        self.testgdb.clean()
        self.testxlsx.delete()
        self.testxlsx.checkinlicense()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_acreate(self):

        self.testxlsx.generate_from_geodatabase(self.testgdb.gdb)

if __name__ == '__main__':
    unittest.main()