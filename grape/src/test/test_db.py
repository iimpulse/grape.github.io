"""
Tests related to database availability, creation, and interaction
"""

# This next line disables checking that instance of 'scoped_session'
# has no 'commit' or 'bulk_save_objects' members, The members are there,
# pylint just can't tell
#pylint: disable=E1101

from src.app.model.type_model import TypeModel, TypeSchema
import unittest
from src.test import BaseDBTestCase
from src.app.model.version_model import VersionModel, VersionSchema


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available ? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


class VersionModelTest(BaseDBTestCase):
    """ Test interacting with the provided sqlalchemy definitions """

    def setUp(self):
        self.data = ({"code": "1.0.0", "name": "winecountry"}, {"code": "2.0.0", "name": "winecountry2"})
        versions = [VersionModel(version_code=version["code"], version_name=version["name"]) for version in self.data]
        self.session.bulk_save_objects(versions)
        self.session.commit()

    def test_get_versions(self):
        """ Test getting back all entries """
        versions = VersionModel.query.all()
        self.assertTrue(len(versions) == 2)
        for version in versions:
            serialized = VersionSchema().dump(version)
            self.assertTrue(serialized['version_code'] in [version["code"] for version in self.data])

    def test_get_version_by_name(self):
        """ Test getting an entry by name """
        version = VersionModel.query.filter_by(version_name=self.data[0]["name"]).first()
        self.assertTrue(version is not None)
        self.assertEqual(version.version_name, self.data[0]["name"])

    def test_query_nonexistant_version(self):
        """ Test that getting by non-existant name has no result """
        version = VersionModel.query.filter_by(version_name="notwinecountry").first()
        self.assertEqual(version, None)

    def tearDown(self):
        VersionModel.query.delete()
        self.session.commit()
        self.session.remove()

class TypeModelTest(BaseDBTestCase):
    """ Test interacting with the provided sqlalchemy definitions """

    def setUp(self):
        self.data = ({"id": 1, "name": "String"}, {"id": 3, "name": "Integer"}, {"id": 2, "name": "Float"})
        types = [TypeModel(type_id=type["id"], type_name=type["name"]) for type in self.data]
        self.session.bulk_save_objects(types)
        self.session.commit()

    def test_get_types(self):
        """ Test getting back all entries """
        types = TypeModel.query.all()
        self.assertTrue(len(types) == 3)
        for type in types:
            serialized = TypeSchema().dump(type)
            self.assertTrue(serialized['type_name'] in [type["name"] for type in self.data])

    def test_get_types_by_name(self):
        """ Test getting an entry by name """
        type = TypeModel.query.filter_by(type_name=self.data[0]["name"]).first()
        self.assertTrue(type is not None)
        self.assertEqual(type.type_name, self.data[0]["name"])

    def test_query_nonexistant_type(self):
        """ Test that getting by non-existant name has no result """
        type = TypeModel.query.filter_by(type_name="hashmap").first()
        self.assertEqual(type, None)

    def tearDown(self):
        TypeModel.query.delete()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
