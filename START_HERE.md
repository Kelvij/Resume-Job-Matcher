# START HERE — Windows

This project is designed to run locally with PostgreSQL, FastAPI, and Vite.

## Step 1 — Install prerequisites

Install:

1. Node.js 22 LTS or newer within the Vite-supported range.
2. Python 3.12.
3. Docker Desktop.
4. Git (optional, but useful for GitHub).

## Step 2 — Put the project somewhere permanent

Extract/copy the repository to a folder such as:

`C:\Users\<you>\Documents\ai-resume-job-matcher`

Open PowerShell in that folder.

## Step 3 — Start PostgreSQL

Run:

```powershell
docker compose up -d db
```

Check:

```powershell
docker compose ps
```

The `resume_matcher_db` container should show as running/healthy.

## Step 4 — Configure the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
pip install -e .
```

You normally do not need an API key.

To enable optional LLM explanations later, open `backend\.env` and set:

```text
LLM_ENABLED=true
LLM_API_KEY=your-key
LLM_MODEL=your-available-model
```

Keep API keys only in `.env`. Never commit `.env` to Git.

## Step 5 — Start the FastAPI backend

From `backend`:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Leave this PowerShell window running.

Check in a browser:

`http://localhost:8000/health`

Then open:

`http://localhost:8000/docs`

## Step 6 — Start the frontend

Open a second PowerShell window:

```powershell
cd C:\path\to\ai-resume-job-matcher\frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually:

`http://localhost:5173`

## Step 7 — Test without a resume or API key

On the home page, click **Try demo analysis**.

This exercises the complete report UI using bundled sample data and does not require an LLM key.

## Step 8 — Test a real resume

Use:

`backend\sample_data\sample_resume.pdf`

And paste:

`backend\sample_data\sample_jd.txt`

Then click **Analyze Match**.

The uploaded PDF is parsed in memory and is not stored in PostgreSQL.

## Step 9 — Run backend tests

From `backend`:

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

## Step 10 — Put it on GitHub

From the project root:

```powershell
git init
git add .
git commit -m "Build AI resume job matcher"
```

Create a new GitHub repository, then connect it and push using the GitHub commands shown for your repository.

Do **not** commit:

- `backend/.env`
- API keys
- `node_modules`
- `.venv`

The included `.gitignore` already protects these files.

## Common problems

### `npm install` fails

Check Node first:

```powershell
node --version
npm --version
```

Then retry from `frontend`.

### `uvicorn` cannot import `app`

Make sure the PowerShell directory is `backend` and the virtual environment is activated.

### Database connection error

Run:

```powershell
docker compose ps
docker compose logs db
```

The backend expects PostgreSQL on `localhost:5432` using the credentials in `.env.example`.

### Scanned PDF is rejected

The current parser is intentionally text-based. A scanned image-only PDF requires an OCR fallback, which is listed as a future improvement.

### First semantic analysis feels slow

The Sentence Transformers model is downloaded/cached on first use. The application has a deterministic fallback so the demo path can still operate without the embedding model package/model being available.
