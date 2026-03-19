from flask import Blueprint, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user

from app.extensions import db
from app.models.delivery import Delivery
from app.services.geocoding_services import get_coordinates_from_address
from app.utils.decorators import role_required
from .forms import DeliveryForm

deliveries_bp = Blueprint("deliveries", __name__, url_prefix="/deliveries")

LBS_TO_KG = 0.45359237


@deliveries_bp.route("/")
@role_required("admin", "business_staff")
def delivery_list():
    deliveries = Delivery.query.order_by(Delivery.created_at.desc()).all()
    return render_template("deliveries/delivery_list.html", deliveries=deliveries)


@deliveries_bp.route("/create", methods=["GET", "POST"])
@role_required("admin", "business_staff")
def create_delivery():
    form = DeliveryForm()

    if form.validate_on_submit():
        existing_delivery = Delivery.query.filter_by(
            order_number=form.order_number.data
        ).first()

        if existing_delivery:
            flash("That order number already exists.", "warning")
            return redirect(url_for("deliveries.create_delivery"))

        lat = form.destination_lat.data
        lng = form.destination_lng.data

        if lat is None or lng is None:
            lat, lng = get_coordinates_from_address(form.customer_address.data)

        if lat is None or lng is None:
            flash(
                "Could not find coordinates for that address. Please check the address and try again.",
                "danger"
            )
            return render_template("deliveries/create_delivery.html", form=form)

        package_weight_lbs = form.package_weight.data
        package_weight_kg = float(package_weight_lbs) * LBS_TO_KG

        delivery = Delivery(
            order_number=form.order_number.data,
            customer_name=form.customer_name.data,
            customer_address=form.customer_address.data,
            customer_phone=form.customer_phone.data,
            package_weight=package_weight_kg,
            destination_lat=lat,
            destination_lng=lng,
            created_by_id=current_user.id,
        )

        db.session.add(delivery)
        db.session.commit()

        flash("Delivery created successfully.", "success")
        return redirect(url_for("deliveries.delivery_list"))

    return render_template("deliveries/create_delivery.html", form=form)


@deliveries_bp.route("/geocode")
@role_required("admin", "business_staff")
def geocode_address():
    address = request.args.get("address", "").strip()

    if not address:
        return jsonify({
            "success": False,
            "message": "Address is required."
        }), 400

    lat, lng = get_coordinates_from_address(address)

    if lat is None or lng is None:
        return jsonify({
            "success": False,
            "message": "Could not find that address."
        }), 404

    return jsonify({
        "success": True,
        "lat": lat,
        "lng": lng
    })