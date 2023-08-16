from mongoengine import Document, StringField, BooleanField, FloatField, EmbeddedDocumentField, \
    EmbeddedDocument, ListField, IntField, ReferenceField
from utils.helper import current_date


class Image(EmbeddedDocument):
    public_id = StringField(required=True)
    url = StringField(required=True)


class Review(EmbeddedDocument):
    name = StringField(required=False)
    email = StringField(required=False)
    rating = FloatField(required=False, default=0)
    comment = StringField(default='')


class Products(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    rating = FloatField(default=0.0)
    images = ListField(EmbeddedDocumentField(Image))
    colors = ListField(required=True)
    sizes = ListField(required=True)
    company = StringField(required=True)
    category = StringField(required=True)
    stock = IntField(required=True, default=0)
    numberOfReviews = IntField(required=True, default=0)
    reviews = ListField(EmbeddedDocumentField(Review))
    shipping = BooleanField(default=True)
    featured = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = ReferenceField('Users', required=True)
    createdAt = StringField(required=True, default=current_date())
