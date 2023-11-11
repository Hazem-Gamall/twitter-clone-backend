FROM nginx:stable-alpine
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python -m ensurepip
RUN mkdir /project
WORKDIR /project
COPY . .
RUN  python -m pip install -r requirements.txt && python -m pip install tzdata
EXPOSE 80

ENV DEBUG=false
ENV ALLOWED_HOSTS=django-api,localhost
ENV SECRET_KEY==r*2jzwrl=iyyhlvvb0!uzp-+67@#x57tsm8)6i-5xz81#!vfk
ENV CORS_ORIGIN_WHITELIST=http://localhost,http://django-api
ENV CSRF_TRUSTED_ORIGINS=http://django-api,http://localhost:8000
RUN python manage.py collectstatic
RUN mv static /static
COPY nginx.conf /etc/nginx/conf.d/default.conf
CMD  nginx && gunicorn --access-logfile - --bind 0.0.0.0:8000 main.wsgi && nginx -s start