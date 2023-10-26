# rinha-de-backend-2023-glaucofilho



# some commands
black --line-length 79 src && isort src && flake8 src

ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'


https://medium.com/@arturocuicas/fastapi-and-redis-cache-a31ca832853e