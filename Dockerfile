FROM ubuntu:bionic

# install rippled service
RUN apt -y update
RUN apt -y install apt-transport-https ca-certificates wget gnupg git python3
RUN wget -q -O - "https://repos.ripple.com/repos/api/gpg/key/public" | apt-key add -
RUN echo "deb https://repos.ripple.com/repos/rippled-deb bionic stable" | tee -a /etc/apt/sources.list.d/ripple.list
RUN apt -y update
RUN apt -y install rippled

ENTRYPOINT [ "rippled" ]