import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    status = Column(String, default="Активна")
    description = Column(String)

    tags = relationship("Query", back_populates="company", cascade="all,delete")

    updated_at = Column(DateTime, default=datetime.datetime.now)



