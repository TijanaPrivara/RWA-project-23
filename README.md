# Before starting, ensure that you have the following prerequisites installed:

python_version: 3.10.11
Git

1. Open git repository
2. Open your terminal or command prompt
3. Change the current working directory to the location where you want to clone the repository
4. Clone the repository using the following command: git clone <repository_url>
5. Change the current working directory to the cloned repository
6. Activate the virtual envirnoment: venv\Scripts\activate
7. Install the required Python packages using the following command: pip install -r requirements.txt
8. Open the .env file and update the MongoDB connection URL and database name according to your setup.
9. Run aplication: uvicorn app:app --reload
10. Open a web browser and visit http://localhost:8000/docs to access the application.

# Database
- MongoDB URI: `mongodb+srv://app:PA4U6EXbJhPadHJW@demo.o2mlker.mongodb.net/`

# Registered user
- username: admin
- password: adminpass1

# Informacije o projektu

Aplikacija je osmišljena kao jednostavno upravljanje projektima. Ovdje su ključne informacije:
- Registracija i Prijava: Korisnici mogu se registrirati i prijaviti. Pristup funkcionalnostima aplikacije omogućen je samo uz ispravne prijavne podatke koji se pohranjuju u bazi.
- Pristup: Prijava s korisničkim imenom `admin` i lozinkom `adminpass1` omogućuje pristup funkcionalnostima.

API Metode:
- `GET /users/me`: Dohvaća osnovne informacije o trenutno prijavljenom korisniku.
- `POST /register/user`: Omogućuje registraciju novog korisnika. Potrebno je unijeti korisničko ime, e-mail i lozinku. E-mail provjerava ispravnost formata, inače vraća grešku "Invalid email format".
- `GET /tasks`: Dohvaća popis svih zadataka (taskova) iz baze zajedno s detaljima.
- `POST /tasks`: Kreira novi zadatak. Potrebna su polja: naslov, opis, prioritet ("low", "regular" ili "high"), status, datum i vrijeme izvršenja te ime projekta.
- `PUT /tasks/{task_id}/status`: Ažurira status zadatka putem ID-a zadatka.
- `DELETE /tasks/{task_id}`: Briše zadatak putem ID-a zadatka.
- `POST /projects/`: Kreira projekte. Potrebna su polja: ime i opis projekta.
- `GET /projects`: Dohvaća popis svih projekata iz baze podataka.
