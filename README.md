# Friend 💌

**Friend** is a minimal, warm web service. Users register to receive short, personalized, AI-generated emails at infrequent, random intervals. It is designed to feel like a message from a caring friend, not a robot.

## 🏗 Architecture

*   **Language:** Python 3.11+
*   **Framework:** Flask (Blueprints, Application Factory)
*   **Database:** PostgreSQL (via Supabase API)
*   **Auth:** Supabase Authentication
*   **AI:** Priyanshu API (Custom Model)
*   **Dependency Management:** Poetry

## 🚀 Setup & Installation

### 1. Prerequisites
*   Python 3.11 or higher
*   Poetry (`pip install poetry`)
*   A free [Supabase](https://supabase.com) account
*   A free [Priyanshu API](https://priyanshuapi.xyz/) account

### 2. Installation
```bash
git clone <your-repo-url>
cd Friend
poetry install
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```ini
FLASK_APP=app
FLASK_ENV=development
FLASK_SECRET_KEY=change_this_to_something_secure

# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-key

# AI Configuration (Priyanshu API)
API_KEY=your-aiml-api-key
```

### 4. Running Locally
```bash
poetry run flask run
```
Visit `http://127.0.0.1:5000` to see the app.

### 5. Running Tests
```bash
poetry run pytest
```

## 📚 Project Chapters

This project is built in modular chapters.

- [x] **Chapter 01: Setup & Architecture**
    - Established Poetry environment, Flask factory pattern, and CI/CD skeleton.
- [x] **Chapter 02: Database (Supabase API)**
    - Integrated Supabase Python client.
    - Created `users_profile` and `email_logs` tables.
    - Implemented `UserService` for data operations.
- [x] **Chapter 03: Authentication & UI**
    - Integrated Supabase Auth for secure signup/login.
    - Built Flask Blueprints and Jinja2 templates (Register, Login, Dashboard).
    - Implemented session management.
- [x] **Chapter 04: Core API (AI Message Generation)**
    - Integrated Priyanshu API (Custom LLM Wrapper).
    - Implemented `AIService` using Python `requests`.
    - Added "Test AI" button to Dashboard.
    - Enforced strict persona prompting.

## 🤝 Contributing
1. Fork the repo.
2. Create a branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "feat: add something"`).
4. Push to branch and open a PR.