"""
Purpose:    Get route segment count for display.
DOB:        12 May 2016
Father:     Joel McCune (https://github.com/knu2xs)
"""
# import modules
import arcpy

# variables
# network = r'D:\arcgisBusinessAnalystData_USA\Data\Streets Data\NAVTEQ_2014_Q3_NA.gdb\Routing\Routing_ND'
# customers = r'Default Group Layer\Customers'
# stores = r'Default Group Layer\REI'
# output = r'D:\dev\route-segment-utilities\data.gdb\routes_count'
network = arcpy.GetParameterAsText(0)
customers = arcpy.GetParameterAsText(1)
stores = arcpy.GetParameterAsText(2)
output = arcpy.GetParameterAsText(3)


def get_closest_facility_routes(network, stores, customers):
    """
    Get the routes for matching each customer with the closest store.
    :param network: Network dataset to be used for solving.
    :param stores: Stores locations.
    :param customers: Customer locations.
    :return: Route feature layer.
    """

    # create a route layer to work with
    arcpy.AddMessage('Setting up routing solution.')
    route_lyr = arcpy.MakeClosestFacilityLayer_na(network, 'closestFacility', "Minutes")[0]

    # add the stores to the route layer
    arcpy.AddMessage('Adding stores to routing solution.')
    arcpy.AddLocations_na(route_lyr, 'Facilities', stores, 'LOCNUM Name #', '5000 meters')

    # add the customers to the route layer
    arcpy.AddMessage('Adding customers to routing solution.')
    arcpy.AddLocations_na(route_lyr, 'Incidents', customers, 'OBJECTID Name #', '5000 meters')

    # solve the route
    arcpy.AddMessage('Solving routing solution.')
    arcpy.Solve_na(route_lyr)

    # return the route layer to work with
    return arcpy.mapping.ListLayers(route_lyr, 'Routes')[0]


def get_route_segment_count_feature_class(routes_feature_layer, output_route_count_feature_class):
    """
    Get the overlapping feature count for each segment of the feature class.
    :param routes_feature_layer: Feature layer output from a route solution.
    :param output_route_count_feature_class: Path to where the new route count feature class is to be saved.
    :return: Path to output route count feature class.
    """

    # split the road line segments at every crossing or intersection
    arcpy.AddMessage('Splitting roads into discrete segments at intersections.')
    roads_temp = arcpy.FeatureToLine_management(routes_feature_layer, 'in_memory/roads_temp')[0]

    # create a dataset with no overlapping features
    arcpy.AddMessage('Creating a dataset with no overlaps.')
    roads_single = arcpy.DeleteIdentical_management(roads_temp, 'Shape')[0]

    # use spatial join to get the feature count
    arcpy.AddMessage('Getting the segment count for overlapping roads.')
    return arcpy.SpatialJoin_analysis(roads_single, roads_temp, output_route_count_feature_class)[0]
