FROM nginx:stable-alpine
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python -m ensurepip
RUN mkdir /project
RUN apk add cargo openssl-dev
WORKDIR /project
COPY . .
RUN  apk add --virtual build-deps gcc g++ python3-dev libffi-dev musl-dev jpeg-dev zlib-dev && \
python -m pip install -r requirements.txt && python -m pip install tzdata && \
apk del build-deps
EXPOSE 80

ENV DEBUG=false
ENV ALLOWED_HOSTS=twitter-clone-api,localhost
ENV SECRET_KEY==r*2jzwrl=iyyhlvvb0!uzp-+67@#x57tsm8)6i-5xz81#!vfk
ENV CORS_ORIGIN_WHITELIST=http://localhost,http://twitter-clone-frontend,http://148.100.108.153
ENV CSRF_TRUSTED_ORIGINS=http://twitter-clone-api,http://localhost,http://148.100.108.153
ENV REDIS_HOST=redis://twitter-clone-redis:6379

RUN python manage.py collectstatic
RUN mv static /static
RUN python manage.py makemigrations && python manage.py migrate
COPY nginx.conf /etc/nginx/conf.d/default.conf
CMD nginx && gunicorn --access-logfile ./gunicorn.log --bind 0.0.0.0:8000  main.asgi:application -k uvicorn.workers.UvicornWorker
