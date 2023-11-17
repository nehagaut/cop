FROM mongo:latest
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get update && apt-get install -y nodejs npm
RUN pip3 install pandas
RUN pip3 install openpyxl
RUN pip3 install flask pymongo
RUN pip3 install flask-cors
RUN mkdir /home/cop