from app import login_manager
from app.model.user import User


@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=int(userid)).first()
    return user