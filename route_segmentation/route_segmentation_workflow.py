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


def get_closest_facility_routes(network, stores, store_id_field, customers, customer_id_field):
    """
    Get the routes for matching each customer with the closest store.
    :param network: Network dataset to be used for solving.
    :param stores: Stores locations.
    :param customers: Customer locations.
    :return: Route feature layer.
    """
    # set the workspace so the network analysis has a place to save output
    arcpy.env.workspace = arcpy.env.scratchGDB

    # create a route layer to work with
    arcpy.AddMessage('Setting up routing solution.')
    route_lyr = arcpy.na.MakeClosestFacilityAnalysisLayer(
        network_data_source=network,
        layer_name='Closest Facility',
        travel_mode='Driving',
        travel_direction="TO_FACILITIES",
        cutoff=None,
        number_of_facilities_to_find=1,
        line_shape='ALONG_NETWORK',
        accumulate_attributes='Minutes;TravelTime'
    )[0]

    # add the stores to the route layer
    arcpy.AddMessage('Adding stores to routing solution.')
    arcpy.na.AddLocations(
        in_network_analysis_layer=route_lyr,
        sub_layer='Facilities',
        in_table=stores,
        field_mappings='{} Name #'.format(store_id_field),
        search_tolerance='5000 Meters',
        snap_to_position_along_network=True,
        snap_offset='5 Meters'
    )

    # add the customers to the route layer
    arcpy.AddMessage('Adding customers to routing solution.')
    arcpy.na.AddLocations(
        in_network_analysis_layer=route_lyr,
        sub_layer='Incidents',
        in_table=customers,
        field_mappings='{} Name #'.format(customer_id_field),
        search_tolerance='5000 Meters',
        snap_to_position_along_network=True,
        snap_offset='5 Meters'
    )

    # solve the route
    arcpy.AddMessage('Solving routing solution.')
    arcpy.Solve_na(route_lyr)

    # return the route layer to work with
    return route_lyr.listLayers('Routes')[0]


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


def get_route_count_feature_class(network, stores, store_id_field, customers, customer_id_field, output_feature_class):
    """
    Route from each customer to the closest store. Dissolve the overlapping route segments into single feature line
    segments with the overlapping count saved as an attribute.
    :param network: Transportation network to be used for routing.
    :param stores: Feature layer with the store locations.
    :param store_id_field: Attribute field with the unique identifier to be used to identify each store.
    :param customers: Feature layer with customer locations.
    :param customer_id_field: Attribute field with the unique identifier to be used to identify each customer.
    :param output_feature_class: Location to store output feature class.
    :return: Path to output feature class.
    """
    # get the raw routes
    routes_lyr = get_closest_facility_routes(network, stores, store_id_field, customers, customer_id_field)

    # distill the raw routes into non-overlapping lines with feature counts
    return get_route_segment_count_feature_class(routes_lyr, output_feature_class)
