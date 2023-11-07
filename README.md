# rinha-de-backend-2023-glaucofilho



# some commands
black --line-length 79 src && isort src && flake8 src

ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'

sudo docker build . -t rinha-glauco

sudo docker compose up -d

sudo chmod +x stress-test/run-test.sh 

sudo ./stress-test/run-test.sh 