"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import re
import secrets
import string
from datetime import timedelta, timezone

from flask import Flask, abort, flash, redirect, render_template, request, url_for

#W4 Imports
from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from models import Customer, Technician, Service, Ticket, ServicesChosen, DevicePhoto, db

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)
PH_TIME = timezone(timedelta(hours=8))

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 26, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""



@app.cli.command("seed")
def seed():
    """Add the starting repair services if they are not there yet."""
    starting = [
        ("Device Checkup", 15),
        ("Screen Replacement", 60),
        ("Battery Replacement", 45),
        ("Charging Port Repair", 60),
        ("LCD and Touchscreen Repair", 90),
        ("Camera Repair or Replacement", 45),
        ("Speaker and Microphone Repair", 45),
        ("Power Button and Volume Button Repair", 45),
        ("Water Damage Repair", 120),
        ("Motherboard Repair", 120),
    ]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, estimated_duration=minutes))
    db.session.commit()
    print("Services are ready.")



def people_ahead(ticket):
    return db.session.scalar(
        db.select(func.count(Ticket.id)).where(
            Ticket.status == "waiting",
            Ticket.id < ticket.id,
        )
    )


def estimated_wait_minutes(ticket):
    return db.session.scalar(
        db.select(func.coalesce(func.sum(Service.estimated_duration), 0))
        .join(ServicesChosen, ServicesChosen.service_id == Service.id)
        .join(Ticket, Ticket.id == ServicesChosen.ticket_id)
        .where(
            Ticket.status == "waiting",
            Ticket.id < ticket.id,
        )
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template(
        "ticket.html",
        ticket=t,
        services=[chosen.service for chosen in t.chosen_services],
        ahead=people_ahead(t),
        estimated_wait_minutes=estimated_wait_minutes(t),
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {
        "status": t.status,
        "ahead": people_ahead(t),
        "estimated_wait_minutes": estimated_wait_minutes(t),
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = db.session.get(Ticket, ticket_id)
    if t is None:
        abort(404)
    t.status = "left"
    db.session.commit()
    flash("You have left the queue.", "success")
    return redirect(url_for("index"))


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)

#Added 

#Retrieves all services ordered by name from database
def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()

#Serves the join.html when a client requests for GET /join
@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})



@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    contact_method = form.get("contact_method", "phone")
    contact = (
        form.get("email", "").strip()
        if contact_method == "email"
        else form.get("contact", "").strip()
    )
    description = form.get("message", "").strip()
    selected_services = form.getlist("service_ids")
    uploaded_photos = [photo for photo in request.files.getlist("photos") if photo.filename]

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    elif len(name) > 100:
        errors["name"] = "Name must be 100 characters or fewer."
    if contact_method == "email":
        local_part = contact.partition("@")[0]
        if (
            len(contact) > 255
            or not EMAIL_PATTERN.fullmatch(contact)
            or len(local_part) > 64
            or ".." in local_part
            or local_part.startswith(".")
            or local_part.endswith(".")
        ):
            errors["email"] = "Enter a valid email address."
    elif contact_method != "phone" or not (
        len(contact) == 11
        and contact.startswith("09")
        and contact.isascii()
        and contact.isdigit()
    ):
        errors["contact"] = "Please enter a valid cellphone number."

    service_ids = []
    try:
        if not selected_services or any(
            not value.isascii() or not value.isdecimal()
            for value in selected_services
        ):
            raise ValueError
        service_ids = list(dict.fromkeys(int(value) for value in selected_services))
    except ValueError:
        errors["services"] = "Choose at least one valid service."

    services = (
        db.session.scalars(db.select(Service).where(Service.id.in_(service_ids))).all()
        if service_ids
        else []
    )
    if service_ids and len(services) != len(service_ids):
        errors["services"] = "Choose valid services from the list."

    if any(not photo.mimetype or not photo.mimetype.startswith("image/") for photo in uploaded_photos):
        errors["photos"] = "Upload image files only."

    if errors:
        if "email" in errors:
            flash(errors["email"], "danger")
        elif "contact" in errors:
            flash("Please enter a valid cellphone number", "danger")
        else:
            flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors=errors,
            selected_services=selected_services,
        ), 400

    if db.session.get(Technician, 1) is None:
        app.logger.error("Cannot create ticket: technician id 1 is not present.")
        errors["form"] = "Ticketing is temporarily unavailable. Please try again later."
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors=errors,
            selected_services=selected_services,
        ), 503

    photo_data = [photo.read() for photo in uploaded_photos]
    try:
        if contact_method == "email":
            normalized_email = contact.lower()
            customer = db.session.scalar(
                db.select(Customer)
                .where(func.lower(Customer.email) == normalized_email)
                .order_by(Customer.id)
                .limit(1)
            )
        else:
            normalized_email = None
            customer = db.session.scalar(
                db.select(Customer)
                .where(Customer.phone_number == contact)
                .order_by(Customer.id)
                .limit(1)
            )
        if customer is None:
            customer = Customer(
                name=name,
                phone_number=contact if contact_method == "phone" else None,
                email=normalized_email,
            )
            db.session.add(customer)
            db.session.flush()
        else:
            customer.name = name
            if normalized_email is not None:
                customer.email = normalized_email

        new_ticket = Ticket(
            ticket_code=generate_ticket_code(),
            status="waiting",
            description=description or None,
            customer_id=customer.id,
            assigned_technician_id=1,
        )
        db.session.add(new_ticket)
        db.session.flush()

        db.session.add_all(
            ServicesChosen(service_id=service.id, ticket_id=new_ticket.id)
            for service in services
        )
        db.session.add_all(
            DevicePhoto(photo=data, ticket_id=new_ticket.id)
            for data in photo_data
        )
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        app.logger.exception("Failed to save a new customer ticket.")
        errors["form"] = "We could not save your ticket. Please try again."
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors=errors,
            selected_services=selected_services,
        ), 500

    flash(f"You joined the queue. Your ticket code is {new_ticket.ticket_code}.", "success")
    return redirect(url_for("ticket", ticket_id=new_ticket.id))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    service_ids = {service["id"] for service in SERVICES}
    if service_id is not None and service_id not in service_ids:
        abort(404)

    queue = sorted(
        (ticket for ticket in TICKETS if ticket["status"] in ("waiting", "called")),
        key=lambda ticket: ticket["number"],
    )
    if service_id is not None:
        queue = [ticket for ticket in queue if ticket["service_id"] == service_id]

    waiting_by_service = {
        service["id"]: sum(
            ticket["service_id"] == service["id"] and ticket["status"] == "waiting"
            for ticket in TICKETS
        )
        for service in SERVICES
    }
    names = {service["id"]: service["name"] for service in SERVICES}
    next_ticket = next((ticket for ticket in queue if ticket["status"] == "waiting"), None)
    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names=names,
        selected=service_id,
        next_ticket=next_ticket,
        waiting_by_service=waiting_by_service,
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    ticket_data = next((ticket for ticket in TICKETS if ticket["number"] == ticket_id), None)
    if ticket_data is None or new_status is None:
        abort(404)

    ticket_data["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    service_id = request.form.get("service_id", type=int)
    redirect_args = {"service_id": service_id} if service_id is not None else {}
    return redirect(url_for("staff_dashboard", **redirect_args))



#Helper function: Generates generate a cryptographically secure random 8-character string.

def generate_ticket_code():
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(8))