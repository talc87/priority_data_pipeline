from datetime import timezone,datetime
from flask import Flask, jsonify, request, g
from pymongo import MongoClient
from functools import wraps
import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

import requests
from requests.auth import HTTPBasicAuth


#custom libraries
from resources.priorityDataSource import priorityDataSource
from resources import mongodbHelper
from resources.sqlDwh import sqlDwh
from resources import config as configFile



#importing the variables names from the yml file (using config.py)
mongodbConnStr = configFile.mongoDbConnStr
sqlConnStr = configFile.sqlConnStr
metadataDbName = configFile.metadataDbName
configDbName = configFile.configDbName
configCollectionName = configFile.configCollectionName
datatypeMappingCollectionName = configFile.datatypeMappingCollectionName


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.getLogger('pymongo').setLevel(logging.WARNING)

app = Flask(__name__)



#custom decorator to fectch the extractionConfig JSON
def getExtractionconfig(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        
        #getting the json body from the request. silent=True --> requestJson will be None of no json was attached
        requestJson = request.get_json(silent=True)

        # Check if the request json is not empty
        if not requestJson or 'datasourceId' not in requestJson.keys():
            return jsonify({'error message': 'The request must include a JSON with a datasourceId key'}), 400
        
        # Use the data in your MongoDB query
        dataSourceId = requestJson['datasourceId']
      
        
        try:
            g.extractionConfig = mongodbHelper.getExtractionConfig(uri=mongodbConnStr,dbName=configDbName,collectionName=configCollectionName, dataSourceId=dataSourceId)

        except Exception as e:
            logging.error(f'Error while trying to fetch the extractionConfig document for _id = {dataSourceId}')
            raise Exception(f"An error occurred during MongoDB operation: {e}")
        return route_function(*args, **kwargs)

    return wrapper



@app.route('/')
def home():

  
    return jsonify({'MomongoDB connection string': mongodbConnStr
                    ,'SQL connection string' : sqlConnStr
                    }),200


@app.route('/pingApi')
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def pingApi():
    extractionConfig = g.extractionConfig
    logging.debug('ping priority erp, mongoDB and SQL to check that the app can access them')
    
    # ping mongoDB
    client = MongoClient(mongodbConnStr)
    mongoDbName = client[configDbName]
    mongoDBPing = str(client.mongoDbName.command('ping'))
    
    # ping SQL
    logging.debug('ping SQL to check the connection is OK')
    dbUri=configFile.sqlConnStr + 'acc-' + extractionConfig['accountID']
    engine = create_engine(dbUri)

    try:
        # Ping the database
        engine.connect()
        sqlPing = ("Database connection is OK.")
    except OperationalError as e:
        sqlPing = f"Error: {e}"
    finally:
        # Close the engine
        engine.dispose()

    # ping priority erp api
    api_credentials = HTTPBasicAuth(extractionConfig['apiUsername'],extractionConfig['apiPassword'])
    r = requests.get(extractionConfig['uri'],auth=api_credentials)
    priorityApiResponse = "priority_api_response:" +str(r.status_code)+ " reponse_text: " +str(r.reason)
    

  
    return jsonify({'MomongoDB response': mongoDBPing
                    ,'SQL reponse' : sqlPing
                    ,'Priority api response':priorityApiResponse
                    }),200
                    


@app.route('/refreshPriorityMetadata', methods=['GET'])
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def refreshMetadta():
    
    extractionConfig = g.extractionConfig
    logging.debug('JSON body was received, trigerring "refreshMeatdata" method')
    startTimestamp = datetime.now(timezone.utc)
    
    logging.debug('extracting datasource metadata')
    ptr = priorityDataSource(extractionConfig)
    metadataRefreshResults = ptr.refreshMeatdata()
    endTimestamp = datetime.now(timezone.utc)
    
    metadataRefreshResults['startTimestampUTC'] = startTimestamp
    metadataRefreshResults['endTimestampUTC'] = endTimestamp
    metadataRefreshResults['totalTimeSeconds'] = (endTimestamp - startTimestamp).total_seconds()
    
    logging.debug(f'Returning the metadata refresh results {metadataRefreshResults}')
    return jsonify({'refreshPriorityMetadata': metadataRefreshResults})



@app.route('/buildDdwhTables', methods=['POST'])
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def buildDdwhTables():

    extractionConfig = g.extractionConfig       # --> get the extractionConfig from @getExtractionconfig
    
    #create a class instance
    ptr=sqlDwh(extractionConfig,sqlSSL=False)

    # create a database in the SQL server if it doesn't exist.
    ptr.createDb()

    # create the tables in the SQL db based on the extractionConfig files.
    r = ptr.deployExtractionconfigTables()
    
    return jsonify({'buildDdwhTables': r }), 200



@app.route('/refreshData', methods=['POST'])
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def refreshData():
    extractionConfig = g.extractionConfig       # --> get the extractionConfig from @getExtractionconfig
    
    # fetching the incremental request parameter and convert it to a boolean expression, if not attached set to true
    incrementalParam = request.args.get('incremental', default='true')
    incremental = incrementalParam.lower() in 'true'

    logging.debug(f'Trigerring "refreshData" method, incrementalFlag set to {incremental}')
    ptr = priorityDataSource(extractionConfig)
    r = ptr.refreshData(incremental)
    
    return jsonify({'refreshData': r}), 200



@app.route('/initialDataLoad', methods=['POST'])
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def initialDataLoad():
    extractionConfig = g.extractionConfig       # --> get the extractionConfig from @getExtractionconfig
    
    
    
    # refreshing the metadata
    logging.debug('JSON body was received, trigerring "refreshMeatdata" method')
    startTimestamp = datetime.now(timezone.utc)
    
    logging.debug('extracting datasource metadata')
    ptr = priorityDataSource(extractionConfig)
    metadataRefreshResults = ptr.refreshMeatdata()
    endTimestamp = datetime.now(timezone.utc)
    
    metadataRefreshResults['startTimestamp'] = startTimestamp
    metadataRefreshResults['endTimestamp'] = endTimestamp
    metadataRefreshResults['totalTimeSeconds'] = (endTimestamp - startTimestamp).total_seconds()
    # return dict ---> metadataRefreshResults
    

    #buidling the dwh
    ptr=sqlDwh(extractionConfig,sqlSSL=False)
    # create a database in the SQL server if it doesn't exist.
    ptr.createDb()
    # create the tables in the SQL db based on the extractionConfig files.
    sqlDeployedTables = ptr.deployExtractionconfigTables()
    # return dict ---> sqlDeployedTables


    #preform a full data loading
    incremental=False
    logging.debug(f'Trigerring "refreshData" method, incrementalFlag set to {incremental}')
    ptr = priorityDataSource(extractionConfig)
    refreshtTablesData = ptr.refreshData(incremental)
    # return dict ---> refreshtTablesData
    


    # Merging all the JSON responses into a single dictionary
    returnedValue = {
                    "metadataRefreshResults": metadataRefreshResults,
                    "sqlDeployedTables": sqlDeployedTables,
                    "refreshtTablesData": refreshtTablesData
                    }


    return jsonify(returnedValue), 200



@app.route('/deleteAllTables', methods=['POST'])
@getExtractionconfig # ---> run custom decorator to fetch the getExtractionconfig json
def deleteAllTables():
    extractionConfig = g.extractionConfig
    t=sqlDwh(extractionConfig,sqlSSL=False)
    deleteAllTables = t.deleteTables()

    return jsonify(deleteAllTables),200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # This is fine since it's running on port 5000 inside the container


