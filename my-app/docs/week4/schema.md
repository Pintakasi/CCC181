# Week 4: Nouns in the Requirements

The table below includes every functional requirement marked **Stores data? = Yes** in [Week 3 requirements](../week3/requirements.md). Bold text in each requirement identifies its nouns. The table/column mappings are proposed candidates for the data model.

| Req ID | Requirement | Nouns | Table or column? |
| :--- | :--- | :--- | :--- |
| FR-01 | A **customer** can join the **queue** by entering their **name**, **phone number** and choosing a **service type**. | customer, queue, name, phone number, service type | `customers`; `customers.name`; `customers.phone_number`; `services`; `tickets.customer_id`; `tickets.service_id`; queue is not a table |
| FR-02 | A **customer** can see their **ticket number**, **status**, **service** chosen, how many **people** are ahead of them and estimated **waiting time**. | customer, ticket number, status, service, people, waiting time | `tickets.ticket_number`; `tickets.status`; `tickets.service_id`; people ahead and estimated waiting time are computed, not stored |
| FR-03 | **Customers** can choose to leave the **queue**. | customers, queue | `tickets.status` (for example, `left`) and `tickets.left_at`; queue is not a table |
| FR-04 | The **technician** can call the next waiting **ticket** for a **service**. | technician, ticket, service | `staff_accounts`; `tickets.status` and `tickets.called_at`; `tickets.service_id`; next ticket is selected from waiting tickets ordered by `created_at` |
| FR-05 | The **technician** can mark a **ticket** as no-show (**Customer** did not arrive) or Served/Completed. | technician, ticket, customer, no-show, Served/Completed | `staff_accounts`; `tickets.status` (for example, `no_show` or `completed`) and corresponding status-change timestamps; customer is associated through `tickets.customer_id` |
| FR-07 | The **technician** can see all the **customer's Ticket ID**, **Name**, **Service**, and **Status**. | technician, customer, Ticket ID, Name, Service, Status | `staff_accounts`; `tickets.id`; `customers.name`; `tickets.service_id` (service name from `services`); `tickets.status` |
| FR-08 | **Technician** can manually add a walk-in **customer** to the **queue**. | technician, customer, queue | `staff_accounts`; `customers`; `tickets` with `tickets.source` set to `walk_in`; queue is not a table |
| FR-13 | **Technician** can login using an **account**. | technician, account | `staff_accounts` (for example, `username` and `password_hash`) |
| FR-14 | Assigning a **customer** to a **technician** (maybe Winston hires an assistant) & **Customers** can choose a preffered **technician** | customer, technician | `tickets.assigned_technician_id`; `customers.preferred_technician_id`; technicians represented by `staff_accounts` |
| FR-16 | **System** auto notifies the **customer** when called via **SMS** | system, customer, SMS | `sms_notifications` (for example, `ticket_id`, `sent_at`, and delivery status); recipient can be associated with `customers.phone_number` |
| FR-17 | **Customer** can send **picture** about their **device's state** and **concern** | customer, picture, device, state, concern | `ticket_photos` (for example, `ticket_id`, `image_path`, `device_state`, `concern`, and `uploaded_at`); ticket links to its customer |

## Modeling notes

- The **queue is not a table**. It is the set of tickets with `status = waiting` for a service, ordered by `created_at`.
- Store facts, not results: record when a ticket was created or its status changed, and compute the number of people ahead and estimated waiting time when requested.
- `customers`, `services`, `tickets`, and `staff_accounts` are proposed entities. The `sms_notifications` and `ticket_photos` tables support the corresponding requirements if those features are implemented.