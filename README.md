# pdf-crawler

This is sample pdf crawler which provide service for parsing incomeing pdf files and executing Internet URLs from them, also it
provides api for getting base statistic information as described in terms of reference.

## Getting Started

For runing this project on your local you need to install and activate python virtualenvironment, 
after that you need to install project dependencies by running: 

```
pip install -r requirements
```

after that you have to run migrations 

```
python manage.py migrate
```

after all dependencies would be installed, you can run django server as you run it normally
```
python manage.py runserver
```


## The server supports the following REST WS:

```
POST: /documents/upload/ - endpoint for uploading PDF file, witch will be analized.
GET: /documents/ - endpoint returns a set of all the of documents that were uploaded: ids, names and number of URLs that were found for each document
GET: /documents/<document_id> - endpoint returns a set of URLs for a specific document
GET: /documents/links/ - endpoint returns a set of all URLs found, including the number of documents that contained the URL.
```

## Samples

You can use any kind of PDF documents for testing, but I want provide you example:
```
https://www.dropbox.com/s/ob6wlyp60hc763t/Igor_Kuzmenko_cv_.pdf?dl=0
```


