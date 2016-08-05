"""
Purpose:    Get route segment count for display.
DOB:        12 May 2016
Father:     Joel McCune (https://github.com/knu2xs)
"""
# import modules
import arcpy
import os.path

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
    joined_roads = arcpy.SpatialJoin_analysis(roads_single, roads_temp, 'in_memory/joined_roads_temp')[0]

    # use feature class to feature class to delete unwanted fields and write a simpler output
    return arcpy.conversion.FeatureClassToFeatureClass(
        in_features=joined_roads,
        out_path=os.path.dirname(output_route_count_feature_class),
        out_name=os.path.basename(output_route_count_feature_class),
        field_mapping='routeCount "Route Count" true true false 4 Long 0 0,First,#,{},Join_Count,-1,-1'.format(joined_roads)
    )[0]


def get_route_count_feature_class(network, stores, customers, output_feature_class):
    """
    Route from each customer to the closest store. Dissolve the overlapping route segments into single feature line
    segments with the overlapping count saved as an attribute.
    :param network: Transportation network to be used for routing.
    :param stores: Feature layer with the store locations.
    :param customers: Feature layer with customer locations.
    :param output_feature_class: Location to store output feature class.
    :return: Path to output feature class.
    """
    # get the raw routes
    routes_lyr = get_closest_facility_routes(network, stores, None, customers, None)

    # distill the raw routes into non-overlapping lines with feature counts
    return get_route_segment_count_feature_class(routes_lyr, output_feature_class)
