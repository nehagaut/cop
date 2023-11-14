### **City of Portland**  
#### **Docker Usage for mapping**:  
1. Pull the docker iamge from docker hub:  
- For arm:
```
docker pull yirum/data_mapping:v0
```
- For amd/x86:
```
docker pull yirum/data_mapping:v1
```
2. Run docker by running the script:
```
sh docker_run.sh
# Note: need to change the absolute path of your Cop directory and the image name(v1 or v0)
```


Run the mapping code:
```
python3 mapping.py
```

#### **Docker Usage for backend**:  
1. Execute the Dockerfile to build the image:
```
docker build -t cop_backend .
```
2. Execute the script to run the image:
```
sh docker_run.sh
# Note: need to change the absolute path of your Cop directory
```
3. Once inside the container, initiate the backend service.
```
python3 app.py
```
For those wishing to access the backend and utilize the API for sending requests, we've provided a front-end script for your convenience. Please ensure you use the appropriate port number. In this example, we've designated port 8080 for our backend.
```
python test_api.py
```