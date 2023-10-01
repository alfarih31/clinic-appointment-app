from .create_appointment.create_appointment_handler import CreateAppointmentCommand, CreateAppointmentHandler
from .create_clinic.create_clinic_handler import CreateClinicCommand, CreateClinicHandler
from .fulfill_appointment.fulfill_appointment_handler import FulfillAppointmentCommand, FulfillAppointmentHandler
from .register_patient.register_patient_handler import RegisterPatientCommand, RegisterPatientHandler

command_handlers = [CreateClinicHandler, RegisterPatientHandler, CreateAppointmentHandler, FulfillAppointmentHandler]
