FROM python:3.8

RUN apt-get update \
    && apt-get install -y \
        python3-pip \
        python-dev

COPY . /projeto-sistema-recomendacao-livros
ENV WORKDIR='/projeto-sistema-recomendacao-livros'
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


