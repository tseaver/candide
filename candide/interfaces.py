from zope.interface import Interface

class ITTWSchema(Interface):
    """ Marker for TTW-managed schema objects.

    Schema is managed as YAML stored in a string property.
    """
    def getSchema():
        """ -> colander.SchemaNode.
        """

class ITTWSchemas(Interface):
    """ Marker for service holding TTW-managed schema objects.
    """
