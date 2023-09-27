PYTHON = .venv/bin/python

.PHONY : dev-server
dev-server:
	sudo docker-compose up --build