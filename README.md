## 🔮 Future Scope

- 🔍 Course search & filtering  
- 📈 Dashboard analytics (enrollment stats)  
- 🔔 Notifications for course updates  
- 📅 Calendar view for course schedules  
- 📌 Waitlist system for full courses  

---

## 🚀 Quick Start

### Clone the repo:
```bash
git clone https://github.com/adarsh-279/Course-Management-System.git
cd Course-Management-System
```

### Create virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start server:
```bash
python manage.py runserver
```

### Access app:
```bash
http://127.0.0.1:8000/
```

---

## 👨‍💻 Roles Overview

**Admin:**
- Manage courses (CRUD)
- View all courses

**Student:**
- View courses
- Enroll in courses

---

## 🤝 Contributing

Contributions are welcome! 🎉
Feel free to fork the project and submit pull requests.

⭐ Final Note
This system ensures efficient course management with role-based access and prevents duplicate enrollments while maintaining a clean user experience.
