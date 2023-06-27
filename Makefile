TOKEN=X9oIrX4UlQsjY5P0XXtO

init:
	# Création de la structure :
	mkdir data

	# Création de l'environnement python
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

test_local:
	@curl -X POST -H "Content-Type: application/json" -d \
	'{"name": "carotte", "date": 2832, "photo": "base64ici", "token": "$(TOKEN)"}' \
	http://localhost:5000/store_data

test:
	@curl -X POST -H "Content-Type: application/json" -d \
	'{"name": "carotte", "date": 2832, "photo": "base64ici", "token": "$(TOKEN)"}' \
	https://biofeed.vitavault.fr:443/store_data


