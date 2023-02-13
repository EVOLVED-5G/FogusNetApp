# base image
FROM node:16.15.0

# install chrome for protractor tests
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -yq curl && apt-get install -yq gettext-base
# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
RUN npm install
RUN npm install -g @angular/cli@13.3.4
# RUN npm install tslib

# add app
COPY . /usr/src/app

# start app
CMD ["/bin/sh",  "-c",  "envsubst < src/assets/env.template.js > src/assets/env.js && exec ng serve --host 0.0.0.0 --disable-host-check;"]
# TLS --ssl true --ssl-key localhost-key.pem --ssl-cert localhost.pem && in package.json =>  --ssl true --ssl-key localhost-key.pem --ssl-cert localhost.pem"
# CMD ng serve --host 0.0.0.0 --disable-host-check
