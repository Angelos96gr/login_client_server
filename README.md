This webapp provides a platform for patients to find doctors in the area of Munich. Additionally, doctors can register their practise so that the patient can contact them to book appointments.



The web app supports:

- Creating user accounts with credentials and passwords (hasehd using BLAKE)
- Registering as a doctor
- Accessing a list of registered doctors in the area
- Login/out of the webpage


The web app is based on:
- Backend: Flask for routing, sqlite3 for database handling (python)
- Frontend: HTML w/Jinja templating, CSS for styling and Javascript for client side input validation


The structure of the repository is as follows:
- app.py includes all the flask code
- db_utils.py provides general functionality to enable database interactions (e.g., creating/deleting users, support server-side authentication)
- templates/ folder contains all the static html templates
- static/ folder contains the Javascript-based functionality to check client-side input validation and the CSS styling
- users.db is the sqite3 database including two tables: one for the users and one for doctors
