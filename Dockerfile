## Custom Dockerfile
FROM consol/debian-xfce-vnc
ENV REFRESHED_AT 2024-03-28
ENV VNC_PW=saitamatechno
ENV VNC_RESOLUTION=1280x720
#ENV RESTART_POLICY=Always

# Switch to root user to install additional software
USER 0
# Set the locale
#RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
#    locale-gen
#ENV LANG en_US.UTF-8  
#ENV LANGUAGE en_US:en  
#ENV LC_ALL en_US.UTF-8

#Turkish Language
RUN sed -i '/tr_TR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG tr_TR.UTF-8  
ENV LANGUAGE en_US:en
ENV LC_ALL tr_TR.UTF-8

RUN apt-get update -y
RUN apt install nano -y
RUN apt install python3-pip -y
RUN apt install git -y
RUN pip install selenium webdriver_manager Flask

RUN git clone https://github.com/ultralytics/google-images-download
RUN pip install -r google-images-download/requirements.txt

COPY templates/index.html /headless/google-images-download/templates/index.html
COPY flask1.py /headless/google-images-download/flask1.py
COPY README.md /headless/google-images-download/README.md

CMD python3 /headless/google-images-download/flask1.py

## switch back to default user
#USER 1000