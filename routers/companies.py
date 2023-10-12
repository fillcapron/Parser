from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from controllers.companies import get_companies, get_company, set_company, update_company, remove_company
from controllers.tags import set_tags
from controllers.posts import save_posts
from models.database import get_db
from models import schemas, companies
from controllers.parser import Parser

router = APIRouter()


@router.get('/', response_model=List[schemas.Company])
def get_companies_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = get_companies(skip=skip, limit=limit, db=db)
    return data


@router.post('/create-company')
def create_company(data = Body(), db: Session = Depends(get_db)):
    if data['name'] and data['description'] and data['tags'] and data['status']:
        set_company(db, name=data['name'], description=data['description'], tags_list=data['tags'], status=data['status'])


@router.patch('/update-company')
def patch_company(data = Body(),  db: Session = Depends(get_db)):
    if data['id'] and data['name'] and data['description'] and data['tags'] and data['status']:
        update_company(
            db, company_id=data['id'], name=data['name'], status=data['status'], description=data['description'],

        )
        set_tags(db=db, company_id=data['id'], queries=data['tags'])
        db.commit()


@router.delete('/delete-company/{company_id}')
def delete_company(company_id: int, db: Session = Depends(get_db)):
    if id:
        remove_company(db=db, company_id=company_id)
        return True
    else:
        return False


@router.get('/{company_id}', response_model=schemas.Company)
def get_company_data(company_id: int, db: Session = Depends(get_db)):
    data = get_company(db, company_id)
    return data


@router.post('/parser-company')
def run_parser_company(data = Body(), db: Session = Depends(get_db)):
    if data['companyId'] and data['queries'] and data['pages']:
        company = get_company(db, data['companyId'])
        if company.name:
            parser = Parser(company.name,  data['queries'], data['pages'])
            posts = parser.parser()

            if len(posts):
                db.query(companies.Company).filter(companies.Company.id == data['companyId']).update({'updated_at': datetime.now()})
                set_tags(db, queries=data['queries'], company_id=data['companyId'])
                save_posts(db, company_id=data['companyId'], posts_with_query=posts)
                db.commit()
                return {"parse": True}
            else:
                return {"parse": False}

    else:
        return {"data": "Error"}
