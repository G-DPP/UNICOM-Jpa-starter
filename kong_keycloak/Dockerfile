FROM kong:3.1.1-alpine

LABEL description="Alpine + Kong"

USER root
RUN apk update && apk add curl git gcc musl-dev
RUN luarocks install luaossl OPENSSL_DIR=/usr/local/kong CRYPTO_DIR=/usr/local/kong
RUN luarocks install --pin lua-resty-jwt
RUN luarocks install --pin lua-resty-openidc
RUN luarocks install lua-resty-http
USER kong
