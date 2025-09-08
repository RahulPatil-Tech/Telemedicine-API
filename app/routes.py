from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import db, bcrypt, socketio
from .models import User, Appointment
from .auth import roles_required
from flask_socketio import emit

main = Blueprint('main', __name__)

# ---------------- WebSocket Events ---------------- #

@socketio.on("doctor_status")
def handle_doctor_status(data):
    """
    Handles real-time doctor status updates via WebSocket
    Example data: {"doctor_id": 1, "status": "online"}
    """
    doctor_id = data.get("doctor_id")
    status = data.get("status")
    emit("doctor_status_update", {"doctor_id": doctor_id, "status": status}, broadcast=True)


# ---------------- REST Endpoints ---------------- #

@main.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [name, email, password, role]
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: mypassword
            role:
              type: string
              enum: [doctor, patient]
              example: patient
    responses:
      201:
        description: User created successfully
      409:
        description: User already exists
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 409
    
    new_user = User(email=email, name=name, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@main.route("/login", methods=["POST"])
def login():
    """
    User Login
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: mypassword
    responses:
      200:
        description: Login successful, returns JWT access token
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401


@main.route("/appointments", methods=["POST"])
@jwt_required()
@roles_required(["patient"])
def create_appointment():
    """
    Create Appointment
    ---
    tags:
      - Appointments
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: "Format: Bearer <JWT>"
      - in: body
        name: body
        schema:
          type: object
          required: [doctor_id]
          properties:
            doctor_id:
              type: integer
              example: 2
            status:
              type: string
              example: scheduled
            timestamp:
              type: string
              format: date-time
              example: "2025-09-08T14:30:00Z"
    responses:
      201:
        description: Appointment created successfully
      401:
        description: Unauthorized (missing or invalid token)
      403:
        description: Forbidden (not a patient)
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    new_appointment = Appointment(
        patient_id=current_user_id,
        doctor_id=data.get("doctor_id"),
        status=data.get("status", "scheduled"),
        timestamp=data.get("timestamp")
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"msg": "Appointment created"}), 201


@main.route("/appointments/my-appointments", methods=["GET"])
@jwt_required()
def get_my_appointments():
    """
    Get My Appointments
    ---
    tags:
      - Appointments
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: "Format: Bearer <JWT>"
    responses:
      200:
        description: List of appointments for the logged-in user
      401:
        description: Unauthorized (missing or invalid token)
      403:
        description: Invalid user role
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role == "patient":
        appointments = user.appointments_as_patient.all()
    elif user.role == "doctor":
        appointments = user.appointments_as_doctor.all()
    else:
        return jsonify({"msg": "Invalid user role"}), 403
    
    return jsonify([
        {
            "id": appt.id,
            "patient_id": appt.patient_id,
            "doctor_id": appt.doctor_id,
            "status": appt.status,
            "timestamp": appt.timestamp
        }
        for appt in appointments
    ]), 200
