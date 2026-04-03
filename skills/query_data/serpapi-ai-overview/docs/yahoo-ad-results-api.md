---
id: "url-5c947386"
type: "api"
title: "Yahoo! Ad Results API"
url: "https://serpapi.com/yahoo-ad-results"
description: "When a Yahoo! search contains advertisements, they are parsed and exist within the ads_results array in the JSON output. Advertisements can optionally contain button and site links (inline or expanded site links).\n\nThe API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo.\n\nWhen SerpApi encounters ads results, we add them to our JSON output as the array ads_results. For each ads result, we are able to extract its position, title, link, displayed_link, snippet."
source: ""
tags: []
crawl_time: "2026-03-18T12:57:54.110Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Ads results overview","description":"When SerpApi encounters ads results, we add them to our JSON output as the array ads_results. For each ads result, we are able to extract its position, title, link, displayed_link, snippet.","requestParams":{"engine":"yahoo","p":"Coffee","highlight":"ads_results"},"responseJson":"{\n  ...\n  \"ads_results\": [\n    {\n      \"position\": 8,\n      \"block_position\": \"bottom\",\n      \"title\": \"Personalized Coffee Mugs & Tea Cups at Things Remembered\",\n      \"link\": \"https://www.bing.com/aclick?ld=e3A3L8cH6D8PkUSc66KOWgLzVUCUxGy5KH2BeX8gKxpcGa8XZHxn4srmsFugIKQqrLCsY4Fs8EY0et5ucbdU4zr1M6-LshfxxIIJkFOJAYuMYJCKVsQmIWdNwmd9uLYefuqrQDz0K6xtkeL06IhQIb04pIbQ4I5fKTM6JnWVku-nIW-V05&u=aHR0cHMlM2ElMmYlMmYxMTMueGc0a2VuLmNvbSUyZnRyayUyZnYxJTNmcHJvZiUzZDczMyUyNmNhbXAlM2Q3ODI5MzYlMjZrY3QlM2Rtc24lMjZrY2hpZCUzZDE1MDMzNDU4MSUyNmNyaXRlcmlhaWQlM2RkYXQtMjMzNDgxMjk0MTYwODQwMSUzYWxvYy05MCUyNmNhbXBhaWduaWQlM2QzNTk3Nzk4MzElMjZsb2NwaHklM2QxNjYzJTI2YWRncm91cGlkJTNkMTMyODIxMDk4MDgyODA0NiUyNmNpZCUzZDgzMDEzMzM1MzczOTM5JTI2a2R2JTNkYyUyNmtleHQlM2QlMjZrcGclM2QlMjZrcGlkJTNkJTI2cXVlcnlTdHIlM2Rjb2ZmZWUlMjUyMG11ZyUyNnVybCUzZGh0dHBzJTNhJTJmJTJmd3d3LnRoaW5nc3JlbWVtYmVyZWQuY29tJTJmcGVyc29uYWxpemVkLWNvZmZlZS1tdWdzLXRlYS1jdXBzJTJmY2F0ZWdvcnklMmZjb2ZmZWUtbXVncy10ZWEtY3VwcyUzZnJtc3JjJTNkMSUyNmZjcmVmJTNkYmluZ3Nob3Bfbm9uJTI2cm1hdHQlM2R0c2lkJTNhMTA5MjU3MyU3Y2NpZCUzYTM1OTc3OTgzMSU3Y2FnaWQlM2ExMzI4MjEwOTgwODI4MDQ2JTdjdGlkJTNhZGF0LTIzMzQ4MTI5NDE2MDg0MDElM2Fsb2MtOTAlN2NwcmQlM2ElN2NjcmlkJTNhODMwMTMzMzUzNzM5MzklN2NudyUzYXNlYXJjaCU3Y2R2YyUzYWMlN2NzdCUzYWNvZmZlZSUyNTIwbXVnJTdjbXQlM2FiYiUyNm1zY2xraWQlM2Q1MWY2NTg1YTFmNWMxZWY1Y2Q4ZTA1OGYwMTE4NTE4Yg&rlid=51f6585a1f5c1ef5cd8e058f0118518b\",\n      \"displayed_link\": \"thingsremembered.com/Official/BOGO\",\n      \"snippet\": \"thingsremembered.com has been visited by 10K+ users in the past month. Wonder is Personal. Bring Holiday Magic with Personalized Gifts & Home Décor. Shop Our Limited Time Sale and BOGO 75% Off Custom Gifts Today! Personalization Experts · Timeless Gifts For All\"\n    }\n  ]\n  ...\n}"}
    - {"title":"Results for: Inline Sitelinks","description":"","requestParams":{"engine":"yahoo","p":"Coffee","highlight":"ads_results"},"responseJson":"{\n  ...\n  \"ads_results\": [\n    {\n      \"position\": 2,\n      \"block_position\": \"top\",\n      \"title\": \"Up to 70% Off Photo Gifts - Custom Photo Gifts\",\n      \"link\": \"https://www.bing.com/aclick?ld=e3f_XPSInhxHPF1QuUdfKRxTVUCUxagbTWoFkCVfGN6y1vwdEYr6rAHKsMOAQm07VTjn7AJswqmqE5yYijUwc97w0IcdIbR1Z4xShU2nb5k-sH_QVKHr2adQgtC8HZOhtfblpKfMHqScOhDFHRlhXcWv3k2c8okG-XpkBha2eVi4oXfzV0&u=aHR0cCUzYSUyZiUyZmNsaWNrc2VydmUuZGFydHNlYXJjaC5uZXQlMmZsaW5rJTJmY2xpY2slM2ZsaWQlM2Q0MzcwMDA0MTg5MTYyMTg5MiUyNmRzX3Nfa3dnaWQlM2Q1ODcwMDAwNDg2MDYyNTgxOSUyNiUyNmRzX2VfYWRpZCUzZDc1ODY2NDA2MjE5NTkxJTI2ZHNfZV90YXJnZXRfaWQlM2Rrd2QtNzU4NjY1MTk5NDcyNzMlM2Fsb2MtOTAlMjYlMjZkc191cmxfdiUzZDIlMjZkc19kZXN0X3VybCUzZGh0dHBzJTNhJTJmJTJmd3d3LnNuYXBmaXNoLmNvbSUyZnBob3RvLWdpZnRzJTNmQ0lEJTNkdXMlN2NzZW0lN2MlNWIqRW5naW5lQWNjb3VudFR5cGUqJTVkJTdjc2YlN2MlNWIqQ2FtcGFpZ24qJTVkJTdjYWxsJTdjb3RoJTdjJTViKnNlYXJjaHRlcm0qJTVkJTI2bXNjbGtpZCUzZDMxMGMzYmY5MDhjZjFlMjg5ZGM2NjYyYzE2OGI5NjA4&rlid=310c3bf908cf1e289dc6662c168b9608\",\n      \"displayed_link\": \"www.snapfish.com/Photo/Gift\",\n      \"snippet\": \"Shop Now. Make Custom Photo Gifts, Mugs, Ornaments & More. Great Prices. Free Shipping $29+. Create the Perfect Gift! View our Favorites & Shop Today. Learn What's New · Free Shipping-Orders $29+ · Make a Beautiful Gift. Types: Photo Mugs, Phone Cases, Photo Blankets, Photo Luggage Tag. The Best Place to Print Photos - Digital Trends\",\n      \"sitelinks\": {\n        \"inline\": [\n          {\n            \"title\": \"Free Shipping Over $29\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9RDgwNkQ4QzM0NjY3NDFDNiZ1dD0xNTc0MjQ4MDAzOTIzJnVvPTc1ODY2NDA2MjE5NTkxJmx0PTImcz0xJmVzPTRNLlZ2b1FHUFM4OGpOWTNkYkVXc082cnRXX3d6X0lsV0E0VkdVRzE1YlJ2NDVURA--/RV=2/RE=1574276804/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de359s5zz2nltzMmcU7bOFbujVUCUyVlBPA4TRzxFl7pVqZ5Qv-Zh6aLJKuu3I6dvFK_nNoAvxyIGKLvZaMTiAfFZ6EJaEaXkhJSwxhgPaShCFfjuZRenWRFRendOPLLaetZl2oskYM88NElZmVbDFlLEe4a8qHTntZ7rTfvsvdtNiGraRw%26u%3daHR0cCUzYSUyZiUyZmNsaWNrc2VydmUuZGFydHNlYXJjaC5uZXQlMmZsaW5rJTJmY2xpY2slM2ZsaWQlM2Q0MzcwMDA0MTg5MTYyMTg5MiUyNmRzX3Nfa3dnaWQlM2Q1ODcwMDAwNDg2MDYyNTgxOSUyNmRzX3hfYWR4aWQlM2Q4MzcwMDAwMjIwMzc3MTYwNiUyNmRzX3hfYWR4dHlwZSUzZDElMjZkc19lX2FkaWQlM2Q3NTg2NjQwNjIxOTU5MSUyNmRzX2VfdGFyZ2V0X2lkJTNka3dkLTc1ODY2NTE5OTQ3MjczJTNhbG9jLTkwJTI2JTI2ZHNfdXJsX3YlM2QyJTI2ZHNfZGVzdF91cmwlM2RodHRwcyUzYSUyZiUyZnd3dy5zbmFwZmlzaC5jb20lMmZzbmFwZmlzaC1jb3Vwb25zJTNmY2lkJTNkdXMlN2NzZW0lN2NvdGglN2NibmclN2Nub24tYnJhbmQtY3Jkcy1mcmVlc2hpcC1lbmhuLXNsLXRoeHMlN2N3ZWIlN2Nub24lN2NzaXRlJTI2Q0lEJTNkdXMlN2NzZW0lN2MlNWIqRW5naW5lQWNjb3VudFR5cGUqJTVkJTdjc2YlN2MlNWIqQ2FtcGFpZ24qJTVkJTdjYWxsJTdjb3RoJTdjJTViKnNlYXJjaHRlcm0qJTVkJTI2bXNjbGtpZCUzZGUzYzQ2MDFmY2ZlZTFmZWI1NTQyM2RjYWQxYWE4M2Iy%26rlid%3de3c4601fcfee1feb55423dcad1aa83b2/RK=2/RS=uAlzYiaI7Jjk1V9IHGsN8dUwh0w-%3b_ylc=cnQDMQ--;_ylt=A2KIbMpDHtVd7VQAjV9XNyoA;_ylu=X3oDMTB2cTMwMWo5BGNvbG8DYmYxBHBvcwMyBHZ0aWQDBHNlYwNvdi10b3A-?p=coffee+mug&IG=62886ccaf02b49f0b6000000000f5e7e\"\n          },\n          {\n            \"title\": \"Create Your Custom Gift\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9RDgwNkQ4QzM0NjY3NDFDNiZ1dD0xNTc0MjQ4MDAzOTIzJnVvPTc1ODY2NDA2MjE5NTkxJmx0PTImcz0xJmVzPTRNLlZ2b1FHUFM4OGpOWTNkYkVXc082cnRXX3d6X0lsV0E0VkdVRzE1YlJ2NDVURA--/RV=2/RE=1574276804/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de3dCqTOJwgfVdl_l-AVtnWXTVUCUyCvNDEKMOvwpIEriDEFekag3FxQVTHJxvU2q7Ay2hF5F1wFDIglSQ4Z8AoVArg3-nUbaL7UrroOE81J26RZ87PYthb8MhV54yts-tBf8AZaBjx3RCUF2pa3r_d8OYymlmVccq2cJ2T3ALKds7SYgsF%26u%3daHR0cCUzYSUyZiUyZmNsaWNrc2VydmUuZGFydHNlYXJjaC5uZXQlMmZsaW5rJTJmY2xpY2slM2ZsaWQlM2Q0MzcwMDA0MTg5MTYyMTg5MiUyNmRzX3Nfa3dnaWQlM2Q1ODcwMDAwNDg2MDYyNTgxOSUyNmRzX3hfYWR4aWQlM2Q4MzcwMDAwMjIwMzc3MTMyNCUyNmRzX3hfYWR4dHlwZSUzZDElMjZkc19lX2FkaWQlM2Q3NTg2NjQwNjIxOTU5MSUyNmRzX2VfdGFyZ2V0X2lkJTNka3dkLTc1ODY2NTE5OTQ3MjczJTNhbG9jLTkwJTI2JTI2ZHNfdXJsX3YlM2QyJTI2ZHNfZGVzdF91cmwlM2RodHRwcyUzYSUyZiUyZnd3dy5zbmFwZmlzaC5jb20lMmZ3YWxsLWNhbGVuZGFyLWRldGFpbHMlM2ZjaWQlM2R1cyU3Y3NlbSU3Y290aCU3Y2JuZyU3Y25vbi1icmFuZC1naWZ0LWVuaG4tc2wtY3JlYXRlJTdjd2ViJTdjbm9uJTdjc2l0ZSUyNkNJRCUzZHVzJTdjc2VtJTdjJTViKkVuZ2luZUFjY291bnRUeXBlKiU1ZCU3Y3NmJTdjJTViKkNhbXBhaWduKiU1ZCU3Y2FsbCU3Y290aCU3YyU1YipzZWFyY2h0ZXJtKiU1ZCUyNm1zY2xraWQlM2RlMzI1MWNhOWE1YzgxZTFiNTFkNjQxN2NiYjhjOTMyMg%26rlid%3de3251ca9a5c81e1b51d6417cbb8c9322/RK=2/RS=eg.RZYyLWgTahw6pLERANogUP9s-%3b_ylc=cnQDMQ--;_ylt=A2KIbMpDHtVd7VQAjl9XNyoA;_ylu=X3oDMTB2cTMwMWo5BGNvbG8DYmYxBHBvcwMyBHZ0aWQDBHNlYwNvdi10b3A-?p=coffee+mug&IG=62886ccaf02b49f0b6000000000f5e7e\"\n          },\n          {\n            \"title\": \"Shop Our Best Sellers\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9RDgwNkQ4QzM0NjY3NDFDNiZ1dD0xNTc0MjQ4MDAzOTIzJnVvPTc1ODY2NDA2MjE5NTkxJmx0PTImcz0xJmVzPTRNLlZ2b1FHUFM4OGpOWTNkYkVXc082cnRXX3d6X0lsV0E0VkdVRzE1YlJ2NDVURA--/RV=2/RE=1574276804/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de3ddcjkhgOO7PICzR1SuX3NTVUCUwnBTkGpeGZGdNSVc8Yr73ghcw0D6VlIirAyqstVMfLah26Xjmha8HupxLuULTGxyZu--bEH0TVOjTfTjFQOMlZcHK2G-6u00OWHFyT5mRKWbspzFMMXwrUTfQiLiJikkmXE9QW_vSuPJ2H3hEGvQXR%26u%3daHR0cCUzYSUyZiUyZmNsaWNrc2VydmUuZGFydHNlYXJjaC5uZXQlMmZsaW5rJTJmY2xpY2slM2ZsaWQlM2Q0MzcwMDA0MTg5MTYyMTg5MiUyNmRzX3Nfa3dnaWQlM2Q1ODcwMDAwNDg2MDYyNTgxOSUyNmRzX3hfYWR4aWQlM2Q4MzcwMDAwMjIwMzc3MTMxOCUyNmRzX3hfYWR4dHlwZSUzZDElMjZkc19lX2FkaWQlM2Q3NTg2NjQwNjIxOTU5MSUyNmRzX2VfdGFyZ2V0X2lkJTNka3dkLTc1ODY2NTE5OTQ3MjczJTNhbG9jLTkwJTI2JTI2ZHNfdXJsX3YlM2QyJTI2ZHNfZGVzdF91cmwlM2RodHRwcyUzYSUyZiUyZnd3dy5zbmFwZmlzaC5jb20lMmZiZXN0c2VsbGVycyUzZmNpZCUzZHVzJTdjc2VtJTdjb3RoJTdjYm5nJTdjYnJhbmQtZ2lmdC1lbmhuLXNsLWJlc3RzbHIlN2N3ZWIlN2Nub24lN2NzaXRlJTI2Q0lEJTNkdXMlN2NzZW0lN2MlNWIqRW5naW5lQWNjb3VudFR5cGUqJTVkJTdjc2YlN2MlNWIqQ2FtcGFpZ24qJTVkJTdjYWxsJTdjb3RoJTdjJTViKnNlYXJjaHRlcm0qJTVkJTI2bXNjbGtpZCUzZDhlYzliNmIyZjcwNzFlNDQxNmNjZWI2N2U5NDNiZmI1%26rlid%3d8ec9b6b2f7071e4416cceb67e943bfb5/RK=2/RS=vZh0kOY63raqhpjSUgjb0FSIMag-%3b_ylc=cnQDMQ--;_ylt=A2KIbMpDHtVd7VQAj19XNyoA;_ylu=X3oDMTB2cTMwMWo5BGNvbG8DYmYxBHBvcwMyBHZ0aWQDBHNlYwNvdi10b3A-?p=coffee+mug&IG=62886ccaf02b49f0b6000000000f5e7e\"\n          },\n          ...\n        ]\n      },\n      \"button\": {\n        \"text\": \"Shop Now\",\n        \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9RDgwNkQ4QzM0NjY3NDFDNiZ1dD0xNTc0MjQ4MDAzOTIzJnVvPTc1ODY2NDA2MjE5NTkxJmx0PTImcz0xJmVzPTRNLlZ2b1FHUFM4OGpOWTNkYkVXc082cnRXX3d6X0lsV0E0VkdVRzE1YlJ2NDVURA--/RV=2/RE=1574276804/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de3wKpQTwUiWZ1SWePlwj7P0TVUCUzjA606O6QKfjWaNVaaDGnSc5AL_XcuF5e6WlPUQln5SGOqrYa4BMJa3UfgWPOrxDdIgOx9GxC9zkdErunJWxlNf21o7txVY6qlPVBWOozM0tmM6nKG6It-XkenCUN8PRFvPu_ur-yUzI2KWlOMIZrWmTlYU2Gf5rZEZvpPZY_ZjA%26u%3daHR0cCUzYSUyZiUyZmNsaWNrc2VydmUuZGFydHNlYXJjaC5uZXQlMmZsaW5rJTJmY2xpY2slM2ZsaWQlM2Q0MzcwMDA0MTg5MTYyMTg5MiUyNmRzX3Nfa3dnaWQlM2Q1ODcwMDAwNDg2MDYyNTgxOSUyNiUyNmRzX2VfYWRpZCUzZDc1ODY2NDA2MjE5NTkxJTI2ZHNfZV90YXJnZXRfaWQlM2Rrd2QtNzU4NjY1MTk5NDcyNzMlM2Fsb2MtOTAlMjYlMjZkc191cmxfdiUzZDIlMjZkc19kZXN0X3VybCUzZGh0dHBzJTNhJTJmJTJmd3d3LnNuYXBmaXNoLmNvbSUyZnNuYXBmaXNoLWNvdXBvbnMlM2ZjaWQlM2R1cyU3Y3NlbSU3Y290aCU3Y2JuZyU3Y2FjdGlvbmV4dCU3Y3dlYiU3Y25vbiU3Y3NpdGUlMjZDSUQlM2R1cyU3Y3NlbSU3YyU1YipFbmdpbmVBY2NvdW50VHlwZSolNWQlN2NzZiU3YyU1YipDYW1wYWlnbiolNWQlN2NhbGwlN2NvdGglN2MlNWIqc2VhcmNodGVybSolNWQlMjZtc2Nsa2lkJTNkODE1YjkyNjZmYmU0MWU2OTFlZGZjZmIzZTVhMDliMWY%26rlid%3d815b9266fbe41e691edfcfb3e5a09b1f/RK=2/RS=eh9McR4EcneisB9dYN8fluCn55E-%3b_ylc=cnQDMQ--;_ylt=A2KIbMpDHtVd7VQAiF9XNyoA;_ylu=X3oDMTB2cTMwMWo5BGNvbG8DYmYxBHBvcwMyBHZ0aWQDBHNlYwNvdi10b3A-?p=coffee+mug&IG=62886ccaf02b49f0b6000000000f5e7e\"\n      }\n    }\n  ]\n  ...\n}"}
    - {"title":"Results for: Expanded Sitelinks","description":"","requestParams":{"engine":"yahoo","p":"Coffee","highlight":"ads_results"},"responseJson":"{\n  ...\n  \"ads_results\": [\n    {\n      \"position\": 6,\n      \"block_position\": \"bottom\",\n      \"title\": \"Order Promotional Products - Free Samples. Expert Service!\",\n      \"link\": \"https://www.bing.com/aclick?ld=e3-MtbAlvmT8JqzOEXaDZ5WzVUCUxbRnATuUOdTld1hQPo6HKBV3xssW1JBz3crBjO-W-cZoXD375XS6LIdgrDN6Es_kmLe0LFZM-xUOW16sO4Z3pbbyXvB0buOQedCGfKRZ5bye-yonREJoFUmos1iY-jifEjDCBpDFKO_7J0_63Klqth&u=aHR0cCUzYSUyZiUyZnBpeGVsLmV2ZXJlc3R0ZWNoLm5ldCUyZjQxNjclMmZjcSUzZmV2X3NpZCUzZDEwJTI2ZXZfbHR4JTNkJTI2ZXZfbHglM2Rrd2QtNzMzMjM3NzIzOTE1NzQlM2Fsb2MtOTAlMjZldl9jcnglM2Q3MzMyMzczNzc4Mjc2NCUyNmV2X210JTNkZSUyNmV2X2R2YyUzZGMlMjZldl9waHklM2QxNjYzJTI2ZXZfbG9jJTNkJTI2ZXZfY3glM2Q1MjE2NjE5NiUyNmV2X2F4JTNkMTc3MTQ2NzU2OSUyNmV2X2V4JTNkJTI2dXJsJTNkaHR0cHMlMjUzQSUyNTJGJTI1MkZ3d3cuNGltcHJpbnQuY29tJTI1MkYlMjUzRm1raWQlMjUzRDM0aTNfMDJfMDAxJTI1MjZ1dG1fc291cmNlJTI1M0RiaW5nJTI1MjZ1dG1fbWVkaXVtJTI1M0RjcGMlMjUyNnV0bV90ZXJtJTI1M0RkaXNjb3VudCUyNTI1MjBtdWdzJTI1MjUyMGNvdXBvbiUyNTI1MjBjb2RlJTI1MjZ1dG1fY2FtcGFpZ24lMjUzREdlbl9VU19Db21wZXRpdGlvbiUyYkJpbmclMjUyNnNfa3djaWQlMjUzREFMITQxNjchMTAhNzMzMjM3Mzc3ODI3NjQhNzMzMjM3NzIzOTE1NzQlMjZtc2Nsa2lkJTNkZmExNTVhYjNkODYzMWZkODQzZmQwNzY2YzYyN2E3ZTMlMjZ1dG1fc291cmNlJTNkYmluZyUyNnV0bV9tZWRpdW0lM2RjcGMlMjZ1dG1fY2FtcGFpZ24lM2RHZW5fVVNfQ29tcGV0aXRpb24lMjZ1dG1fdGVybSUzZGRpc2NvdW50JTI1MjBtdWdzJTI1MjBjb3Vwb24lMjUyMGNvZGUlMjZ1dG1fY29udGVudCUzZENvbXBldGl0aW9u&rlid=fa155ab3d8631fd843fd0766c627a7e3\",\n      \"displayed_link\": \"www.4imprint.com\",\n      \"snippet\": \"Sale. 4imprint.com has been visited by 100K+ users in the past month. 1000's of Products Printed with Your Logo. Ships On-Time Guaranteed.\",\n      \"sitelinks\": {\n        \"expanded\": [\n          {\n            \"title\": \"Wedding Outside Ideas\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9NTU2MDMzQkMzQjdCNDQ1RSZ1dD0xNjYxMzkzNzQxODUxJnVvPTgzODM3OTgyNzUwOTI4Jmx0PTImcz0xJmVzPVZtV0pVbHdHUFM4MGFvZGRiZ1UyUTNlUHMwVjE5TThTLlZuaWlnV0N3bjEwbE5tVw--/RV=2/RE=1661422542/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8x1KSpiOyNu5YX4WGs-UqPTVUCUxZHb8sjoFVVa8pEBZcM32CqX-lKzYNEeoEOmH1gzH-PG78qso6FIasxnWjPZCFDZbMvFEV2wstg83bWfW4glgq6NRoA7rNdVJmnjBw1_XNYz9JAytlYfKuQoLv7IYtTfT4QIGX4GmXXuZNUidmW01f247pP8TYTFNfmV9y1YkXACWA9dm14qFMslsp0JH8MLY%26u%3daHR0cHMlM2ElMmYlMmZ3d3cuYW1hem9uLmNvbSUyZnMlMmYlM2ZpZSUzZFVURjglMjZrZXl3b3JkcyUzZHdlZGRpbmclMmJvdXRzaWRlJTJiaWRlYXMlMjZpbmRleCUzZGFwcw%26rlid%3d93c908274404188e1dee6b219f4a2274/RK=2/RS=hLtN_fn8elwrdRYAQ1H40QVL7M0-;_ylt=Awr9F7BN2wZjYPwAlwlXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA292LXRvcA--?IG=0afd17b0978140039d00000000207b5e\",\n            \"snippet\": \"Get Inspired By Unique Wedding\\nOutside Ideas For Your Big Day.\"\n          },\n          {\n            \"title\": \"Shop Now\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9NTU2MDMzQkMzQjdCNDQ1RSZ1dD0xNjYxMzkzNzQxODUxJnVvPTgzODM3OTgyNzUwOTI4Jmx0PTImcz0xJmVzPVZtV0pVbHdHUFM4MGFvZGRiZ1UyUTNlUHMwVjE5TThTLlZuaWlnV0N3bjEwbE5tVw--/RV=2/RE=1661422542/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8VEL6sG1fAHdMrjxFp_OabzVUCUyejq-tZeAaf-E1KBzocQETR6gYmN4DxO64KVCsCbuUWKzxMoApW_uyGZEJ8OY0TSoWw61sNvhmy6GSgGPlrc8_upZcA00jluKXeDjx-ar5AB_1UjZv9jYrDs_Nj526Vvk3RSmgXTCxnOHzz4_ww5gyu3Ta5MLZLfnt6NiuVx_YDdSipWcxVqMLUI-uzTUNJGQ%26u%3daHR0cHMlM2ElMmYlMmYlMmZhbWF6b24uY29tJTJmc3RvcmVzJTJmcGFnZSUyZkI1RjFDOUEwLUZENDYtNDczMi1CQjkzLUZFMjJDRERCQjUzQg%26rlid%3da46be14ad8d01b2123a7824c039e221d/RK=2/RS=eT64hAnGHnw9mfpYwrp0PX7b35w-;_ylt=Awr9F7BN2wZjYPwAmAlXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA292LXRvcA--?IG=0afd17b0978140039d00000000207b5e\",\n            \"snippet\": \"Choose From A Wide Variety Of\\nProducts To Suit Your Needs.\"\n          },\n          {\n            \"title\": \"Guillotine Paper Cutter\",\n            \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9NTU2MDMzQkMzQjdCNDQ1RSZ1dD0xNjYxMzkzNzQxODUxJnVvPTgzODM3OTgyNzUwOTI4Jmx0PTImcz0xJmVzPVZtV0pVbHdHUFM4MGFvZGRiZ1UyUTNlUHMwVjE5TThTLlZuaWlnV0N3bjEwbE5tVw--/RV=2/RE=1661422542/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de8V5Xdfpo8973X0jhgsrHINjVUCUxdqr2bBofbSro84RBP5kfGSWVzJOGDbfWdJs9ZJaWLZaY66essmJ4kjxwrk3OLVy5X-fehXbOtCa9WzFY1VTF-9qpmuPBQLIokEIE2hsUuJ13wLg5qaoDKeXD6DkD6hoAcbsvyh31KNGuFG5aQepHqeOArmu30mJCAuDjTHIXdN1CcHFO5cRbZm3Mld3N3zKw%26u%3daHR0cHMlM2ElMmYlMmZ3d3cuYW1hem9uLmNvbSUyZmJlc3QtZ3VpbGxvdGluZS1wYXBlci1jdXR0ZXIlMmZzJTNmayUzZGJlc3QlMmJndWlsbG90aW5lJTJicGFwZXIlMmJjdXR0ZXI%26rlid%3d4bfa8b36b7721655f4f3e8306c3c9d2a/RK=2/RS=mFhKszXuuApbI8xsxWpYhQiLY5w-;_ylt=Awr9F7BN2wZjYPwAmQlXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA292LXRvcA--?IG=0afd17b0978140039d00000000207b5e\",\n            \"snippet\": \"Find Deals on best guillotine paper\\ncutter in Office Supplies on ...\"\n          },\n          ...\n        ]\n      },\n      \"button\": {\n        \"text\": \"Sale\",\n        \"link\": \"https://r.search.yahoo.com/cbclk2/dWU9RDgwNkQ4QzM0NjY3NDFDNiZ1dD0xNTc0MjQ4MDAzOTIzJnVvPTczMzIzNzM3NzgyNzY0Jmx0PTImcz0xJmVzPW9CM2NEQllHUFMuNzFBODRMYkJWSkRWSDBPeGlqLkphZFMzZEIzWDMyUGZLdC44RTdnLS0-/RV=2/RE=1574276804/RO=10/RU=https%3a%2f%2fwww.bing.com%2faclick%3fld%3de3ecrmdPCnq2xMvsixzPfiTjVUCUzn0hLiQcxId-gXXho03wpqfdmxqqtu3fDvi8QMwWpdb72EyxVPqukuYhdK2OPw2OVen-xK_UAfa5psM1B6h3pLOubbtvkWWUuSbsFr_veD9D5igAYNAYGeSFPXza0TZ2SWpzWlP3ohhkcMcrUnA6MmRVKcBfweuUbVboTr0DANEw%26u%3daHR0cCUzYSUyZiUyZnBpeGVsLmV2ZXJlc3R0ZWNoLm5ldCUyZjQxNjclMmZjcSUzZmV2X3NpZCUzZDEwJTI2ZXZfbHR4JTNkJTI2ZXZfbHglM2Rrd2QtNzMzMjM3NzIzOTE1NzQlM2Fsb2MtOTAlMjZldl9jcnglM2Q3MzMyMzczNzc4Mjc2NCUyNmV2X210JTNkZSUyNmV2X2R2YyUzZGMlMjZldl9waHklM2QxNjYzJTI2ZXZfbG9jJTNkJTI2ZXZfY3glM2Q1MjE2NjE5NiUyNmV2X2F4JTNkMTc3MTQ2NzU2OSUyNmV2X2V4JTNkJTI2dXJsJTNkaHR0cHMlMjUzQSUyNTJGJTI1MkZ3d3cuNGltcHJpbnQuY29tJTI1MkZzYWxlJTI1M0Zta2lkJTI1M0QzNGlfQWN0aW9uMDMlMjUyNnV0bV9zb3VyY2UlMjUzRGJpbmclMjUyNnV0bV9tZWRpdW0lMjUzRGNwYyUyNTI2dXRtX3Rlcm0lMjUzRGRpc2NvdW50JTI1MjUyMG11Z3MlMjUyNTIwY291cG9uJTI1MjUyMGNvZGUlMjUyNnV0bV9jYW1wYWlnbiUyNTNENGltcHJpbnQlMjUyNTIwQmluZyUyNTI2c19rd2NpZCUyNTNEQUwhNDE2NyExMCE3MzMyMzczNzc4Mjc2NCE3MzMyMzc3MjM5MTU3NCUyNm1zY2xraWQlM2Q1MjA4M2Q0M2JmOGMxYTIxZTdmODYwOTZhMWM4M2E5OCUyNnV0bV9zb3VyY2UlM2RiaW5nJTI2dXRtX21lZGl1bSUzZGNwYyUyNnV0bV9jYW1wYWlnbiUzZEdlbl9VU19Db21wZXRpdGlvbiUyNnV0bV90ZXJtJTNkZGlzY291bnQlMjUyMG11Z3MlMjUyMGNvdXBvbiUyNTIwY29kZSUyNnV0bV9jb250ZW50JTNkQ29tcGV0aXRpb24%26rlid%3d52083d43bf8c1a21e7f86096a1c83a98/RK=2/RS=PeW.b7JHlUt0wzuPFrt6zuMOjko-%3b_ylc=cnQDMQ--;_ylt=A2KIbMpDHtVd7VQA3F9XNyoA;_ylu=X3oDMTEyaDFtbTljBGNvbG8DYmYxBHBvcwMxBHZ0aWQDBHNlYwNvdi1ib3R0b20-?p=coffee+mug&IG=62886ccaf02b49f0b6000000000f5e7e\"\n      }\n    }\n  ]\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "yahoo-ad-results-api"
---

# Yahoo! Ad Results API

## 源URL

https://serpapi.com/yahoo-ad-results

## 描述

When a Yahoo! search contains advertisements, they are parsed and exist within the ads_results array in the JSON output. Advertisements can optionally contain button and site links (inline or expanded site links).

The API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo.

When SerpApi encounters ads results, we add them to our JSON output as the array ads_results. For each ads result, we are able to extract its position, title, link, displayed_link, snippet.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

When a Yahoo! search contains advertisements, they are parsed and exist within the ads_results array in the JSON output. Advertisements can optionally contain button and site links (inline or expanded site links).

The API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo.

When SerpApi encounters ads results, we add them to our JSON output as the array ads_results. For each ads result, we are able to extract its position, title, link, displayed_link, snippet.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Api Dashboard

Api Dashboard

Your Account

Edit Profile

Extra Credits

Api Documentation

Api Documentation

Google Search API

AI Overview

About Carousel

Ask AI Mode

Available On

Broaden Searches

Buying Guide

Complementary Results

DMCA Messages

Discover More Places

Discussions and Forums

Episode Guide

Events Results

Find Results On

Google About This Result API

Grammar Check

Immersive Products

Inline Images

Inline People Also Search For

Inline Products

Inline Shopping

Inline Videos

Interactive Diagram

Jobs Results

Knowledge Graph

Latest From

Latest Posts

Menu Highlights

News Results

Nutrition Information

Organic Results

Perspectives

Places Sites

Popular Destinations

Product Result

Product Sites

Questions And Answers

Recipes Results

Refine Search Filters

Refine This Search

Related Brands

Related Categories

Related Questions

Related Searches

Scholarly Articles

Short Videos

Showtimes Results

Spell Check

Sports Results

Things To Know

Top Carousel

Top Insights

Top Stories

Twitter Results

Visual Stories

Google Light Search API

Knowledge Graph

Organic Results

Related Questions

Related Searches

Spell Check

Top Stories

Google AI Mode API

Google AI Overview API

Google Ads Transparency API

Ad Details API

Google Autocomplete API

Google Events API

Google Finance API

Google Finance Markets API

Google Flights API

Airports Results

Autocomplete API

Booking Options

Flights Results

Price Insights

Google Forums API

Google Hotels API

Autocomplete API

Property Details

Reviews API

Google Images API

Images Results

Related Content API

Related Searches

Shopping Results

Suggested Searches

Google Images Light API

Google Immersive Product API

Google Jobs API

Listing API

Google Lens API

About This Image
