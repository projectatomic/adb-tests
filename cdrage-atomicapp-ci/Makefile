PROVIDER := "docker"
ACTION := "run"

define WORDPRESS_ANSWERS

[mariadb-atomicapp]
	db_user = foo
	db_pass = foo
	db_name = foo

[wordpress]
	db_user = foo
	db_pass = foo
	db_name = foo

endef
export WORDPRESS_ANSWERS

container:
	# Pull the latest CentOS image
	docker pull centos:7

	# Builds the atomicapp image as atomicapp:build
	./atomicapp.sh docker

provider:
	./providers/$(PROVIDER).sh $(ACTION)

library: 
	git clone https://github.com/projectatomic/nulecule-library

	# Replace each example with "atomicapp:build"
	find . -type f -iname 'Dockerfile' -exec sed -i 's/^FROM.*/FROM atomicapp:build/' "{}" +;

install: container library
	./atomic.sh install
	./atomicapp.sh install

clean:
	rm -rf build answers.conf

clean-all:
	rm -rf build answers.conf nulecule-library

test-helloapache:
	mkdir build
	cd nulecule-library/helloapache && docker build -t projectatomic/helloapache .
	atomic $(ACTION) projectatomic/helloapache --provider=$(PROVIDER) -a answers.conf --destination=build

# We build mariadb as wordpress uses an aggregated database of mariadb
test-wordpress: 
	mkdir build
	cd nulecule-library/mariadb-centos7-atomicapp && docker build -t projectatomic/mariadb-centos7-atomicapp .
	cd nulecule-library/wordpress-centos7-atomicapp && docker build -t projectatomic/wordpress-centos7-atomicapp .
	echo "$$WORDPRESS_ANSWERS" >> answers.conf
	atomic $(ACTION) projectatomic/wordpress-centos7-atomicapp --provider=$(PROVIDER) -a answers.conf --destination=build

stop: 
	cd build && atomicapp stop . # temp fix until atomic cli stop works

docker:
	# Test Docker first
	make provider PROVIDER=docker ACTION=answers 
	make test-helloapache
	make stop
	make clean

	make provider PROVIDER=docker ACTION=answers 
	make test-wordpress
	make stop
	make clean

openshift:
	# Start it! (delay needed to init http front-end)
	make provider PROVIDER=openshift ACTION=start
	sleep 15

	make provider PROVIDER=openshift ACTION=answers
	make test-wordpress PROVIDER=openshift
	make stop
	make clean

	make provider PROVIDER=openshift ACTION=stop

kubernetes:
	# Start it! (delay needed to init http front-end)
	make provider PROVIDER=kubernetes ACTION=start
	sleep 15

	make provider PROVIDER=kubernetes ACTION=answers 
	make test-helloapache PROVIDER=kubernetes
	make stop
	make clean

	make provider PROVIDER=kubernetes ACTION=answers
	make test-wordpress PROVIDER=kubernetes
	make stop
	make clean

# the whole shebang
all: clean-all install
	make docker
	make openshift
	make kubernetes
