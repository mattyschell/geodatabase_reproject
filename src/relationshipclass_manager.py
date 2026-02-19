import arcpy
import os
from pprint import pformat

class RelationshipClassManager(object):

    def __init__(self
                ,geodatabase
                ,name
                ,origin_class = None
                ,destination_class = None
                ,relationship_type = 'SIMPLE'
                ,cardinality = 'ONE_TO_MANY'
                ,origin_primary_key=None
                ,destination_foreign_key=None
                ,attributed='NONE'
                ,attributed_table=None
                ,message_direction='NONE'
                ,notification='NONE'):

        self.geodatabase  = geodatabase
        self.name         = name
        self.relclasspath = os.path.join(self.geodatabase
                                        ,self.name)

        self.origin_class            = origin_class
        self.destination_class       = destination_class
        self.relationship_type       = (relationship_type or 'SIMPLE').upper()
        self.cardinality             = (cardinality or 'ONE_TO_MANY').upper()
        self.origin_primary_key      = origin_primary_key
        self.destination_foreign_key = destination_foreign_key
        self.attributed              = attributed
        self.attributed_table        = attributed_table
        self.message_direction       = (message_direction or 'NONE').upper()
        self.notification            = (notification or 'NONE').upper()

        self.forward_label           = ''
        self.backward_label          = ''
        self.origin_foreign_key      = ''
        self.destination_primary_key = ''

    def exists(self):
        if arcpy.Exists(self.relclasspath):
            return True
        else:
            return False

    def describe_in_gdb(self):
    
        # describe the geodatabase not the instance
        # returns a dict 

        if not self.exists():
            raise FileNotFoundError(
                'Relationship class does not exist: {0}'.format(self.relclasspath)
            )

        desc = arcpy.Describe(self.relclasspath)

        # for some reason ESRI doesnt expose properties like originPrimaryKey
        # or destinationForeignKey on the relationship class. They are at 
        # the geodatabase level I guess?  
        info = {
            "name": desc.name,
            "path": self.relclasspath,
            "dataType": desc.dataType,
            "originClassNames": desc.originClassNames,
            "destinationClassNames": desc.destinationClassNames,
            "cardinality": desc.cardinality,
            "isAttributed": desc.isAttributed,
            "attributedTable": getattr(desc, "attributedTable", None),
        }

        return info

    def describe_in_gdb_pretty(self): 

        # returns a string
        return pformat(self.describe_in_gdb()
                      ,indent=2
                      ,width=80)    

    def delete(self):

        if self.exists():
            arcpy.management.Delete(self.relclasspath)

    def create(self):

        if self.attributed != 'NONE':
            raise ValueError('Not ready for attributed yet')

        origin_path = os.path.join(self.geodatabase
                                  ,self.origin_class)              
        dest_path = os.path.join(self.geodatabase
                                ,self.destination_class)

        # The order of these inputs and the acceptable values
        # requires both santitation and a santiarium

        relationship_type = (self.relationship_type or "SIMPLE").upper()
        cardinality = (self.cardinality or "ONE_TO_MANY").upper()
        forward_label = self.forward_label or ""
        backward_label = self.backward_label or ""
        attributed_table = self.attributed_table if self.attributed else ""
        origin_pk = self.origin_primary_key or ""
        origin_fk = ""
        dest_pk = self.destination_primary_key or ""   # <-- REQUIRED
        dest_fk = self.destination_foreign_key or ""

        if relationship_type not in {"SIMPLE", "COMPOSITE"}:
            raise ValueError(
                'Invalid relationship_type: {0}'.format(relationship_type))
        if cardinality not in {"ONE_TO_ONE", "ONE_TO_MANY", "MANY_TO_MANY"}:
            raise ValueError('Invalid cardinality {0}'.format(cardinality))

        # This is the ArcGIS Pro signature as of 20260218
        arcpy.management.CreateRelationshipClass(
            origin_path,
            dest_path,
            self.relclasspath,
            relationship_type, 
            forward_label, 
            backward_label, 
            self.message_direction,  
            cardinality,
            self.attributed,
            origin_pk,
            origin_fk,
            dest_pk,
            dest_fk
        )


