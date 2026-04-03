接口: macro_china_urban_unemployment

目标地址: https://data.stats.gov.cn/easyquery.htm?cn=A01&zb=A0203&sj=202304

描述: 国家统计局-月度数据-城镇调查失业率

限量: 单次返回所有历史数据

输入参数

| 名称  | 类型  | 描述  |
|-----|-----|-----|
| -   | -   | -   |

输出参数

| 名称    | 类型      | 描述 |
|-------|---------|----|
| date  | object  | 年月 |
| item  | object  | -  |
| value | float64 | -  |

接口示例

```python
import akshare as ak

macro_china_urban_unemployment_df = ak.macro_china_urban_unemployment()
print(macro_china_urban_unemployment_df)
```

数据示例

```
       date                     item  value
0    201812         全国城镇16—24岁劳动力失业率   10.1
1    201812  全国城镇不包含在校生的25—29岁劳动力失业率    0.0
2    201812  全国城镇不包含在校生的16—24岁劳动力失业率    0.0
3    201812            企业就业人员周平均工作时间    0.0
4    201812         全国城镇25—59岁劳动力失业率    4.4
..      ...                      ...    ...
715  202411         全国城镇16—24岁劳动力失业率    0.0
716  202411  全国城镇不包含在校生的16—24岁劳动力失业率    0.0
717  202411         全国城镇25—59岁劳动力失业率    0.0
718  202411           全国城镇本地户籍劳动力失业率    0.0
719  202411                全国城镇调查失业率    0.0
[720 rows x 3 columns]
```

###### 社会融资规模增量统计
