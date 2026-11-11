# Part 3: Self-review of your schema

Works well: One thing in the schema that works is that the relationships between tickets, device_photos, customers and technicians are well defined and reviewed thoroughly to match what my functional requirements needed.

**Problem**
- (i) [Coverage] : I missed the column for description in FR-17


- (ii) The tickets table has a service_id foreign key that directly references services.id. This means each ticket can only be associated with one service. If a customer wants to avail of multiple services, they must create a separate ticket for each service.

**Change**
- I added description(Text) column in tickets table in my ERD.
- Updated erd.png (schema.md)
- Updated 2c. Choose types and constraints on purpose Table, Delete Rules, Relationship sentences(schema.md)
- Updated 2b. List your tables and columns

- I created a `services_chosen` table `containing id`, `service_id`, and      `ticket_id` to address Problem (ii). This allows each ticket to be associated with multiple services instead of being limited to just one service.