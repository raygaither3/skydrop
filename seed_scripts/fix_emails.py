from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        if user.email:
            user.email = user.email.strip().lower()
    db.session.commit()
    print("Done. Emails normalized.")