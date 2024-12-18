from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Uzivatel(db.Model):
    __tablename__ = 'uzivatel'
    id = db.Column(db.Integer, primary_key=True)
    jmeno = db.Column(db.String(100), nullable=False)
    prijmeni = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"<Person {self.jmeno} {self.prijmeni}>"
