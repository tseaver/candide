import unittest


class CandidePropertysheetTests(unittest.TestCase):

    def setUp(self):
        from pyramid.testing import setUp
        setUp()

    def tearDown(self):
        from pyramid.testing import tearDown
        tearDown()

    def _getTargetClass(self):
        from candide.property import CandidePropertysheet
        return CandidePropertysheet

    def _makeRequest(self):
        from pyramid.testing import DummyRequest
        class DummyContent(object):
            def typeof(self, content):
                return 'Dummy'
        request = DummyRequest()
        request.registry.content = DummyContent()
        return request

    def _makeOne(self, context=None, request=None):
        from pyramid.testing import DummyModel
        if context is None:
            context = DummyModel()
        if request is None:
            request = self._makeRequest()
        return self._getTargetClass()(context, request)

    def test_class_conforms_to_IPropertySheet(self):
        from zope.interface.verify import verifyClass
        from substanced.interfaces import IPropertySheet
        verifyClass(IPropertySheet, self._getTargetClass())

    def test_instance_conforms_to_IPropertySheet(self):
        from zope.interface.verify import verifyObject
        from substanced.interfaces import IPropertySheet
        verifyObject(IPropertySheet, self._makeOne())

    def test_schema_no_service(self):
        ps = self._makeOne()
        self.assertEqual(list(ps.schema), [])

    def test_schema_w_service_no_schema(self):
        from pyramid.testing import DummyModel
        from zope.interface import directlyProvides
        from substanced.interfaces import IFolder
        root = DummyModel()
        directlyProvides(root, IFolder)
        schemas = root['schemas'] = DummyModel()
        context = root['name'] = DummyModel()
        ps = self._makeOne(context)
        self.assertEqual(list(ps.schema), [])

    def test_schema_w_service_w_schema(self):
        from pyramid.testing import DummyModel
        from zope.interface import directlyProvides
        from substanced.interfaces import IFolder
        root = DummyModel()
        directlyProvides(root, IFolder)
        schemas = root['schemas'] = DummyModel()
        directlyProvides(schemas, IFolder)
        schemas.__is_service__ = True
        ttw = schemas['Dummy'] = DummyModel()
        def _getSchema(*args):
            return ['A', 'B', 'C']
        ttw.getSchema = _getSchema
        context = root['name'] = DummyModel()
        ps = self._makeOne(context)
        self.assertEqual(list(ps.schema), ['A', 'B', 'C'])
