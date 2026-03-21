from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import User, HighwayNode, HighwayEdge, NoFlyZone

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/health")
def health():
    return "ok", 200


