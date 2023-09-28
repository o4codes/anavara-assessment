PYTHON = .venv/bin/python
PIP = .venv/bin/pip

.PHONY : dev-setup
dev-setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt
	pre-commit install


.PHONY : dev-server
dev-server:
	sudo docker-compose up --build


.PHONY : test
test:
	sudo docker-compose up -d
	sudo docker-compose exec web python manage.py test
	sudo docker-compose down


.PHONY : createsuperuser
createsuperuser:
	sudo docker-compose up -d
	sudo docker-compose exec web python manage.py createsuperuser
	sudo docker-compose down
