PROVIDER := "docker"
ACTION := "run"

# Env variables
export USER := root
export SUDO_USER := root

install:
	# Fixups depending on what system we are on
	./prepare.sh install

	# Install Atomic CLI and Atomic App CLI
	./atomic.sh install $(ATOMIC_SOURCE)
	./atomicapp.sh install $(ATOMICAPP_PR)

	# Download the library as well
	git clone https://github.com/projectatomic/nulecule-library
	find . -type f -iname 'Dockerfile' -exec sed -i 's/^FROM.*/FROM atomicapp:build/' "{}" +;

clean:
	rm -rf build answers.conf

clean-all:
	rm -rf build answers.conf nulecule-library
	./providers/docker.sh stop || true
	./providers/kubernetes.sh stop || true
	./providers/openshift.sh stop || true

docker:
	./providers/docker.sh answers
	./helloapache.sh run docker
	./helloapache.sh stop docker
	make clean

	./providers/docker.sh answers
	./wordpress.sh run docker
	./wordpress.sh stop docker
	make clean

	./providers/docker.sh stop

openshift:
	# Start it! (delay needed to init http front-end)
	./providers/openshift.sh start 

	./providers/openshift.sh answers
	./wordpress.sh run openshift
	./wordpress.sh stop openshift
	make clean

	./providers/openshift.sh answers
	./etherpad.sh run openshift
	./etherpad.sh stop openshift
	make clean

	./providers/openshift.sh stop

kubernetes:
	# Start it! (delay needed to init http front-end)
	./providers/kubernetes.sh start 

	./providers/kubernetes.sh answers
	./helloapache.sh run kubernetes
	./helloapache.sh stop kubernetes
	make clean

	./providers/kubernetes.sh answers
	./wordpress.sh run kubernetes
	./wordpress.sh stop kubernetes
	make clean

	./providers/kubernetes.sh answers
	./etherpad.sh run kubernetes
	./etherpad.sh stop kubernetes
	make clean

	./providers/kubernetes.sh stop

# the whole shebang
all: clean-all install
	make docker openshift kubernetes clean-all
