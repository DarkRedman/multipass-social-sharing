# multipass-social-sharing
A web Application to program post in social networks (Facebook, Twitter, Instagram ...)

Note: In some cases sqlite can throws `sqlite3.OperationalError` errors.

# To launch it (linux WSL)

gunicorn -c gunicorn.conf.py app:app
