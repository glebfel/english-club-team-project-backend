def convert_sqlalchemy_row_to_dict(row) -> dict:
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d