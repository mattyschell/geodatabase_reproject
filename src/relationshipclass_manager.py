import arcpy
import os
import stat
import shutil
import glob
from pathlib import Path
from pprint import pformat

#import filegeodatabase_manager

class RelationshipClassManager(object):

    def __init__(self
                ,geodatabase
                ,name
                ,origin_class = None
                ,destination_class = None
                ,relationship_type = None
                ,cardinality = None
                ,origin_primary_key=None
                ,destination_foreign_key=None
                ,attributed=False
                ,attributed_table=None
                ,message_direction='NONE'
                ,notification='NONE'):

        self.geodatabase  = geodatabase
        self.name         = name
        self.relclasspath = os.path.join(self.geodatabase
                                        ,self.name)

        self.origin_class            = origin_class
        self.destination_class       = destination_class
        self.relationship_type       = relationship_type
        self.cardinality             = cardinality
        self.origin_primary_key      = origin_primary_key
        self.destination_foreign_key = destination_foreign_key
        self.attributed              = attributed
        self.attributed_table        = attributed_table
        self.message_direction       = message_direction
        self.notification            = notification

    def exists(self):
        print(self.relclasspath)
        if arcpy.Exists(self.relclasspath):
            return True
        else:
            return False

#    def _describe(self):
#    
#        # returns a dict based on what exists in the gdb
#
#        if not self.exists():
#            raise FileNotFoundError(
#                'Relationship class does not exist: {0}'.format(self.relclasspath)
#            )
#
#        desc = arcpy.Describe(self.relclasspath)
#
#        info = {
#            "name": desc.name,
#            "path": self.relclasspath,
#            "dataType": desc.dataType,  # should be "RelationshipClass"
#            "originClassNames": desc.originClassNames,
#            "destinationClassNames": desc.destinationClassNames,
#            "relationshipType": desc.relationshipType,  # SIMPLE or COMPOSITE
#            "cardinality": desc.cardinality,            # ONE_TO_MANY, etc.
#            "isAttributed": desc.isAttributed,
#            "attributedTable": getattr(desc, "attributedTable", None),
#            "originPrimaryKey": desc.originPrimaryKey,
#            "destinationPrimaryKey": desc.destinationPrimaryKey,
#            "originForeignKey": desc.originForeignKey,
#            "destinationForeignKey": desc.destinationForeignKey,
#            "notification": desc.notification,
#            "messageDirection": desc.messageDirection,
#        }
#
#        return info
#
#    def describe_pretty(self): 
#
#        # returns a string
#        return pformat(self._describe())
#
#    def delete(self):
#
#        if self.exists():
#            arcpy.management.Delete(self.relclasspath)
#
#    def create(self):
#
#        origin_path = os.path.join(self.geodatabase
#                                  ,self.origin_class) 
#                                  
#        dest_path = os.path.join(self.geodatabase
#                                ,self.destination_class)
#
#        arcpy.management.CreateRelationshipClass(origin_path
#                                                ,dest_path
#                                                ,self.relclasspath
#                                                ,self.relationship_type
#                                                ,"" # forward label (optional)
#                                                ,"" # backward label (optional) 
#                                                ,self.cardinality
#                                                ,self.attributed
#                                                ,self.attributed_table if self.attributed else ""
#                                                ,self.origin_primary_key
#                                                ,self.destination_foreign_key
#                                                ,self.message_direction
#                                                ,self.notification)