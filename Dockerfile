# Dockerfile
FROM ubuntu
MAINTAINER AndresPosada

# Some installs
RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get install -y cron
RUN apt-get install -y python-pip

# Get source code
COPY src/ /src/
RUN chmod 755 src -R

# Install libs
RUN pip install -r /src/config/requirements.txt
RUN pip list

# Setup Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY src/config/nginx/DjangoProject.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/DjangoProject.conf /etc/nginx/sites-enabled/DjangoProject.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
COPY /src/config/supervisord.conf /etc/supervisord.conf

# Migrate and collect Django
RUN bash -c "cd src && python manage.py makemigrations && python manage.py migrate"
RUN bash -c "cd src && python manage.py collectstatic --noinput && bash createsuper.sh"

RUN bash -c "cd src && python manage.py crontab add"

# Start supervisord processes
CMD ["supervisord"]

EXPOSE 80