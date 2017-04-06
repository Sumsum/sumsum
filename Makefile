newdb:
	find -maxdepth 3 -name "00??_*.py" -delete
	dropdb sumsum; true
	createdb sumsum && ./manage.py makemigrations && ./manage.py migrate
