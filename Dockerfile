FROM python

LABEL maintainer="mail@williamku.dev"

COPY dependencies.txt dependencies.txt

RUN pip3 install -r dependencies.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]