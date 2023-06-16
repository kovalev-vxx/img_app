FROM nginx:1.19.0-alpine

RUN apk add --no-cache openssl

RUN openssl genrsa -out /etc/ssl/private/nginx-selfsigned.key 2048 && openssl req -new -key /etc/ssl/private/nginx-selfsigned.key -out /tmp/cert.csr -subj "/C=US/ST=CA/L=San Francisco/O=My Company/CN=localhost" && openssl x509 -req -days 365 -in /tmp/cert.csr -signkey /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

COPY ./default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443