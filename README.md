# 🧾 Online Bursary Application System

This is a web application that enables students to apply for bursaries **online** without the need to submit documents physically. The platform categorizes bursaries by **County**, **Constituency**, and **Ward** levels, enforcing application rules specific to each category.

---

## 🌐 Features

### 🎓 For Students

* Register, log in, and apply for bursaries.
* **County-level bursaries**: Open to students from any ward or constituency within the county.
* **Constituency-level bursaries**: Restricted to students from a specific constituency, regardless of their ward.
* **Ward-level bursaries**: Restricted to students residing in the specific ward.
* Students can **only apply once** to any given bursary.
* Document submission is handled digitally—no physical documents required.

### 🛡️ For Admins

* **CRUD operations**: Create, update, delete, and manage bursary categories (County, Constituency, Ward).
* **Application Review**: View all bursary applications.
* **Approval Workflow**:

  * Review submitted supporting documents.
  * **Approve** or **cancel** applications based on document verification.
* Manage user accounts and monitor system usage.

---

## 🛠️ Tech Stack

* **Backend**: Python, Django
* **Frontend**: HTML5, CSS, Bootstrap
* **Forms**: Django Crispy Forms with Bootstrap 5 integration
* **Database**: PostgreSQL (via `psycopg2`)

---

## 📦 Required Packages

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```txt
asgiref==3.7.2
chardet==5.2.0
crispy-bootstrap5==2024.2
dj-database-url==2.1.0
Django==5.0.3
django-crispy-forms==2.1
django-filter==24.2
gunicorn==22.0.0
packaging==24.0
pillow==10.2.0
psycopg2==2.9.9
psycopg2-binary==2.9.9
python-decouple==3.8
reportlab==4.2.0
sqlparse==0.4.4
typing_extensions==4.11.0
tzdata==2024.1
whitenoise==6.6.0
```

---

## 🧩 PostgreSQL Database Setup

1. **Create a PostgreSQL database**:

   ```bash
   psql -U postgres
   CREATE DATABASE bursary_db;
   CREATE USER bursary_user WITH PASSWORD 'your_secure_password';
   ALTER ROLE bursary_user SET client_encoding TO 'utf8';
   ALTER ROLE bursary_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE bursary_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE bursary_db TO bursary_user;
   ```

2. **Create a `.env` file** in your project root:

   ```
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   ALLOWED_HOSTS=127.0.0.1,localhost

   DB_NAME=bursary_db
   DB_USER=bursary_user
   DB_PASSWORD=your_secure_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Update `settings.py`** to use `python-decouple` and `dj-database-url` for DB config (example snippet):

   ```python
   from decouple import config
   import dj_database_url

   DATABASES = {
       'default': dj_database_url.config(
           default=f"postgres://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
       )
   }
   ```

---

## 🚧 Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/bursary-app.git](https://github.com/Bonfeb/Bursary-Application-System.git
   cd Bursary-Application-System
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create PostgreSQL DB and configure `.env`** as shown above.

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Start development server:

   ```bash
   python manage.py runserver
   ```

## 📄 License
This project is licensed under the MIT License.
