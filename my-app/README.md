# Fix Point

Fix Point is a Flask-based queue management prototype for a cellphone repair shop. Customers can view services and join the queue, check their ticket status and the number of people ahead, while staff can manage the waiting list.

## Features

- Join the queue with a name, cellphone number, and selected repair service.
- Receive a numbered ticket and view its status, selected service, and people ahead.
- Automatically refresh ticket status and queue count while the ticket page is open.
- View and filter the staff queue by service.
- Call the next waiting customer, mark customers served, or record a no-show.
- Responsive pages built with Jinja templates, custom CSS, and Bootstrap.

## Project structure

```text
my-app/
├── app.py                 # Flask app, routes, sample services, and in-memory tickets
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html          # Shared page layout and navigation
│   ├── index.html         # Home page
│   ├── join.html          # Customer join-queue form
│   ├── ticket.html        # Customer ticket and live status
│   └── staff.html         # Staff queue dashboard
├── static/
│   ├── css/style.css      # Custom styles
│   └── js/main.js         # Shared client-side JavaScript
└── docs/week3/            # Personas, wireframes, accessibility, and usability documentation
```

## Routes

| Method | URL | Purpose |
|---|---|---|
| `GET` | `/` | Home page with a link to join the queue |
| `GET` | `/join` | Display the customer registration form |
| `POST` | `/join` | Validate customer details and create a ticket |
| `GET` | `/queue/<ticket_id>` | Show a ticket, service, status, and people ahead |
| `GET` | `/queue/<ticket_id>/status.json` | Return the latest ticket status and people-ahead count |
| `POST` | `/queue/<ticket_id>/leave` | Leave the queue |
| `GET` | `/staff` | View the staff dashboard; optionally filter with `?service_id=<id>` |
| `POST` | `/staff/tickets/<ticket_id>/<action>` | Update a ticket with `call`, `serve`, or `no-show` |
| `GET` | `/hello` | Return a simple Flask greeting |

## Run locally

Run these commands from the `my-app` directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat
```

Install dependencies and start the development server:

```bash
pip install -r requirements.txt
flask --app app run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The debug server is for local development only; do not use it to deploy the app publicly.

## Prototype limitations

- Services and tickets are stored in Python lists in `app.py`. Changes are temporary and reset when the server restarts; this prototype does not use a database.
- The staff dashboard has no authentication or authorization. Do not expose it to the public.
- The Flask secret key in `app.py` is a development placeholder and must be replaced with a securely configured secret before deployment.
- The waiting-time text is currently a fixed estimate, not a calculation based on the live queue.

## Project documentation

See [`docs/week3/`](docs/week3/) for the personas, wireframes, design feedback, Lighthouse accessibility results, and usability test summary.
