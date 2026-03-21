from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email="ray@test.com").first()

    if user:
        user.role = "admin"
        db.session.commit()
        print(f"{user.email} is now an admin.")
    else:
        print("User not found.")