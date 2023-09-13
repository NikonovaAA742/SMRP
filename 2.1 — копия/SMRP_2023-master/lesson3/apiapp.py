import uvicorn
from fastapi import FastAPI

from lesson3.database import global_init, create_session, Patient, Insurance, Doctor, insurance, DoctorPatient

app = FastAPI()
global_init("database/db.db")

@app.get("/insurances")
def get_insurance():
    session = create_session()
    with session.begin():
        p = session.query(Insurance).all()
    session.remove()
    return p


@app.post("/insurances/{insurance_id}")
def change_insurance_name(insurance_id: int, new_name: str):
    session = create_session()
    with session.begin():
        updinsurance = session.query(Insurance).get(insurance_id)
    updinsurance.name = new_name
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": updinsurance}

@app.post("/insurances/")
def create_insurance(new_name: str, new_city: str):
    session = create_session()
    new_insurance = Insurance(name=new_name, city=new_city)
    with session.begin():
        session.add(new_insurance)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": new_insurance}

@app.delete("/insurances/{insurance_id}")
def delete_insurance(insurance_id: int):
    session = create_session()
    with session.begin():
        delinsurance = session.query(Insurance).get(insurance_id)
        session.delete(delinsurance)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": "deleted"}
#===================================================
@app.get("/doctors")
def get_doctor():
    session = create_session()
    with session.begin():
        k = session.query(Doctor).all()
    session.remove()
    return k

@app.post("/doctors/{doctors_id}")
def change_doctor_name(doctor_id: int, new_name: str):
    session = create_session()
    with session.begin():
        upddoctor = session.query(Doctor).get(doctor_id)
    upddoctor.name = new_name
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": upddoctor}

@app.post("/doctors/")
def create_doctor(new_name: str):
    session = create_session()
    new_doctor = Doctor(name=new_name)
    with session.begin():
        session.add(new_doctor)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": new_doctor}

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    session1 = create_session()

    with session1.begin():
        session1.query(DoctorPatient).filter(DoctorPatient.doctor_id == doctor_id).delete(synchronize_session='fetch')
    session1.commit()
    session1.close()
    session1.remove()
    session = create_session()
    with session.begin():
        deldoctor = session.query(Doctor).get(doctor_id)
        session.delete(deldoctor)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": "deleted"}

#==========================================

@app.get("/patients")
def get_patient():
    session = create_session()
    with session.begin():
        f = session.query(Patient).all()
    session.remove()
    return f

@app.post("/patients/{patients_id}")
def change_patient_name(patient_id: int, new_name: str):
    session = create_session()
    with session.begin():
        updpatient = session.query(Patient).get(patient_id)
    updpatient.name = new_name
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": updpatient}

@app.post("/patients/")
def create_patient(new_name: str, new_bdate: str, insurance_id: int):
    session = create_session()
    new_patient = Patient(name=new_name, bdate=new_bdate, insurance_id=insurance_id)
    with session.begin():
        session.add(new_patient)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": new_patient}

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    session1 = create_session()

    with session1.begin():
        session1.query(DoctorPatient).filter(DoctorPatient.patient_id == patient_id).delete(synchronize_session='fetch')
    session1.commit()
    session1.close()
    session1.remove()
    session = create_session()
    with session.begin():
        delpatient = session.query(Patient).get(patient_id)
        session.delete(delpatient)
    session.commit()
    session.close()
    session.remove()
    return {"status": 200, "data": "deleted"}

if __name__ == '__main__':
    uvicorn.run(app, log_level="debug")


