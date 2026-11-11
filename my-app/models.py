from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, func, true
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(255), nullable=True)

    tickets = db.relationship("Ticket", back_populates="customer", cascade="all, delete-orphan")


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    estimated_duration = db.Column(db.Integer, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    __table_args__ = (
        CheckConstraint("estimated_duration > 0", name="service_estimated_duration_positive"),
    )

    chosen_services = db.relationship("ServicesChosen", back_populates="service", cascade="all, delete-orphan")
    tickets = db.relationship("Ticket", secondary="services_chosen", viewonly=True)


class Technician(db.Model):
    __tablename__ = "technicians"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    assigned_tickets = db.relationship("Ticket", back_populates="assigned_technician")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_code = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False, default="waiting")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    called_at = db.Column(db.DateTime(timezone=True), nullable=True)
    description = db.Column(db.Text, nullable=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    assigned_technician_id = db.Column(
        db.Integer,
        db.ForeignKey("technicians.id", ondelete="SET NULL"),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'completed', 'no_show', 'left')",
            name="ticket_status_valid",
        ),
    )

    customer = db.relationship("Customer", back_populates="tickets")
    assigned_technician = db.relationship("Technician", back_populates="assigned_tickets")
    photos = db.relationship("DevicePhoto", back_populates="ticket", cascade="all, delete-orphan")
    chosen_services = db.relationship("ServicesChosen", back_populates="ticket", cascade="all, delete-orphan")


class DevicePhoto(db.Model):
    __tablename__ = "device_photos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo = db.Column(db.LargeBinary, nullable=False)
    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )

    ticket = db.relationship("Ticket", back_populates="photos")


class ServicesChosen(db.Model):
    __tablename__ = "services_chosen"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
    )
    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )

    service = db.relationship("Service", back_populates="chosen_services")
    ticket = db.relationship("Ticket", back_populates="chosen_services")


__all__ = [
    "db",
    "Customer",
    "Service",
    "Technician",
    "Ticket",
    "DevicePhoto",
    "ServicesChosen",
]
