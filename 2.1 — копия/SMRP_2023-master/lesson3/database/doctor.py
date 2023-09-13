from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm import relationship

from .base_meta import Base


class Doctor(Base):
    __tablename__ = 'Doctor'
    __table_args__ = {'extend_existing': True}

    name = Column(Text, nullable=False)
    id = Column(Integer, primary_key=True)
    #phone = Column(Text, nullable=False)

    patients = relationship("DoctorPatient", back_populates="doctor")

    def __str__(self):
        return f"Врач {self.id}: {self.name}"