# Setup Guide

This guide runs the Tech Market Trend Analyzer on your own computer. You will use a Python virtual environment (no Docker).

When you are done, you will have:

- The website at [http://localhost:8001](http://localhost:8001) (this checkout defaults to **8001** so it does not clash with Career Intelligence on 8000)
- Health check at [http://localhost:8001/health](http://localhost:8001/health)
- Dashboard at [http://localhost:8001/dashboard](http://localhost:8001/dashboard)

---

## What you need

| Requirement | Why |
| --- | --- |
| **Python 3.10+** | The app and the pipeline |
| **pip** | Installs packages from `requirements.txt` |
| **An OpenAI API key** | Embeddings and cluster write-ups. The homepage loads without it; the pipeline does not. |
| **Internet** | RSS feeds and the OpenAI API |

If Career Intelligence is already running, leave `PORT=8001` in `.env`. If this project is the only app on the machine, you can set `PORT=8000`.

---

## 1. Open the project

From the Career Intelligence root (where you cloned this folder):

```bash
cd tech_market_trend_analyzer
```

Or clone it on its own:

```bash
git clone https://github.com/prashere/tech_market_trend_analyzer.git
cd tech_market_trend_analyzer
```

---

## 2. Create a virtual environment

macOS / Linux:

```bash
python3 --version
```

You need **3.10 or newer**. On many Macs `python3` is still 3.9. If so, use Homebrew Python:

```bash
python3.12 -m venv market_env
source market_env/bin/activate
```

If `python3` is already 3.10+:

```bash
python3 -m venv market_env
source market_env/bin/activate
```

Windows:

```bash
python -m venv market_env
market_env\Scripts\activate
```

Your prompt should show `(market_env)`.

---

## 3. Install packages

```bash
pip install -r requirements.txt
```

The first install can take several minutes (`faiss-cpu`, `scikit-learn`, `newspaper3k`).

`newspaper3k` may need NLTK tokenizers the first time you scrape. If article extraction fails with an NLTK error, run:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

---

## 4. Get an OpenAI API key

Embeddings (`text-embedding-3-small`) and cluster analysis (`gpt-4o-mini` by default) both call OpenAI.

1. Create a key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. You need billing enabled on the OpenAI account, or the pipeline will fail when it embeds articles.
3. Keep the key private. Never commit `.env`.

Without a key you can still start the website and click through an empty dashboard.

---

## 5. Create your environment file

```bash
cp .env.template .env
```

Open `.env` and set at least:

```env
OPENAI_API_KEY=sk-your-key-here
PORT=8001
```

Optional tunables (defaults are already in `.env.template`):

| Variable | Meaning |
| --- | --- |
| `CHAT_MODEL` | Chat model for cluster write-ups (`gpt-4o-mini` is the default) |
| `EMBEDDING_MODEL` | Embedding model (`text-embedding-3-small`) |
| `CLUSTER_COUNT` | Topic groups to form (will not exceed the number of articles) |
| `RSS_UPDATE_INTERVAL` | Hours between refreshes if you run `python main.py` |

`.env` is listed in `.gitignore`. Do not add it to Git.

---

## 6. Start the website

With `market_env` active, from `tech_market_trend_analyzer/`:

```bash
python app.py
```

You should see Uvicorn listening on the port from `.env`.

In a **new** terminal (activate `market_env` again if you need it):

```bash
curl http://localhost:8001/health
```

You should see:

```json
{"status":"ok","service":"tech-market-trend-analyzer"}
```

Open [http://localhost:8001](http://localhost:8001). You should see the landing page. **View Market Analysis** goes to the dashboard.

The dashboard will be empty until the pipeline has run once.

---

## 7. Run the data pipeline (needs the API key)

The pipeline fetches RSS, stores new articles, builds embeddings, and writes the FAISS index.

### From the website

With the app running:

```bash
curl -X POST "http://localhost:8001/api/pipeline/run"
```

Watch status:

```bash
curl http://localhost:8001/api/pipeline/status
```

Wait until `"status":"completed"`. Then refresh analysis for the dashboard:

```bash
curl -X POST "http://localhost:8001/api/analysis/refresh"
```

Reload [http://localhost:8001/dashboard](http://localhost:8001/dashboard).

The first pipeline run talks to three RSS feeds and OpenAI. It often takes several minutes. Some article pages block scrapers; those URLs are skipped.

### From the command line (optional 24-hour loop)

Stop `python app.py` first if you only have one terminal, or use a second terminal with `market_env` active:

```bash
python main.py
```

This runs a full pipeline, then sleeps and refreshes on `RSS_UPDATE_INTERVAL`. Stop with Ctrl+C. You still need `python app.py` in another process to serve the website.

---

## 8. Stop

In the terminal that is running Uvicorn, press **Ctrl+C**.

Deactivate the virtualenv:

```bash
deactivate
```

SQLite, FAISS files, and `cluster_analysis.json` stay on disk. The next `python app.py` will reuse them.

To start clean (deletes stored articles and analysis):

```bash
rm -f db/articles.db cluster_analysis.json articles_cleaned_*.csv
rm -rf faiss
```

---

## Everyday commands

```bash
source market_env/bin/activate      # Windows: market_env\Scripts\activate
python app.py                       # website
curl http://localhost:8001/health
curl -X POST http://localhost:8001/api/pipeline/run
curl http://localhost:8001/api/pipeline/status
curl -X POST http://localhost:8001/api/analysis/refresh
python main.py                      # pipeline + scheduler only
```

---

## Troubleshooting

**`address already in use` on port 8000 or 8001**  
Something else is bound to that port (Career Intelligence uses 8000). Change `PORT` in `.env` and restart `python app.py`.

**`OPENAI_API_KEY is not set` or 401 from OpenAI**  
`.env` is missing, the key is empty, or billing is not enabled. Confirm you copied `.env.template` to `.env` in this folder (not only in Career Intelligence).

**Dashboard: “No FAISS index yet” / no clusters**  
The pipeline has not finished. Run step 7 and wait for `completed`.

**Pipeline completes but few articles**  
Feeds were filtered to AI/startup keywords, capped at six items per source, and some full-text fetches fail. That is expected. Re-run later for a new batch.

**`faiss-cpu` fails to install on Apple Silicon**  
Use Python 3.10–3.12 from [python.org](https://www.python.org/downloads/) rather than an old system Python, then recreate `market_env`.

**Want a full reset**

```bash
deactivate
rm -rf market_env db/articles.db faiss cluster_analysis.json articles_cleaned_*.csv
python3.12 -m venv market_env
source market_env/bin/activate
pip install -r requirements.txt
python app.py
```

---

## What “working” looks like

1. `curl http://localhost:8001/health` returns `{"status":"ok","service":"tech-market-trend-analyzer"}`
2. [http://localhost:8001](http://localhost:8001) shows the landing page
3. The dashboard route loads (it may be empty)
4. With an OpenAI key, `POST /api/pipeline/run` reaches `"completed"`
5. After `POST /api/analysis/refresh`, the dashboard shows topic clusters

For what the product does, see [README.md](README.md).
