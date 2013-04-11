import unittest


class TTWSchemaTests(unittest.TestCase):

    def _getTargetClass(self):
        from candide.schema import TTWSchema
        return TTWSchema

    def _makeOne(self, yaml=''):
        return self._getTargetClass()(yaml)

    def test_class_conforms_to_ITTWSchema(self):
        from zope.interface.verify import verifyClass
        from candide.interfaces import ITTWSchema
        verifyClass(ITTWSchema, self._getTargetClass())

    def test_instance_conforms_to_ITTWSchema(self):
        from zope.interface.verify import verifyObject
        from candide.interfaces import ITTWSchema
        verifyObject(ITTWSchema, self._makeOne())

    def test_getSchema_empty(self):
        import colander
        ttw = self._makeOne()
        schema = ttw.getSchema()
        self.assertTrue(isinstance(schema, colander.SchemaNode))
        self.assertEqual(len(list(schema)), 0)

    def test_getSchema_non_empty(self):
        import colander
        ttw = self._makeOne(YAML)
        schema = ttw.getSchema()
        self.assertTrue(isinstance(schema, colander.SchemaNode))
        children = list(schema)
        self.assertEqual(len(children), 2)
        self.assertEqual(children[0].name, 'min')
        self.assertTrue(isinstance(children[0].typ, colander.Float))
        self.assertEqual(children[1].name, 'max')
        self.assertTrue(isinstance(children[1].typ, colander.Float))


YAML = """
--- !schema
    children :
      - !field.float
        name : min
      - !field.float
        name : max
"""


class TTWSchemasTests(unittest.TestCase):

    def _getTargetClass(self):
        from candide.schema import TTWSchemas
        return TTWSchemas

    def _makeOne(self, yaml=''):
        return self._getTargetClass()(yaml)

    def test_class_conforms_to_ITTWSchemas(self):
        from zope.interface.verify import verifyClass
        from candide.interfaces import ITTWSchemas
        verifyClass(ITTWSchemas, self._getTargetClass())

    def test_instance_conforms_to_ITTWSchemas(self):
        from zope.interface.verify import verifyObject
        from candide.interfaces import ITTWSchemas
        verifyObject(ITTWSchemas, self._makeOne())

    def test__sdi_addable___miss(self):
        ttws = self._makeOne()
        self.assertFalse(ttws.__sdi_addable__(None,
                                              {'content_type': 'nonesuch'}))

    def test__sdi_addable___hit(self):
        ttws = self._makeOne()
        self.assertTrue(ttws.__sdi_addable__(None,
                                             {'content_type': 'TTWSchema'}))


class Test_root_created(unittest.TestCase):

    def _callFUT(self, event):
        from candide.schema import root_created
        return root_created(event)

    def _makeEvent(self, root):
        class Event(object):
            def __init__(self, object):
                self.object = object
        return Event(root)

    def test_wo_existing_schemas(self):
        from pyramid.testing import DummyModel
        from candide.schema import TTWSchemas
        root = DummyModel()
        self._callFUT(self._makeEvent(root))
        self.assertTrue(isinstance(root['schemas'], TTWSchemas))

    def test_w_existing_schemas_not_service(self):
        from pyramid.testing import DummyModel
        from substanced.interfaces import IFolder
        from zope.interface import directlyProvides
        from candide.schema import TTWSchemas
        root = DummyModel()
        directlyProvides(root, IFolder)
        schemas = root['schemas'] = DummyModel()
        self._callFUT(self._makeEvent(root))
        self.assertFalse(root['schemas'] is schemas)
        self.assertTrue(isinstance(root['schemas'], TTWSchemas))

    def test_w_existing_schemas_service(self):
        from pyramid.testing import DummyModel
        from zope.interface import directlyProvides
        from substanced.interfaces import IFolder
        root = DummyModel()
        directlyProvides(root, IFolder)
        schemas = root['schemas'] = DummyModel()
        schemas.__is_service__ = True
        self._callFUT(self._makeEvent(root))
        self.assertTrue(root['schemas'] is schemas)
