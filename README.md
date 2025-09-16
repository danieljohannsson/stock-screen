A website for keeping track of the most undervalued stocks at the moment

Start frontend:

cd frontend/
npm install
npm run dev

Start backend:
cd backend/
source venv/bin/activate #Start environment
pip install -r requirements.txt
uvicorn app.main:app --reload #start application
