from substanced.property import PropertySheet
from substanced.util import find_service

class CandidePropertysheet(PropertySheet):

    @property
    def schema(self):
        type_name = self.request.registry.content.typeof(self.context)
        ttw = find_service(self.context, 'schemas', type_name)
        if ttw is not None:
            return ttw.getSchema()
        return ()
