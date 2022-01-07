"""
    This defines the version table for use with sqlalchemy
"""
# Disable "Too few public methods" check
# pylint: disable=R0903


from sqlalchemy import Column, Integer, String, DateTime
from . import BASE, MA

class VersionModel(BASE):
    """ Keep track of who says hello and when """
    __tablename__ = "versions"
    version_code = Column(String, primary_key=True, unique=True)
    version_name = Column(String, unique=True)
    created = Column(DateTime)

class VersionSchema(MA.SQLAlchemyAutoSchema): # pylint: disable=too-many-ancestors
    """ Creates a serializer from the sqlalchemy model definition """
    class Meta:
        """ Metaclass """
        model = VersionModel
        strict = True
