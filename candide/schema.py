import colander
import deform.widget
from persistent import Persistent
from substanced.content import content
from substanced.property import PropertySheet
from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer
from sweetpotatopie.parsers import SchemaParser

_parser = SchemaParser()

def context_is_a_ttw_schema(context, request): #pragma NO COVER
    return request.registry.content.istype(context, 'TTWSchema')

class TTWSchemaSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_ttw_schema,
        )
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=20, cols=70),
        )

class TTWSchemaPropertySheet(PropertySheet):
    schema = TTWSchemaSchema()
    
@content(
    'TTWSchema',
    icon='icon-align-left',
    add_view='add_ttw_schema', 
    propertysheets = (
        ('Basic', TTWSchemaPropertySheet),
        ),
    )
class TTWSchema(Persistent):

    name = renamer()
    
    def __init__(self, yaml=''):
        self.yaml = yaml

    def getSchema(self):
        yaml = self.yaml.strip()
        if yaml:
            return _parser(self.yaml)
        return colander.Schema()
