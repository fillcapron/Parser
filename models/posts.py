from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    label = Column(String, index=True)
    link = Column(String)

    tag_id = Column(Integer, ForeignKey("tags.id"))
    tags = relationship("Query", cascade="all,delete", back_populates="posts")
