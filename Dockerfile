FROM emiliano41/bustertfandptorch:latest
LABEL maintainer="Kwaai - Arkusnexus AI Labs"

ENV PYTHONUNBUFFERED 1
ENV HF_HOME /home/django-user/.cache/huggingface/hub

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts
EXPOSE 8000

ARG DEV=true

RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip

RUN rm -rf /tmp

RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static /vol/temp && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
    
RUN mkdir -p /home/django-user/.cache/huggingface && \
    chown -R django-user:django-user /home/django-user/.cache/huggingface

RUN mkdir -p /home/django-user/.embedchain && \
    chown -R django-user:django-user /home/django-user/.embedchain

RUN mkdir -p /var/run/postgresql && \
    chown -R django-user:django-user /var/run/postgresql

RUN  /py/bin/pip install pip install -U djangorestframework

RUN mkdir -p /app/utilities && \
    chown -R django-user:django-user /app/utilities

RUN mkdir -p /app/db && \
    chown -R django-user:django-user /app/db

RUN /py/bin/pip install django-bootstrap3 && \
    /py/bin/pip install docx2txt && \
    /py/bin/pip install flask && \
    /py/bin/pip install pillow && \
    /py/bin/pip install pypdf && \
    /py/bin/pip install --upgrade 'embedchain[json]' && \
    /py/bin/pip install -U drf-spectacular


RUN mkdir -p /home/django-user/.wdm && \
    chown -R django-user:django-user /home/django-user/.wdm

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]