"""
Purpose:    Toolbox for routing utilities useful for creating demonstration datasets.
Developer:  Joel McCune (joel.mccune@gmail.com)
DOB:        04 Aug 2016
"""
import arcpy
from routing_utilities import get_route_count_feature_class
from get_business_analyst_data_paths import get_usa_network_dataset_path


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Route Segmentation Toolbox"
        self.alias = "route_segmentation_toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GetRouteCountFeatureClass]


class GetRouteCountFeatureClass(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Get Route Count Feature Class"
        self.description = "Get feature class with overlapping route count."
        self.canRunInBackground = True

        # couple of properties needed in tool
        self.store_field_dictionary = {}
        self.customer_id_dictionary = {}

    def getParameterInfo(self):
        """Define parameter definitions"""
        # define parameters
        network = arcpy.Parameter(
            displayName='Transportation Network',
            name='network',
            datatype='DENetworkDataset',
            parameterType='Required',
            direction='input'
        )
        stores = arcpy.Parameter(
            displayName='Stores Feature Layer',
            name='stores',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='input'
        )
        store_id_field = arcpy.Parameter(
            displayName='Stores Unique Identifier Field',
            name='store_id_field',
            datatype='GPString',
            parameterType='Required',
            direction='input'
        )
        customers = arcpy.Parameter(
            displayName='Customers Feature Layer',
            name='customers',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='input'
        )
        customer_id_field = arcpy.Parameter(
            displayName='Customers Unique Identifier Field',
            name='customer_id_field',
            datatype='GPString',
            parameterType='Required',
            direction='input'
        )
        output_feature_class = arcpy.Parameter(
            displayName='Output Feature Class',
            name='output_feature_class',
            datatype='DEFeatureClass',
            parameterType='Required',
            direction='output'
        )

        # disable the field selector parameters
        store_id_field.enabled = False
        customer_id_field.enabled = False

        # set the default path for the network dataset
        network.value = get_usa_network_dataset_path()

        # roll up all the parameters into a single list and return it
        params = [network, stores, store_id_field, customers, customer_id_field, output_feature_class]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # helper function to create a dictionary of field aliases and field names
        def get_field_dictionary(feature_layer):

            # create a dictionary to store values
            field_dictionary = {}

            # iterate the field list and create dictionary entries for aliases and names
            for field in arcpy.ListFields(feature_layer):
                field_dictionary[field.aliasName] = field.name

            # return the populated dictionary
            return field_dictionary

        # if the store feature layer parameter has been changed and there is something in it
        if parameters[1].value and parameters[1].altered:

            # get a dictionary of field aliases and names
            self.store_field_dictionary = get_field_dictionary(parameters[1].valueAsText)

            # create a list of field aliases from the dictionary keys and feed it into the store UID parameter
            parameters[2].filter.list = [key for key in self.store_field_dictionary.keys()]

            # enable the store UID parameter
            parameters[2].enabled = True

        # if the customer feature layer parameter has been changes and there is something in it
        if parameters[3].value and parameters[3].altered:

            # get a dictionary of field aliases and names
            self.customer_id_dictionary = get_field_dictionary(parameters[3].valueAsText)

            # create a list of field aliases from the dictionary keys and feed it into the customer UID parameter
            parameters[4].filter.list = [key for key in self.customer_id_dictionary.keys()]

            # enable the customer UID parameter
            parameters[4].enabled = True

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # look up the field names from the parameter inputs using field aliases
        store_id_field = self.store_field_dictionary[parameters[2]]
        customer_id_field = self.customer_id_dictionary[parameters[4]]

        # execute the tool
        get_route_count_feature_class(parameters[0], parameters[1], store_id_field, parameters[3], customer_id_field,
                                      parameters[5])
        return
