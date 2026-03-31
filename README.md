# 📦 Flask CRUD Warehouse App (Gudang D&L)

A simple web-based warehouse management system built using Flask.
This project demonstrates a complete end-to-end workflow: from local development to live deployment.

🔗 **Live Demo**: https://flask-crud-app-918c.onrender.com/
🔗 **Repository**: https://github.com/trishnantidea-sys/flask-crud-app

---

## 🚀 Features

* 🔐 User Authentication (Register & Login)
* 📋 CRUD Operations (Create, Read, Update, Delete)
* 👤 User profile data management
* 🎨 Simple and clean UI
* ☁️ Deployed to cloud using Render

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLite
* **Frontend**: HTML, CSS
* **Deployment**: Render
* **Version Control**: GitHub

---

## 📂 Project Structure

```
flask-crud-app/
│── app.py
│── requirements.txt
│── Procfile
│── templates/
│── static/
│── instance/
```

---

## ⚙️ Installation (Run Locally)

### 1. Clone repository

```bash
git clone https://github.com/trishnantidea-sys/flask-crud-app.git
cd flask-crud-app
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run application

```bash
python app.py
```

App will run on:

```
http://127.0.0.1:5000
```

---

## ☁️ Deployment

This project is deployed using Render.

### Steps:

1. Push project to GitHub
2. Connect repository to Render
3. Configure:

   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
4. Deploy 🚀

---

## 🧠 Lessons Learned

* Understanding full-stack workflow (backend → frontend → deployment)
* Debugging real-world deployment issues
* Importance of clean project structure
* Improving UI for better user experience

---

## 📌 Future Improvements

* 🔐 Password hashing & security enhancement
* 🐘 Migrate database to PostgreSQL
* 🎨 Improve UI with modern framework (Bootstrap / Tailwind)
* 📊 Add dashboard analytics

---

## 👤 Author

**Dea Trishnanti**
Data Science

