newdb:
	find -maxdepth 3 -name "00??_*.py" -delete && dropdb yashop && createdb yashop && ./manage.py makemigrations && ./manage.py migrate
