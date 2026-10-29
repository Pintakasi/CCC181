# Fix Point requirements

**Setting:** Cellphone repair shop, business, 8:00 am - 5:00 pm  on weekdays


**People who wait:** Rey, a third-year BS IT student from Iligan City who needs cellphone repair from a trusted shop in Cagayan de Oro ([persona](personas/personas.md#rey-the-person-waiting))


**People who serve:** Winston, a cellphone technician who runs his repair shop and manages customer inquiries and repairs ([persona](personas/personas.md#winston-the-staff-member)).

**Problem statements:**
- Rey needs a way to check the queue, join it, and track his place remotely because he wants to know whether he can be served before spending time and money traveling from Iligan City to Cagayan de Oro.
- Winston needs a way to organize the queue and quickly notify the next customer while he is repairing phones because repeated wait-time questions and a crowded shop interrupt his work and can cause customers to leave.

# Functional Requirements

| ID | Requirement | Priority | Stores data? | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 | A customer can join the queue by entering their name, phone number and choosing a service type. | Must | **Yes** | Built(Week3)|
| FR-02 | A customer can see their ticket number, status, service chosen, how many people are ahead of them and estimated waiting time. |Must|**Yes**| Built(week3) |
| FR-03 | Customers can choose to leave the queue | Must |**Yes**| Built(Week3) |
| FR-04 | The technician can call the next waiting ticket for a service | Must |**Yes**| Built(Week3) |
| FR-05 | The technician can mark a ticket as no-show(Customer did not arrive) or Served/Completed | Must |**Yes**| Built(Week3)|
| FR-06 | The technician can Filter Tickets by services | Must |**No**| Built(Week3) |
| FR-07 | The technician can see all the customer's Ticket ID, Name, Service, and Status  | Must |**Yes**| Built(Week3) |
|★FR-08|Technician can manually add a walk-in customer to the queue|Must|**Yes**|This Week|
|★FR-09|Customer can re-access "My Place" by their Ticket ID.|Must|**No**|This Week|
|FR-10|Customer can see if the shop is open Today|Must|**No**|This Week|
|FR-11|Customer can see shop address in Join|Must|**No**|LATER|
|FR-12|Technician can see waiting count|Must|**No**|LATER|
|FR-13|Technician can login using an account|Must|**Yes**|This Week|
| FR-14 | Assigning a customer to a technician(maybe Winston hires an assistant) & Customers can choose a preffered technician| Could |**Yes**| LATER |
| FR-15 | In join screen, the customers can see current number of people waiting  | Could |**No**| LATER |
|FR-16| System auto notifies the customer when called via SMS |Won't|**Yes**| --------  |
|★FR-17| Customer can send picture about their device’s state and concern | Must | **Yes** | This Week |

### Non-functional requirements


| ID | Requirement | Category | Priority |
| :--- | :--- | :--- | :--- |
| NFR-01 | Every confirmed ticket and ticket status change remains available after the app or database restarts; no confirmed queue record is lost. | Data integrity | Must |
| NFR-02 | When  customers join at the same time, each receives a distinct ticket number and exactly one ticket is created for each successful submission. | Data integrity | Must |
| NFR-03 | The Join, My Place, and staff queue pages load within 2 seconds with 10 concurrent users on a mobile connection. | Performance | Should |
| NFR-04 | Every customer and staff screen scores at least 90 in Lighthouse Accessibility, and all forms and queue actions can be completed using a keyboard. | Accessibility | Must |
| NFR-05 | At a 375-pixel-wide mobile viewport, all screens have no horizontal page scrolling and every interactive control is at least 44 by 44 pixels. | Usability | Must |
| NFR-06 | Unauthenticated users cannot view the staff dashboard or change ticket statuses; verify that requests to staff pages and actions are denied until staff login. | Security | Must |
| NFR-07 | A customer's cellphone number is never shown on public pages or returned by public status endpoints. | Privacy | Must |

### MVP

**MVP IDs:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-07, FR-08, FR-09, FR-13.

This is the smallest version that lets customers join the queue, retrieve and track their tickets, and leave if needed, while giving the technician the tools to manage both online and walk-in customers. Staff login protects the management functions.

### Out of scope

- **FR-14 — Technician assignment and customer technician preferences:** This semester's MVP focuses on one technician managing customers. 
- **FR-16 — Automatic SMS notifications:** This requires an external SMS provider, additional cost and configuration, so customers will use My Place to check their ticket status instead.



[Real person who checked my list screenshot](screenshots/person-checked-my-FR-list.png)

|Who|What they said| What changed|
| :--- | :--- | :--- |
|Customer(needs repair service for her device)|"A feature that is missing is Customer can send picture about their device’s state and concern, so technician can assess it even if customer is not yet around., ID 8,9, 10  matters me the most and overall, I see nothing wrong"| Added FR-17 (Should)|
