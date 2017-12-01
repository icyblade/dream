from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    recv = db.Column(db.String(255), unique=True, nullable=False)
    send = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %s>' % self.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Config(db.Model):
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Key %s>' % self.key

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
