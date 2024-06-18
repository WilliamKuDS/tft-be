FROM python

LABEL maintainer="mail@williamku.dev"

COPY dependencies.txt dependencies.txt

RUN pip3 install -r dependencies.txt

COPY . .

ENTRYPOINT ["gunicorn", "tft_django.wsgi"]