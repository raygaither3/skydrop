from flask import Blueprint, render_template
from app.extensions import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/create-db")
def create_db():
    db.create_all()
    return "Database tables created."

@main_bp.route("/health")
def health():
    return "ok", 200