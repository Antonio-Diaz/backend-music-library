def check_if_exists_field(db, model, field, value):
    return db.query(model).filter(field == value).first()
