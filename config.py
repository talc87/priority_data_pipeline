import yaml


with open('resources/config.yml','r') as file:
    config=yaml.safe_load(file)


#mySQL
sqlConnStr = config['sqlDB']['sqlConnStr']

#mongo DB
mongoDbConnStr = config['mongoDB']['mongoDbConnStr']
metadataDbName = config['mongoDB']['metadataDbName']
configDbName = config['mongoDB']['configDbName']
configCollectionName = config['mongoDB']['configCollectionName']
datatypeMappingCollectionName = config['mongoDB']['datatypeMappingCollectionName']

