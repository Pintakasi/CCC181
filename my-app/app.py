"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, render_template, request, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

# Sample data for the demo. A real app would load this from a database later.
SERVICES = [
    {"id": 0, "name": "Device Checkup"},
    {"id": 1, "name": "Screen Replacement"},
    {"id": 2, "name": "Battery Replacement"},
    {"id": 3, "name": "Charging Port Repair"},
    {"id": 4, "name": "LCD and Touchscreen Repair"},
    {"id": 5, "name": "Camera Repair or Replacement"},
    {"id": 6, "name": "Speaker and Microphone Repair"},
    {"id": 7, "name": "Power Button and Volume Button Repair"},
    {"id": 8, "name": "Water Damage Repair"},
    {"id": 9, "name": "Motherboard Repair"},
]

# Each ticket: number, name, email, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"ticket_id": 1, "name": "Theo", "Contact No.": "09099143656", "service_id": 2, "status": "waiting"},
    {"ticket_id": 2, "name": "Jian", "Contact No.": "09353660678", "service_id": 9, "status": "called"},
    {"ticket_id": 3, "name": "Rey", "Contact No.": "09353560634", "service_id": 1, "status": "called"},
]


def get_ticket_by_id(ticket_id):
    for ticket in TICKETS:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return None


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Rey", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    ticket_data = get_ticket_by_id(ticket_id)
    if ticket_data is None:
        abort(404)
    return render_template("ticket.html", ticket=ticket_data)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)

#Added 

@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})

@app.post("/join")
def join():
    form = request.form
    contact = form.get("contact", "")
    service_id = form.get("service_id", type=int)

    errors = {}
    if not (
        len(contact) == 11
        and contact.startswith("09")
        and contact.isascii()
        and contact.isdigit()
    ):
        errors["contact"] = "Please enter a valid cellphone number."
    # if "@" not in email:
    #     errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        if "contact" in errors:
            flash("Please enter a valid cellphone number", "danger")
        else:
            flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.route("/staff")
def staff_dashboard():
    return render_template("staff.html")