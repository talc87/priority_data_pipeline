from pymongo import MongoClient, DESCENDING,errors
import json
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def deployMongodb(uri:str,dbName:str,collectionName:str):
    """
    The method connects to a MongoDB instance, clears an existing collection, 
    and loads new data mapping documents from a JSON file.

    Args:
        uri (str): MongoDB connection string.
        dbName (str): Name of the database to connect to.
        collectionName (str): Name of the collection to clear and insert data into.
        
    """

    # Connect to the MongoDB instance using the connection string
    client = MongoClient(uri)
    db = client[dbName]
    dataMappingCollection = db[collectionName]

    
    #delete all documents in the collection
    dataMappingCollection.delete_many({})
    # Load the data from the metadata_json.json file
    with open('resources/static/datatypesConvert.json', "r") as f:
        data = json.load(f)

    # Insert the data into the collection
    dataMappingCollection.insert_many(data)





def getExtractionConfig(uri:str, dbName:str, collectionName:str, dataSourceId:str)->dict:
    '''
    description: get the latest extraction config for a given data source id
    params: dataSourceId:str - the data source id
    returns: 
            if the document was found in the mongoDB, retun thr document, else return None
    raise: raise 
    '''
    
    logging.debug(f'fetching the extractionConfig JSON for dataSourceId- {dataSourceId} from mongoDB')
    # Connect to the MongoDB instance using the connection string
    try:
        client = MongoClient(uri)

        # Get a reference to the specified database
        db = client[dbName]
        config_collection = db[collectionName]

        
        query = {"_id": dataSourceId}
        sort_by = [("submitTimestampUTC", DESCENDING)]
        extractionConfig = config_collection.find_one(query, sort=sort_by)
        return extractionConfig
    
    except Exception as e:
        logging.error(f'Error while trying to fetch the extractionConfig document for _id = {dataSourceId}')
        raise Exception(f"An error occurred during MongoDB operation: {e}")
    

