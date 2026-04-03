---
id: "url-2ee401db"
type: "api"
title: "Security"
url: "https://api-dashboard.search.brave.com/documentation/resources/security"
description: "Internally, we require security and privacy reviews from our dedicated\nsecurity and privacy teams, both during the design phase and\nimplementation phase of new features, as well as for new vendor\nrequests and certain bug fixes. A member of the security and privacy\nteams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security\nsign-off. In addition, we often require threat modeling as part\nof specification design, usually as a “Security and Privacy Considerations”\nsection in the spec."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:36.644Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search"
  method: "GET"
  sections:
    - {"level":"H2","title":"Internal process","content":["Internally, we require security and privacy reviews from our dedicated\nsecurity and privacy teams, both during the design phase and\nimplementation phase of new features, as well as for new vendor\nrequests and certain bug fixes. A member of the security and privacy\nteams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security\nsign-off. In addition, we often require threat modeling as part\nof specification design, usually as a “Security and Privacy Considerations”\nsection in the spec."],"codeBlocks":[]}
    - {"level":"H2","title":"Bug bounty program","content":["Brave highly prioritizes responsiveness to external security reports.\nWe have an extremely active bug bounty program at hackerone.com/brave; as of October 2024,\nour average time to triage is about 10 hours and average time to\nresolution is about 4 days. We also solicit security reports at security@brave.com. We contracted an\nexternal penetration test of Brave Search (prior to development of the API)\nvia a HackerOne Challenge in May 2021; 2 high severity and 1 medium severity were reported\nand fixed promptly. In addition, Brave Search API’s last external penetration\ntest was completed in April 2025, and we are in the process of being certified\nfor SOC 2 (proof can be provided upon request to customers)."],"codeBlocks":[]}
    - {"level":"H2","title":"Compliance","content":["Our Data Protection Officer (DPO) advises on our compliance\nwith data protection and privacy laws such as the EU’s General\nData Protection Regulation (GDPR) and ePrivacy Directive, and\nthe California Consumer Privacy Act (CCPA) and California\nPrivacy Rights Act (CPRA). They also participate in security\nand privacy reviews, handle Right to Be Forgotten (RTFB) requests, and ensure our privacy policy is up\nto date. Brave adopts a baseline standard to data protection based on\ncommon data protection principles but we adapt our approach where\nnecessary and appropriate for specific jurisdictions and rules.\nCompliance, as with all organizations subject to data protection\nlaw, is an ongoing process and considered within the security and\nprivacy review process established within Brave. ISO standards\nsuch as 27001 and 27701 provide guidance for establishing,\nimplementing, maintaining and continuously improving our approach\nto information security and privacy information management."],"codeBlocks":[]}
    - {"level":"H2","title":"Malicious content","content":["Brave takes the utmost care in preventing malicious content from\npersisting in the search index and addresses feedback in a timely manner. For example:","• Not all URLs we know about (>100B) make it into the index (20B+).\nWe only index pages visited by\nreal people (determined via privacy preserving techniques), linked from\nmultiple pages in the index (reputation transfer), and from curated\nRSS feeds.\n• We use real-time blacklists for phishing and malware, similar to Safe Browsing\n• We do active scans for child sexual abuse material (CSAM),\nboth internally and using a paid 3rd party\n(ActiveFence) and block such content.\n• We acknowledge and consider RTBF requests from individuals\nwherever they are located (not just from the EU) after our DPO’s\ninternal assessment for justification."],"codeBlocks":[]}
    - {"level":"H2","title":"Resources","content":["We have a business continuity plan available upon request and\nregularly perform backups.","Brave grants access to resources under the principle of least\nprivilege. Access requests are subject to security/privacy\nreviews and promptly revoked upon termination. Note that all Brave\nstaff and contractors are bound by a confidentiality policy.\nWe enable SSO and non-SMS MFA when possible for our employees.\nThe Brave Search API dashboard also supports login via non-SMS MFA.\nOur production deployment and access control policies are available\nupon request.","Third-party services and dependencies are subject to security\nand privacy review upon initialization. We use a combination of\nDependabot and Socket.dev for automated third party dependency\nsecurity scanning whenever a dependency changes or a new\nvulnerability is released.","Our security incident handling policy is available upon request.\nSecurity events in Search products are monitored by the Search\nSecOps team. We will promptly notify affected customers and the\nrelevant regulatory authorities if we experience a data breach\naccording to our obligations and risks to individuals.","For more info, please contact privacy@brave.com for privacy and data protection inquiries or security@brave.com for security inquiries."],"codeBlocks":[]}
  tables: []
  examples: []
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nResources\n\nSecurity at Brave\n\nBrave takes our customers’ security and privacy very seriously.\nAs an API provider for some of the biggest names in tech, we’ve\npassed numerous vendor audits and are always happy to answer security\nquestions from potential customers.\n\nInternal process\n\nInternally, we require security and privacy reviews from our dedicated\nsecurity and privacy teams, both during the design phase and\nimplementation phase of new features, as well as for new vendor\nrequests and certain bug fixes. A member of the security and privacy\nteams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security\nsign-off. In addition, we often require threat modeling as part\nof specification design, usually as a “Security and Privacy Considerations”\nsection in the spec.\n\nBug bounty program\n\nBrave highly prioritizes responsiveness to external security reports.\nWe have an extremely active bug bounty program at hackerone.com/brave; as of October 2024,\nour average time to triage is about 10 hours and average time to\nresolution is about 4 days. We also solicit security reports at security@brave.com. We contracted an\nexternal penetration test of Brave Search (prior to development of the API)\nvia a HackerOne Challenge in May 2021; 2 high severity and 1 medium severity were reported\nand fixed promptly. In addition, Brave Search API’s last external penetration\ntest was completed in April 2025, and we are in the process of being certified\nfor SOC 2 (proof can be provided upon request to customers).\n\nCompliance\n\nOur Data Protection Officer (DPO) advises on our compliance\nwith data protection and privacy laws such as the EU’s General\nData Protection Regulation (GDPR) and ePrivacy Directive, and\nthe California Consumer Privacy Act (CCPA) and California\nPrivacy Rights Act (CPRA). They also participate in security\nand privacy reviews, handle Right to Be Forgotten (RTFB) requests, and ensure our privacy policy is up\nto date. Brave adopts a baseline standard to data protection based on\ncommon data protection principles but we adapt our approach where\nnecessary and appropriate for specific jurisdictions and rules.\nCompliance, as with all organizations subject to data protection\nlaw, is an ongoing process and considered within the security and\nprivacy review process established within Brave. ISO standards\nsuch as 27001 and 27701 provide guidance for establishing,\nimplementing, maintaining and continuously improving our approach\nto information security and privacy information management.\n\nMalicious content\n\nBrave takes the utmost care in preventing malicious content from\npersisting in the search index and addresses feedback in a timely manner. For example:\n\nNot all URLs we know about (>100B) make it into the index (20B+).\nWe only index pages visited by\nreal people (determined via privacy preserving techniques), linked from\nmultiple pages in the index (reputation transfer), and from curated\nRSS feeds.\n\nWe use real-time blacklists for phishing and malware, similar to Safe Browsing\n\nWe do active scans for child sexual abuse material (CSAM),\nboth internally and using a paid 3rd party\n(ActiveFence) and block such content.\n\nWe acknowledge and consider RTBF requests from individuals\nwherever they are located (not just from the EU) after our DPO’s\ninternal assessment for justification.\n\nWe have a business continuity plan available upon request and\nregularly perform backups.\n\nBrave grants access to resources under the principle of least\nprivilege. Access requests are subject to security/privacy\nreviews and promptly revoked upon termination. Note that all Brave\nstaff and contractors are bound by a confidentiality policy.\nWe enable SSO and non-SMS MFA when possible for our employees.\nThe Brave Search API dashboard also supports login via non-SMS MFA.\nOur production deployment and access control policies are available\nupon request.\n\nThird-party services and dependencies are subject to security\nand privacy review upon initialization. We use a combination of\nDependabot and Socket.dev for automated third party dependency\nsecurity scanning whenever a dependency changes or a new\nvulnerability is released.\n\nOur security incident handling policy is available upon request.\nSecurity events in Search products are monitored by the Search\nSecOps team. We will promptly notify affected customers and the\nrelevant regulatory authorities if we experience a data breach\naccording to our obligations and risks to individuals.\n\nFor more info, please contact privacy@brave.com for privacy and data protection inquiries or security@brave.com for security inquiries.\n\nOn this page"
  suggestedFilename: "resources-security"
---

# Security

## 源URL

https://api-dashboard.search.brave.com/documentation/resources/security

## 描述

Internally, we require security and privacy reviews from our dedicated
security and privacy teams, both during the design phase and
implementation phase of new features, as well as for new vendor
requests and certain bug fixes. A member of the security and privacy
teams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security
sign-off. In addition, we often require threat modeling as part
of specification design, usually as a “Security and Privacy Considerations”
section in the spec.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search`

## 文档正文

Internally, we require security and privacy reviews from our dedicated
security and privacy teams, both during the design phase and
implementation phase of new features, as well as for new vendor
requests and certain bug fixes. A member of the security and privacy
teams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security
sign-off. In addition, we often require threat modeling as part
of specification design, usually as a “Security and Privacy Considerations”
section in the spec.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Resources

Security at Brave

Brave takes our customers’ security and privacy very seriously.
As an API provider for some of the biggest names in tech, we’ve
passed numerous vendor audits and are always happy to answer security
questions from potential customers.

Internal process

Internally, we require security and privacy reviews from our dedicated
security and privacy teams, both during the design phase and
implementation phase of new features, as well as for new vendor
requests and certain bug fixes. A member of the security and privacy
teams must sign off on any changes or specs that warrant review. github.com/brave/brave-browser/wiki/Security-reviews outlines the types of changes which explicitly require security
sign-off. In addition, we often require threat modeling as part
of specification design, usually as a “Security and Privacy Considerations”
section in the spec.

Bug bounty program

Brave highly prioritizes responsiveness to external security reports.
We have an extremely active bug bounty program at hackerone.com/brave; as of October 2024,
our average time to triage is about 10 hours and average time to
resolution is about 4 days. We also solicit security reports at security@brave.com. We contracted an
external penetration test of Brave Search (prior to development of the API)
via a HackerOne Challenge in May 2021; 2 high severity and 1 medium severity were reported
and fixed promptly. In addition, Brave Search API’s last external penetration
test was completed in April 2025, and we are in the process of being certified
for SOC 2 (proof can be provided upon request to customers).

Compliance

Our Data Protection Officer (DPO) advises on our compliance
with data protection and privacy laws such as the EU’s General
Data Protection Regulation (GDPR) and ePrivacy Directive, and
the California Consumer Privacy Act (CCPA) and California
Privacy Rights Act (CPRA). They also participate in security
and privacy reviews, handle Right to Be Forgotten (RTFB) requests, and ensure our privacy policy is up
to date. Brave adopts a baseline standard to data protection based on
common data protection principles but we adapt our approach where
necessary and appropriate for specific jurisdictions and rules.
Compliance, as with all organizations subject to data protection
law, is an ongoing process and considered within the security and
privacy review process established within Brave. ISO standards
such as 27001 and 27701 provide guidance for establishing,
implementing, maintaining and continuously improving our approach
to information security and privacy information management.

Malicious content

Brave takes the utmost care in preventing malicious content from
persisting in the search index and addresses feedback in a timely manner. For example:

Not all URLs we know about (>100B) make it into the index (20B+).
We only index pages visited by
real people (determined via privacy preserving techniques), linked from
multiple pages in the index (reputation transfer), and from curated
RSS feeds.

We use real-time blacklists for phishing and malware, similar to Safe Browsing

We do active scans for child sexual abuse material (CSAM),
both internally and using a paid 3rd party
(ActiveFence) and block such content.

We acknowledge and consider RTBF requests from individuals
wherever they are located (not just from the EU) after our DPO’s
internal assessment for justification.

We have a business continuity plan available upon request and
regularly perform backups.

Brave grants access to resources under the principle of least
privilege. Access requests are subject to security/privacy
reviews and promptly revoked upon termination. Note that all Brave
staff and contractors are bound by a confidentiality policy.
We enable SSO and non-SMS MFA when possible for our employees.
The Brave Search API dashboard also supports login via non-SMS MFA.
Our production deployment and access control policies are available
upon request.

Third-party services and dependencies are subject to security
and privacy review upon initialization. We use a combination of
Dependabot and Socket.dev for automated third party dependency
security scanning whenever a dependency changes or a new
vulnerability is released.

Our security incident handling policy is available upon request.
Security events in Search products are monitored by the Search
SecOps team. We will promptly notify affected customers and the
relevant regulatory authorities if we experience a data breach
according to our obligations and risks to individuals.

For more info, please contact privacy@brave.com for privacy and data protection inquiries or security@brave.com for
