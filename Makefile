
# Informations
TOKEN=X9oIrX4UlQsjY5P0XXtO
DISTANT_URL=biofeed.vitavault.fr
DISTANT_PORT=443
LOCAL_URL=localhost
LOCAL_PORT=5000

# Variables par défaut
URL=$(DISTANT_URL)
PORT=$(DISTANT_PORT)
HTTP=https

init:
	# Création de la structure :
	mkdir data

	# Création de l'environnement python
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

.SILENT:
test_local:
	@make test URL=$(LOCAL_URL) PORT=$(LOCAL_PORT) HTTP=http

.SILENT:
test:
	@curl -X POST -H "Content-Type: application/json" -d \
	'{"name": "carotte", "date": 2832, "photo": "base64ici", "token": "$(TOKEN)"}' \
	$(HTTP)://$(URL):$(PORT)/store_data
	@curl -X POST -H "Content-Type: application/json" -d \
	'{"command": "save", "token": "$(TOKEN)"}' \
	$(HTTP)://$(URL):$(PORT)/command

