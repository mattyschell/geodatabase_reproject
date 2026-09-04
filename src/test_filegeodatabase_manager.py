import unittest
import os
from pathlib import Path
import tempfile
from unittest import mock

import filegeodatabase_manager

class FileGeodatabaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.tempdir = Path(tempfile.gettempdir())
        self.testdatadir = os.path.join(os.path.dirname(os.path.abspath(__file__))
                                       ,'testdata')
        self.testgdbpath = os.path.join(self.testdatadir
                                       ,'testsample.gdb')
        self.testgdb = filegeodatabase_manager.LocalGDB(self.testgdbpath)
        self.tempgdb = filegeodatabase_manager.LocalGDB(
                            os.path.join(self.tempdir
                                        ,'tempsample.gdb'))

    def tearDown(self):

        self.testgdb.clean()
        self.tempgdb.clean()

    @classmethod
    def tearDownClass(self):
        pass
        
    def test_acreate(self):

        self.assertEqual(self.testgdb.name,'testsample.gdb')
        self.assertEqual(self.testgdb.path,self.testdatadir)
        self.assertEqual(self.testgdb.basename,'testsample')
        self.testgdb.create()
        self.assertTrue(self.testgdb.exists())
        self.testgdb.clean()

    def test_blocks(self):

        self.testgdb.create()
        self.assertFalse(self.testgdb.has_locks())
        self.testgdb.clean()

    def test_nonexistent_gdb(self):

        nonexistent = filegeodatabase_manager.LocalGDB(
            os.path.join(self.tempdir, 'does-not-exist.gdb')
        )

        self.assertFalse(nonexistent.exists())
        self.assertFalse(nonexistent.has_locks())
        nonexistent.clean()

    def test_existing_target(self):

        self.testgdb.create()

        with mock.patch.object(
            filegeodatabase_manager.arcpy.management,
            'CreateFileGDB',
            side_effect=RuntimeError('target already exists')
        ) as create_file_gdb:
            with self.assertRaisesRegex(RuntimeError, 'target already exists'):
                self.testgdb.create()

        create_file_gdb.assert_called_once_with(
            self.testgdb.path,
            self.testgdb.name
        )

    def test_lock_file(self):

        self.testgdb.create()
        lock_file = Path(self.testgdb.gdb, 'test.lock')
        lock_file.touch()

        self.assertTrue(self.testgdb.has_locks())

        lock_file.unlink()
        self.assertFalse(self.testgdb.has_locks())

    def test_cleanup_failure_is_propagated(self):

        self.testgdb.create()

        with mock.patch.object(
            filegeodatabase_manager.shutil,
            'rmtree',
            side_effect=OSError('cleanup failed')
        ):
            with self.assertRaisesRegex(OSError, 'cleanup failed'):
                self.testgdb.clean()

    def test_cclean(self):

        self.testgdb.create()
        self.testgdb.clean()
        self.assertFalse(self.testgdb.exists())

    def test_dcopy(self):

        self.testgdb.create()
        self.testgdb.copy(self.tempgdb.gdb)
        self.assertTrue(self.tempgdb.exists())
        self.tempgdb.clean()
        self.testgdb.clean()

if __name__ == '__main__':
    unittest.main()