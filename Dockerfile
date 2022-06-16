FROM python:3.9-slim

RUN useradd -ms /bin/bash kvuser
USER kvuser
WORKDIR /home/kvuser

ENV PATH="/home/kvuser/.local/bin:${PATH}"

COPY --chown=kvuser:kvuser requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY --chown=kvuser:kvuser . .

CMD  [ "python3", "./app.py"]