# Checkpoint 10: Validation testing

Tests were run against the local PostgreSQL database and Flask app. Database
constraint probes ran inside a transaction that was rolled back, so they did
not leave test rows behind. The existing ticket count was 20 before and after
the invalid Flask requests.

| Rule | Layer | How I tested it | What happened |
| :--- | :--- | :--- | :--- |
| Name is required and at most 100 characters (`customers.name`, `String(100)`) | Browser | Checked the join form's `required` and `maxlength="100"` attributes; native validation is enabled. | The browser blocks an empty or overlong name before submission. |
| Contact and service are required by the form; email uses `type="email"` and `maxlength="255"`; phone uses `maxlength="11"` | Browser | Checked the join form fields and contact-toggle behavior against `customers.email` (`String(255)`) and `customers.phone_number` (`String(11)`). | The active contact field and at least one service are required; the browser can provide fast feedback. |
| Name cannot be empty | Flask | `curl -X POST /join` with `name=`, a valid phone, and `service_ids=1` | `400 BAD REQUEST`; no ticket saved. |
| Email must be valid | Flask | `curl -X POST /join` with `contact_method=email`, `email=not-an-email`, a valid name, and `service_ids=1` | `400 BAD REQUEST`; no ticket saved. |
| Name cannot exceed 100 characters | Flask | `curl -X POST /join` with a 200-character name, a valid phone, and `service_ids=1` | `400 BAD REQUEST`; no ticket saved. |
| Selected service must be active | Flask | `curl -X POST /join` with a valid name and phone and inactive `service_ids=3` | `400 BAD REQUEST`; no ticket saved. |
| Service reference must exist (`FOREIGN KEY`) | Database | Inserted a `services_chosen` row with `service_id=999999` and a valid `ticket_id`. | `ERROR: insert or update on table "services_chosen" violates foreign key constraint "services_chosen_service_id_fkey"` |
| Ticket status must be allowed (`CHECK`) | Database | Updated a test ticket to `status='lost'`. | `ERROR: new row for relation "tickets" violates check constraint "ticket_status_valid"` |
| Service name must be unique (`UNIQUE`) | Database | Inserted a second service with the same name as a test service. | `ERROR: duplicate key value violates unique constraint "services_name_key"` |
| Customer name cannot be NULL (`NOT NULL`) | Database | Inserted a customer with `name=NULL`. | `ERROR: null value in column "name" of relation "customers" violates not-null constraint` |
| A service referenced by a ticket cannot be deleted (`ON DELETE RESTRICT`) | Database | Deleted a test service referenced by `services_chosen`. | `ERROR: update or delete on table "services" violates foreign key constraint "services_chosen_service_id_fkey" on table "services_chosen"` |
| Database-generated values on a valid ticket | Database | Inserted a ticket with its required `ticket_code`, `status`, and `customer_id`, then used `RETURNING id, status, created_at`. | Insert succeeded; PostgreSQL generated the `id` and `created_at`. The current schema requires `status` and `ticket_code`, so those were supplied. |
| No SQL built in f-strings | Source check | `git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"` | No matches. |

