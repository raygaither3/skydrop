from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from app.extensions import db
from app.models.user import User
from app.utils.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/users")
@role_required("admin")
def user_list():
    users = User.query.order_by(User.name.asc()).all()
    return render_template("admin/user_list.html", users=users)


@admin_bp.route("/users/<int:user_id>/make-admin")
@role_required("admin")
def make_admin(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Your account is already managing this page.", "info")
        return redirect(url_for("admin.user_list"))

    user.role = "admin"
    db.session.commit()

    flash(f"{user.email} is now an admin.", "success")
    return redirect(url_for("admin.user_list"))


@admin_bp.route("/users/<int:user_id>/make-staff")
@role_required("admin")
def make_staff(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot change your own role here.", "warning")
        return redirect(url_for("admin.user_list"))

    user.role = "business_staff"
    db.session.commit()

    flash(f"{user.email} is now business staff.", "success")
    return redirect(url_for("admin.user_list"))