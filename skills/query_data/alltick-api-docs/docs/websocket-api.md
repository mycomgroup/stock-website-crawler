---
id: "url-781ace27"
type: "api"
title: "Websocket 请求示例"
url: "https://apis.alltick.co/websocket-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:56:47.250Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["Websocket API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"code","language":"http","value":"复制package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"复制import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"复制<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"复制import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
    - {"type":"code","language":"http","value":"import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
    - {"type":"code","language":"http","value":"import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于2个月前"}]}
  codeExamples:
    - {"type":"code","language":"http","value":"复制package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}"}
    - {"type":"code","language":"http","value":"复制import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}"}
    - {"type":"code","language":"http","value":"复制<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>"}
    - {"type":"code","language":"http","value":"复制import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
    - {"type":"code","language":"http","value":"import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
    - {"type":"code","language":"http","value":"import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()"}
  tables: []
  parameters: []
  markdownContent: "# Websocket 请求示例\n\n1. Websocket API\n\nEnglish / 中文\n\n```http\n复制package main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}\n```\n\n```http\npackage main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}\n```\n\n```http\npackage main\n\nimport (\n\t\"encoding/json\"\n\t\"github.com/google/uuid\"\n\t\"github.com/gorilla/websocket\"\n\t\"log\"\n\t\"time\"\n)\n\ntype Symbol struct {\n\tCode       string `json:\"code\"`\n\tDepthLevel int    `json:\"depth_level\"`\n}\n\ntype Data struct {\n\tSymbolList []Symbol `json:\"symbol_list\"`\n}\n\ntype Request struct {\n\tCmdID  int    `json:\"cmd_id\"`\n\tSeqID  int    `json:\"seq_id\"`\n\tTrace  string `json:\"trace\"`\n\tData   Data   `json:\"data\"`\n}\n\n/*\n\tSpecial Note:\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\tToken Application: https://alltick.co\n\tReplace \"testtoken\" in the URL below with your own token\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\twss://quote.alltick.co/quote-b-ws-api\n\tStock API address:\n\twss://quote.alltick.co/quote-stock-b-ws-api\n*/\nconst (\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n)\n\nfunc websocket_example() {\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\tif err != nil {\n\t\tlog.Fatal(\"dial:\", err)\n\t}\n\tdefer c.Close()\n\n\t// Send heartbeat every 10 seconds\n\tgo func() {\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\t\t\treq := Request{\n\t\t\t\tCmdID: 22000,\n\t\t\t\tSeqID: 123,\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\t\t\t\tData:  Data{},\n\t\t\t}\n\t\t\tmessageBytes, err := json.Marshal(req)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\t\t\t\treturn\n\t\t\t}\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\t\t\tif err != nil {\n\t\t\t\tlog.Println(\"write:\", err)\n\t\t\t}\n\t\t}\n\t}()\n\n\treq := Request{\n\t\tCmdID: 22002,\n\t\tSeqID: 123,\n\t\tTrace: uuid.New().String(),\n\t\tData: Data{SymbolList: []Symbol{\n\t\t\t{\"GOLD\", 5},\n\t\t\t{\"AAPL.US\", 5},\n\t\t\t{\"700.HK\", 5},\n\t\t\t{\"USDJPY\", 5},\n\t\t}},\n\t}\n\tmessageBytes, err := json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\treq.CmdID = 22004\n\tmessageBytes, err = json.Marshal(req)\n\tif err != nil {\n\t\tlog.Println(\"json.Marshal error:\", err)\n\t\treturn\n\t}\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\tif err != nil {\n\t\tlog.Println(\"write:\", err)\n\t}\n\n\trece_count := 0\n\tfor {\n\t\t_, message, err := c.ReadMessage()\n\n\t\tif err != nil {\n\t\t\tlog.Println(\"read:\", err)\n\t\t\tbreak\n\t\t} else {\n\t\t\tlog.Println(\"Received message:\", string(message))\n\t\t}\n\n\t\trece_count++\n\t\tif rece_count%10000 == 0 {\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\t\t}\n\t}\n\n}\n```\n\n```http\n复制import java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}\n```\n\n```http\nimport java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}\n```\n\n```http\nimport java.io.IOException;\nimport java.net.URI;\nimport java.net.URISyntaxException;\nimport javax.websocket.*;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n@ClientEndpoint\npublic class WebSocketJavaExample {\n\n    private Session session;\n\n    @OnOpen\n    public void onOpen(Session session) {\n        System.out.println(\"Connected to server\");\n        this.session = session;\n    }\n\n    @OnMessage\n    public void onMessage(String message) {\n        System.out.println(\"Received message: \" + message);\n    }\n\n    @OnClose\n    public void onClose(Session session, CloseReason closeReason) {\n        System.out.println(\"Disconnected from server\");\n    }\n\n    @OnError\n    public void onError(Throwable throwable) {\n        System.err.println(\"Error: \" + throwable.getMessage());\n    }\n\n    public void sendMessage(String message) throws Exception {\n        this.session.getBasicRemote().sendText(message);\n    }\n\n    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {\n        // Special Note:\n        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n        // Token Application: https://alltick.co\n        // Replace \"testtoken\" in the URL below with your own token\n        // API addresses for forex, cryptocurrencies, and precious metals:\n        // wss://quote.alltick.co/quote-b-ws-api\n        // Stock API address:\n        // wss://quote.alltick.co/quote-stock-b-ws-api\n\n        WebSocketContainer container = ContainerProvider.getWebSocketContainer();\n        URI uri = new URI(\"wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\"); // Replace with your websocket endpoint URL\n\n        WebSocketJavaExample client = new WebSocketJavaExample();\n\n        container.connectToServer(client, uri);\n\n        // Send messages to the server using the sendMessage() method\n        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details\n        client.sendMessage(\"{\\\"cmd_id\\\": 22002, \\\"seq_id\\\": 123,\\\"trace\\\":\\\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\\\",\\\"data\\\":{\\\"symbol_list\\\":[{\\\"code\\\": \\\"700.HK\\\",\\\"depth_level\\\": 5},{\\\"code\\\": \\\"UNH.US\\\",\\\"depth_level\\\": 5}]}}\");\n\n        // Wait for the client to be disconnected from the server (or until the user presses Enter)\n        System.in.read(); // Wait for user input before closing the program\n    }\n}\n```\n\n```http\n复制<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>\n```\n\n```http\n<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>\n```\n\n```http\n<?php\nrequire_once __DIR__ . '/vendor/autoload.php';\n\nuse Workerman\\Protocols\\Ws;\nuse Workerman\\Worker;\nuse Workerman\\Connection\\AsyncTcpConnection;\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// wss://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// wss://quote.alltick.co/quote-stock-b-ws-api\n\n$worker = new Worker();\n// When the process starts\n$worker->onWorkerStart = function()\n{\n    // Connect to remote websocket server using the websocket protocol\n    $ws_connection = new AsyncTcpConnection(\"ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken\", [\n        'ssl' => [\n            'verify_peer' => false,\n            'verify_peer_name' => false,\n        ]\n    ]);\n    $ws_connection->transport = 'ssl';\n    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds\n    $ws_connection->websocketPingInterval = 10;\n    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary\n    // After the TCP handshake is completed\n    $ws_connection->onConnect = function($connection){\n        echo \"TCP connected\\n\";\n        // Send subscription request\n        $connection->send('{\"cmd_id\":22002,\"seq_id\":123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\":\"700.HK\",\"depth_level\":5},{\"code\":\"AAPL.US\",\"depth_level\":5}]}}');\n    };\n    // After the websocket handshake is completed\n    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {\n        echo $response;\n    };\n    // When a message is received from the remote websocket server\n    $ws_connection->onMessage = function($connection, $data){\n        echo \"Received: $data\\n\";\n    };\n    // When an error occurs, usually due to failure to connect to the remote websocket server\n    $ws_connection->onError = function($connection, $code, $msg){\n        echo \"Error: $msg\\n\";\n    };\n    // When the connection to the remote websocket server is closed\n    $ws_connection->onClose = function($connection){\n        echo \"Connection closed and trying to reconnect\\n\";\n        // If the connection is closed, reconnect after 1 second\n        $connection->reConnect(1);\n    };\n    // After setting up all the callbacks above, initiate the connection\n    $ws_connection->connect();\n};\nWorker::runAll();\n?>\n```\n\n```http\n复制import json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()\n```\n\n```http\nimport json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()\n```\n\n```http\nimport json\nimport websocket    # pip install websocket-client\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# wss://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# wss://quote.alltick.co/quote-stock-b-ws-api\n'''\n\nclass Feed(object):\n\n    def __init__(self):\n        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here\n        self.ws = None\n\n    def on_open(self, ws):\n        \"\"\"\n        Callback object which is called at opening websocket.\n        1 argument:\n        @ ws: the WebSocketApp object\n        \"\"\"\n        print('A new WebSocketApp is opened!')\n\n        # Start subscribing (an example)\n        sub_param = {\n            \"cmd_id\": 22002,\n            \"seq_id\": 123,\n            \"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\n            \"data\":{\n                \"symbol_list\":[\n                    {\n                        \"code\": \"700.HK\",\n                        \"depth_level\": 5,\n                    },\n                    {\n                        \"code\": \"UNH.US\",\n                        \"depth_level\": 5,\n                    }\n                ]\n            }\n        }\n\n        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details\n        sub_str = json.dumps(sub_param)\n        ws.send(sub_str)\n        print(\"depth quote are subscribed!\")\n\n    def on_data(self, ws, string, type, continue_flag):\n        \"\"\"\n        4 arguments.\n        The 1st argument is this class object.\n        The 2nd argument is utf-8 string which we get from the server.\n        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.\n        The 4th argument is continue flag. If 0, the data continue\n        \"\"\"\n\n    def on_message(self, ws, message):\n        \"\"\"\n        Callback object which is called when received data.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ message: utf-8 data received from the server\n        \"\"\"\n        # Parse the received message\n        result = eval(message)\n        print(result)\n\n    def on_error(self, ws, error):\n        \"\"\"\n        Callback object which is called when got an error.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ error: exception object\n        \"\"\"\n        print(error)\n\n    def on_close(self, ws, close_status_code, close_msg):\n        \"\"\"\n        Callback object which is called when the connection is closed.\n        2 arguments:\n        @ ws: the WebSocketApp object\n        @ close_status_code\n        @ close_msg\n        \"\"\"\n        print('The connection is closed!')\n\n    def start(self):\n        self.ws = websocket.WebSocketApp(\n            self.url,\n            on_open=self.on_open,\n            on_message=self.on_message,\n            on_data=self.on_data,\n            on_error=self.on_error,\n            on_close=self.on_close,\n        )\n        self.ws.run_forever()\n\n\nif __name__ == \"__main__\":\n    feed = Feed()\n    feed.start()\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于2个月前\n"
  rawContent: "复制\nWEBSOCKET API\nWebsocket 请求示例\n\nEnglish / 中文\n\nWebsocket 行情 API 地址说明\nGo\nJava\nPHP\nPyton\n复制\npackage main\n\n\n\nimport (\n\n\t\"encoding/json\"\n\n\t\"github.com/google/uuid\"\n\n\t\"github.com/gorilla/websocket\"\n\n\t\"log\"\n\n\t\"time\"\n\n)\n\n\n\ntype Symbol struct {\n\n\tCode       string `json:\"code\"`\n\n\tDepthLevel int    `json:\"depth_level\"`\n\n}\n\n\n\ntype Data struct {\n\n\tSymbolList []Symbol `json:\"symbol_list\"`\n\n}\n\n\n\ntype Request struct {\n\n\tCmdID  int    `json:\"cmd_id\"`\n\n\tSeqID  int    `json:\"seq_id\"`\n\n\tTrace  string `json:\"trace\"`\n\n\tData   Data   `json:\"data\"`\n\n}\n\n\n\n/*\n\n\tSpecial Note:\n\n\tGitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\n\tToken Application: https://alltick.co\n\n\tReplace \"testtoken\" in the URL below with your own token\n\n\tAPI addresses for forex, cryptocurrencies, and precious metals:\n\n\twss://quote.alltick.co/quote-b-ws-api\n\n\tStock API address:\n\n\twss://quote.alltick.co/quote-stock-b-ws-api\n\n*/\n\nconst (\n\n\turl = \"wss://quote.alltick.co/quote-b-ws-api?token=testtoken\"\n\n)\n\n\n\nfunc websocket_example() {\n\n\n\n\tlog.Println(\"Connecting to server at\", url)\n\n\n\n\tc, _, err := websocket.DefaultDialer.Dial(url, nil)\n\n\tif err != nil {\n\n\t\tlog.Fatal(\"dial:\", err)\n\n\t}\n\n\tdefer c.Close()\n\n\n\n\t// Send heartbeat every 10 seconds\n\n\tgo func() {\n\n\t\tfor range time.NewTicker(10 * time.Second).C {\n\n\t\t\treq := Request{\n\n\t\t\t\tCmdID: 22000,\n\n\t\t\t\tSeqID: 123,\n\n\t\t\t\tTrace: \"3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462\",\n\n\t\t\t\tData:  Data{},\n\n\t\t\t}\n\n\t\t\tmessageBytes, err := json.Marshal(req)\n\n\t\t\tif err != nil {\n\n\t\t\t\tlog.Println(\"json.Marshal error:\", err)\n\n\t\t\t\treturn\n\n\t\t\t}\n\n\t\t\tlog.Println(\"req data:\", string(messageBytes))\n\n\n\n\t\t\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\n\t\t\tif err != nil {\n\n\t\t\t\tlog.Println(\"write:\", err)\n\n\t\t\t}\n\n\t\t}\n\n\t}()\n\n\n\n\treq := Request{\n\n\t\tCmdID: 22002,\n\n\t\tSeqID: 123,\n\n\t\tTrace: uuid.New().String(),\n\n\t\tData: Data{SymbolList: []Symbol{\n\n\t\t\t{\"GOLD\", 5},\n\n\t\t\t{\"AAPL.US\", 5},\n\n\t\t\t{\"700.HK\", 5},\n\n\t\t\t{\"USDJPY\", 5},\n\n\t\t}},\n\n\t}\n\n\tmessageBytes, err := json.Marshal(req)\n\n\tif err != nil {\n\n\t\tlog.Println(\"json.Marshal error:\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\n\tif err != nil {\n\n\t\tlog.Println(\"write:\", err)\n\n\t}\n\n\n\n\treq.CmdID = 22004\n\n\tmessageBytes, err = json.Marshal(req)\n\n\tif err != nil {\n\n\t\tlog.Println(\"json.Marshal error:\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"req data:\", string(messageBytes))\n\n\n\n\terr = c.WriteMessage(websocket.TextMessage, messageBytes)\n\n\tif err != nil {\n\n\t\tlog.Println(\"write:\", err)\n\n\t}\n\n\n\n\trece_count := 0\n\n\tfor {\n\n\t\t_, message, err := c.ReadMessage()\n\n\n\n\t\tif err != nil {\n\n\t\t\tlog.Println(\"read:\", err)\n\n\t\t\tbreak\n\n\t\t} else {\n\n\t\t\tlog.Println(\"Received message:\", string(message))\n\n\t\t}\n\n\n\n\t\trece_count++\n\n\t\tif rece_count%10000 == 0 {\n\n\t\t\tlog.Println(\"count:\", rece_count, \" Received message:\", string(message))\n\n\t\t}\n\n\t}\n\n\n\n}\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n涨跌幅、休市、假期、涨停跌停、新股上市和退市\n下一页\nWebsocket接口API\n\n最后更新于2个月前"
  suggestedFilename: "websocket-api"
---

# Websocket 请求示例

## 源URL

https://apis.alltick.co/websocket-api

## 文档正文

1. Websocket API

English / 中文

```http
复制package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"log"
	"time"
)

type Symbol struct {
	Code       string `json:"code"`
	DepthLevel int    `json:"depth_level"`
}

type Data struct {
	SymbolList []Symbol `json:"symbol_list"`
}

type Request struct {
	CmdID  int    `json:"cmd_id"`
	SeqID  int    `json:"seq_id"`
	Trace  string `json:"trace"`
	Data   Data   `json:"data"`
}

/*
	Special Note:
	GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
	Token Application: https://alltick.co
	Replace "testtoken" in the URL below with your own token
	API addresses for forex, cryptocurrencies, and precious metals:
	wss://quote.alltick.co/quote-b-ws-api
	Stock API address:
	wss://quote.alltick.co/quote-stock-b-ws-api
*/
const (
	url = "wss://quote.alltick.co/quote-b-ws-api?token=testtoken"
)

func websocket_example() {

	log.Println("Connecting to server at", url)

	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	// Send heartbeat every 10 seconds
	go func() {
		for range time.NewTicker(10 * time.Second).C {
			req := Request{
				CmdID: 22000,
				SeqID: 123,
				Trace: "3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462",
				Data:  Data{},
			}
			messageBytes, err := json.Marshal(req)
			if err != nil {
				log.Println("json.Marshal error:", err)
				return
			}
			log.Println("req data:", string(messageBytes))

			err = c.WriteMessage(websocket.TextMessage, messageBytes)
			if err != nil {
				log.Println("write:", err)
			}
		}
	}()

	req := Request{
		CmdID: 22002,
		SeqID: 123,
		Trace: uuid.New().String(),
		Data: Data{SymbolList: []Symbol{
			{"GOLD", 5},
			{"AAPL.US", 5},
			{"700.HK", 5},
			{"USDJPY", 5},
		}},
	}
	messageBytes, err := json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	req.CmdID = 22004
	messageBytes, err = json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	rece_count := 0
	for {
		_, message, err := c.ReadMessage()

		if err != nil {
			log.Println("read:", err)
			break
		} else {
			log.Println("Received message:", string(message))
		}

		rece_count++
		if rece_count%10000 == 0 {
			log.Println("count:", rece_count, " Received message:", string(message))
		}
	}

}
```

```http
package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"log"
	"time"
)

type Symbol struct {
	Code       string `json:"code"`
	DepthLevel int    `json:"depth_level"`
}

type Data struct {
	SymbolList []Symbol `json:"symbol_list"`
}

type Request struct {
	CmdID  int    `json:"cmd_id"`
	SeqID  int    `json:"seq_id"`
	Trace  string `json:"trace"`
	Data   Data   `json:"data"`
}

/*
	Special Note:
	GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
	Token Application: https://alltick.co
	Replace "testtoken" in the URL below with your own token
	API addresses for forex, cryptocurrencies, and precious metals:
	wss://quote.alltick.co/quote-b-ws-api
	Stock API address:
	wss://quote.alltick.co/quote-stock-b-ws-api
*/
const (
	url = "wss://quote.alltick.co/quote-b-ws-api?token=testtoken"
)

func websocket_example() {

	log.Println("Connecting to server at", url)

	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	// Send heartbeat every 10 seconds
	go func() {
		for range time.NewTicker(10 * time.Second).C {
			req := Request{
				CmdID: 22000,
				SeqID: 123,
				Trace: "3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462",
				Data:  Data{},
			}
			messageBytes, err := json.Marshal(req)
			if err != nil {
				log.Println("json.Marshal error:", err)
				return
			}
			log.Println("req data:", string(messageBytes))

			err = c.WriteMessage(websocket.TextMessage, messageBytes)
			if err != nil {
				log.Println("write:", err)
			}
		}
	}()

	req := Request{
		CmdID: 22002,
		SeqID: 123,
		Trace: uuid.New().String(),
		Data: Data{SymbolList: []Symbol{
			{"GOLD", 5},
			{"AAPL.US", 5},
			{"700.HK", 5},
			{"USDJPY", 5},
		}},
	}
	messageBytes, err := json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	req.CmdID = 22004
	messageBytes, err = json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	rece_count := 0
	for {
		_, message, err := c.ReadMessage()

		if err != nil {
			log.Println("read:", err)
			break
		} else {
			log.Println("Received message:", string(message))
		}

		rece_count++
		if rece_count%10000 == 0 {
			log.Println("count:", rece_count, " Received message:", string(message))
		}
	}

}
```

```http
package main

import (
	"encoding/json"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"log"
	"time"
)

type Symbol struct {
	Code       string `json:"code"`
	DepthLevel int    `json:"depth_level"`
}

type Data struct {
	SymbolList []Symbol `json:"symbol_list"`
}

type Request struct {
	CmdID  int    `json:"cmd_id"`
	SeqID  int    `json:"seq_id"`
	Trace  string `json:"trace"`
	Data   Data   `json:"data"`
}

/*
	Special Note:
	GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
	Token Application: https://alltick.co
	Replace "testtoken" in the URL below with your own token
	API addresses for forex, cryptocurrencies, and precious metals:
	wss://quote.alltick.co/quote-b-ws-api
	Stock API address:
	wss://quote.alltick.co/quote-stock-b-ws-api
*/
const (
	url = "wss://quote.alltick.co/quote-b-ws-api?token=testtoken"
)

func websocket_example() {

	log.Println("Connecting to server at", url)

	c, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	// Send heartbeat every 10 seconds
	go func() {
		for range time.NewTicker(10 * time.Second).C {
			req := Request{
				CmdID: 22000,
				SeqID: 123,
				Trace: "3380a7a-3e1f-c3a5-5ee3-9e5be0ec8c241692805462",
				Data:  Data{},
			}
			messageBytes, err := json.Marshal(req)
			if err != nil {
				log.Println("json.Marshal error:", err)
				return
			}
			log.Println("req data:", string(messageBytes))

			err = c.WriteMessage(websocket.TextMessage, messageBytes)
			if err != nil {
				log.Println("write:", err)
			}
		}
	}()

	req := Request{
		CmdID: 22002,
		SeqID: 123,
		Trace: uuid.New().String(),
		Data: Data{SymbolList: []Symbol{
			{"GOLD", 5},
			{"AAPL.US", 5},
			{"700.HK", 5},
			{"USDJPY", 5},
		}},
	}
	messageBytes, err := json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	req.CmdID = 22004
	messageBytes, err = json.Marshal(req)
	if err != nil {
		log.Println("json.Marshal error:", err)
		return
	}
	log.Println("req data:", string(messageBytes))

	err = c.WriteMessage(websocket.TextMessage, messageBytes)
	if err != nil {
		log.Println("write:", err)
	}

	rece_count := 0
	for {
		_, message, err := c.ReadMessage()

		if err != nil {
			log.Println("read:", err)
			break
		} else {
			log.Println("Received message:", string(message))
		}

		rece_count++
		if rece_count%10000 == 0 {
			log.Println("count:", rece_count, " Received message:", string(message))
		}
	}

}
```

```http
复制import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import javax.websocket.*;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

@ClientEndpoint
public class WebSocketJavaExample {

    private Session session;

    @OnOpen
    public void onOpen(Session session) {
        System.out.println("Connected to server");
        this.session = session;
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
    }

    @OnClose
    public void onClose(Session session, CloseReason closeReason) {
        System.out.println("Disconnected from server");
    }

    @OnError
    public void onError(Throwable throwable) {
        System.err.println("Error: " + throwable.getMessage());
    }

    public void sendMessage(String message) throws Exception {
        this.session.getBasicRemote().sendText(message);
    }

    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Special Note:
        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
        // Token Application: https://alltick.co
        // Replace "testtoken" in the URL below with your own token
        // API addresses for forex, cryptocurrencies, and precious metals:
        // wss://quote.alltick.co/quote-b-ws-api
        // Stock API address:
        // wss://quote.alltick.co/quote-stock-b-ws-api

        WebSocketContainer container = ContainerProvider.getWebSocketContainer();
        URI uri = new URI("wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken"); // Replace with your websocket endpoint URL

        WebSocketJavaExample client = new WebSocketJavaExample();

        container.connectToServer(client, uri);

        // Send messages to the server using the sendMessage() method
        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details
        client.sendMessage("{\"cmd_id\": 22002, \"seq_id\": 123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\": \"700.HK\",\"depth_level\": 5},{\"code\": \"UNH.US\",\"depth_level\": 5}]}}");

        // Wait for the client to be disconnected from the server (or until the user presses Enter)
        System.in.read(); // Wait for user input before closing the program
    }
}
```

```http
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import javax.websocket.*;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

@ClientEndpoint
public class WebSocketJavaExample {

    private Session session;

    @OnOpen
    public void onOpen(Session session) {
        System.out.println("Connected to server");
        this.session = session;
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
    }

    @OnClose
    public void onClose(Session session, CloseReason closeReason) {
        System.out.println("Disconnected from server");
    }

    @OnError
    public void onError(Throwable throwable) {
        System.err.println("Error: " + throwable.getMessage());
    }

    public void sendMessage(String message) throws Exception {
        this.session.getBasicRemote().sendText(message);
    }

    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Special Note:
        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
        // Token Application: https://alltick.co
        // Replace "testtoken" in the URL below with your own token
        // API addresses for forex, cryptocurrencies, and precious metals:
        // wss://quote.alltick.co/quote-b-ws-api
        // Stock API address:
        // wss://quote.alltick.co/quote-stock-b-ws-api

        WebSocketContainer container = ContainerProvider.getWebSocketContainer();
        URI uri = new URI("wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken"); // Replace with your websocket endpoint URL

        WebSocketJavaExample client = new WebSocketJavaExample();

        container.connectToServer(client, uri);

        // Send messages to the server using the sendMessage() method
        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details
        client.sendMessage("{\"cmd_id\": 22002, \"seq_id\": 123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\": \"700.HK\",\"depth_level\": 5},{\"code\": \"UNH.US\",\"depth_level\": 5}]}}");

        // Wait for the client to be disconnected from the server (or until the user presses Enter)
        System.in.read(); // Wait for user input before closing the program
    }
}
```

```http
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import javax.websocket.*;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

@ClientEndpoint
public class WebSocketJavaExample {

    private Session session;

    @OnOpen
    public void onOpen(Session session) {
        System.out.println("Connected to server");
        this.session = session;
    }

    @OnMessage
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
    }

    @OnClose
    public void onClose(Session session, CloseReason closeReason) {
        System.out.println("Disconnected from server");
    }

    @OnError
    public void onError(Throwable throwable) {
        System.err.println("Error: " + throwable.getMessage());
    }

    public void sendMessage(String message) throws Exception {
        this.session.getBasicRemote().sendText(message);
    }

    public static void main(String[] args) throws Exception, URISyntaxException, DeploymentException, IOException, IllegalArgumentException, SecurityException, NoSuchMethodException, IllegalAccessException, InvocationTargetException, InstantiationException {
        // Special Note:
        // GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
        // Token Application: https://alltick.co
        // Replace "testtoken" in the URL below with your own token
        // API addresses for forex, cryptocurrencies, and precious metals:
        // wss://quote.alltick.co/quote-b-ws-api
        // Stock API address:
        // wss://quote.alltick.co/quote-stock-b-ws-api

        WebSocketContainer container = ContainerProvider.getWebSocketContainer();
        URI uri = new URI("wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken"); // Replace with your websocket endpoint URL

        WebSocketJavaExample client = new WebSocketJavaExample();

        container.connectToServer(client, uri);

        // Send messages to the server using the sendMessage() method
        // If you want to run for a long time, in addition to sending subscriptions, you also need to modify the code to send heartbeats regularly to prevent disconnection. Refer to the interface documentation for details
        client.sendMessage("{\"cmd_id\": 22002, \"seq_id\": 123,\"trace\":\"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806\",\"data\":{\"symbol_list\":[{\"code\": \"700.HK\",\"depth_level\": 5},{\"code\": \"UNH.US\",\"depth_level\": 5}]}}");

        // Wait for the client to be disconnected from the server (or until the user presses Enter)
        System.in.read(); // Wait for user input before closing the program
    }
}
```

```http
复制<?php
require_once __DIR__ . '/vendor/autoload.php';

use Workerman\Protocols\Ws;
use Workerman\Worker;
use Workerman\Connection\AsyncTcpConnection;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

$worker = new Worker();
// When the process starts
$worker->onWorkerStart = function()
{
    // Connect to remote websocket server using the websocket protocol
    $ws_connection = new AsyncTcpConnection("ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken", [
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
        ]
    ]);
    $ws_connection->transport = 'ssl';
    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds
    $ws_connection->websocketPingInterval = 10;
    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary
    // After the TCP handshake is completed
    $ws_connection->onConnect = function($connection){
        echo "TCP connected\n";
        // Send subscription request
        $connection->send('{"cmd_id":22002,"seq_id":123,"trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806","data":{"symbol_list":[{"code":"700.HK","depth_level":5},{"code":"AAPL.US","depth_level":5}]}}');
    };
    // After the websocket handshake is completed
    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {
        echo $response;
    };
    // When a message is received from the remote websocket server
    $ws_connection->onMessage = function($connection, $data){
        echo "Received: $data\n";
    };
    // When an error occurs, usually due to failure to connect to the remote websocket server
    $ws_connection->onError = function($connection, $code, $msg){
        echo "Error: $msg\n";
    };
    // When the connection to the remote websocket server is closed
    $ws_connection->onClose = function($connection){
        echo "Connection closed and trying to reconnect\n";
        // If the connection is closed, reconnect after 1 second
        $connection->reConnect(1);
    };
    // After setting up all the callbacks above, initiate the connection
    $ws_connection->connect();
};
Worker::runAll();
?>
```

```http
<?php
require_once __DIR__ . '/vendor/autoload.php';

use Workerman\Protocols\Ws;
use Workerman\Worker;
use Workerman\Connection\AsyncTcpConnection;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

$worker = new Worker();
// When the process starts
$worker->onWorkerStart = function()
{
    // Connect to remote websocket server using the websocket protocol
    $ws_connection = new AsyncTcpConnection("ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken", [
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
        ]
    ]);
    $ws_connection->transport = 'ssl';
    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds
    $ws_connection->websocketPingInterval = 10;
    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary
    // After the TCP handshake is completed
    $ws_connection->onConnect = function($connection){
        echo "TCP connected\n";
        // Send subscription request
        $connection->send('{"cmd_id":22002,"seq_id":123,"trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806","data":{"symbol_list":[{"code":"700.HK","depth_level":5},{"code":"AAPL.US","depth_level":5}]}}');
    };
    // After the websocket handshake is completed
    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {
        echo $response;
    };
    // When a message is received from the remote websocket server
    $ws_connection->onMessage = function($connection, $data){
        echo "Received: $data\n";
    };
    // When an error occurs, usually due to failure to connect to the remote websocket server
    $ws_connection->onError = function($connection, $code, $msg){
        echo "Error: $msg\n";
    };
    // When the connection to the remote websocket server is closed
    $ws_connection->onClose = function($connection){
        echo "Connection closed and trying to reconnect\n";
        // If the connection is closed, reconnect after 1 second
        $connection->reConnect(1);
    };
    // After setting up all the callbacks above, initiate the connection
    $ws_connection->connect();
};
Worker::runAll();
?>
```

```http
<?php
require_once __DIR__ . '/vendor/autoload.php';

use Workerman\Protocols\Ws;
use Workerman\Worker;
use Workerman\Connection\AsyncTcpConnection;

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// wss://quote.alltick.co/quote-b-ws-api
// Stock API address:
// wss://quote.alltick.co/quote-stock-b-ws-api

$worker = new Worker();
// When the process starts
$worker->onWorkerStart = function()
{
    // Connect to remote websocket server using the websocket protocol
    $ws_connection = new AsyncTcpConnection("ws://quote.alltick.co/quote-stock-b-ws-api?token=testtoken", [
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
        ]
    ]);
    $ws_connection->transport = 'ssl';
    // Send a websocket heartbeat opcode (0x9) to the server every 55 seconds
    $ws_connection->websocketPingInterval = 10;
    $ws_connection->websocketType = Ws::BINARY_TYPE_BLOB; // BINARY_TYPE_BLOB for text, BINARY_TYPE_ARRAYBUFFER for binary
    // After the TCP handshake is completed
    $ws_connection->onConnect = function($connection){
        echo "TCP connected\n";
        // Send subscription request
        $connection->send('{"cmd_id":22002,"seq_id":123,"trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806","data":{"symbol_list":[{"code":"700.HK","depth_level":5},{"code":"AAPL.US","depth_level":5}]}}');
    };
    // After the websocket handshake is completed
    $ws_connection->onWebSocketConnect = function(AsyncTcpConnection $con, $response) {
        echo $response;
    };
    // When a message is received from the remote websocket server
    $ws_connection->onMessage = function($connection, $data){
        echo "Received: $data\n";
    };
    // When an error occurs, usually due to failure to connect to the remote websocket server
    $ws_connection->onError = function($connection, $code, $msg){
        echo "Error: $msg\n";
    };
    // When the connection to the remote websocket server is closed
    $ws_connection->onClose = function($connection){
        echo "Connection closed and trying to reconnect\n";
        // If the connection is closed, reconnect after 1 second
        $connection->reConnect(1);
    };
    // After setting up all the callbacks above, initiate the connection
    $ws_connection->connect();
};
Worker::runAll();
?>
```

```http
复制import json
import websocket    # pip install websocket-client

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# wss://quote.alltick.co/quote-b-ws-api
# Stock API address:
# wss://quote.alltick.co/quote-stock-b-ws-api
'''

class Feed(object):

    def __init__(self):
        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here
        self.ws = None

    def on_open(self, ws):
        """
        Callback object which is called at opening websocket.
        1 argument:
        @ ws: the WebSocketApp object
        """
        print('A new WebSocketApp is opened!')

        # Start subscribing (an example)
        sub_param = {
            "cmd_id": 22002,
            "seq_id": 123,
            "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
            "data":{
                "symbol_list":[
                    {
                        "code": "700.HK",
                        "depth_level": 5,
                    },
                    {
                        "code": "UNH.US",
                        "depth_level": 5,
                    }
                ]
            }
        }

        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details
        sub_str = json.dumps(sub_param)
        ws.send(sub_str)
        print("depth quote are subscribed!")

    def on_data(self, ws, string, type, continue_flag):
        """
        4 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 string which we get from the server.
        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.
        The 4th argument is continue flag. If 0, the data continue
        """

    def on_message(self, ws, message):
        """
        Callback object which is called when received data.
        2 arguments:
        @ ws: the WebSocketApp object
        @ message: utf-8 data received from the server
        """
        # Parse the received message
        result = eval(message)
        print(result)

    def on_error(self, ws, error):
        """
        Callback object which is called when got an error.
        2 arguments:
        @ ws: the WebSocketApp object
        @ error: exception object
        """
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback object which is called when the connection is closed.
        2 arguments:
        @ ws: the WebSocketApp object
        @ close_status_code
        @ close_msg
        """
        print('The connection is closed!')

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

if __name__ == "__main__":
    feed = Feed()
    feed.start()
```

```http
import json
import websocket    # pip install websocket-client

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# wss://quote.alltick.co/quote-b-ws-api
# Stock API address:
# wss://quote.alltick.co/quote-stock-b-ws-api
'''

class Feed(object):

    def __init__(self):
        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here
        self.ws = None

    def on_open(self, ws):
        """
        Callback object which is called at opening websocket.
        1 argument:
        @ ws: the WebSocketApp object
        """
        print('A new WebSocketApp is opened!')

        # Start subscribing (an example)
        sub_param = {
            "cmd_id": 22002,
            "seq_id": 123,
            "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
            "data":{
                "symbol_list":[
                    {
                        "code": "700.HK",
                        "depth_level": 5,
                    },
                    {
                        "code": "UNH.US",
                        "depth_level": 5,
                    }
                ]
            }
        }

        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details
        sub_str = json.dumps(sub_param)
        ws.send(sub_str)
        print("depth quote are subscribed!")

    def on_data(self, ws, string, type, continue_flag):
        """
        4 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 string which we get from the server.
        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.
        The 4th argument is continue flag. If 0, the data continue
        """

    def on_message(self, ws, message):
        """
        Callback object which is called when received data.
        2 arguments:
        @ ws: the WebSocketApp object
        @ message: utf-8 data received from the server
        """
        # Parse the received message
        result = eval(message)
        print(result)

    def on_error(self, ws, error):
        """
        Callback object which is called when got an error.
        2 arguments:
        @ ws: the WebSocketApp object
        @ error: exception object
        """
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback object which is called when the connection is closed.
        2 arguments:
        @ ws: the WebSocketApp object
        @ close_status_code
        @ close_msg
        """
        print('The connection is closed!')

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

if __name__ == "__main__":
    feed = Feed()
    feed.start()
```

```http
import json
import websocket    # pip install websocket-client

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# wss://quote.alltick.co/quote-b-ws-api
# Stock API address:
# wss://quote.alltick.co/quote-stock-b-ws-api
'''

class Feed(object):

    def __init__(self):
        self.url = 'wss://quote.alltick.co/quote-stock-b-ws-api?token=testtoken'  # Enter your websocket URL here
        self.ws = None

    def on_open(self, ws):
        """
        Callback object which is called at opening websocket.
        1 argument:
        @ ws: the WebSocketApp object
        """
        print('A new WebSocketApp is opened!')

        # Start subscribing (an example)
        sub_param = {
            "cmd_id": 22002,
            "seq_id": 123,
            "trace":"3baaa938-f92c-4a74-a228-fd49d5e2f8bc-1678419657806",
            "data":{
                "symbol_list":[
                    {
                        "code": "700.HK",
                        "depth_level": 5,
                    },
                    {
                        "code": "UNH.US",
                        "depth_level": 5,
                    }
                ]
            }
        }

        # If you want to run for a long time, you need to modify the code to send heartbeats periodically to avoid disconnection, please refer to the API documentation for details
        sub_str = json.dumps(sub_param)
        ws.send(sub_str)
        print("depth quote are subscribed!")

    def on_data(self, ws, string, type, continue_flag):
        """
        4 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 string which we get from the server.
        The 3rd argument is data type. ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY will be came.
        The 4th argument is continue flag. If 0, the data continue
        """

    def on_message(self, ws, message):
        """
        Callback object which is called when received data.
        2 arguments:
        @ ws: the WebSocketApp object
        @ message: utf-8 data received from the server
        """
        # Parse the received message
        result = eval(message)
        print(result)

    def on_error(self, ws, error):
        """
        Callback object which is called when got an error.
        2 arguments:
        @ ws: the WebSocketApp object
        @ error: exception object
        """
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback object which is called when the connection is closed.
        2 arguments:
        @ ws: the WebSocketApp object
        @ close_status_code
        @ close_msg
        """
        print('The connection is closed!')

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.run_forever()

if __name__ == "__main__":
    feed = Feed()
    feed.start()
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于2个月前
