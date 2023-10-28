FROM python:3.11.2-slim-bullseye

ARG UID
ARG GID

ENV UID=${UID}
ENV GID=${GID}

# Upgrade and install utilities
User root
RUN apt-get -y update
RUN apt-get install -y unzip curl

# Download and install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Create a demo user with same UID and GID as the host
# RUN usermod -u ${UID} demo
# RUN groupmod -g ${GID} demo
RUN groupadd -g "${GID}" demo \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" demo

WORKDIR /home/demo/

# Install python libs
COPY --chown=demo:demo requirements.txt /home/demo
RUN pip install -r requirements.txt

User demo

CMD python server.py
