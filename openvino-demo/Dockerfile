FROM openvino_rpi:latest

SHELL ["/bin/bash", "-c"]

RUN pip3 install setuptools wheel

COPY ./files /root

RUN pip3 install -r /root/requirement.txt

WORKDIR /root

CMD source /opt/intel/openvino/bin/setupvars.sh && \
    ./start.sh
