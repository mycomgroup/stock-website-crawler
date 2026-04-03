# Flat Files Quickstart

## 源URL

https://massive.com/docs/flat-files

## 描述

Massive's Flat Files provide extensive historical market data through convenient, compressed CSV files accessible via a S3-compatible endpoint. Instead of making potentially hundreds of thousands of individual REST API requests, Flat Files enables you to easily download large volumes of historical data with just a few clicks or commands, saving significant time and simplifying your workflow.

## 代码示例

```text
ticker,volume,open,close,high,low,window_start,transactions
AAPL,4930,200.29,200.5,200.63,200.29,1744792500000000000,129
AAPL,1815,200.39,200.34,200.61,200.34,1744792560000000000,57
AAPL,1099,200.3,200.28,200.3,200.13,1744792620000000000,40
AAPL,3672,200.39,200.61,200.64,200.39,1744792680000000000,71
AAPL,4322,200.72,200.69,200.8,200.69,1744792740000000000,88
AAPL,3675,200.7,201.5,201.5,200.7,1744792800000000000,119
AAPL,12785,201.49,202.33,202.33,201.49,1744792860000000000,329
AAPL,11473,202.39,201.81,202.46,201.81,1744792920000000000,199
AAPL,3895,202.0,201.82,202.0,201.65,1744792980000000000,116
AAPL,4322,201.76,201.36,201.76,201.17,1744793040000000000,85
AAPL,2089,201.31,201.35,201.35,201.04,1744793100000000000,48
AAPL,7317,201.31,200.88,201.31,200.71,1744793160000000000,121
```

```text
# Configure your S3 Access and Secret keys
aws configure set aws_access_key_id YOUR_ACCESS_KEY_ID
aws configure set aws_secret_access_key YOUR_SECRET_ACCESS_KEY

# List
aws s3 ls s3://flatfiles/ --endpoint-url https://files.massive.com

# Copy
aws s3 cp s3://flatfiles/us_stocks_sip/trades_v1/2025/11/2025-11-05.csv.gz . --endpoint-url https://files.massive.com
```

```text
# Set up your rclone configuration
rclone config create s3massive s3 env_auth=false access_key_id=YOUR_ACCESS_KEY_ID secret_access_key=YOUR_SECRET_ACCESS_KEY endpoint=https://files.massive.com

# List
rclone ls s3massive:flatfiles

# Copy
rclone copy s3massive:flatfiles/us_stocks_sip/trades_v1/2025/11/2025-11-05.csv.gz .
```

```text
# Enter S3 Access and Secret keys in config file ~/.mc/config.json
mc alias set s3massive https://files.massive.com YOUR_ACCESS_KEY_ID YOUR_SECRET_ACCESS_KEY

# List
mc ls s3massive/flatfiles

# View
mc cat s3massive/flatfiles/us_stocks_sip/trades_v1/2025/11/2025-11-05.csv.gz | gzcat | head -4

# Copy
mc cp s3massive/flatfiles/us_stocks_sip/trades_v1/2025/11/2025-11-05.csv.gz .
```

```python
import boto3
from botocore.config import Config

# Initialize a session using your credentials
session = boto3.Session(
  aws_access_key_id='YOUR_ACCESS_KEY_ID',
  aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
)

# Create a client with your session and specify the endpoint
s3 = session.client(
  's3',
  endpoint_url='https://files.massive.com',
  config=Config(signature_version='s3v4'),
)

# List Example
# Initialize a paginator for listing objects
paginator = s3.get_paginator('list_objects_v2')

# Choose the appropriate prefix depending on the data you need:
# - 'global_crypto' for global cryptocurrency data
# - 'global_forex' for global forex data
# - 'us_indices' for US indices data
# - 'us_options_opra' for US options (OPRA) data
# - 'us_stocks_sip' for US stocks (SIP) data
prefix = 'us_stocks_sip'  # Example: Change this prefix to match your data need

# List objects using the selected prefix
for page in paginator.paginate(Bucket='flatfiles', Prefix=prefix):
  for obj in page['Contents']:
    print(obj['Key'])

# Copy example
# Specify the bucket name
bucket_name = 'flatfiles'

# Specify the S3 object key name
object_key = 'us_stocks_sip/trades_v1/2025/11/2025-11-05.csv.gz'

# Specify the local file name and path to save the downloaded file
# This splits the object_key string by '/' and takes the last segment as the file name
local_file_name = object_key.split('/')[-1]

# This constructs the full local file path
local_file_path = './' + local_file_name

# Download the file
s3.download_file(bucket_name, object_key, local_file_path)
```
