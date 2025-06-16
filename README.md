### Create virtual environment (first time only)
```bash
python -m venv venv
```

### Activate the virtual environment
```bash
conda deactivate (base) removed
source venv/bin/activate
```

### Install all dependencies (first time only)
```bash
pip install -r requirements.txt
```

### Run the FastAPI app
```bash
uvicorn app.main:app --reload
```

### Testing endpoints with curl
```bash
curl http://127.0.0.1:8000/macro/indicator/CPIAUCSL
curl "http://127.0.0.1:8000/macro/trend/CPIAUCSL?months=12"

```

### Git Setup Instructions

##### 1. Initialize a new Git repository (first time only)
```bash
git init
```

##### 2. Remove any existing remote origin if needed
```bash
git remote remove origin
```

##### 3. Add your GitHub repository as the remote origin
```bash
git remote add origin https://github.com/nia-q/quant-api.git
```

##### 4. Stage all files for commit
```bash
git add .
```

##### 5. Create initial commit
```bash
git commit -m "Initial commit"
```

##### 6. Rename the default branch to main (if not already on main)
```bash
git branch -M main
```

##### 7. Push your code to GitHub and set up tracking
```bash
git push -u origin main
```