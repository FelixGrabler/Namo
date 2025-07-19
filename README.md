# Namo 👶📝  
**A baby name decision app by Felix Grabler**

Namo helps you browse, like, and dislike baby names from real-world name data.

Sources (will) include Austria, Germany, Switzerland, UK, Australia, USA, Spain, France, Liechtenstein, and maybe more.

## 🚀 Tech Stack

### Frontend
- [Vue 3](https://vuejs.org/) — modern frontend framework
- [Vite](https://vitejs.dev/) — lightning-fast dev/build tool
- [Pinia](https://pinia.vuejs.org/) — state management
- [Axios](https://axios-http.com/) — HTTP client

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) — Python web API framework
- [PostgreSQL](https://www.postgresql.org/) — relational database
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for DB access
- [Alembic](https://alembic.sqlalchemy.org/) — DB migrations
- [bcrypt](https://pypi.org/project/bcrypt/) — password hashing
- [JWT](https://jwt.io/) — token-based authentication

## ✅ Core Features (v0)
- User registration & login (username/password)
- Load names from Austria (rank, count, gender)
- Swipe yes/no on names
- Store votes in backend
- Simple UI with vote buttons
- No filters or sorting (yet)

## 🧠 Planned Features
- Filter by gender, length, first letter, frequency
- Add more countries (DE, UK, etc.)
- Collaboration between users (couples)

## ⚙️ Setup (coming soon)

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```