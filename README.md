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
