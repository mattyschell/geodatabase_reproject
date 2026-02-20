import unittest
import os
from pathlib import Path
import tempfile

import filegeodatabase_manager
import relationshipclass_manager

class RelationshipClassManagerTestCase(unittest.TestCase):

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
        self.testoriginkey    = 'BoroCode'    
        self.testforeignkey   = 'BOROCODE'            

    def setUp(self):

        # will create and delete an tghis scratch gdb for each test
        self.sourcegdb.copy(self.testgdbpath)
        self.testgdb  = filegeodatabase_manager.LocalGDB(self.testgdbpath)
        self.boroughfc = 'nybb'
        self.neighborhoodtable = 'NEIGHBORHOODS'

        self.testrelclass = (
            relationshipclass_manager.RelationshipClassManager(
                self.testgdb.gdb
               ,self.testrelclassname)
        )

        self.testrelclass.origin_class = self.boroughfc
        self.testrelclass.destination_class = self.neighborhoodtable
        self.testrelclass.origin_primary_key = self.testoriginkey
        self.testrelclass.destination_foreign_key = self.testforeignkey

    def tearDown(self):

        self.testgdb.clean()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_aexists(self):

        self.assertFalse(self.testrelclass.exists())

    def test_bcreate(self):

        self.testrelclass.create()
        self.assertTrue(self.testrelclass.exists())

    def test_cdelete(self):

        self.testrelclass.create()
        self.assertTrue(self.testrelclass.exists())
        self.testrelclass.delete()
        self.assertFalse(self.testrelclass.exists())

    def test_ddescribe(self):

        self.testrelclass.create()
        result = self.testrelclass.describe_in_gdb()
        self.assertIsInstance(result, dict)
        # empty is False
        self.assertTrue(result)

    def test_edescribepretty(self):

        self.testrelclass.create()
        result = self.testrelclass.describe_pretty(
            self.testrelclass.describe_in_gdb()
        )
        self.assertIn('name', result)
        self.assertIn('Boroughs_Neighborhoods_Rel', result)
        self.assertIn('cardinality', result)
        # note annoying difference between input ONE_TO_MANY
        # and desc OneToMany
        self.assertIn('OneToMany', result)  
        # line breaks are pretty
        self.assertGreater(result.count('\n'), 0)  

    def test_fcopy(self):

        clone = self.testrelclass.copyto(self.testgdb.gdb) 
        # different instance
        self.assertIsNot(self.testrelclass, clone) 
        # same attributes (works here because same gdb)
        self.assertEqual(self.testrelclass.__dict__, clone.__dict__) 
        clone.create()
        self.assertTrue(clone.exists())
        
    def test_gdescribe_instance(self):

        result = self.testrelclass.describe_instance()
        self.assertIsInstance(result, dict)
        # empty is False
        self.assertTrue(result)

    def test_fdescribe_instance_pretty(self):

        result = self.testrelclass.describe_pretty(
            self.testrelclass.describe_instance()
        )
        self.assertIn('name', result)
        self.assertIn('Boroughs_Neighborhoods_Rel', result)
        self.assertIn('cardinality', result)
        # note real world ONE_TO_MANY in the instance
        # isntead of OneToMany returned by arcpy.desc
        self.assertIn('ONE_TO_MANY', result)  
        # line breaks are pretty
        self.assertGreater(result.count('\n'), 0) 

    def test_gcreateattributed(self):

        # basic attributed relationship class
        # no additional special columns
        self.testrelclass.attributed = 'ATTRIBUTED'
        # origin_foreign_key is required for attributed
        # it "links to the origin_primary_key field in the origin table"
        self.testrelclass.origin_foreign_key = 'OBJECTID'
        self.testrelclass.create()
        self.assertTrue(self.testrelclass.exists())
        result = self.testrelclass.describe_in_gdb()
        # again note that the inputs are ATTRIBUTED or 'NONE'
        # but arcpy.Describe is different. True or False
        self.assertTrue(result.get("isAttributed"))




if __name__ == '__main__':
    unittest.main()

       