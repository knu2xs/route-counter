import arcpy


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
            datatype='Field',
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
            datatype='Field',
            parameterType='Required',
            direction='input'
        )
        output_feature_class = arcpy.Parameter(
            displayName='Output Feature Class',
            name='output_feature_class',
            datatype='DEFeatureClass',
            parameterType='Required',
            direction='input'
        )

        # disable the field selector parameters


        params = [network, stores, store_id_field, customers, customer_id_field, output_feature_class]
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
        return
