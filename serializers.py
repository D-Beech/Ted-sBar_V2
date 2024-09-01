from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import MenuItem

class MenuItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: MenuItem
        include_relationships = True
        load_instance = True

