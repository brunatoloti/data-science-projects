FROM python:3.8

RUN apt-get update \
    && apt-get install -y \
        python3-pip \
        python-dev \
        libpq-dev \
        r-base \
        r-cran-plotly \
        libudunits2-dev \
        libgdal-dev \
        libgeos-dev \
        libproj-dev

COPY . /projeto-imoveis-olx
ENV WORKDIR='/projeto-imoveis-olx'
ENV PYTHONPATH=$WORKDIR
ENV PYTHONIOENCODING=UTF-8
WORKDIR $WORKDIR

RUN apt-get -y install locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ENV AIRFLOW_HOME $WORKDIR/airflow
COPY . $WORKDIR
COPY entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]


