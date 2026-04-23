# FastAPI Social Media Backend

A production-ready REST API for a social media platform — built with FastAPI, PostgreSQL, and JWT authentication. Supports posts, users, voting, and full database migrations via Alembic.

> **Live docs:** `http://localhost:8000/docs` after startup

---

## Table of Contents

- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)
- [Database Schema](#database-schema)
- [Migration History](#migration-history)
- [Tech Stack](#tech-stack)

---

## Quick Start

```bash
# 1. Clone & enter project
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file (see next section)

# 5. Apply database migrations
alembic upgrade head

# 6. Start the server
uvicorn main:app --reload
```

The API is now running at **http://localhost:8000**

---

## Environment Variables

Create a `.env` file in the project root:

```env
# ── Database ──────────────────────────────
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# ── Table Names ───────────────────────────
TABLE_NAME=orm_posts
USER_TABLE_NAME=users
VOTE_TABLE_NAME=votes

# ── Auth (JWT) ────────────────────────────
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=30
```

---

## Project Structure

```
FASTAPI/
│
├── app/                        # Main application package
│   ├── routers/
│   │   ├── auth.py             # POST /login
│   │   ├── posts.py            # Full CRUD for posts
│   │   ├── users.py            # Register & fetch users
│   │   └── vote.py             # Upvote / remove vote
│   │
│   ├── config.py               # Loads all settings from .env
│   ├── database.py             # DB engine, session factory, psycopg2 connection
│   ├── main.py                 # App entry point — registers all routers
│   ├── models.py               # SQLAlchemy ORM table definitions
│   ├── Oauth2.py               # JWT create / verify / get_current_user
│   ├── schemas.py              # Pydantic request / response shapes
│   └── utils.py                # Password hashing (Argon2 via pwdlib)
│
├── alembic/                    # Database migration tool
│   ├── versions/               # 6 migration files (full schema history)
│   ├── env.py                  # Alembic runtime environment config
│   ├── README                  # Alembic default readme
│   └── script.py.mako          # Migration file template
│
├── venv/                       # Virtual environment (not committed)
│
├── .env                        # Secret environment variables (not committed)
├── .gitignore
├── alembic.ini                 # Alembic configuration file
├── example_env.txt             # Example .env template for new developers
├── LICENSE
├── README.md
├── requirements.txt            # Python dependencies
├── sql_commands.sql            # Handy raw SQL reference / scratch queries
└── venv_setup.txt              # Virtual environment setup instructions
```

---

## API Reference

### Authentication

| Method | Endpoint | Description | Auth? |
|--------|----------|-------------|:-----:|
| `POST` | `/login` | Login — returns a JWT bearer token | No |

> Login uses **form-data** fields (`username` + `password`), not JSON.

---

### Users

| Method | Endpoint | Description | Auth? |
|--------|----------|-------------|:-----:|
| `POST` | `/users/` | Create a new account | No |
| `GET` | `/users/{id}` | Get user by ID | No |

---

### Posts

| Method | Endpoint | Description | Auth? |
|--------|----------|-------------|:-----:|
| `GET` | `/posts/` | List all posts with vote counts | Yes |
| `POST` | `/posts/` | Create a new post | Yes |
| `GET` | `/posts/{id}` | Get a single post with vote count | Yes |
| `PUT` | `/posts/{id}` | Update a post *(owner only)* | Yes |
| `DELETE` | `/posts/{id}` | Delete a post *(owner only)* | Yes |

**Optional query parameters for `GET /posts/`:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `limit` | `10` | Max posts to return |
| `skip` | `0` | Offset for pagination |
| `search` | `""` | Filter posts by title keyword |

---

### Votes

| Method | Endpoint | Description | Auth? |
|--------|----------|-------------|:-----:|
| `POST` | `/vote/` | Cast or remove a vote on a post | Yes |

**Request body:**
```json
{ "post_id": 1, "dir": 1 }
```
- `dir: 1` — add a vote
- `dir: 0` — remove your existing vote

---

## How It Works

### Step 1 — Register & Login

```
POST /users/   →  Password is hashed with Argon2 before storing in DB
POST /login    →  Credentials verified → JWT token returned
```

### Step 2 — Authenticated Requests

Include the token in every protected request:
```
Authorization: Bearer <your_token>
```
The server decodes the token → looks up the user → proceeds with the request.

### Step 3 — Posts & Votes

```
POST /posts/        →  Creates a post linked to the logged-in user (owner_id)

GET  /posts/        →  Runs a LEFT JOIN on votes table
                        Groups by post ID → returns each post + its vote count

POST /vote/         →  Checks post exists
                        Checks for duplicate vote
                        Inserts or deletes the vote record
```

### Ownership enforcement

`PUT` and `DELETE` on `/posts/{id}` check that `post.owner_id == current_user.id`.
Any mismatch returns `403 Forbidden`.

---

## Example Requests

**Register a user:**
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/login \
  -F "username=user@example.com" \
  -F "password=secret123"
```

**Create a post** *(paste your token from login)*:
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello World", "content": "My first post", "published": true}'
```

**Upvote a post:**
```bash
curl -X POST http://localhost:8000/vote/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"post_id": 1, "dir": 1}'
```

---

## Database Schema

```
┌─────────────────────────┐       ┌──────────────────────────────────────┐
│         users           │       │              orm_posts               │
├─────────────────────────┤       ├──────────────────────────────────────┤
│ id          INT  (PK)   │◄──┐   │ id          INT        (PK)          │
│ email       VARCHAR     │   │   │ title       VARCHAR                   │
│ password    VARCHAR     │   │   │ content     VARCHAR                   │
│ created_at  TIMESTAMPTZ │   │   │ published   BOOL  (default: true)     │
└─────────────────────────┘   │   │ created_at  TIMESTAMPTZ               │
                              └───│ owner_id    INT        (FK → users)   │
                                  └──────────────────────────────────────┘
                                                  │ id
                                  ┌───────────────▼───────────────────────┐
                                  │               votes                   │
                                  ├───────────────────────────────────────┤
                                  │ user_id   INT  (FK → users.id,  PK)   │
                                  │ post_id   INT  (FK → orm_posts, PK)   │
                                  └───────────────────────────────────────┘
                                  Composite PK prevents duplicate votes.
```

---

## Migration History

Migrations are applied in sequence with `alembic upgrade head`:

| Step | Revision | What it does |
|:----:|----------|--------------|
| 1 | `380d27bfc34c` | Create `orm_posts` table (`id`, `title`) |
| 2 | `e09466a5ed25` | Add `content` column |
| 3 | `39342041c719` | Add `published` and `created_at` columns |
| 4 | `670d7b9a1a0f` | Create `users` table |
| 5 | `bda63131d549` | Add `owner_id` FK (`orm_posts` → `users`) |
| 6 | `6e175e1a0518` | Create `votes` table |

**Common Alembic commands:**

```bash
alembic upgrade head                              # Apply all migrations
alembic downgrade -1                              # Roll back last migration
alembic current                                   # Show current revision
alembic history                                   # Show full migration chain
alembic revision --autogenerate -m "description"  # Generate a new migration
```

---

## Tech Stack

| Purpose | Library |
|---------|---------|
| Web framework | FastAPI |
| ORM | SQLAlchemy |
| Raw SQL driver | psycopg2 |
| Database | PostgreSQL |
| Schema migrations | Alembic |
| Auth tokens | PyJWT |
| Password hashing | pwdlib (Argon2) |
| Request validation | Pydantic v2 |
| Config management | pydantic-settings |

---

## License

MIT — free to use, modify, and distribute.
