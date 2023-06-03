from sqlalchemy import VARCHAR, Column, Integer
from app.models.basemodel import BaseModel


class ArticleModel(BaseModel):
    __tablename__ = 'article'

    title = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    content = Column(VARCHAR(5000), nullable=False)
    author = Column(Integer, nullable=False)
    email = Column(VARCHAR(320), nullable=False)
    phone = Column(VARCHAR(15), nullable=True)

    def __repr__(self):
        return f'{self.title} {self.author}'