from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base_meta import Base


class Patient(Base):
    __tablename__ = 'Patient'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(Text(100), nullable=False)
    bdate = Column(Text(10), nullable=False)
    insurance_id = Column(ForeignKey('Insurance.id'), nullable=False)

    insurance = relationship('Insurance')
    doctors = relationship("DoctorPatient", back_populates="patient")

    def __str__(self):
        return f"Пациент {self.id}: {self.name} {self.bdate}"