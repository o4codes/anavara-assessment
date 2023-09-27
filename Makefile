PYTHON = .venv/bin/python

.PHONY : dev-server
dev-server:
	sudo docker-compose up --build


.PHONY : test
test:
	sudo docker-compose up -d
	sudo docker-compose exec web python manage.py test
	sudo docker-compose down
