from mongoengine import Document, StringField, BooleanField, FloatField, EmbeddedDocumentField, \
    EmbeddedDocument, ListField, IntField, ReferenceField
from utils.helper import current_date, current_date_time


class ShippingInformation(EmbeddedDocument):
    address = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)
    pinCode = StringField(required=True)
    phoneNumber = StringField(required=True)


class Items(EmbeddedDocument):
    name = StringField(required=True)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    image = StringField(required=True)
    color = StringField(required=True)
    size = StringField(required=True)
    product = ReferenceField('Products', required=True)


class User(EmbeddedDocument):
    name = StringField(required=True)
    email = StringField(required=True)


class PaymentInformation(EmbeddedDocument):
    id = StringField(required=True)
    status = StringField(required=True, default='pending')


class Orders(Document):
    shippingInfo = EmbeddedDocumentField(ShippingInformation)
    orderItems = ListField(EmbeddedDocumentField(Items))
    user = EmbeddedDocumentField(PaymentInformation)
    paymentInfo = EmbeddedDocumentField(PaymentInformation)
    paidAt = StringField(required=True, default=current_date_time())
    itemsPrice = FloatField(required=True)
    shippingPrice = FloatField(required=True, default=0.00)
    totalPrice = FloatField(required=True)
    orderStatus = StringField(required=True, default='processing')
    deliveredAt = StringField()
    createdAt = StringField(required=True, default=current_date())
    updatedAt = StringField(required=True, default=current_date())
    is_active = BooleanField(default=True, required=True)
    taxPrice = FloatField(default=0.00)

