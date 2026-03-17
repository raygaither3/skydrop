from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class DeliveryForm(FlaskForm):
    order_number = StringField(
        "Order Number",
        validators=[DataRequired(), Length(max=50)]
    )

    customer_name = StringField(
        "Customer Name",
        validators=[DataRequired(), Length(max=100)]
    )

    customer_address = StringField(
        "Customer Address",
        validators=[DataRequired(), Length(max=200)]
    )

    customer_phone = StringField(
        "Customer Phone",
        validators=[DataRequired(), Length(max=30)]
    )

    package_weight = DecimalField(
        "Package Weight (kg)",
        validators=[DataRequired()]
    )

    destination_lat = DecimalField(
        "Destination Latitude",
        places=6
    )

    destination_lng = DecimalField(
        "Destination Longitude",
        places=6
    )

    submit = SubmitField("Create Delivery")