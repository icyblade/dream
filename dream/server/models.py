from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Integer, unique=True, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False)

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


class Quota(db.Model):
    type = db.Column(db.String(255), primary_key=True)
    maximum_quota = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Type %s>' % self.type

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
