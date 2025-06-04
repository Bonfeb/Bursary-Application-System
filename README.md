Here's a `README.md` file content for your bursary application web app:

---

# 🧾 Online Bursary Application System

This is a web application that enables students to apply for bursaries **online** without the need to submit documents physically. The platform categorizes bursaries by **County**, **Constituency**, and **Ward** levels, enforcing application rules specific to each category.

---

## 🌐 Features

* Students can register, log in, and apply for bursaries.
* **County-level bursaries**: Open to students from any ward or constituency within the county.
* **Constituency-level bursaries**: Restricted to students from a specific constituency, regardless of their ward.
* **Ward-level bursaries**: Restricted to students residing in the specific ward.
* Students can **only apply once** to any given bursary.
* Document submission is handled digitally—no physical documents required.

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

## ⚙️ Deployment

* Configure environment variables using `.env` and `python-decouple`.
* Serve static files using **WhiteNoise**.
* Deploy using **Gunicorn** and any WSGI-compatible web server.

---

## 🚧 Development Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/bursary-app.git
   cd bursary-app
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

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start development server:

   ```bash
   python manage.py runserver
   ```

---

## 📄 License

This project is licensed under the MIT License.


