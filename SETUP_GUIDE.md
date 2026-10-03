# OpsPilot — সম্পূর্ণ প্রজেক্ট সেটআপ ও কমান্ড গাইড (JS to Python)

এই গাইডটি বিশেষভাবে তৈরি করা হয়েছে যাতে **JavaScript / Node.js** ব্যাকগ্রাউন্ড থেকে এসে খুব সহজে **FastAPI + Next.js + Python** আর্কিটেকচার এবং এর প্রতিটি ফাইল ও কমান্ড বোঝা যায়।

---

## ১. প্রজেক্টের সারসংক্ষেপ (Quick Overview)

* **প্রজেক্টের নাম:** OpsPilot
* **কী ধরনের প্রজেক্ট:** Enterprise AI Knowledge & Operations Assistant (RAG Platform)
* **আর্কিটেকচার:** Modular Monolith (FastAPI) + Next.js Frontend + PostgreSQL (pgvector) + Celery/Redis
* **প্রধান কাজ:** কোম্পানির নিয়মকানুন ও পলিসি ডক (PDF) আপলোড করে রাখা, এবং এমপ্লয়িরা প্রশ্ন করলে হুবহু রেফারেন্স/সাইটেশন (Page no, Section) সহ উত্তর দেওয়া।

---

## ২. JS বনাম Python কনসেপ্ট ও ফাইল ম্যাপিং

| JavaScript / Node.js জগতে | Python / OpsPilot জগতে | ফাইল / টুলের কাজ |
| :--- | :--- | :--- |
| `package.json` | `backend/pyproject.toml` | প্রজেক্টের নাম, ডিপেন্ডেন্সি এবং স্ক্রিপ্ট কনফিগারেশন। |
| `package-lock.json` | `backend/uv.lock` | লাইব্রেরির এক্স্যাক্ট ভার্সন পিন/লক করে রাখে। |
| `npm` / `bun` | `uv` | দ্রুতগতির মডার্ন প্যাকেজ ম্যানেজার (Rust দিয়ে তৈরি)। |
| `node_modules/` | `backend/.venv/` | প্রজেক্টের আইসোলেটেড ভার্চুয়াল এনভায়রনমেন্ট (সব লাইব্রেরি এখানে থাকে)। |
| `Express.js` / `NestJS` | `FastAPI` | ব্যাকএন্ড ওয়েব এপিআই ফ্রেমওয়ার্ক। |
| `nodemon` / `tsx watch` | `uv run uvicorn app.main:app --reload` | ডেভেলপমেন্ট লোকাল সার্ভার (অটো-রিলোড)। |
| `dotenv` / `process.env` | `pydantic-settings` | `.env` ফাইলের ভ্যারিয়েবল ভ্যালিডেট ও লোড করা। |
| `Prisma` / `TypeORM` | `SQLAlchemy` | ডাটাবেস ORM। |
| `prisma migrate` | `Alembic` | ডাটাবেস স্কিমা মাইগ্রেশন। |
| `BullMQ` + `Redis` | `Celery` + `Redis` | ব্যাকগ্রাউন্ড টাস্ক কিউ (যেমন হেভি PDF প্রসেসিং)। |
| `Jest` / `Vitest` | `pytest` | ইউনিট ও ইন্টিগ্রেশন টেস্ট রানার। |
| `ESLint` + `Prettier` | `Ruff` | কোড ফরম্যাটার ও লিন্টার। |
| `TypeScript` (tsc) | `mypy` | পাইথনে স্ট্যাটিক টাইপ চেকিং টুল। |

---

## ৩. ফাইল ও ফোল্ডার পরিচিতি

```text
OpsPilot/
├── docs/                   # আর্কিটেকচার, সিস্টেম ডিজাইন ও ইন্টারভিউ গাইড
├── backend/                # FastAPI পাইথন ব্যাকএন্ড
│   ├── pyproject.toml      # ডিপেন্ডেন্সি লিস্ট (package.json এর মতো)
│   ├── uv.lock             # ভার্সন লক ফাইল (package-lock.json এর মতো)
│   ├── app/
│   │   ├── main.py         # ব্যাকএন্ড এন্ট্রি পয়েন্ট (server.ts এর মতো)
│   │   └── core/           # কনফিগারেশন ও গ্লোবাল সেটিংস
│   └── tests/              # টেস্ট কোড
├── frontend/               # Next.js (React + TypeScript + Tailwind) ফ্রন্টএন্ড
│   ├── package.json
│   └── app/                # Next.js App Router পেজ ও কম্পোনেন্ট
├── infra/                  # Docker Compose ও ডাটাবেস স্ক্রিপ্টস
└── SETUP_GUIDE.md          # এই গাইডটি
```

---

## ৪. স্ক্র্যাচ থেকে নতুন প্রজেক্ট তৈরি করার কমান্ড (Step-by-Step)

ভবিষ্যতে যদি নতুন কোনো প্রজেক্ট স্ক্র্যাচ থেকে তৈরি করতে চান, নিচের ধাপগুলো ফলো করবেন:

### ধাপ ক: প্রি-রিক্যুইজিট (Pre-requisites)
```bash
# uv ইনস্টল না থাকলে (Linux/macOS):
curl -LsSf https://astral.sh/uv/install.sh | sh

# নোড ও ডকার চেক:
node --version
docker --version
```

### ধাপ খ: ব্যাকএন্ড ইনিট ও ডিপেন্ডেন্সি ইনস্টল
```bash
# ১. মেইন ফোল্ডার তৈরি ও প্রবেশ
mkdir MyProject && cd MyProject

# ২. ফোল্ডার স্ট্রাকচার তৈরি
mkdir -p backend frontend infra/postgres/init docs/notes

# ৩. uv দিয়ে পাইথন অ্যাপ ইনিশিয়ালাইজ (npm init এর মতো)
uv init --app --python 3.12 backend

# ৪. backend এ গিয়ে প্রোডাকশন লাইব্রেরি যোগ করা (npm install এর মতো)
cd backend
uv add fastapi "uvicorn[standard]" pydantic-settings sqlalchemy asyncpg alembic pgvector redis celery boto3

# ৫. ডেভেলপমেন্ট লাইব্রেরি যোগ করা (npm install -D এর মতো)
uv add --dev pytest pytest-asyncio httpx ruff mypy import-linter pre-commit

# ৬. সমস্ত লাইব্রেরি সিঙ্ক করা (npm install এর মতো)
uv sync

# ৭. রুট ফোল্ডারে ফিরে আসা
cd ..
```

### ধাপ গ: ফ্রন্টএন্ড ইনিট (Next.js)
```bash
# রুট ফোল্ডার থেকেই রান করুন:
npx create-next-app@latest frontend --yes
```

---

## ৫. প্রজেক্ট রান করার দৈনন্দিন কমান্ড (Daily Development)

### ১. ব্যাকএন্ড রান করা
```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```
* **লাইভ এন্ডপয়েন্ট চেক:** [http://localhost:8000/health/live](http://localhost:8000/health/live)
* **অটোমেটিক সোয়েগার ডক:** [http://localhost:8000/docs](http://localhost:8000/docs)

### ২. ফ্রন্টএন্ড রান করা (আলাদা টার্মিনালে)
```bash
cd frontend
npm run dev
```
* **ওয়েবসাইট:** [http://localhost:3000](http://localhost:3000)

---

## ৬. কোড ফরম্যাটিং, টাইপ চেক ও টেস্ট কমান্ড

পাইথনে সব টুল রান করার আগে `uv run` প্রিফিক্স ব্যবহার করতে হয়:

```bash
cd backend

# ১. কোড ফরম্যাট করা (Prettier এর মতো)
uv run ruff format .

# ২. লিন্ট এরর চেক ও ফিক্স করা (ESLint এর মতো)
uv run ruff check --fix .

# ৩. টাইপ চেকিং করা (TypeScript এর মতো)
uv run mypy app

# ৪. টেস্ট রান করা (Jest এর মতো)
uv run pytest
```

---

## ৭. এডিটরে (VS Code / Cursor) পাইথন সিলেক্ট করার নিয়ম

পাইথনে কোনো ফাইল ওপেন করলে যাতে লাল দাগ (Import missing) না দেখায়:
1. কিবোর্ডে চাপুন: `Ctrl + Shift + P`
2. সার্চ বক্সে লিখুন: `Python: Select Interpreter`
3. এন্টার দিয়ে নিচের পাথটি সিলেক্ট করুন বা পেস্ট করুন:
   ```text
   /home/awolad/Projects/OpsPilot/backend/.venv/bin/python
   ```

---

## ৮. নতুন লাইব্রেরি যোগ ও বাদ দেওয়ার নিয়ম

* **নতুন কোনো লাইব্রেরি ইনস্টল করতে:**
  ```bash
  uv add <package-name>
  # উদাহরণ: uv add langchain
  ```
* **কোনো লাইব্রেরি আনইনস্টল/রিমুভ করতে:**
  ```bash
  uv remove <package-name>
  ```
* **গিট থেকে ক্লোন করার পর নতুন কম্পিউটারে ইনস্টল করতে:**
  ```bash
  uv sync
  ```
