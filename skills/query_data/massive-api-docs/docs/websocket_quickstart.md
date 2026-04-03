# WebSocket Quickstart

## 源URL

https://massive.com/docs/websocket/quickstart

## 描述

The Massive WebSocket API provides streaming market data from major U.S. exchanges and other sources. For most users, integrating our official client libraries is the easiest and quickest way to handle authentication, subscription management, and message parsing. To get started, you will need to sign up for an account and authenticate your requests using an API key.

## 代码示例

```text
npm install -g wscat
```

### Websocket

```text
wscat -c wss://delayed.massive.com/stocks
```

### Websocket

```text
wscat -c wss://socket.massive.com/stocks
```

```json
[{
  "ev":"status",
  "status":"connected",
  "message":"Connected Successfully"
}]
```

```json
{
  "action":"auth",
  "params":"YOUR_API_KEY"
}
```

```json
[{
  "ev":"status",
  "status":"auth_success",
  "message":"authenticated"
}]
```

```json
{
  "action":"subscribe",
  "params":"AM.AAPL,AM.MSFT"
}
```

```json
[
  {
    "ev": "AM",
    "sym": "AAPL",
    "v": 12345,
    "o": 150.85,
    "c": 152.90,
    "h": 153.17,
    "l": 150.50,
    "a": 151.87,
    "s": 1611082800000,
    "e": 1611082860000
  }
]
```

```json
[
  {
    "ev": "T",        
    "sym": "MSFT",    
    "i": "50578",     
    "x": 4,           
    "p": 215.9721,    
    "s": 100,         
    "t": 1611082428813,
    "z": 3            
  },
  {
    "ev": "T",
    "sym": "MSFT",
    "i": "12856",
    "x": 4,
    "p": 215.989,
    "s": 1,
    "c": [37],        
    "t": 1611082428814,
    "z": 3
  }
]
```
