<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

-->

<!-- PROJECT LOGO
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
<h1 align="center" style="color:#black;">Priority ERP Data Platform</h3>
<!--
  <p align="center">
    <strong><em><span style="color:#black;">Priority Data Platform is a self service DWH platform which helps the user to builds end-to-end MySQL DWH. The app gets the data incrementaly using the Priority API and builds a MySQL DWH.</strong></em></span>
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>

<style>
a {
  color: red;
}
</style>

-->

<!-- TABLE OF CONTENTS -->

<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
    <ul>
      <li><a href="#built-with">Build With</a></li>
      <li><a href="#data-platform-architecture">Data Platform Architecture</a></li>
    </ul>
  </li>
  
  <li>
    <a href="#prerequisites">Prerequisites</a>
    <ul>
      <li><a href="#priority-prerequisites">Priority Prerequisites</a></li>
      <li><a href="#setting-to-config-file">Setting to config file"</a></li>
      <li><a href="#mongodb-prerequisites">MongoDB prerequisites</a></li>
      <li><a href="#postgres-db-prerequisites">Postgres DB Prerequisites</a></li>
    </ul>
  </li>
  
  <li>
    <a href="#the-extractionconfig-json">The extractionConfig JSON</a>
  </li>
  
  
  
  <li>
    <a href="#API-endpoints">API endpoints</a>
    <ul>
      <li><a href="#refreshprioritymetadata">refreshPriorityMetadata</a></li>
      <li><a href="#buildddwhtables">buildDdwhTables</a></li>
      <li><a href="#refreshdata">refreshData</a></li>
    </ul>

  </li>

  <li><a href="#roadmap">Roadmap</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
  <li><a href="#contact">Contact</a></li>
  <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>

<!-- ABOUT THE PROJECT -->

### About The Project

Priority is an ERP system for S&M business. <br>
The project builds your Priority using on a Postgres DB using the it's API. The API allow you to get the data exactly the same way the business user sees it on the Priority GUI. Unlike connecting to the Priority SQL DB which requires the BI developer to create the user business logics using SQL queries.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- [![Laravel][Azure]][azure-url]&emsp; -->

[![Laravel][MongoDB]][MongoDB-url]&emsp;
[![Laravel][Postgres]][Postgres-url]&emsp;
[![Laravel][Python]][python-url]&emsp;
[![Laravel][flask]][flask-url]&emsp;

<!-- [![Laravel][Docker]][Docker-url] -->

<!--The platform was developed on Azure, and can be hosted on other cloud providers (i.e. AWS or GCP) and on-prem with the required modification. -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Data Platform Architecture

<!-- ![process flow diagram](https://raw.githubusercontent.com/talc87/Priority-Data-Platform-ELT/main/process%20flow.jpg) -->

_Will be Added_
<br>

<!-- GETTING STARTED -->

## Prerequisites

### Priority Prerequisites

_The doc will not include a step by step guide of how to set the Priority user and API access rights and API subscription fees. I assume that you know how how to grant access to the API, how to set the relevnt screens etc. For any issues around this topic are, I recomand to contanct you Priority support team/system admin/implementor._

1. Create a dedicated user with API access. **The data platform doesn't write any data to your Priority system and required only ("read only") HTTP GET access**
1. Make sure you have the API address, username and password.
1. [For testing purposes you can use the free Priority API sandbox](https://prioritysoftware.github.io/restapi/).

<br>

### Setting to config file.

```yaml
#resources/config.yml

sqlDB:
  sqlConnStr: postgresql+psycopg2://<username>:<password>@<url>:<port>/

mongoDB:
  mongoDbConnStr: mongodb+srv://<username>:<password>@<url>/

  metadataDbName: MetadataDB
  configDbName: admin
  configCollectionName: configCollection
  datatypeMappingCollectionName: datatypeMapping
```

<br>

- sqlConnStr: uri to a postgres DB. Don't delete the '/' at the end.
- mongoDbConnStr: uri to the MongoDB you will use.

- metadataDbName: the Mongo DB name which stores the metadata of the Priority ERP system. You can choose any name you want.
- configDbName: the Mongo DB name which stores the extractionConfig. You can choose any name you want.
- configCollectionName: The Mongo DB collection which stores the extractionConfig JSON documents. You can choose any name you want. The configCollectionName will be created under the configDbName DB.

- Choose "accountID"- accountID is a uniqe ID string which identify you inside the data platform and let the MongoDB fetch the extraction configuration from the MongoDB, the Postgres DB name be named according to your AccountID (accountID- <accountID string>).
  Each accountID can include multiple datasources (extractionConfig).

<br>
<br>

### MongoDB prerequisites

The MongoDB stores metadata, extraction logs and other app related data. While developing I used [MongoDB free tier](https://www.mongodb.com/). Using a free tier on production is not recomanded. While tesing I used a paid tier of [Azure Cosmos DB for MongoDB](https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/introduction). Feel free ot use other MongoDB based DB of other cloud providers.

#### Setup a MongoDB instance

- After deploying your mongoDB in you enviorment, send a post request to the API <http://<api address>:<port>/deployMongoDB>
  to create create a required collection.
- Don't forget to allow incoming traffic from the IP you are running the API on.

<br>

### Postgres DB Prerequisites

The Postgres stores the data which come from the Priority system (Invoices, JE, PO etc.) and served as a DWH.
I used [Azure Database for PostgreSQL flexible server](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/service-overview).

- Create a DB and name it acc-<accountID>
- Don't forget to allow incoming traffic from the IP you are running the API on.
- You don't need to create any tables, all tables will be created later automatically.

<br>
<br>

<!-- ### Azure Cloud Prerequisites

The data platform is running in a containerize enviorment. I developed and tested the data platform on Azure cloud and so this readme will guide you to deploy the data platform to Azure, based on "Azure Container Apps" and "Azure Container Regenstry" (ECR). You can try and deploy the data platform to other cloud providers (i.e. to AWS using AWS Fargate (Azure container Apps equivalent) and AWS ECR. Or any other container compute and container regestry.
<br>

#### Setup Azure container Apps

Will be updated soon.

#### Setup Azure Container Registry (ACR)

Will be updated soon.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

<br>

## The extractionConfig JSON

In the section below you will get the required information reagrding the extractionConfig json document, which is main responsible for the data extraction from the Priority API. The extractionConfig defines the API credentionals, url,and extraction scope.

**After completing reading this section, create your extractionConfig according to your requests and inswer the json document to the MongoDB '<configDbName>.<\_id>'.
configDbName is defined @config.yml. '\_id' is a uniqe identifier of the extractionConfig as desribed below.**

The extractionConfig JSON represents the most basic layer of the extraction, extractionConfig represents a Priority API route. In a case you have more then 1 accounting instance (Priority company code in you enviorment) each accounting instnace will be represented by a extractionConfig. All accounting instaces will be included in the same accountID.

<p>
For example: company "The best smartphone" has 3 major business activities: sells smartphone to the customer (B2C), provide repairs and spare-part services and import smartphone and sell them as a wholesaler (B2B). each business activity is manages in a different company (accounting instance) in the Priority System.
In the exaple above "The best smartphone" will be represented by an accountID (choose the string as you want). Inside this accountID there will be 3 extractionConfigs, one for each company code.

**Check out the folder "extractionConfig_examples" to see examples of the extractionConfig json.**

### Populate extractionConfig JSON

```json
{
	"_id": "65fddeb2721b0abe0f9c04ff",
	"datasourceName": "priority_companyA",
	"uri": "https://www.eshbelsaas.com/ui/odata/Priority/tabmob.ini/usdemo/",
	"apiUsername": "apidemo",
	"apiPassword": "123",
	"accountID": "03445d66",
	"systemTimezone": "Israel",
	"sourceSystem": "priority",
	"entities": [
		{
			"EntityID": "ORDERS",
			"filterFlag": true,
			"filterField": "CURDATE",
			"expand": ["ORDERITEMS"],
			"lastRun": "2024-06-12 21:53:35",
			"datarStartDate": "2020-05-30 00:00:00"
		},
		{
			"EntityID": "CTYPE",
			"filterFlag": false,
			"filterField": "",
			"expand": [],
			"lastRun": "2024-06-12 21:53:40",
			"datarStartDate": "2020-05-30 00:00:00"
		}
	]
}
```

**Field details and description**

- **\_id**- uuid4 string. a uniqe identifier of the extractionConfig.
- **datasourceName** - string. Choose a name to the extractionConfig.
- **uri-** string. The Prioriy API address according to your Priority system.
- **apiUsername-** Username to the API user you created for the data extraction.
- **apiPassword-** Password to the API user you created for the data extraction.
- **accountID**- string. Enter the accountID you chose in section Priority Prerequisites > Choose accountID above.
- **PrioritySystemTimeZoneId-** Priority system timezone. [For the full timezones list refer to pytz-time-zones](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568).
- **sourceSystem**- string. No need to modify, keep 'priority'.

- **Entities-** A list of entities (Priority screens) you ask to extract the data from. Each entity is represented by list item. You need to complete all the fields below:

  - EntityID- entity name (Priority screen technical name).
  - filterFlag- boolean. A flag which determines whether a filter will be applied while extracting the data from this entity.
  - filterField- Determine according to which filter the data will be filtered too.
  - expand- a list of sub-forms/sub-screens that you want to extract together wi the entityID. In the example above together with the screen "ORDERS" the sub-screen "ORDERITEMS" will be extracted as well. the subscreen will be stored in a different table inside the Postgres DB.

  - lastRun- Auto-generated by the app, No need to modify. The last timestamp which the entityID was extracted from the API.
  - datarStartDate - timestamp (yyyy-MM-dd HH:mm:ss) The baseline timestamp which you want to extract the data from. In the example above the extraction will fetch all the ORDERS which thier.

> **For example**:<p>
> In the extractionConfig above, each time the the data in the dwh will be refresh:
> The entity "ORDERS" will be filterd according to the "CURDATE" field. The value which be filterd depands if the data-refresh is incremental or not. If the refresh is incremental, all the orders from '2024-06-12 21:53:35' <lastrun> will be enterd to the dwh. If the refresh is not incremental, all the orders from '2020-05-30 00:00:00' <datarStartDate> will be enterd to the dwh.
> The entity 'CTYPE' won't be filterd (filterFlag set to false) and since there is no filterField, each refresh all the historical data will be enterd to the dwh.
> For more information about incremental refresh, refer to the API documention.

<br>

## API endpoints

**All requests except deployMongoDB [POST] should include the datasourceId you chose as a body json.**

```sh
  {
    "datasourceId": "65fddeb2721b0abe0f9c04ff"
  }
```

<br>

### refreshPriorityMetadata

Fetch Priority full metadata (GET serviceRoot/$metadata), parse the XML, convert to JSON and insert it to MongoDB <metadataDbName>.<\_id> collection. In a case that the collection contains previoues metadata documents, all previoues metadata will be deleted.
Example of a metadata document of the entity "ABILITIES"

```json
{
	"_id": "ABILITIES",
	"SourceSystem": "Priority",
	"Desc": "כישורים",
	"Fields": [
		{
			"fieldName": "ABILITYCODE",
			"SourceDataType": "Edm.String",
			"desc": "קוד כישור",
			"KeyFlag": true,
			"targetDataType": "TEXT(255)"
		},
		{
			"fieldName": "ABILITYDES",
			"SourceDataType": "Edm.String",
			"desc": "תאור כישור",
			"KeyFlag": false,
			"targetDataType": "TEXT(255)"
		},
		{
			"fieldName": "ABILITY",
			"SourceDataType": "Edm.Int64",
			"KeyFlag": false,
			"targetDataType": "BigInteger"
		}
	],
	"LastModified": {
		"$date": {
			"$numberLong": "1682096005711"
		}
	}
}
```

Python syntax:

```python
url = "http://localhost:5000/refreshPriorityMetadata"

Method = 'GET'

payload = {
           "datasourceId": <data source _id>
          }

headers = {
            'Content-Type': 'application/json'
          }

response = requests.request(Method, url, headers=headers, data=payload)

```

refreshPriorityMetadata endpoint response:

```jsonc
{
	"getPriorityMetadata": {
		"documentsDeleted": 3737, //num of deleted documents before populated the current metadata documents
		"endTimestamp": "Fri, 12 Jul 2024 14:00:25 GMT", //timestamp the metadata refresh ended
		"metadataInserted": true, //boolean expression if the documents
		"metadataRecordsBeforeDelete": 3737, //num of documents in the metadataDbName._id collection before running getPriorityMetadata
		"metadataRecordsDatatypedModified": 3737, //num of documents in which their data type translated from Priority to Postgres data type
		"metadataRecordsExtractedFromApi": 3737, //num of documents extracted from the API
		"startTimestamp": "Fri, 12 Jul 2024 14:00:04 GMT", //timestamp the metadata refresh started
		"totalTimeSeconds": 21.033948 //endTimestamp - startTimestamp
	}
}
```

<br>

### buildDdwhTables

**Must run GET refreshPriorityMetadata before**<p>
Deploy a table in the Postgres DWH for each entity and sub-entity in extractionConfig json, according to the entity/sub-entity metadata.
The API will set the relevant data types and primary keys according to the Priority system.

CreateDWHTable endpoint request example:

Python syntax:

```python
url = "http://localhost:5000/buildDdwhTables"

Method = 'POST'

payload = {
            "datasourceId": <data source _id>
          }

headers = {
            'Content-Type': 'application/json'
          }

response = requests.request(Method, url, headers=headers, data=payload)

```

buildDdwhTables endpoint response:

```jsonc
{
	"buildDdwhTables": {
		"exists": [], //list. Tables which already in the Postgres DB and should not re-created
		"failed": [], //list. Tables which weren't created due to errors
		"success": ["ORDERS", "ORDERITEMS", "CTYPE"] //list. Tables which created successfully
	}
}
```

<br>

### refreshData

Refresh and write the data into stg\_<entity name> tables.
**incremental parameter set to False**: all data in the stg tables will be dropped a the refresh will be preformed from datarStartDate till today.

**incremental parameter set to True**: refresh will be preformed from lastRun till today according to the filterField key.

refreshData endpoint request example:

**Python syntax**:

```python
url = "http://localhost:5000/refreshData?incremental=False"

Method = 'POST'

payload = {
            "datasourceId": <data source _id>
          }

headers = {
            'Content-Type': 'application/json'
          }

response = requests.request(Method, url, headers=headers, data=payload)

```

refreshData endpoint response:

```jsonc
{
	"refreshData": [
		{
			"entityName": "ORDERS", //the entity/sub-entity name according to the Priority system
			"recordsWritten": 284, //number of records which were written to the table
			"tableName": "stg_ORDERS" //Postgres table name which the data was written to
		},
		{
			"entityName": "ORDERITEMS_SUBFORM", //
			"recordsWritten": 13, //
			"tableName": "stg_ORDERITEMS" //
		},
		{
			"entityName": "CTYPE", //
			"recordsWritten": 5, //
			"tableName": "stg_CTYPE" //
		}
	]
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

Will be updated soon.

See the [open issues][issues-url] for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Will be updated soon.

<!--
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 -->
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License.

## Contact

Tal Cohen - [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tal-cohen-b5127852/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/talc87/Priority-Data-Platform-ELT/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[MongoDB]: https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/
[Postgres]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Azure]: https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white
[azure-url]: https://azure.microsoft.com/en-us/
