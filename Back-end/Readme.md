### **City of Portland**  

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