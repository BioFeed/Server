# Créer le dossier `data/` où seront stockés `data.json` et `tokens.json`
mkdir -p data 

# Créer le virtual environment python et installer les modules 
python3 -m venv venv 
source venv/bin/activate
python3 -m pip install --upgrade pip 
python3 -m pip install -r requirements.txt 

# Générer un premier token
python3 modules/generate_tokens.py
