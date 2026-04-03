---
id: "url-3f201fa8"
type: "api"
title: "1.2 Connecting"
url: "https://www.tiingo.com/documentation/general/connecting"
description: "Just remember, you will need your token in order to connect. Keep it safe."
source: ""
tags: []
crawl_time: "2026-03-18T02:54:35.274Z"
metadata:
  sections:
    - {"title":"1.2 Connecting","content":[{"type":"text","content":"Just remember, you will need your token in order to connect. Keep it safe."},{"type":"text","content":"Click here to see your API Token."}]}
    - {"title":"1.2.1 Connecting to the REST API","content":[{"type":"text","content":"Using our REST API is super easy to do. Just use your favorite programming language's web request package and the data will be returned via JSON or CSV."},{"type":"text","content":"To use the REST API, you must let our server know you have an account. You can do this by passing your API Token."},{"type":"text","content":"There are two (2) ways to pass your API token using the REST API."},{"type":"text","content":"1. Pass the token directly within the request URL."},{"type":"text","content":"You can pass the token directly in the request URL by passing the token parameter. For example you would query the https://api.tiingo.com/api/test/ endpoint with the token in URL by adding ?token=. Check out the copy & paste example below."},{"type":"text","content":"2. Pass the token in your request headers."},{"type":"text","content":"You can also pass the token in the request headers. Note you can do this by passing \"Token \" + your API token to the \"Authorization\" header. Check out the copy & paste examples below."},{"type":"code","content":"import requests\n\nheaders = {\n        'Content-Type': 'application/json'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\",\n                                    headers=headers)\nprint(requestResponse.json())"},{"type":"code","content":"{'message': 'You successfully sent a request'}"},{"type":"code","content":"import requests\n\nheaders = {\n        'Content-Type': 'application/json',\n        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test/\",\n                                    headers=headers)\nprint(requestResponse.json())"},{"type":"code","content":"{'message': 'You successfully sent a request'}"},{"type":"list","items":["Pass the token directly within the request URL.","Pass the token in your request headers."]}]}
    - {"title":"1.2.2 Connecting to the Websocket API","content":[{"type":"text","content":"Websockets allow for two-way communication, allowing us to data to you as soon as it's available. If you want real-time data, this is the fastest way to get it."},{"type":"text","content":"This can seem complicated if it's your first experience with websockets, but don't worry - it's just as easy with a RESTful interface and even more efficient. Websockets are both faster and uses less data than RESTful requests."},{"type":"text","content":"The web socket API functions a bit differently as you \"subscribe\" and \"unsubscribe\" to data sources. From there, you will receive all updates as soon as they're received without having to make requests."},{"type":"text","content":"Additionally, when new data comes in there will be a \"messageType\" which can be"},{"type":"text","content":"This lets us pass on notices that data has updated or some data is no longer considered valid Each request made to the websocket server contains a JSON object that follows the format:"},{"type":"text","content":"Notice how we have to pass an authorization token just like a REST request. Also notice the HeartBeat message. This is sent every 30 seconds to keep the connection alive."},{"type":"text","content":"Once we get our first data request back on a successful connection, the \"data\" attribute will contain a subscriptionId. This will be used for managing the connection. For example with IEX data, if we want to add or remove tickers in our subscription, we can send updates using the subscriptionId."},{"type":"code","content":"{\n    'eventName': 'subscribe',\n    'eventData': {\n                    'authToken': 'Not logged-in or registered. Please login or register to see your API Token',\n                    'service':'test'\n                }\n}"},{"type":"code","content":"from websocket import create_connection\nimport simplejson as json\nws = create_connection(\"wss://api.tiingo.com/test\")\n\nsubscribe = {\n                'eventName':'subscribe',\n                'eventData': {\n                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                            }\n                }\n\nws.send(json.dumps(subscribe))\nwhile True:\n    print(ws.recv())"},{"type":"code","content":"#Notice the \"HeartBeat\" message. This is sent every 30 seconds\n{\"data\": {\"subscriptionId\": 61}, \"response\": {\"message\": \"Success\", \"code\": 200}, \"messageType\": \"I\"}\n{\"response\": {\"message\": \"HeartBeat\", \"code\": 200}, \"messageType\": \"H\"}"},{"type":"list","items":["\"A\" for new data","\"U\" for updating existing data","\"D\" for deleing existing data","\"I\" for informational/meta data","\"E\" for error messages","\"H\" for Heartbeats (can be ignored for most cases)"]}]}
  codeExamples:
    - "import requests\n\nheaders = {\n        'Content-Type': 'application/json'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\",\n                                    headers=headers)\nprint(requestResponse.json())"
    - "{'message': 'You successfully sent a request'}"
    - "import requests\n\nheaders = {\n        'Content-Type': 'application/json',\n        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test/\",\n                                    headers=headers)\nprint(requestResponse.json())"
    - "{'message': 'You successfully sent a request'}"
    - "{\n    'eventName': 'subscribe',\n    'eventData': {\n                    'authToken': 'Not logged-in or registered. Please login or register to see your API Token',\n                    'service':'test'\n                }\n}"
    - "from websocket import create_connection\nimport simplejson as json\nws = create_connection(\"wss://api.tiingo.com/test\")\n\nsubscribe = {\n                'eventName':'subscribe',\n                'eventData': {\n                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                            }\n                }\n\nws.send(json.dumps(subscribe))\nwhile True:\n    print(ws.recv())"
    - "#Notice the \"HeartBeat\" message. This is sent every 30 seconds\n{\"data\": {\"subscriptionId\": 61}, \"response\": {\"message\": \"Success\", \"code\": 200}, \"messageType\": \"I\"}\n{\"response\": {\"message\": \"HeartBeat\", \"code\": 200}, \"messageType\": \"H\"}"
  tables: []
  tabContents:
    - {"sectionTitle":"1.2 Connecting","groupIndex":0,"tabIndex":0,"label":"Python","content":"import requests\n\nheaders = {\n        'Content-Type': 'application/json'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\",\n                                    headers=headers)\nprint(requestResponse.json())","tables":[],"codeExamples":["import requests\n\nheaders = {\n        'Content-Type': 'application/json'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\",\n                                    headers=headers)\nprint(requestResponse.json())"]}
    - {"sectionTitle":"1.2 Connecting","groupIndex":0,"tabIndex":1,"label":"Node","content":"var request = require('request');\nvar requestOptions = {\n        'url': 'https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token',\n        'headers': {\n            'Content-Type': 'application/json'\n            }\n        };\n\nrequest(requestOptions,\n        function(error, response, body) {\n            console.log(body);\n        }\n);","tables":[],"codeExamples":["var request = require('request');\nvar requestOptions = {\n        'url': 'https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token',\n        'headers': {\n            'Content-Type': 'application/json'\n            }\n        };\n\nrequest(requestOptions,\n        function(error, response, body) {\n            console.log(body);\n        }\n);"]}
    - {"sectionTitle":"1.2 Connecting","groupIndex":0,"tabIndex":2,"label":"PHP","content":"<?php\nrequire 'vendor/autoload.php';\nuse GuzzleHttp\\Client;\n\n$client = new Client();\n$res = $client->get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\", [\n'headers' => [\n    'Content-type' =>  'application/json'\n    ]\n]);","tables":[],"codeExamples":["<?php\nrequire 'vendor/autoload.php';\nuse GuzzleHttp\\Client;\n\n$client = new Client();\n$res = $client->get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\", [\n'headers' => [\n    'Content-type' =>  'application/json'\n    ]\n]);"]}
    - {"sectionTitle":"1.2 Connecting","groupIndex":1,"tabIndex":0,"label":"Python","content":"import requests\n\nheaders = {\n        'Content-Type': 'application/json',\n        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test/\",\n                                    headers=headers)\nprint(requestResponse.json())","tables":[],"codeExamples":["import requests\n\nheaders = {\n        'Content-Type': 'application/json',\n        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test/\",\n                                    headers=headers)\nprint(requestResponse.json())"]}
    - {"sectionTitle":"1.2 Connecting","groupIndex":1,"tabIndex":1,"label":"Node","content":"var request = require('request');\nvar requestOptions = {\n        'url': 'https://api.tiingo.com/api/test/',\n        'headers': {\n            'Content-Type': 'application/json',\n            'Authorization': 'Token Not logged-in or registered. Please login or register to see your API Token'\n            }\n        };\n\nrequest(requestOptions,\n        function(error, response, body) {\n            console.log(body);\n        }\n);","tables":[],"codeExamples":["var request = require('request');\nvar requestOptions = {\n        'url': 'https://api.tiingo.com/api/test/',\n        'headers': {\n            'Content-Type': 'application/json',\n            'Authorization': 'Token Not logged-in or registered. Please login or register to see your API Token'\n            }\n        };\n\nrequest(requestOptions,\n        function(error, response, body) {\n            console.log(body);\n        }\n);"]}
    - {"sectionTitle":"1.2 Connecting","groupIndex":1,"tabIndex":2,"label":"PHP","content":"<?php\nrequire 'vendor/autoload.php';\nuse GuzzleHttp\\Client;\n\n$client = new Client();\n$res = $client->get(\"https://api.tiingo.com/api/test/\", [\n'headers' => [\n    'Content-type' =>  'application/json',\n    'Authorization'     => 'Token Not logged-in or registered. Please login or register to see your API Token'\n    ]\n]);","tables":[],"codeExamples":["<?php\nrequire 'vendor/autoload.php';\nuse GuzzleHttp\\Client;\n\n$client = new Client();\n$res = $client->get(\"https://api.tiingo.com/api/test/\", [\n'headers' => [\n    'Content-type' =>  'application/json',\n    'Authorization'     => 'Token Not logged-in or registered. Please login or register to see your API Token'\n    ]\n]);"]}
    - {"sectionTitle":"1.2.1 Connecting to the REST API","groupIndex":2,"tabIndex":0,"label":"Python","content":"from websocket import create_connection\nimport simplejson as json\nws = create_connection(\"wss://api.tiingo.com/test\")\n\nsubscribe = {\n                'eventName':'subscribe',\n                'eventData': {\n                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                            }\n                }\n\nws.send(json.dumps(subscribe))\nwhile True:\n    print(ws.recv())","tables":[],"codeExamples":["from websocket import create_connection\nimport simplejson as json\nws = create_connection(\"wss://api.tiingo.com/test\")\n\nsubscribe = {\n                'eventName':'subscribe',\n                'eventData': {\n                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                            }\n                }\n\nws.send(json.dumps(subscribe))\nwhile True:\n    print(ws.recv())"]}
    - {"sectionTitle":"1.2.1 Connecting to the REST API","groupIndex":2,"tabIndex":1,"label":"Node","content":"var WebSocket = require('ws');\nvar ws = new WebSocket('wss://api.tiingo.com/test');\n\nvar subscribe = {\n        'eventName':'subscribe',\n        'eventData': {\n                        'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                    }\n        }\nws.on('open', function open() {\n    ws.send(JSON.stringify(subscribe));\n});\n\nws.on('message', function(data, flags) {\n    console.log(data)\n});","tables":[],"codeExamples":["var WebSocket = require('ws');\nvar ws = new WebSocket('wss://api.tiingo.com/test');\n\nvar subscribe = {\n        'eventName':'subscribe',\n        'eventData': {\n                        'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                    }\n        }\nws.on('open', function open() {\n    ws.send(JSON.stringify(subscribe));\n});\n\nws.on('message', function(data, flags) {\n    console.log(data)\n});"]}
  rawContent: "1. GENERAL\n1.2 Connecting\n\nJust remember, you will need your token in order to connect. Keep it safe.\n\nClick here to see your API Token\n.\n\n1.2 GENERAL - CONNECTING\n1.2.1 Connecting to the REST API\n\nUsing our REST API is super easy to do. Just use your favorite programming language's web request package and the data will be returned via JSON or CSV.\n\nTo use the REST API, you must let our server know you have an account. You can do this by passing your API Token\n.\n\nThere are two (2) ways to pass your API token using the REST API.\n\nPass the token directly within the request URL.\nPass the token in your request headers.\n\n1. Pass the token directly within the request URL.\n\nYou can pass the token directly in the request URL by passing the token parameter. For example you would query the https://api.tiingo.com/api/test/ endpoint with the token in URL by adding ?token=. Check out the copy & paste example below.\n\nPython\nNode\nPHP\nimport requests\n\nheaders = {\n        'Content-Type': 'application/json'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token\",\n                                    headers=headers)\nprint(requestResponse.json())\n                        \nResponse:\n{'message': 'You successfully sent a request'}\n\n\n2. Pass the token in your request headers.\n\nYou can also pass the token in the request headers. Note you can do this by passing \"Token \" + your API token\n to the \"Authorization\" header. Check out the copy & paste examples below.\n\nPython\nNode\nPHP\nimport requests\n\nheaders = {\n        'Content-Type': 'application/json',\n        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'\n        }\nrequestResponse = requests.get(\"https://api.tiingo.com/api/test/\",\n                                    headers=headers)\nprint(requestResponse.json())\n                        \nResponse:\n{'message': 'You successfully sent a request'}\n\n1.2 GENERAL - CONNECTING\n1.2.2 Connecting to the Websocket API\n\nWebsockets allow for two-way communication, allowing us to data to you as soon as it's available. If you want real-time data, this is the fastest way to get it.\n\nThis can seem complicated if it's your first experience with websockets, but don't worry - it's just as easy with a RESTful interface and even more efficient. Websockets are both faster and uses less data than RESTful requests.\n\nThe web socket API functions a bit differently as you \"subscribe\" and \"unsubscribe\" to data sources. From there, you will receive all updates as soon as they're received without having to make requests.\n\nAdditionally, when new data comes in there will be a \"messageType\" which can be\n\n\"A\" for new data\n\"U\" for updating existing data\n\"D\" for deleing existing data\n\"I\" for informational/meta data\n\"E\" for error messages\n\"H\" for Heartbeats (can be ignored for most cases)\n\nThis lets us pass on notices that data has updated or some data is no longer considered valid Each request made to the websocket server contains a JSON object that follows the format:\n\nResponse:\n{\n    'eventName': 'subscribe',\n    'eventData': {\n                    'authToken': 'Not logged-in or registered. Please login or register to see your API Token',\n                    'service':'test'\n                }\n}\n\n\nNotice how we have to pass an authorization token just like a REST request. Also notice the HeartBeat message. This is sent every 30 seconds to keep the connection alive.\n\nOnce we get our first data request back on a successful connection, the \"data\" attribute will contain a subscriptionId. This will be used for managing the connection. For example with IEX data, if we want to add or remove tickers in our subscription, we can send updates using the subscriptionId.\n\nPython\nNode\nfrom websocket import create_connection\nimport simplejson as json\nws = create_connection(\"wss://api.tiingo.com/test\")\n\nsubscribe = {\n                'eventName':'subscribe',\n                'eventData': {\n                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'\n                            }\n                }\n\nws.send(json.dumps(subscribe))\nwhile True:\n    print(ws.recv())\n                        \nResponse:\n#Notice the \"HeartBeat\" message. This is sent every 30 seconds\n{\"data\": {\"subscriptionId\": 61}, \"response\": {\"message\": \"Success\", \"code\": 200}, \"messageType\": \"I\"}\n{\"response\": {\"message\": \"HeartBeat\", \"code\": 200}, \"messageType\": \"H\"}\n"
  suggestedFilename: "general_connecting"
---

# 1.2 Connecting

## 源URL

https://www.tiingo.com/documentation/general/connecting

## 描述

Just remember, you will need your token in order to connect. Keep it safe.

## 代码示例

### 示例 1 (python)

```python
import requests

headers = {
        'Content-Type': 'application/json'
        }
requestResponse = requests.get("https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token",
                                    headers=headers)
print(requestResponse.json())
```

### 示例 2 (json)

```json
{'message': 'You successfully sent a request'}
```

### 示例 3 (json)

```json
{
    'eventName': 'subscribe',
    'eventData': {
                    'authToken': 'Not logged-in or registered. Please login or register to see your API Token',
                    'service':'test'
                }
}
```

### 示例 4 (text)

```text
from websocket import create_connection
import simplejson as json
ws = create_connection("wss://api.tiingo.com/test")

subscribe = {
                'eventName':'subscribe',
                'eventData': {
                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'
                            }
                }

ws.send(json.dumps(subscribe))
while True:
    print(ws.recv())
```

### 示例 5 (text)

```text
#Notice the "HeartBeat" message. This is sent every 30 seconds
{"data": {"subscriptionId": 61}, "response": {"message": "Success", "code": 200}, "messageType": "I"}
{"response": {"message": "HeartBeat", "code": 200}, "messageType": "H"}
```

## 文档正文

Just remember, you will need your token in order to connect. Keep it safe.

1. GENERAL
1.2 Connecting

Just remember, you will need your token in order to connect. Keep it safe.

Click here to see your API Token
.

1.2 GENERAL - CONNECTING
1.2.1 Connecting to the REST API

Using our REST API is super easy to do. Just use your favorite programming language's web request package and the data will be returned via JSON or CSV.

To use the REST API, you must let our server know you have an account. You can do this by passing your API Token
.

There are two (2) ways to pass your API token using the REST API.

Pass the token directly within the request URL.
Pass the token in your request headers.

1. Pass the token directly within the request URL.

You can pass the token directly in the request URL by passing the token parameter. For example you would query the https://api.tiingo.com/api/test/ endpoint with the token in URL by adding ?token=. Check out the copy & paste example below.

Python
Node
PHP
import requests

headers = {
        'Content-Type': 'application/json'
        }
requestResponse = requests.get("https://api.tiingo.com/api/test?token=Not logged-in or registered. Please login or register to see your API Token",
                                    headers=headers)
print(requestResponse.json())
                        
Response:
{'message': 'You successfully sent a request'}

2. Pass the token in your request headers.

You can also pass the token in the request headers. Note you can do this by passing "Token " + your API token
 to the "Authorization" header. Check out the copy & paste examples below.

Python
Node
PHP
import requests

headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token Not logged-in or registered. Please login or register to see your API Token'
        }
requestResponse = requests.get("https://api.tiingo.com/api/test/",
                                    headers=headers)
print(requestResponse.json())
                        
Response:
{'message': 'You successfully sent a request'}

1.2 GENERAL - CONNECTING
1.2.2 Connecting to the Websocket API

Websockets allow for two-way communication, allowing us to data to you as soon as it's available. If you want real-time data, this is the fastest way to get it.

This can seem complicated if it's your first experience with websockets, but don't worry - it's just as easy with a RESTful interface and even more efficient. Websockets are both faster and uses less data than RESTful requests.

The web socket API functions a bit differently as you "subscribe" and "unsubscribe" to data sources. From there, you will receive all updates as soon as they're received without having to make requests.

Additionally, when new data comes in there will be a "messageType" which can be

"A" for new data
"U" for updating existing data
"D" for deleing existing data
"I" for informational/meta data
"E" for error messages
"H" for Heartbeats (can be ignored for most cases)

This lets us pass on notices that data has updated or some data is no longer considered valid Each request made to the websocket server contains a JSON object that follows the format:

Response:
{
    'eventName': 'subscribe',
    'eventData': {
                    'authToken': 'Not logged-in or registered. Please login or register to see your API Token',
                    'service':'test'
                }
}

Notice how we have to pass an authorization token just like a REST request. Also notice the HeartBeat message. This is sent every 30 seconds to keep the connection alive.

Once we get our first data request back on a successful connection, the "data" attribute will contain a subscriptionId. This will be used for managing the connection. For example with IEX data, if we want to add or remove tickers in our subscription, we can send updates using the subscriptionId.

Python
Node
from websocket import create_connection
import simplejson as json
ws = create_connection("wss://api.tiingo.com/test")

subscribe = {
                'eventName':'subscribe',
                'eventData': {
                            'authToken': 'Not logged-in or registered. Please login or register to see your API Token'
                            }
                }

ws.send(json.dumps(subscribe))
while True:
    print(ws.recv())
                        
Response:
#Notice the "HeartBeat" message. This is sent every 30 seconds
{"data": {"subscriptionId": 61}, "response": {"message": "Success", "code": 200}, "messageType": "I"}
{"response": {"message": "HeartBeat", "code": 200}, "messageType": "H"}
