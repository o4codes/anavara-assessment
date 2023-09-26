PYTHON = .venv/bin/python

.PHONY : dev-server
dev-server:
	sudo docker-compose up --build -d
	sudo docker-compose exec web python manage.py migrate