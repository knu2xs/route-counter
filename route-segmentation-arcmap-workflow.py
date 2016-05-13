"""
Purpose:    Get route segment count for display.
DOB:        12 May 2016
Father:     Joel McCune (https://github.com/knu2xs)
"""
# import modules
import arcpy

# variables
network = r'D:\arcgisBusinessAnalystData_USA\Data\Streets Data\NAVTEQ_2014_Q3_NA.gdb\Routing\Routing_ND'
customers = r'Default Group Layer\Customers'
stores = r'Default Group Layer\REI'
output = r'D:\dev\route-segment-utilities\data.gdb\routes_count'

# create a route layer to work with
route_lyr = arcpy.MakeClosestFacilityLayer_na(network, 'closestFacility', "Minutes")[0]

# add the stores to the route layer
arcpy.AddLocations_na(route_lyr, 'Facilities', stores, 'LOCNUM Name #', '5000 meters')

# add the customers to the route layer
arcpy.AddLocations_na(route_lyr, 'Incidents', customers, 'OBJECTID Name #', '5000 meters')

# solve the route
arcpy.Solve_na(route_lyr)

# get the route layer to work with
route_lyr = arcpy.mapping.ListLayers(route_lyr, 'Routes')[0]

# split the road line segments at every crossing or intersection
roads_temp = arcpy.FeatureToLine_management(route_lyr, 'in_memory/roads_temp')[0]

# create a dataset with no overlapping features
roads_single = arcpy.DeleteIdentical_management(roads_temp, 'Shape')[0]

# use spatial join to get the feature count
roads_spatialJoin = arcpy.SpatialJoin_analysis(roads_single, roads_temp, output)
