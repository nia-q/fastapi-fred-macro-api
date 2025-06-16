
### 2. Create virtual environment (first time only)
python -m venv venv

### 3. Activate the virtual environment
# On macOS/Linux:
conda deactivate (base) removed
source venv/bin/activate


### 4. Install all dependencies(first time only)
pip install -r requirements.txt

### 5. Run the FastAPI app
uvicorn app.main:app --reload


### testing endpoints with curl

 curl http://127.0.0.1:8000/macro/indicator/CPIAUCSL




### Git Setup Instructions

##### Initialize a new Git repository (first time only)
git init

##### Remove any existing remote origin if needed
git remote remove origin

##### Add your GitHub repository as the remote origin
git remote add origin https://github.com/nia-q/quant-api.git

##### Stage all files for commit
git add .

##### Create initial commit
git commit -m "Initial commit"

##### Rename the default branch to main (if not already on main)
git branch -M main

##### Push your code to GitHub and set up tracking
git push -u origin main