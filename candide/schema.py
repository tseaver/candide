import colander
import deform.widget
from persistent import Persistent
from pyramid.httpexceptions import HTTPFound
from substanced.content import content
from substanced.content import service
from substanced.event import subscribe_created
from substanced.folder import Folder
from substanced.form import FormView
from substanced.property import PropertySheet
from substanced.root import Root
from substanced.schema import Schema
from substanced.schema import NameSchemaNode
from substanced.sdi import mgmt_view
from substanced.util import find_service
from substanced.util import renamer
from sweetpotatopie.parsers import SchemaParser
from zope.interface import implementer

from .interfaces import ITTWSchema
from .interfaces import ITTWSchemas

_parser = SchemaParser()

def context_is_a_ttw_schema(context, request): #pragma NO COVER
    return request.registry.content.istype(context, 'TTWSchema')


class TTWSchemaSchema(Schema):
    name = NameSchemaNode(
        editing=context_is_a_ttw_schema,
        )
    yaml = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=20, cols=70),
        )


class TTWSchemaPropertySheet(PropertySheet):
    schema = TTWSchemaSchema()


@content(
    'TTWSchema',
    icon='icon-wrench',
    add_view='add_ttw_schema',
    propertysheets = (
        ('Basic', TTWSchemaPropertySheet),
        ),
    )
@implementer(ITTWSchema)
class TTWSchema(Persistent):

    name = renamer()

    def __init__(self, yaml=''):
        self.yaml = yaml

    def getSchema(self):
        yaml = self.yaml.strip()
        if yaml:
            return _parser(self.yaml)
        return colander.Schema()
#
#   SDI "add" view for TTWSchema
#
@mgmt_view(
    context=ITTWSchemas,
    name='add_ttw_schema',
    tab_title='Add TTW Schema',
    permission='sdi.add-content',
    renderer='substanced.sdi:templates/form.pt',
    tab_condition=False,
    )
class AddTTWSchemaView(FormView):
    title = 'Add TTWSchema'
    schema = TTWSchemaSchema()
    buttons = ('add',)

    def add_success(self, appstruct): #pragma NO COVER boilerplate
        registry = self.request.registry
        name = appstruct.pop('name')
        ttw = registry.content.create('TTWSchema', **appstruct)
        self.context[name] = ttw
        return HTTPFound(
            self.request.sdiapi.mgmt_path(self.context, '@@contents')
            )


#
#   Service containing TTWSchema objects.
#
@service(
    'TTWSchemas',
    service_name='ttw_schemas',
    icon='icon-wrench',
    add_view='add_ttw_schemas_service',
    )
@implementer(ITTWSchemas)
class TTWSchemas(Folder):
    """ Service object representing a collection of through-the-web schemas.
    """
    def __sdi_addable__(self, context, introspectable):
        return introspectable.get('content_type') == 'TTWSchema'


@subscribe_created(Root)
def root_created(event):
    root = event.object
    schemas = find_service(root, 'schemas')
    if schemas is None:
        schemas = root['schemas'] = TTWSchemas()
        schemas.__is_service__ = True
        schemas.__sdi_deletable__ = False
