from quitter_app.extensions import app, db
from quitter_app.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)