---
id: "url-56037e15"
type: "website"
title: "Nueva función de búsqueda por ISIN"
url: "https://eodhd.com/financial-apis-blog/nueva-funcion-de-busqueda-por-isin"
description: "Hoy introducimos una nueva función en nuestra API de búsqueda: la búsqueda por ISIN. Los números internacionales de identificación de valores (o ISIN) son muy importantes para inversores y operadores. Y mantenemos la atención profunda en nuestra base de datos ISINs. Seguimos añadiendo más y más números y por el momento ya tenemos más de 45000 ISINs."
source: ""
tags: []
crawl_time: "2026-03-18T08:30:27.497Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# Nueva función de búsqueda por ISIN\n\n## 正文\n\nHoy introducimos una nueva función en nuestra API de búsqueda: la búsqueda por ISIN. Los números internacionales de identificación de valores (o ISIN) son muy importantes para inversores y operadores. Y mantenemos la atención profunda en nuestra base de datos ISINs. Seguimos añadiendo más y más números y por el momento ya tenemos más de 45000 ISINs.\n\nEs fácil utilizar la búsqueda, basta con utilizar ISIN en la cadena de consulta. Se aceptan ISIN completos o incompletos. A continuación puede ver un ejemplo de consulta y salida con ISIN incompleto:\n\nhttps://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN\n\nSi sólo tiene CUSIP en su base de datos, es fácil calcular el ISIN a partir del CUSIP. Debe añadir caracteres “US” al principio del CUSIP y la suma de comprobación al final. La suma de comprobación se calcula con el algoritmo de Luhn. Si es difícil calcular la suma de comprobación, puede buscar ISIN incompleto, si tenemos este ISIN en nuestra base de datos, lo encontramos.\n\nEncontrará más información y ejemplos en nuestra página de documentación de Search API.\n\n> https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN\n\n![](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/12/search_by_isin.jpg)\n\n![Búsqueda por ISIN. Búsqueda ISIN](https://eodhistoricaldata.com/financial-apis-blog/wp-content/uploads/2019/12/image.png)\n"
  rawContent: ""
  suggestedFilename: "-blog_nueva-funcion-de-busqueda-por-isin"
  publishDate: ""
  author: ""
  categories: []
---

# Nueva función de búsqueda por ISIN

## 源URL

https://eodhd.com/financial-apis-blog/nueva-funcion-de-busqueda-por-isin

## 正文

Hoy introducimos una nueva función en nuestra API de búsqueda: la búsqueda por ISIN. Los números internacionales de identificación de valores (o ISIN) son muy importantes para inversores y operadores. Y mantenemos la atención profunda en nuestra base de datos ISINs. Seguimos añadiendo más y más números y por el momento ya tenemos más de 45000 ISINs.

Es fácil utilizar la búsqueda, basta con utilizar ISIN en la cadena de consulta. Se aceptan ISIN completos o incompletos. A continuación puede ver un ejemplo de consulta y salida con ISIN incompleto:

https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN

Si sólo tiene CUSIP en su base de datos, es fácil calcular el ISIN a partir del CUSIP. Debe añadir caracteres “US” al principio del CUSIP y la suma de comprobación al final. La suma de comprobación se calcula con el algoritmo de Luhn. Si es difícil calcular la suma de comprobación, puede buscar ISIN incompleto, si tenemos este ISIN en nuestra base de datos, lo encontramos.

Encontrará más información y ejemplos en nuestra página de documentación de Search API.

> https://eodhistoricaldata.com/api/search/AAPL?api_token=YOUR_API_TOKEN

![](https://eodhd.com/financial-apis-blog/wp-content/uploads/2019/12/search_by_isin.jpg)

![Búsqueda por ISIN. Búsqueda ISIN](https://eodhistoricaldata.com/financial-apis-blog/wp-content/uploads/2019/12/image.png)
