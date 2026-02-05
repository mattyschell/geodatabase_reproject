# geodatabase_reproject

Reproject a file geodatabase. Reprojection includes correcting bad resolution and tolerance values that shadow data for decades.  Friends, this our shadow escape, our rules, the trick is never to be afraid.

ESRI developed an original version of this code and gifted it to us as a single python function snippet. We naively wrapped it up into py\stash\reprojectgeodatabase.py. When further development of reprojectgeodatabase.py proved unworkable we migrated to this standalone repository.

# You Will Need

1. arcpy from ArcGIS Pro 
2. [ArcGIS Pro Topographic Production toolbox license](https://pro.arcgis.com/en/pro-app/latest/tool-reference/topographic-production/topographic-production-toolbox-license.htm) (aka arcpy.topographic.xyz)