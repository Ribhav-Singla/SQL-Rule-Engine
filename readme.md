1. create virtual environment
   python -m venv venv
   venv\Scripts\activate
2. install dependencies
   pip install -r requirements.txt
3. Run docker
   docker-compose up -d
4. run backend
   uvicorn main:app --reload --port 8000
5. run frontend
   cd frontend
   npm install
   npm run build
   npm run start
