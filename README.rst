``candide`` README
==================

This application demonstrates defining ``colander`` scheams as
through-the-web (TWW) objects, managed in `SubstanceD <http://substanced.net>`_
Schema definitions are managed as `YAML <http://yaml.org>`_, using the
bindings defined in `sweetpotatopie
<https://github.com/Pylons/sweetpotatopie/>`_.

Defining Schemas
-----------------

In the SubstanceD management interface (SDI), visit the ``schemas`` service,
found in the ZODB root.  For each content type which should have a TTW schema,
add a ``TTWSchema`` object, naming it for the content type (e.g., 'Document').

Edit the 'yaml' property, using the `sweetpotatopie documentation
<https://github.com/Pylons/sweetpotatopie/blob/master/doc/narrative.rst>`_
as a guide.  E.g.::

   !schema
     children:
       - !field.string
         name: title
       - !field.integer
         name: rating
       - !field.float
         name: weight
       - !field.decimal
         name: price
       - !field.boolean
         name: active
       - !field.datetime
         name: expires
       - !field.date
         name: joined

Associating Schemas with Types
------------------------------

Any type which should use a TTW schema needs (for now) to add a propertysheet
to its SubstanceD `@content` registration.  E.g.::


    from candide.property import CandidePropertysheet
    from persistent import Persistent
    from substanced.content import content

    @content(
        'MyType',
        add_view='add_my_type',
        propertysheets = (
            # others...
            ('TTW', CandidePropertysheet), 
        )
    )
    class MyType(Persistent):
        pass


This package defines a 'Document' type which enables such a propertysheet.
