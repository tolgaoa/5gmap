# Use the latest Ubuntu image for the base.
FROM ubuntu:focal

# Install the iptables command.
RUN apt-get update && \
    apt-get install -y iptables wget curl vim net-tools make

RUN wget https://dl.google.com/go/go1.23.1.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.1.linux-amd64.tar.gz

ENV PATH="$PATH:/usr/local/go/bin"

COPY ./ /usr/src/
WORKDIR /usr/src/cmd
RUN ls
WORKDIR /usr/src/
RUN make build

RUN adduser --disabled-password --gecos '' --uid 1005 proxyop
USER proxyop

ENV PATH="$PATH:/usr/local/go/bin"
WORKDIR /usr/src/

#ENTRYPOINT [ "su", "proxyop", "/bin/bash", "-l", "-c" ]
CMD ["su", "proxyop", "-c", "./bin/proxyapp"]

