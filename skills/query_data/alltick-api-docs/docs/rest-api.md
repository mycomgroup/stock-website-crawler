---
id: "url-5f37e1ae"
type: "api"
title: "HTTP 请求示例"
url: "https://apis.alltick.co/rest-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T04:56:40.813Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["REST API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"code","language":"http","value":"复制package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"复制import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"复制<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"复制import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
    - {"type":"code","language":"http","value":"import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
    - {"type":"code","language":"http","value":"import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于5个月前"}]}
  codeExamples:
    - {"type":"code","language":"http","value":"复制package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}"}
    - {"type":"code","language":"http","value":"复制import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}"}
    - {"type":"code","language":"http","value":"复制<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>"}
    - {"type":"code","language":"http","value":"复制import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
    - {"type":"code","language":"http","value":"import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
    - {"type":"code","language":"http","value":"import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)"}
  tables: []
  parameters: []
  markdownContent: "# HTTP 请求示例\n\n1. REST API\n\nEnglish / 中文\n\n```http\n复制package main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}\n```\n\n```http\npackage main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}\n```\n\n```http\npackage main\n\nimport (\n\t\"fmt\"\n\t\"io/ioutil\"\n\t\"log\"\n\t\"net/http\"\n)\n\nfunc http_example() {\n\n\t/*\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\t\t特别注意：\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\t\ttoken申请：https://alltick.co\n\t\t把下面url中的testtoken替换为您自己的token\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\t\thttps://quote.alltick.co/quote-b-api\n\t\t股票api地址:\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\t*/\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\tlog.Println(\"请求内容：\", url)\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\tif err != nil {\n\t\tfmt.Println(\"Error creating request:\", err)\n\t\treturn\n\t}\n\n\tq := req.URL.Query()\n\ttoken := \"testtoken\"\n\tq.Add(\"token\", token)\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\tq.Add(\"query\", queryStr)\n\treq.URL.RawQuery = q.Encode()\n\t// 发送请求\n\tresp, err := http.DefaultClient.Do(req)\n\tif err != nil {\n\t\tfmt.Println(\"Error sending request:\", err)\n\t\treturn\n\t}\n\tdefer resp.Body.Close()\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\tif err != nil {\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\t\treturn\n\n\t}\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n}\n```\n\n```http\n复制import java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}\n```\n\n```http\nimport java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}\n```\n\n```http\nimport java.io.BufferedReader;\nimport java.io.InputStreamReader;\nimport java.net.HttpURLConnection;\nimport java.net.URL;\n\npublic class HttpJavaExample {\n\n    public static void main(String[] args) {\n\n        try {\n\n            /*\n            Encode the following JSON into URL format and copy it to the query field of the HTTP request\n            {\"trace\" : \"java_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n            Special Note:\n            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n            Token Application: https://alltick.co\n            Replace \"testtoken\" in the URL below with your own token\n            API addresses for forex, cryptocurrencies, and precious metals:\n            https://quote.alltick.co/quote-b-api\n            Stock API address:\n            https://quote.alltick.co/quote-stock-b-api\n            */\n            String url = \"http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D\";\n\n            URL obj = new URL(url);\n\n            HttpURLConnection con = (HttpURLConnection) obj.openConnection();\n\n            con.setRequestMethod(\"GET\");\n\n            int responseCode = con.getResponseCode();\n\n            System.out.println(\"Response Code: \" + responseCode);\n\n            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));\n\n            String inputLine;\n\n            StringBuffer response = new StringBuffer();\n\n            while ((inputLine = in.readLine()) != null) {\n                response.append(inputLine);\n            }\n\n            in.close();\n\n            System.out.println(response.toString());\n\n        } catch (Exception e) {\n            e.printStackTrace();\n        }\n    }\n}\n```\n\n```http\n复制<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>\n```\n\n```http\n<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>\n```\n\n```http\n<?php\n\n// Special Note:\n// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n// Token Application: https://alltick.co\n// Replace \"testtoken\" in the URL below with your own token\n// API addresses for forex, cryptocurrencies, and precious metals:\n// https://quote.alltick.co/quote-b-ws-api\n// Stock API address:\n// https://quote.alltick.co/quote-stock-b-ws-api\n\n$params = '{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}';\n\n$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';\n$method = 'GET';\n\n$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);\n\n/* Set specific parameters based on request type */\nswitch (strtoupper($method)) {\n    case 'GET':\n        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);\n        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';\n        break;\n    default:\n}\n\n/* Initialize and execute curl request */\n$ch = curl_init();\ncurl_setopt_array($ch, $opts);\n$data = curl_exec($ch);\n$error = curl_error($ch);\ncurl_close($ch);\n\nif ($error) {\n    $data = null;\n}\n\necho $data;\n?>\n```\n\n```http\n复制import time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)\n```\n\n```http\nimport time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)\n```\n\n```http\nimport time\nimport requests\nimport json\n\n# Extra headers\ntest_headers = {\n    'Content-Type': 'application/json'\n}\n\n'''\n# Special Note:\n# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n# Token Application: https://alltick.co\n# Replace \"testtoken\" in the URL below with your own token\n# API addresses for forex, cryptocurrencies, and precious metals:\n# https://quote.alltick.co/quote-b-ws-api\n# Stock API address:\n# https://quote.alltick.co/quote-stock-b-ws-api\nEncode the following JSON and copy it to the \"query\" field of the HTTP query string\n{\"trace\": \"python_http_test1\", \"data\": {\"code\": \"700.HK\", \"kline_type\": 1, \"kline_timestamp_end\": 0, \"query_kline_num\": 2, \"adjust_type\": 0}}\n{\"trace\": \"python_http_test2\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n{\"trace\": \"python_http_test3\", \"data\": {\"symbol_list\": [{\"code\": \"700.HK\"}, {\"code\": \"UNH.US\"}]}}\n'''\ntest_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'\ntest_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\ntest_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'\n\nresp1 = requests.get(url=test_url1, headers=test_headers)\ntime.sleep(1)\nresp2 = requests.get(url=test_url2, headers=test_headers)\ntime.sleep(1)\nresp3 = requests.get(url=test_url3, headers=test_headers)\n\n# Decoded text returned by the request\ntext1 = resp1.text\nprint(text1)\n\ntext2 = resp2.text\nprint(text2)\n\ntext3 = resp3.text\nprint(text3)\n```\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于5个月前\n"
  rawContent: "复制\nREST API\nHTTP 请求示例\n\nEnglish / 中文\n\nGo\nJava\nPHP\nPyton\n复制\npackage main\n\n\n\nimport (\n\n\t\"fmt\"\n\n\t\"io/ioutil\"\n\n\t\"log\"\n\n\t\"net/http\"\n\n)\n\n\n\nfunc http_example() {\n\n\n\n\t/*\n\n\t\t将如下JSON进行url的encode，复制到http的查询字符串的query字段里\n\n\t\t{\"trace\" : \"go_http_test1\",\"data\" : {\"code\" : \"700.HK\",\"kline_type\" : 1,\"kline_timestamp_end\" : 0,\"query_kline_num\" : 2,\"adjust_type\": 0}}\n\n\n\n\t\t特别注意：\n\n\t\tgithub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api\n\n\t\ttoken申请：https://alltick.co\n\n\t\t把下面url中的testtoken替换为您自己的token\n\n\t\t外汇，加密货币（数字币），贵金属的api址：\n\n\t\thttps://quote.alltick.co/quote-b-api\n\n\t\t股票api地址:\n\n\t\thttps://quote.alltick.co/quote-stock-b-api\n\n\t*/\n\n\turl := \"https://quote.alltick.co/quote-stock-b-api/kline\"\n\n\tlog.Println(\"请求内容：\", url)\n\n\n\n\treq, err := http.NewRequest(\"GET\", url, nil)\n\n\tif err != nil {\n\n\t\tfmt.Println(\"Error creating request:\", err)\n\n\t\treturn\n\n\t}\n\n\n\n\tq := req.URL.Query()\n\n\ttoken := \"testtoken\"\n\n\tq.Add(\"token\", token)\n\n\tqueryStr := `{\"trace\":\"1111111111111111111111111\",\"data\":{\"code\":\"AAPL.US\",\"kline_type\":1,\"kline_timestamp_end\":0,\"query_kline_num\":10,\"adjust_type\":0}}`\n\n\tq.Add(\"query\", queryStr)\n\n\treq.URL.RawQuery = q.Encode()\n\n\t// 发送请求\n\n\tresp, err := http.DefaultClient.Do(req)\n\n\tif err != nil {\n\n\t\tfmt.Println(\"Error sending request:\", err)\n\n\t\treturn\n\n\t}\n\n\tdefer resp.Body.Close()\n\n\n\n\tbody2, err := ioutil.ReadAll(resp.Body)\n\n\n\n\tif err != nil {\n\n\n\n\t\tlog.Println(\"读取响应失败：\", err)\n\n\n\n\t\treturn\n\n\n\n\t}\n\n\n\n\tlog.Println(\"响应内容：\", string(body2))\n\n\n\n}\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n外汇\n下一页\nHTTP接口API\n\n最后更新于5个月前"
  suggestedFilename: "rest-api"
---

# HTTP 请求示例

## 源URL

https://apis.alltick.co/rest-api

## 文档正文

1. REST API

English / 中文

```http
复制package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func http_example() {

	/*
		将如下JSON进行url的encode，复制到http的查询字符串的query字段里
		{"trace" : "go_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}

		特别注意：
		github: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
		token申请：https://alltick.co
		把下面url中的testtoken替换为您自己的token
		外汇，加密货币（数字币），贵金属的api址：
		https://quote.alltick.co/quote-b-api
		股票api地址:
		https://quote.alltick.co/quote-stock-b-api
	*/
	url := "https://quote.alltick.co/quote-stock-b-api/kline"
	log.Println("请求内容：", url)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	q := req.URL.Query()
	token := "testtoken"
	q.Add("token", token)
	queryStr := `{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}`
	q.Add("query", queryStr)
	req.URL.RawQuery = q.Encode()
	// 发送请求
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	body2, err := ioutil.ReadAll(resp.Body)

	if err != nil {

		log.Println("读取响应失败：", err)

		return

	}

	log.Println("响应内容：", string(body2))

}
```

```http
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func http_example() {

	/*
		将如下JSON进行url的encode，复制到http的查询字符串的query字段里
		{"trace" : "go_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}

		特别注意：
		github: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
		token申请：https://alltick.co
		把下面url中的testtoken替换为您自己的token
		外汇，加密货币（数字币），贵金属的api址：
		https://quote.alltick.co/quote-b-api
		股票api地址:
		https://quote.alltick.co/quote-stock-b-api
	*/
	url := "https://quote.alltick.co/quote-stock-b-api/kline"
	log.Println("请求内容：", url)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	q := req.URL.Query()
	token := "testtoken"
	q.Add("token", token)
	queryStr := `{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}`
	q.Add("query", queryStr)
	req.URL.RawQuery = q.Encode()
	// 发送请求
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	body2, err := ioutil.ReadAll(resp.Body)

	if err != nil {

		log.Println("读取响应失败：", err)

		return

	}

	log.Println("响应内容：", string(body2))

}
```

```http
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func http_example() {

	/*
		将如下JSON进行url的encode，复制到http的查询字符串的query字段里
		{"trace" : "go_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}

		特别注意：
		github: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
		token申请：https://alltick.co
		把下面url中的testtoken替换为您自己的token
		外汇，加密货币（数字币），贵金属的api址：
		https://quote.alltick.co/quote-b-api
		股票api地址:
		https://quote.alltick.co/quote-stock-b-api
	*/
	url := "https://quote.alltick.co/quote-stock-b-api/kline"
	log.Println("请求内容：", url)

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	q := req.URL.Query()
	token := "testtoken"
	q.Add("token", token)
	queryStr := `{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}`
	q.Add("query", queryStr)
	req.URL.RawQuery = q.Encode()
	// 发送请求
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	body2, err := ioutil.ReadAll(resp.Body)

	if err != nil {

		log.Println("读取响应失败：", err)

		return

	}

	log.Println("响应内容：", string(body2))

}
```

```http
复制import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpJavaExample {

    public static void main(String[] args) {

        try {

            /*
            Encode the following JSON into URL format and copy it to the query field of the HTTP request
            {"trace" : "java_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}
            Special Note:
            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
            Token Application: https://alltick.co
            Replace "testtoken" in the URL below with your own token
            API addresses for forex, cryptocurrencies, and precious metals:
            https://quote.alltick.co/quote-b-api
            Stock API address:
            https://quote.alltick.co/quote-stock-b-api
            */
            String url = "http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D";

            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            con.setRequestMethod("GET");

            int responseCode = con.getResponseCode();

            System.out.println("Response Code: " + responseCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));

            String inputLine;

            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            in.close();

            System.out.println(response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

```http
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpJavaExample {

    public static void main(String[] args) {

        try {

            /*
            Encode the following JSON into URL format and copy it to the query field of the HTTP request
            {"trace" : "java_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}
            Special Note:
            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
            Token Application: https://alltick.co
            Replace "testtoken" in the URL below with your own token
            API addresses for forex, cryptocurrencies, and precious metals:
            https://quote.alltick.co/quote-b-api
            Stock API address:
            https://quote.alltick.co/quote-stock-b-api
            */
            String url = "http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D";

            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            con.setRequestMethod("GET");

            int responseCode = con.getResponseCode();

            System.out.println("Response Code: " + responseCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));

            String inputLine;

            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            in.close();

            System.out.println(response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

```http
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpJavaExample {

    public static void main(String[] args) {

        try {

            /*
            Encode the following JSON into URL format and copy it to the query field of the HTTP request
            {"trace" : "java_http_test1","data" : {"code" : "700.HK","kline_type" : 1,"kline_timestamp_end" : 0,"query_kline_num" : 2,"adjust_type": 0}}
            Special Note:
            GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
            Token Application: https://alltick.co
            Replace "testtoken" in the URL below with your own token
            API addresses for forex, cryptocurrencies, and precious metals:
            https://quote.alltick.co/quote-b-api
            Stock API address:
            https://quote.alltick.co/quote-stock-b-api
            */
            String url = "http://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22java_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D";

            URL obj = new URL(url);

            HttpURLConnection con = (HttpURLConnection) obj.openConnection();

            con.setRequestMethod("GET");

            int responseCode = con.getResponseCode();

            System.out.println("Response Code: " + responseCode);

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));

            String inputLine;

            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            in.close();

            System.out.println(response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

```http
复制<?php

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// https://quote.alltick.co/quote-b-ws-api
// Stock API address:
// https://quote.alltick.co/quote-stock-b-ws-api

$params = '{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}';

$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';
$method = 'GET';

$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);

/* Set specific parameters based on request type */
switch (strtoupper($method)) {
    case 'GET':
        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);
        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';
        break;
    default:
}

/* Initialize and execute curl request */
$ch = curl_init();
curl_setopt_array($ch, $opts);
$data = curl_exec($ch);
$error = curl_error($ch);
curl_close($ch);

if ($error) {
    $data = null;
}

echo $data;
?>
```

```http
<?php

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// https://quote.alltick.co/quote-b-ws-api
// Stock API address:
// https://quote.alltick.co/quote-stock-b-ws-api

$params = '{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}';

$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';
$method = 'GET';

$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);

/* Set specific parameters based on request type */
switch (strtoupper($method)) {
    case 'GET':
        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);
        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';
        break;
    default:
}

/* Initialize and execute curl request */
$ch = curl_init();
curl_setopt_array($ch, $opts);
$data = curl_exec($ch);
$error = curl_error($ch);
curl_close($ch);

if ($error) {
    $data = null;
}

echo $data;
?>
```

```http
<?php

// Special Note:
// GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
// Token Application: https://alltick.co
// Replace "testtoken" in the URL below with your own token
// API addresses for forex, cryptocurrencies, and precious metals:
// https://quote.alltick.co/quote-b-ws-api
// Stock API address:
// https://quote.alltick.co/quote-stock-b-ws-api

$params = '{"trace":"1111111111111111111111111","data":{"code":"AAPL.US","kline_type":1,"kline_timestamp_end":0,"query_kline_num":10,"adjust_type":0}}';

$url = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken';
$method = 'GET';

$opts = array(CURLOPT_TIMEOUT => 10, CURLOPT_RETURNTRANSFER => 1, CURLOPT_SSL_VERIFYPEER => false, CURLOPT_SSL_VERIFYHOST => false);

/* Set specific parameters based on request type */
switch (strtoupper($method)) {
    case 'GET':
        $opts[CURLOPT_URL] = $url.'&query='.rawurlencode($params);
        $opts[CURLOPT_CUSTOMREQUEST] = 'GET';
        break;
    default:
}

/* Initialize and execute curl request */
$ch = curl_init();
curl_setopt_array($ch, $opts);
$data = curl_exec($ch);
$error = curl_error($ch);
curl_close($ch);

if ($error) {
    $data = null;
}

echo $data;
?>
```

```http
复制import time
import requests
import json

# Extra headers
test_headers = {
    'Content-Type': 'application/json'
}

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# https://quote.alltick.co/quote-b-ws-api
# Stock API address:
# https://quote.alltick.co/quote-stock-b-ws-api
Encode the following JSON and copy it to the "query" field of the HTTP query string
{"trace": "python_http_test1", "data": {"code": "700.HK", "kline_type": 1, "kline_timestamp_end": 0, "query_kline_num": 2, "adjust_type": 0}}
{"trace": "python_http_test2", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
{"trace": "python_http_test3", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
'''
test_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'
test_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'
test_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'

resp1 = requests.get(url=test_url1, headers=test_headers)
time.sleep(1)
resp2 = requests.get(url=test_url2, headers=test_headers)
time.sleep(1)
resp3 = requests.get(url=test_url3, headers=test_headers)

# Decoded text returned by the request
text1 = resp1.text
print(text1)

text2 = resp2.text
print(text2)

text3 = resp3.text
print(text3)
```

```http
import time
import requests
import json

# Extra headers
test_headers = {
    'Content-Type': 'application/json'
}

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# https://quote.alltick.co/quote-b-ws-api
# Stock API address:
# https://quote.alltick.co/quote-stock-b-ws-api
Encode the following JSON and copy it to the "query" field of the HTTP query string
{"trace": "python_http_test1", "data": {"code": "700.HK", "kline_type": 1, "kline_timestamp_end": 0, "query_kline_num": 2, "adjust_type": 0}}
{"trace": "python_http_test2", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
{"trace": "python_http_test3", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
'''
test_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'
test_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'
test_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'

resp1 = requests.get(url=test_url1, headers=test_headers)
time.sleep(1)
resp2 = requests.get(url=test_url2, headers=test_headers)
time.sleep(1)
resp3 = requests.get(url=test_url3, headers=test_headers)

# Decoded text returned by the request
text1 = resp1.text
print(text1)

text2 = resp2.text
print(text2)

text3 = resp3.text
print(text3)
```

```http
import time
import requests
import json

# Extra headers
test_headers = {
    'Content-Type': 'application/json'
}

'''
# Special Note:
# GitHub: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api
# Token Application: https://alltick.co
# Replace "testtoken" in the URL below with your own token
# API addresses for forex, cryptocurrencies, and precious metals:
# https://quote.alltick.co/quote-b-ws-api
# Stock API address:
# https://quote.alltick.co/quote-stock-b-ws-api
Encode the following JSON and copy it to the "query" field of the HTTP query string
{"trace": "python_http_test1", "data": {"code": "700.HK", "kline_type": 1, "kline_timestamp_end": 0, "query_kline_num": 2, "adjust_type": 0}}
{"trace": "python_http_test2", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
{"trace": "python_http_test3", "data": {"symbol_list": [{"code": "700.HK"}, {"code": "UNH.US"}]}}
'''
test_url1 = 'https://quote.alltick.co/quote-stock-b-api/kline?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test1%22%2C%22data%22%20%3A%20%7B%22code%22%20%3A%20%22700.HK%22%2C%22kline_type%22%20%3A%201%2C%22kline_timestamp_end%22%20%3A%200%2C%22query_kline_num%22%20%3A%202%2C%22adjust_type%22%3A%200%7D%7D'
test_url2 = 'https://quote.alltick.co/quote-stock-b-api/depth-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test2%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'
test_url3 = 'https://quote.alltick.co/quote-stock-b-api/trade-tick?token=testtoken&query=%7B%22trace%22%20%3A%20%22python_http_test3%22%2C%22data%22%20%3A%20%7B%22symbol_list%22%3A%20%5B%7B%22code%22%3A%20%22700.HK%22%7D%2C%7B%22code%22%3A%20%22UNH.US%22%7D%5D%7D%7D'

resp1 = requests.get(url=test_url1, headers=test_headers)
time.sleep(1)
resp2 = requests.get(url=test_url2, headers=test_headers)
time.sleep(1)
resp3 = requests.get(url=test_url3, headers=test_headers)

# Decoded text returned by the request
text1 = resp1.text
print(text1)

text2 = resp2.text
print(text2)

text3 = resp3.text
print(text3)
```

#### AllTick网站

官方网站：https://alltick.co/

最后更新于5个月前
