PROVIDER := "docker"
ACTION := "run"

define WORDPRESS_ANSWERS


endef
export WORDPRESS_ANSWERS


provider:

# Replace each example with "atomicapp:build"
library: 
	git clone https://github.com/projectatomic/nulecule-library
	find . -type f -iname 'Dockerfile' -exec sed -i 's/^FROM.*/FROM atomicapp:build/' "{}" +;

install: library
	./atomic.sh install
	./atomicapp.sh install
	./atomicapp.sh docker

clean:
	rm -rf build answers.conf

clean-all:
	rm -rf build answers.conf nulecule-library
	./providers/docker.sh stop || true
	./providers/kubernetes.sh stop || true
	./providers/openshift.sh stop || true

stop: 
	cd build && atomicapp stop . # temp fix until atomic cli stop works

docker:
	# Test Docker first
	./providers/docker.sh answers
	./helloapache.sh docker
	make stop
	make clean

	./providers/docker.sh answers
	./wordpress.sh docker
	make stop
	make clean

	./providers/docker.sh stop

openshift:
	# Start it! (delay needed to init http front-end)
	./providers/openshift.sh start 

	./providers/openshift.sh answers
	./wordpress.sh openshift
	make stop
	make clean

	./providers/openshift.sh stop

kubernetes:
	# Start it! (delay needed to init http front-end)
	./providers/kubernetes.sh start 

	./providers/kubernetes.sh answers
	./helloapache.sh kubernetes
	make stop
	make clean

	./providers/kubernetes.sh answers
	./wordpress.sh kubernetes
	make stop
	make clean

	./providers/kubernetes.sh stop

# the whole shebang
all: clean-all install
	make docker
	make openshift
	make kubernetes
