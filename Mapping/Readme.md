### **City of Portland: Designing an Open Contracting Program Mapping**  

The mapping.py script serves as a mapper to transform contract data into the Open Contracting Data Standard (OCDS) format and subsequently stores this converted data in a MongoDB database.

The mongodb_connect.py script is a Python utility designed to facilitate the retrieval of JSON files based on the contract ID. For example, to fetch a specific contract's data, you can use a command like this in your terminal:
```
python3 mongodb_connect.py 30006409
```
This command will access the MongoDB database and return the JSON data associated with the contract ID 30006409.

