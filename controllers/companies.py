from sqlalchemy.orm import Session

from models import companies, tags


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(companies.Company).offset(skip).limit(limit).all()


def update_company(
        db: Session, company_id: int, name: str, description: str, status: str = 'Активна'):
    db.query(companies.Company).filter(companies.Company.id == company_id).update(
        {"name": name, "description": description, "status": status})


def remove_company(db: Session, company_id: int):
    res = db.query(companies.Company).filter(companies.Company.id == company_id).first()
    db.delete(res)
    db.commit()

def set_company(db: Session, name: str, description: str, tags_list: list[str], status: str = 'Активна'):
    result_array = []

    try:
        company = companies.Company(name=name, description=description, status=status)
        db.add(company)
        db.flush()

        id = company.id
        print(id)
        if id:
            for tag in tags_list:
                result_array.append(tags.Query(name=tag, company_id=id))

        db.add_all(result_array)
        db.commit()


    except ExceptionGroup as e:
        print(e)


def get_company(db: Session, company_id: int):
    return db.query(companies.Company).get(company_id)
