import arcpy
import os
import stat
import shutil
import glob
from pathlib import Path

class LocalGDB(object):

    def __init__(self
                ,filegdb):

        # we dont check for existence
        # so we can use clean() as a pre-step
        self.gdb      = filegdb
        self.name     = os.path.basename(self.gdb)
        self.path     = os.path.dirname(self.gdb)
        self.basename = self.name.split('.')[0]

    def create(self):

        arcpy.management.CreateFileGDB(self.path
                                      ,self.name)

    def _remove_readonly(self
                       ,func
                       ,path
                       ,_):
        
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def exists(self):

        if arcpy.Exists(self.gdb) and os.path.isdir(self.gdb):
            return True
        else:
            return False

    def clean(self):

        if os.path.isdir(self.gdb) and arcpy.Exists(self.gdb):
            
            arcpy.Compact_management(self.gdb)
            shutil.rmtree(self.gdb, onerror=self._remove_readonly)   
    
    def has_locks(self):

        # after copying from self.gdb source
        # none of our target gdbs should contain locks
        if ( self.gdb 
             and Path(self.gdb).exists() 
             and any(Path(self.gdb).glob("*.lock"))
           ):
           return True
        else:
            return False

    def copy(self
            ,out_gdb):

        shutil.copytree(self.gdb
                       ,out_gdb)
