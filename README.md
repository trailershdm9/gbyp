# GDTOT Link Bypasser (Flask)

Paste a GDTOT or Google Drive link, get direct file links back. Works with the official `new.gdtot.com` API.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r gunicorn-requirements.txt
export DEMO_MODE=true  # or set in .env
python app.py
```

Open http://127.0.0.1:5000

## Deploy to Render

1. Push this folder to GitHub.
2. Create a **Web Service** on Render, pick the repo.
3. Build Command:
```
pip install -r requirements.txt && pip install -r gunicorn-requirements.txt
```
4. Start Command:
```
gunicorn app:app
```
5. Add Environment Variables:
   - `GDTOT_EMAIL`
   - `GDTOT_API_TOKEN`
   - (optional) `DEMO_MODE=false`

## Environment variables

- `GDTOT_EMAIL` — your account email.
- `GDTOT_API_TOKEN` — your API token.
- `DEMO_MODE` — set to `true` to return sample responses without calling the API.
- `HTTP_TIMEOUT` — request timeout seconds.
- `PORT` — port for local dev.

## Notes
- If the link contains `"folders"` we send to `/api/upload/folder`, otherwise `/api/upload/link`.
- The UI lists all returned files and their direct URLs.
