import unittest
import os
from pathlib import Path
import tempfile

import filegeodatabase_manager
import relationshipclass_manager

class XlsxManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.tempdir = Path(tempfile.gettempdir())
        self.testdatadir = os.path.join(
            os.path.dirname(os.path.abspath(__file__))
           ,'testdata')
        # this geodatabase has one feature class nybb (borough) in 2263
        # and one table NEIGHBORHOODS
        self.sourcepath = os.path.join(self.testdatadir
                                     ,'sample.gdb')
        self.sourcegdb    = filegeodatabase_manager.LocalGDB(self.sourcepath)
        # create in setup    
        self.testgdbpath    = os.path.join(self.tempdir
                                          ,'test.gdb')
        # our fella
        self.testrelclassname = 'Boroughs_Neighborhoods_Rel'                    

    def setUp(self):

        # will create and delete an tghis scratch gdb for each test
        self.sourcegdb.copy(self.testgdbpath)
        self.testgdb  = filegeodatabase_manager.LocalGDB(self.testgdbpath)

        self.testrelclass = (
            relationshipclass_manager.RelationshipClassManager(
                self.testgdb.gdb
               ,self.testrelclassname)
        )

    def tearDown(self):

        self.testgdb.clean()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_aexists(self):

        self.assertFalse(self.testrelclass.exists())
        


if __name__ == '__main__':
    unittest.main()

       