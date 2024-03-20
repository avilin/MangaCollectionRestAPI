from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def save_model_to_db(model) -> None:
    db.session.add(model)
    db.session.commit()

def delete_model_from_db(model) -> None:
    db.session.delete(model)
    db.session.commit()