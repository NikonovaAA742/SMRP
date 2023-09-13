from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base_meta import Base


class DoctorPatient(Base):
    __tablename__ = 'DoctorPatient'
    __table_args__ = {'extend_existing': True}

    doctor_id = Column(ForeignKey("Doctor.id"), primary_key=True)
    patient_id = Column(ForeignKey("Patient.id"), primary_key=True)

    doctor = relationship("Doctor", back_populates="patients")
    patient = relationship("Patient", back_populates="doctors")


    def __str__(self):
        return f"Страховая компания {self.id}: {self.name} в городе {self.city}"