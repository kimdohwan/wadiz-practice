FROM            dosio0102/teamproject:base
MAINTAINER      dosio0102@gmail.com

ENV             BUILD_MODE                  production
#ENV             DJANGO_SETTINGS_MODULE      config.settings
ENV             DJANGO_SETTINGS_MODULE      config.settings.${BUILD_MODE}

COPY            .       /srv/project

RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf \
                        /etc/nginx/nginx.conf && \
                cp -f   /srv/project/.config/${BUILD_MODE}/nginx_app.conf \
                        /etc/nginx/sites-available/ && \
                ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                        /etc/nginx/sites-enabled/

RUN             cp -f   /srv/project/.config/${BUILD_MODE}/supervisor.conf \
                        /etc/supervisor/conf.d/

EXPOSE          7000

CMD             supervisord -n