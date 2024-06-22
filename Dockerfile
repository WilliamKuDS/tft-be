FROM python

LABEL maintainer="mail@williamku.dev"

COPY dependencies.txt dependencies.txt

RUN pip3 install -r dependencies.txt

COPY . .

ENV PORT=8000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:$PORT", "tft_django.wsgi"]