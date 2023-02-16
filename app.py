from quitter_app.extensions import *
from quitter_app.main.routes import main
from quitter_app.auth.routes import auth
from datetime import datetime

# app.register_blueprint(main)
# app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)