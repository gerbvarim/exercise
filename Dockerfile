FROM python:3

RUN pip install Flask


RUN groupadd -r gerber_web && useradd --no-log-init -r -g gerber_web gerber_web

WORKDIR /app
RUN chown gerber_web:gerber_web .

USER gerber_web


EXPOSE 12345
COPY --chown=gerber_web . .
CMD [ "python", "gerber_website.py" ]
#in order to be trully working with docker-toolbox, need to manually set port forwarding on default machine, at ports 12345 of host and machine.
#no need to set the ip addresses.

#do note you also need to add flag "-p 12345:12345" when running the container.
#example build command: "docker build --tag test ."
#example run command: "docker run --name bb -p 12345:12345 test"

