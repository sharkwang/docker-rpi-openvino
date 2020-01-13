FROM balenalib/rpi-raspbian:latest

RUN apt-get update && \
    apt-get install -y wget cmake g++ autoconf libtool \
       apt-utils automake cpio gcc g++ usbutils libatlas-base-dev \
       libgtk-3-dev libstdc++6 lsb-release make \
       python3-pip python3-numpy python3-scipy udev \
       unzip vim  && \
       apt-get autoremove && \
       rm -rf /var/lib/apt/lists/*

# Install openvino package
RUN wget https://download.01.org/opencv/2019/openvinotoolkit/R3/l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz && \
    mkdir -p /opt/intel/openvino && \
    tar xzvf l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz --strip 1 -C /opt/intel/openvino

# Install libusb to find Movidius device
RUN wget https://github.com/libusb/libusb/archive/v1.0.23.tar.gz && \
    tar xzvf v1.0.23.tar.gz && \
    cd libusb-1.0.23 && \
    ./bootstrap.sh && \
    ./configure --disable-udev --enable-shared  && \
    make && \
    make install && \
    ldconfig /usr/local/lib && \
    rm -rf libusb-1.0.23

RUN rm -f l_openvino_toolkit_runtime_raspbian_p_2019.3.334.tgz v1.0.23.tar.gz && \
    echo "source /opt/intel/openvino/bin/setupvars.sh" >> ~/.bashrc

