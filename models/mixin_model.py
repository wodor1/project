from db import db

class MixinModel():

  @classmethod
  def find_by_attribute(cls, **kwargs):
    return cls.query.filter_by(**kwargs).first()

  @classmethod
  def find_by_id(cls, id):
    return cls.query.get(id)

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()