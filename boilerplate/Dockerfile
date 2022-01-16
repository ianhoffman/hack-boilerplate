FROM hhvm/hhvm:latest

RUN apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y php-cli zip unzip openssh-client

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

ADD . /app
WORKDIR /app
