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
        self.attributed              = (attributed or 'NONE').upper()
        self.attributed_table        = attributed_table
        self.message_direction       = (message_direction or 'NONE').upper()
        self.notification            = (notification or 'NONE').upper()

        self.forward_label           = ''
        self.backward_label          = ''
        self.origin_foreign_key      = ''
        self.destination_primary_key = ''

    def copyto(self
              ,geodatabase):

        output = self.__class__.__new__(self.__class__)
        output.__dict__ = self.__dict__.copy()
        output.geodatabase = geodatabase
        return output

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
        # add more here if useful
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

    def describe_instance(self):
        
        return self.__dict__.copy()

    def describe_pretty(self
                       ,data: dict): 

        # returns a string
        return pformat(data
                      ,indent=2
                      ,width=80)  

    def create(self):

        origin_path, dest_path = self._build_paths()

        # The order of these inputs and the acceptable values
        # requires both santitation and a sanitarium
        params = self._sanitize_params()
        self._validate_params(params)

        # This is the ArcGIS Pro signature as of 20260218
        arcpy.management.CreateRelationshipClass(
            origin_path
           ,dest_path
           ,self.relclasspath
           ,params["relationship_type"]
           ,params["forward_label"]
           ,params["backward_label"]
           ,self.message_direction
           ,params["cardinality"]
           ,params["attributed"]
           ,params["origin_pk"]
           ,params["origin_fk"]
           ,params["dest_pk"]
           ,params["dest_fk"]
        )

    def delete(self):

        if self.exists():
            arcpy.management.Delete(self.relclasspath)

    def exists(self):
        if arcpy.Exists(self.relclasspath):
            return True
        else:
            return False
    
    def _build_paths(self):
        origin = os.path.join(self.geodatabase, self.origin_class)
        dest = os.path.join(self.geodatabase, self.destination_class)
        return origin, dest

    def _sanitize_params(self):
        return {
            "relationship_type": (self.relationship_type or 'SIMPLE').upper(),
            "cardinality": (self.cardinality or 'ONE_TO_MANY').upper(),
            "forward_label": self.forward_label or "",
            "backward_label": self.backward_label or "",
            "origin_pk": self.origin_primary_key or "",
            "origin_fk": self.origin_foreign_key or "",
            "dest_pk": self.destination_primary_key or "",  # REQUIRED
            "dest_fk": self.destination_foreign_key or "",
            "attributed" : (self.attributed or 'NONE').upper() 
        }

    def _validate_params(self
                        ,p):

        if p['relationship_type'] not in {'SIMPLE', 'COMPOSITE'}:
            raise ValueError(
                'Invalid relationship_type: {0}'.format(p['relationship_type'])
            )

        if p['cardinality'] not in {'ONE_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_MANY'}:
            raise ValueError(
                'Invalid cardinality: {0}'.format(p['cardinality'])
            )

        if p['attributed'] not in {'NONE', 'ATTRIBUTED'}:
            raise ValueError(
                'Invalid attributed: {0}'.format(p['attributed'])
            )

        if p['attributed'] == 'ATTRIBUTED' and not p['origin_fk']:
            raise ValueError(
                'origin_foreign_key required for attributed relationships'
            )
