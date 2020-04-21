FROM python:3

WORKDIR /
RUN pip install Flask

EXPOSE 12345
COPY . .
CMD [ "python", "gerber_website.py" ]
#in order to be trully working with docker-toolbox, need to manually set port forwarding on default machine, at ports 12345 of host and machine.
#no need to set the ip addresses.

#do note you also need to add flag "-p 12345:12345" when running the container.
#example build command: "docker build --tag test ."
#example run command: "docker run --name bb -p 12345:12345 test"

