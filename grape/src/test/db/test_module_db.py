"""
Tests related to database model Module availability, creation, and interaction
"""

# This next line disables checking that instance of 'scoped_session'
# has no 'commit' or 'bulk_save_objects' members, The members are there,
# pylint just can't tell
#pylint: disable=E1101

import unittest
from src.app.model.module_model import ModuleSchema
from src.app.model.module_model import ModuleModel
from src.app.model.version_model import VersionModel
from src.test import BaseDBTestCase
from datetime import date


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available ? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)

class ModuleModelTest(BaseDBTestCase):
    """ Test interacting with the provided sqlalchemy definitions """

    def setUp(self):
        self.module_data = ({"id": 1, "name": "WineModule", "created": date.today(), "version": 1}, {"id": 2, "name": "WineModuleExtra", "created": date.today(), "version": 2},
        {"id": 3, "name": "WineModuleExtraWine", "created": date.today(), "version": 1})
        self.version_data = ({"code": "1.0.0", "name": "winecountry"}, {"code": "2.0.0", "name": "winecountry2"})
        modules = [ModuleModel(module_id=module["id"], module_name=module["name"], created=module["created"], version_id=module["version"]) for module in self.module_data]
        versions = [VersionModel(version_code=version["code"], version_name=version["name"]) for version in self.version_data]
        self.session.bulk_save_objects(modules)
        self.session.bulk_save_objects(versions)
        self.session.commit()

    def test_get_modules(self):
        """ Test getting back all entries """
        modules = ModuleModel.query.all()
        self.assertTrue(len(modules) == 3)
        for module in modules:
            serialized = ModuleSchema().dump(module)
            self.assertTrue(serialized['module_name'] in [module_data["name"] for module_data in self.module_data])

    def test_get_module_by_name(self):
        """ Test getting an entry by name """
        module = ModuleModel.query.filter_by(module_name=self.module_data[0]["name"]).first()
        self.assertTrue(module is not None)
        self.assertEqual(module.module_name, self.module_data[0]["name"])

    def test_query_nonexistant_module(self):
        """ Test that getting by non-existant name has no result """
        module = ModuleModel.query.filter_by(module_id=4).first()
        self.assertEqual(module, None)

    def tearDown(self):
        ModuleModel.query.delete()
        VersionModel.query.delete()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
