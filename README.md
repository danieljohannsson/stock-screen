<h2 align="center">
Stock Screen: <br /> Identify undervalued stocks in real-time.
</h2>

## ✨ Key features

* **Undervalued Stocks:** Identify stocks with strong fundamentals such as low P/E, PEG, and healthy growth metrics.
* **Real-time Data:** Fetch updated stock information from external APIs like Yahoo Finance.
* **Pre Defined Filters:** Screen stocks by criteria such as revenue growth, debt-to-equity ratio, or analyst ratings.
* **Frontend Dashboard:** Modern UI built with React + TypeScript to view results in real time.

---

## 📖 About the project

This project was created to make stock screening accessible and transparent. Instead of relying solely on third-party platforms, the goal was to build a screener where users can easily identify new investment possibilities.

The backend is powered by **FastAPI**, handling data fetching, screening logic, and scheduling background jobs (via APScheduler). The frontend uses **React + Vite + TypeScript** with a clean UI to display stock insights.

A cron job runs periodically to fetch batches of tickers and update their metrics, helping keep recommendations fresh while respecting API rate limits.

---

## ⚙️ Technologies used

| Technology                  | Use case                                            |
| :-------------------------- | :-------------------------------------------------- |
| FastAPI                     | Backend web framework                               |
| Python                      | Data fetching, API integration, and cron scheduling |
| React + Vite + TypeScript   | Frontend application                                |
| Tailwind                    | UI styling                                          |
| yfinance API                | Stock quotes and financial metrics                  |
| Render                      | Backend deployment                                  |
| Netlify                     | Frontend deployment                                 |

---

## 🚫 Limitations

* Free APIs like Finnhub or Yahoo Finance impose **rate limits**, so batch fetching is required.
* Free hosting platforms (Render, Netlify) may spin down instances after inactivity unless external uptime monitors are used.
* Historical data storage is limited without connecting to an external persistent database (Postgres, Supabase, MongoDB).

---

## 🚀 Getting started

### Step 1: Clone the repo

```bash
git clone https://github.com/danieljohannsson/stock-rec.git
cd stock-rec
```

### Step 2: Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Run the backend:

```bash
python main.py
```

### Step 3: Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Update `.env` with the backend URL:

```
VITE_BACKEND_LOCAL_URL=<localhost_url>
```
or
```
VITE_BACKEND_PRODUCTION_URL=<production_url>
```

## 📸 Screenshots
<p align="center">
<img width="1397" height="611" alt="image" src="https://github.com/user-attachments/assets/59156923-0001-4e5a-87c5-775914c61b11" />
<p align="center">Homepage with investment strategy choice</p>
<br />
</p>

<p align="center">
<img width="1429" height="668" alt="image" src="https://github.com/user-attachments/assets/b62d79fa-514c-4c22-89da-c47c35016dcd" />
<p align="center">Undervalued stock results displayed in table format</p>
<br />
</p>

<p align="center">
<img width="1185" height="750" alt="image" src="https://github.com/user-attachments/assets/ce294173-d217-4124-b68d-fcfa265fd771" />
<p align="center">Once a row/company is clicked upon it links to a basic company profile</p>
<br />
</p>

---

## 🔮 Future improvements

* Add persistent database for storing stock history
* User authentication
* Custom metric filtering
* Deploy backend & frontend to a single domain for production use

---

