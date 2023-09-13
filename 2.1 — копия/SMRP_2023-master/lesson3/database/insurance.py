from sqlalchemy import Column, Text, Integer

from .base_meta import Base


class Insurance(Base):
    __tablename__ = 'Insurance'
    __table_args__ = {'extend_existing': True}

    name = Column(Text(100), nullable=False)
    id = Column(Integer, primary_key=True)
    city = Column(Text(100), nullable=False)

    def __str__(self):
        return f"Страховая компания {self.id}: {self.name} в городе {self.city}"