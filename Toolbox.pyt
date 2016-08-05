"""
Purpose:    Toolbox for routing utilities useful for creating demonstration datasets.
Developer:  Joel McCune (joel.mccune@gmail.com)
DOB:        04 Aug 2016
"""
import arcpy
from routing_utilities import get_route_count_feature_class, add_customer_drive_time_closest
from get_business_analyst_data_paths import get_usa_network_dataset_path


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [
            GetRouteCountFeatureClassClosest,
            AddDriveTimeToCustomersClosest
        ]


class GetRouteCountFeatureClassClosest(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Get Route Count Feature Class - Closest"
        self.description = "Get feature class with overlapping route count for the closest store."
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
        customers = arcpy.Parameter(
            displayName='Customers Feature Layer',
            name='customers',
            datatype='GPFeatureLayer',
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

        # set the default path for the network dataset
        network.value = get_usa_network_dataset_path()

        # roll up all the parameters into a single list and return it
        params = [network, stores, customers, output_feature_class]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # execute the tool
        get_route_count_feature_class(parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText,
                                      parameters[3].valueAsText)
        return


class AddDriveTimeToCustomersClosest(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Drive Time to Customers Feature Class - Closest"
        self.description = "Add the drive time to the customers feature class for the closest store."
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
        customers = arcpy.Parameter(
            displayName='Customers Feature Layer',
            name='customers',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='input'
        )

        # set the default path for the network dataset
        network.value = get_usa_network_dataset_path()

        # roll up all the parameters into a single list and return it
        params = [network, stores, customers]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # execute the tool
        add_customer_drive_time_closest(parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText)
        return
