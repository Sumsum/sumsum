newdb:
	dropdb yashop && createdb yashop && ./manage.py makemigrations && ./manage.py migrate
