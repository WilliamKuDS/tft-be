FROM python

LABEL maintainer="mail@williamku.dev"

COPY dependencies.txt dependencies.txt

RUN pip3 install -r dependencies.txt

COPY . .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "tft_django.wsgi"]