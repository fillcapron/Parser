from sqlalchemy.orm import Session

from models import tags


def delete_tag(db: Session, tag_id: int):
    return db.query(tags.Query).where(tags.Query.id == tag_id).delete()


def set_tags(db: Session, company_id: int, queries: list[str]):
    array_objects = []

    for query in queries:
        tag = db.query(tags.Query).where(tags.Query.name == query and tags.Query.company_id == company_id).first()

        if not tag:
            array_objects.append(tags.Query(name=query, company_id=company_id))

    db.add_all(array_objects)

