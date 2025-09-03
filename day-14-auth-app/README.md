# Authentication API (Flask + JWT)

This is a **backend-only authentication system** built with Flask. It uses **JWT (JSON Web Tokens)** for authentication and **SQLite** as the database.

---

## Features
- Register user (with hashed password using bcrypt)
- Login user (generate JWT token)
- Protected route (requires valid token)

---

## Setup
1. Install dependencies:
   ```bash
   pip install flask flask-cors bcrypt pyjwt
