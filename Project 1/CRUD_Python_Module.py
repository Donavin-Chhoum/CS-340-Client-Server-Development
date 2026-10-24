# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, USER, PASS): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        # The USER and PASS are commented as they are used in the test script and are provided by the user
        # USER = 'aacuser' 
        # PASS = 'notarealpassword' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def get_next_rec_num(self, field_name='rec_num'):
        result = list(self.collection.find().sort(field_name, -1).limit(1))
        if result:
            return result[0][field_name] + 1 # Adds 1 to the current record count to get the next record number
        else:
            return 1 # If rec_num field is empty, 1 is the next/first record
        
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            data['rec_num'] = self.get_next_rec_num() # assigns the next available record number
            result = self.database.animals.insert_one(data)  # data should be dictionary 
            return True if result.acknowledged else False
        else: 
            print("Nothing to save, because data parameter is empty") 
            return False

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            result = list(self.collection.find(query))
            return result
        else:
            print("Nothing to read, because query parameter is empty")
            return []
        
    # Update Method in CRUD
    def update(self, query, new_data):
        if query is not None and new_data is not None:
            result = self.database.animals.update_many(query, {"$set": new_data})
            return result.modified_count
        else:
            print("Nothing to update, because query or new_data parameter is empty")
    
    # Delete Method in CRUD
    def delete(self, data):
        # if data: rejects empty dict {}, prevents deleting the entire database 
        if data:
            result = self.database.animals.delete_many(data)
            return result.deleted_count
        else:
            print("Nothing to delete, because data parameter is empty")
        
    