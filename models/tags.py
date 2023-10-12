from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from .database import Base


class Query(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="tags", cascade="all,delete",)

    posts = relationship("Post", back_populates="tags", cascade="all,delete")
