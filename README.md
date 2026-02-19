# geodatabase_reproject

Reproject a file geodatabase. Reprojection includes correcting bad resolution and tolerance values that shadow data for decades.  Friends, this our shadow escape, our rules, the trick is never to be afraid.

ESRI developed an original version of this code and gifted it to us as a single ~500 line python function. We naively wrapped that up as \stash\reprojectgeodatabase.py. Further development of a single function with several different goals and object types proved unworkable. We then migrated to this standalone repository with tests and looser coupling of components.

# You Will Need

1. arcpy from ArcGIS Pro 
2. [ArcGIS Pro Topographic Production toolbox license](https://pro.arcgis.com/en/pro-app/latest/tool-reference/topographic-production/topographic-production-toolbox-license.htm) (aka arcpy.topographic.xyz)

## The Workflow

1. Input file geodatabase generates excel workbook schema
2. Tweak/correct excel workbook schema
3. Excel workbook generates empty output file geodatabase
4. Load output geodatabase data from input geodatabase
5. Create relationship classes in output file geodatabase
6. Load tables and attributed relationship classes in output geodatabase

Why load tables separately in step 6 instead of as part of 4?