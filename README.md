# Sumsum

** Warning: This project is very much work in progress, do not expect anything
to work.**

## Installation
```
$ git clone https://github.com/SumsumShop/sumsum.git
$ cd sumsum
$ mkvirtualenv --python `which python3` sumsum
$ pip install -r requirements.txt
$ createdb sumsum
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./run
```

Open up a new shell and cd into sumsum dir.

```
$ cd nimda
$ yarn install
$ ./buildjs
```

Navigate to http://localhost:8000/admin/


## What?
Sumsum is a Shopify like ecom plattform built using Django. It is a clone in
the sense that we are trying to mimic the tempalte language, data model, API
and Administration panel.

## Data model
The data model is the result of inspecting Shopifys API and templates.
Currently we only support PostgreSQL, mostly because we think that
JSONFields are such an awesome features and the use of them will greatly
reduce the amount of required db queries per view.

## Liquid templates
We are working on a fork of Jinja2 template engine that can parse Shopify
Liquid syntax as well as most of standard Jinja2 syntax. Most tests for Liquid
templates have been implemented in python but there is still some work to be
done. Our goal is to be able to use Shopify templates without modification.

## Admin panel
We are currently using Djangos admin application with the AdminLTE theme and
until we have time to do something creative we will continue to use this
approach since it results in very fast development. There is always a
braeking point when you want to implement something fancy and you almost
break your legs trying to build a nice interface using Django admin app,
we try to avoid this point and instead make it good enough for practical
purposes. Sometime in the future however we will want to make a custom
admin, probably a modern single page application using the API.

## API
We will try to implement the Shopify API as close as possible using
Django rest framework. The rest framework is little overengineered but we
think it is worth investing in for the sake of standards and developer
recognition/friendlyness.
