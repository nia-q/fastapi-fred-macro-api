
# 2. Create virtual environment (first time only)
python -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
conda deactivate (base) removed
source venv/bin/activate


# 4. Install all dependencies(first time only)
pip install -r requirements.txt

# 5. Run the FastAPI app
uvicorn app.main:app --reload



# testing endpoints with curl

 curl http://127.0.0.1:8000/macro/indicator/CPIAUCSL
 