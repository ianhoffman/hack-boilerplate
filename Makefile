.PHONY: build test hh_autoload format

build:
	docker build .

install: build
	docker run -v `pwd`:/app -i composer install

update: build
	docker run -v `pwd`:/app -i composer update

hh_autoload:
	docker run -v `pwd`:/app -i ./vendor/bin/hh-autoload

test:
	docker run -v `pwd`:/app -i ./vendor/bin/hacktest tests

format:
	docker run -v `pwd`:/app -i find {src,tests} -type f -name "*.hack" -exec hackfmt -i {} \;
