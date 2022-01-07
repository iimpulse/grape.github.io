"""
Tests related to database model Class availability, creation, and interaction
"""

# This next line disables checking that instance of 'scoped_session'
# has no 'commit' or 'bulk_save_objects' members, The members are there,
# pylint just can't tell
#pylint: disable=E1101

from src.app.model.version_model import VersionModel
from src.app.model.module_model import ModuleModel
from src.app.model.class_model import ClassModel, ClassSchema
import unittest
from src.test import BaseDBTestCase
from datetime import date


class DbConnectionTest(BaseDBTestCase):
    """ Is the database available ? """

    def test_db(self):
        """ Smoke test """
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)

class ClassModelTest(BaseDBTestCase):
    """ Test interacting with the provided sqlalchemy definitions """

    def setUp(self):
        self.class_data = ({"id": 1, "name": "Class1", "description": "some desc", "module_id": 1}, 
        {"id": 3, "name": "Class2", "description": "some description", "module_id": 2},{"id": 4, "name": "Class3", "description": "some description", "module_id": 1})
        self.module_data = ({"id": 1, "name": "WineModule", "created": date.today(), "version": 1}, {"id": 2, "name": "WineModuleExtra", "created": date.today(), "version": 2},
        {"id": 3, "name": "WineModuleExtraWine", "created": date.today(), "version": 1})
        self.version_data = ({"code": "1.0.0", "name": "winecountry"}, {"code": "2.0.0", "name": "winecountry2"})
        self.method_data = ({"method_id": 1, "method_name": "method1", "htc": 10.0, "ftc": 30.0, "desc": "somedesc", "created": date.today(),
        "version_id": 1, 
        })
        classes = [ClassModel(class_id=classObj["id"], class_name=classObj["name"], description=classObj["description"], module_id=classObj["module_id"]) for classObj in self.class_data]
        modules = [ModuleModel(module_id=module["id"], module_name=module["name"], created=module["created"], version_id=module["version"]) for module in self.module_data]
        versions = [VersionModel(version_code=version["code"], version_name=version["name"]) for version in self.version_data]
        self.session.bulk_save_objects(versions)
        self.session.bulk_save_objects(classes)
        self.session.bulk_save_objects(modules)
        self.session.commit()

    def test_get_types(self):
        """ Test getting back all entries """
        classes = ClassModel.query.all()
        self.assertTrue(len(classes) == 3)
        for classObj in classes:
            serialized = ClassSchema().dump(classObj)
            self.assertTrue(serialized['class_name'] in [classObj["name"] for classObj in self.class_data])

    def test_get_class_by_module_id(self):
        """ Test getting an entry by name """
        classObj = ClassModel.query.filter_by(module_id=1).first()
        self.assertTrue(classObj is not None)
        self.assertEqual(classObj.class_name, self.class_data[0]["name"])

    def test_get_all_classes_by_module_and_version(self):
        """ Test that getting all classes by module and version """
        classes = ClassModel.query.filter(ClassModel.module.has(ModuleModel.version.has(VersionModel.version_code=="1.0.0")))
        self.assertTrue(classes is not None)
        self.assertEqual(classes[0].class_name, self.class_data[0]["name"])

    def tearDown(self):
        ClassModel.query.delete()
        VersionModel.query.delete()
        ModuleModel.query.delete()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
