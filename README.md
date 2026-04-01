# 🎓 Course Management System

A full-stack Django-based web application that allows administrators to manage courses and students to enroll seamlessly. Built with a focus on simplicity, usability, and role-based access.

---

## 🧰 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** MySQL  
- **Authentication:** Django Auth System  
- **UI Enhancements:** Bootstrap Modals, Animations  

---

## ✨ Features

- 👤 **User Authentication**
  - Secure login & registration
  - Role-based access (Admin / Student)

- 📚 **Course Management (Admin)**
  - Create, edit, delete courses
  - Add instructor, capacity, dates

- 🎓 **Student Features**
  - View available courses
  - Enroll in courses
  - Prevent duplicate enrollment

- 📊 **Dynamic Course Info**
  - Instructor details
  - Course capacity
  - Start & End dates

- ⚡ **Interactive UI**
  - Modal-based view & edit
  - Clean table design
  - Hover effects & animations

---

## 🧠 Problem Solving Journey

- ⚡ **Challenge:** Prevent duplicate enrollments  
  ✅ **Solution:** Used `unique_together` constraint in Enrollment model  

- ⚡ **Challenge:** Role-based access control  
  ✅ **Solution:** Used Django user roles (`is_staff`) to separate admin/student  

- ⚡ **Challenge:** Smooth UI without page reloads  
  ✅ **Solution:** Implemented AJAX (Fetch API) for edit/delete actions  

- ⚡ **Challenge:** Managing course data with additional fields  
  ✅ **Solution:** Extended model with instructor & date fields  

---
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
