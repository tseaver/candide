import unittest


class TTWSchemaTests(unittest.TestCase):

    def _getTargetClass(self):
        from candide.schema import TTWSchema
        return TTWSchema

    def _makeOne(self, yaml=''):
        return self._getTargetClass()(yaml)

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
