# -*- coding: utf-8 -*-
'''
数据查询接口
'''
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pandas import json_normalize
from lixinger_openapi.token import get_token

BASEURL = "https://open.lixinger.com/api/"

def get_fullurl(url_suffix):
    url_suffix = url_suffix.replace('.', '/')
    if url_suffix.startswith('/'):
        url_suffix = url_suffix[1:]
    return BASEURL + url_suffix

def query_json(url_suffix, query_params):
    '''
    API接口，返回json结构
    params:
        url_suffix: api地址后缀, https://open.lixinger.com/api/ 之后的，可以用/或. 例如a/stock/fs或a.stock.fs
        query_params: API的查询json，不需要填token
    '''
    if get_token() is None:
        raise Exception("token未设置")
    query_params["token"] = get_token()
  
    headers = {"Content-Type": "application/json"}
    
    # 创建带重试机制的 session
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # 总共重试3次
        backoff_factor=1,  # 重试间隔：1秒、2秒、4秒
        status_forcelist=[429, 500, 502, 503, 504],  # 这些状态码会触发重试
        allowed_methods=["POST"]  # 允许 POST 请求重试
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        response = session.post(
            url=get_fullurl(url_suffix), 
            data=json.dumps(query_params), 
            headers=headers,
            timeout=30  # 30秒超时
        )
        return response.json()
    except requests.exceptions.SSLError as e:
        # SSL 错误时，尝试禁用 SSL 验证（不推荐用于生产环境）
        print(f"SSL Error occurred, retrying without verification: {e}")
        response = session.post(
            url=get_fullurl(url_suffix), 
            data=json.dumps(query_params), 
            headers=headers,
            timeout=30,
            verify=False  # 禁用 SSL 验证
        )
        return response.json()
    finally:
        session.close()

def query_dataframe(url_suffix, query_params):
    '''
    API接口，返回字典结构
    key     value       type
    code    返回值       int
    data    返回结果     dataframe
    msg     返回消息     string
    '''
    return_value = {'code': -1, 'data': None, 'msg': ''}
    rlt = query_json(url_suffix, query_params)
    if rlt is None:
        return_value['msg'] = 'query failed.'
    else:
        if 'code' in rlt.keys():
            return_value['code'] = rlt['code']
        if 'msg' in rlt.keys():
            return_value['msg'] = rlt['msg']
        if 'data' in rlt.keys():
            return_value['data'] = json_normalize(rlt['data'])
    return return_value
