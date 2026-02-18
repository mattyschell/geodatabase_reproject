import unittest
import os
import openpyxl
from pathlib import Path
import tempfile

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
        self.sourcepath = os.path.join(self.testdatadir
                                     ,'sample.gdb')
        self.sourcegdb    = filegeodatabase_manager.LocalGDB(self.sourcepath)
        # the remainder do not yet exist
        self.testxlsxpath = os.path.join(self.tempdir
                                        ,'test.xlsx')        
        self.ingdbpath    = os.path.join(self.tempdir
                                        ,'test.gdb')
        self.outxlsxpath  = os.path.join(self.tempdir
                                        ,'out.xlsx')
        self.outgdbpath   = os.path.join(self.tempdir
                                        ,'out.gdb')
        self.outgdb      = filegeodatabase_manager.LocalGDB(self.outgdbpath)

    def setUp(self):

        # will create and delete an excel file and a scratch gdb for each test
        # the first instance should check out the topo production license
        self.testxlsx = xlsx_manager.ExcelFile(self.testxlsxpath)
        self.testxlsx.checkoutlicense()
        self.sourcegdb.copy(self.ingdbpath)
        self.ingdb  = filegeodatabase_manager.LocalGDB(self.ingdbpath)

    def tearDown(self):

        self.ingdb.clean()
        self.testxlsx.delete()
        self.testxlsx.checkinlicense()
        self.outgdb.clean()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_alicenseshenanigans(self):

        # this should not check out additional licenses (see setUp)
        # futile checkins should be harmless 
        self.testxlsx.checkoutlicense()
        self.testxlsx.checkoutlicense()
        self.testxlsx.checkinlicense()
        self.testxlsx.checkinlicense()

    def test_bcreateanddelete(self):

        self.testxlsx.generate_from_geodatabase(self.ingdb.gdb)
        self.assertTrue(self.testxlsx.exists())
        self.testxlsx.delete()
        self.assertFalse(self.testxlsx.exists())

    def test_ccopy(self):

        self.testxlsx.generate_from_geodatabase(self.ingdb.gdb)
        outxlsx = self.testxlsx.copy(self.outxlsxpath)
        self.assertTrue(outxlsx.exists())
        outxlsx.delete()
        self.assertFalse(outxlsx.exists())

    def test_dgenerategeodatabase(self):

        self.testxlsx.generate_from_geodatabase(self.ingdb.gdb)
        self.testxlsx.generate_to_geodatabase(self.outgdb.gdb)
        self.assertTrue(self.outgdb.exists())

    def test_eupdatespatialreference(self):

        self.testxlsx.generate_from_geodatabase(self.ingdb.gdb)
        self.testxlsx.update_all_spatial_reference(6539)
        outxlsx = self.testxlsx.copy(self.outxlsxpath)
        self.assertEqual(outxlsx.workbook['SpatialReferences']['C2'].value
                        ,6539)
        outxlsx.delete()        

    def test_fcopygeodatabase(self):

        self.testxlsx.generate_from_geodatabase(self.ingdb.gdb)
        self.testxlsx.copygeodatabase(self.ingdb.gdb
                                     ,self.outgdb.gdb)
        self.assertTrue(self.outgdb.exists())




if __name__ == '__main__':
    unittest.main()