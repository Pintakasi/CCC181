"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import secrets
import string

from flask import Flask, abort, flash, redirect, render_template, request, url_for

#W4 Imports
from dotenv import load_dotenv
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Customer, Technician, Service, Ticket, ServicesChosen, DevicePhoto, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)



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
    return sum(
        1 for other in TICKETS
        if other["status"] == "waiting"
        and other["number"] < ticket["number"]
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template(
        "ticket.html", ticket=t, service=service, position=people_ahead(t)
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    return {"status": t["status"], "ahead": people_ahead(t)}


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
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
    contact = form.get("contact", "")
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None #dire ko nag end

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if not (
        len(contact) == 11
        and contact.startswith("09")
        and contact.isascii()
        and contact.isdigit()
    ):
        errors["contact"] = "Please enter a valid cellphone number."
    
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        if "contact" in errors:
            flash("Please enter a valid cellphone number", "danger")
        else:
            flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400


    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

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