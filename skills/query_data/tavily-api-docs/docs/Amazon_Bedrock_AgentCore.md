---
id: "url-43878d9c"
type: "website"
title: "Amazon Bedrock AgentCore"
url: "https://docs.tavily.com/documentation/partnerships/amazon"
description: "Integrate Tavily MCP Server with Amazon Bedrock AgentCore for scalable AI agent deployment on AWS."
source: ""
tags: []
crawl_time: "2026-03-18T06:09:26.471Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"Tavily MCP Server"}
    - {"level":5,"text":"Tavily Agent Skills"}
    - {"level":5,"text":"tavily-cli"}
    - {"level":5,"text":"Partnerships"}
    - {"level":5,"text":"Integrations"}
    - {"level":1,"text":"Amazon Bedrock AgentCore"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/amazon#overview)Overview"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/amazon#prerequisites)Prerequisites"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/amazon#setup)Setup"}
    - {"level":2,"text":"[​](https://docs.tavily.com/documentation/partnerships/amazon#resources)Resources"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/amazon#overview)Overview"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/amazon#prerequisites)Prerequisites"}
    - {"type":"list","listType":"ul","items":["[AWS account](https://aws.amazon.com/)","[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and [configured](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)","[Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP Server","An IAM role with a trust policy allowing `bedrock-agentcore.amazonaws.com` to assume the role"]}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/amazon#setup)Setup"}
    - {"type":"paragraph","content":"Subscribe on the AWS Marketplace"}
    - {"type":"paragraph","content":"Select Amazon Bedrock AgentCore"}
    - {"type":"paragraph","content":"Create an IAM Role"}
    - {"type":"codeblock","language":"","content":"{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"Statement1\",\n      \"Effect\": \"Allow\",\n      \"Principal\": {\n        \"Service\": \"bedrock-agentcore.amazonaws.com\"\n      },\n      \"Action\": \"sts:AssumeRole\"\n    }\n  ]\n}"}
    - {"type":"paragraph","content":"Deploy the Agent Runtime"}
    - {"type":"list","listType":"ul","items":["`<AGENT_NAME>`: A name of your choice","`<AGENT_DESCRIPTION>`: A description of your choice","`<AGENT_ROLE_ARN>`: The ARN of the IAM role created in the previous step","`<your-tavily-api-key>`: Your [Tavily API key](https://app.tavily.com/home)"]}
    - {"type":"codeblock","language":"","content":"aws bedrock-agentcore-control create-agent-runtime \\\n  --region us-east-1 \\\n  --agent-runtime-name \"<AGENT_NAME>\" \\\n  --description \"<AGENT_DESCRIPTION>\" \\\n  --agent-runtime-artifact '{\n    \"containerConfiguration\": {\n      \"containerUri\": \"709825985650.dkr.ecr.us-east-1.amazonaws.com/tavily/tavily-mcp:v6\"\n    }\n  }' \\\n  --role-arn \"<AGENT_ROLE_ARN>\" \\\n  --network-configuration '{\n    \"networkMode\": \"PUBLIC\"\n  }' \\\n  --protocol-configuration '{\n    \"serverProtocol\": \"MCP\"\n  }' \\\n  --environment-variables '{\n    \"TAVILY_API_KEY\": \"<your-tavily-api-key>\"\n  }'"}
    - {"type":"codeblock","language":"","content":"{\n  \"agentRuntimeArn\": \"...\",\n  \"workloadIdentityDetails\": {\n    \"workloadIdentityArn\": \"...\"\n  },\n  \"agentRuntimeId\": \"...\",\n  \"agentRuntimeVersion\": \"...\",\n  \"createdAt\": \"...\",\n  \"status\": \"...\"\n}"}
    - {"type":"paragraph","content":"Invoke the Agent Runtime"}
    - {"type":"codeblock","language":"","content":"export PAYLOAD='{ \"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"tools/list\",\n  \"params\": { \"_meta\": { \"progressToken\": 1 }}}'\n\naws bedrock-agentcore invoke-agent-runtime \\\n  --agent-runtime-arn \"<AGENT_RUNTIME_ARN>\" \\\n  --content-type \"application/json\" \\\n  --accept \"application/json, text/event-stream\" \\\n  --payload \"$(echo -n \"$PAYLOAD\" | base64)\" output.json"}
    - {"type":"codeblock","language":"","content":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_search\",\n    \"arguments\": { \"query\": \"latest AI news\", \"max_results\": 10 }\n  }\n}"}
    - {"type":"codeblock","language":"","content":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_extract\",\n    \"arguments\": { \"urls\": [\"www.tavily.com\"] }\n  }\n}"}
    - {"type":"codeblock","language":"","content":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_crawl\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
    - {"type":"codeblock","language":"","content":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_map\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/documentation/partnerships/amazon#resources)Resources"}
    - {"type":"list","listType":"ul","items":["[Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)","[AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)","[Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)","[Tavily API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)"]}
  paragraphs:
    - "Subscribe on the AWS Marketplace"
    - "Select Amazon Bedrock AgentCore"
    - "Create an IAM Role"
    - "Deploy the Agent Runtime"
    - "Invoke the Agent Runtime"
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Tavily MCP Server](https://docs.tavily.com/documentation/mcp)"]}
    - {"type":"ul","items":["[Tavily Agent Skills](https://docs.tavily.com/documentation/agent-skills)"]}
    - {"type":"ul","items":["[Tavily CLI](https://docs.tavily.com/documentation/tavily-cli)"]}
    - {"type":"ul","items":["[Databricks](https://docs.tavily.com/documentation/partnerships/databricks)","[Amazon Bedrock AgentCore](https://docs.tavily.com/documentation/partnerships/amazon)","[Microsoft Azure](https://docs.tavily.com/documentation/partnerships/azure)","[IBM watsonx Orchestrate](https://docs.tavily.com/documentation/partnerships/ibm)","[Snowflake](https://docs.tavily.com/documentation/partnerships/snowflake)"]}
    - {"type":"ul","items":["[LangChain](https://docs.tavily.com/documentation/integrations/langchain)","[Vercel AI SDK](https://docs.tavily.com/documentation/integrations/vercel)","[LlamaIndex](https://docs.tavily.com/documentation/integrations/llamaindex)","[OpenAI](https://docs.tavily.com/documentation/integrations/openai)","[Google ADK](https://docs.tavily.com/documentation/integrations/google-adk)","[Anthropic](https://docs.tavily.com/documentation/integrations/anthropic)","[n8n](https://docs.tavily.com/documentation/integrations/n8n)","[Make](https://docs.tavily.com/documentation/integrations/make)","[OpenAI Agent Builder](https://docs.tavily.com/documentation/integrations/agent-builder)","[Langflow](https://docs.tavily.com/documentation/integrations/langflow)","[Zapier](https://docs.tavily.com/documentation/integrations/zapier)","[Tines](https://docs.tavily.com/documentation/integrations/tines)","[Dify](https://docs.tavily.com/documentation/integrations/dify)","[Composio](https://docs.tavily.com/documentation/integrations/composio)","[Agno](https://docs.tavily.com/documentation/integrations/agno)","[Pydantic AI](https://docs.tavily.com/documentation/integrations/pydantic-ai)","[FlowiseAI](https://docs.tavily.com/documentation/integrations/flowise)","[CrewAI](https://docs.tavily.com/documentation/integrations/crewai)","[StackAI](https://docs.tavily.com/documentation/integrations/stackai)"]}
    - {"type":"ul","items":["[Overview](https://docs.tavily.com/documentation/partnerships/amazon#overview)","[Prerequisites](https://docs.tavily.com/documentation/partnerships/amazon#prerequisites)","[Setup](https://docs.tavily.com/documentation/partnerships/amazon#setup)","[Resources](https://docs.tavily.com/documentation/partnerships/amazon#resources)"]}
    - {"type":"ul","items":["[AWS account](https://aws.amazon.com/)","[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and [configured](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)","[Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP Server","An IAM role with a trust policy allowing bedrock-agentcore.amazonaws.com to assume the role"]}
    - {"type":"ul","items":["<AGENT_NAME>: A name of your choice","<AGENT_DESCRIPTION>: A description of your choice","<AGENT_ROLE_ARN>: The ARN of the IAM role created in the previous step","<your-tavily-api-key>: Your [Tavily API key](https://app.tavily.com/home)"]}
    - {"type":"ul","items":["[Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)","[AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)","[Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)","[Tavily API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"json","code":"{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"Statement1\",\n      \"Effect\": \"Allow\",\n      \"Principal\": {\n        \"Service\": \"bedrock-agentcore.amazonaws.com\"\n      },\n      \"Action\": \"sts:AssumeRole\"\n    }\n  ]\n}"}
    - {"language":"json","code":"{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"Statement1\",\n      \"Effect\": \"Allow\",\n      \"Principal\": {\n        \"Service\": \"bedrock-agentcore.amazonaws.com\"\n      },\n      \"Action\": \"sts:AssumeRole\"\n    }\n  ]\n}"}
    - {"language":"text","code":"aws bedrock-agentcore-control create-agent-runtime \\\n  --region us-east-1 \\\n  --agent-runtime-name \"<AGENT_NAME>\" \\\n  --description \"<AGENT_DESCRIPTION>\" \\\n  --agent-runtime-artifact '{\n    \"containerConfiguration\": {\n      \"containerUri\": \"709825985650.dkr.ecr.us-east-1.amazonaws.com/tavily/tavily-mcp:v6\"\n    }\n  }' \\\n  --role-arn \"<AGENT_ROLE_ARN>\" \\\n  --network-configuration '{\n    \"networkMode\": \"PUBLIC\"\n  }' \\\n  --protocol-configuration '{\n    \"serverProtocol\": \"MCP\"\n  }' \\\n  --environment-variables '{\n    \"TAVILY_API_KEY\": \"<your-tavily-api-key>\"\n  }'"}
    - {"language":"text","code":"aws bedrock-agentcore-control create-agent-runtime \\\n  --region us-east-1 \\\n  --agent-runtime-name \"<AGENT_NAME>\" \\\n  --description \"<AGENT_DESCRIPTION>\" \\\n  --agent-runtime-artifact '{\n    \"containerConfiguration\": {\n      \"containerUri\": \"709825985650.dkr.ecr.us-east-1.amazonaws.com/tavily/tavily-mcp:v6\"\n    }\n  }' \\\n  --role-arn \"<AGENT_ROLE_ARN>\" \\\n  --network-configuration '{\n    \"networkMode\": \"PUBLIC\"\n  }' \\\n  --protocol-configuration '{\n    \"serverProtocol\": \"MCP\"\n  }' \\\n  --environment-variables '{\n    \"TAVILY_API_KEY\": \"<your-tavily-api-key>\"\n  }'"}
    - {"language":"json","code":"{\n  \"agentRuntimeArn\": \"...\",\n  \"workloadIdentityDetails\": {\n    \"workloadIdentityArn\": \"...\"\n  },\n  \"agentRuntimeId\": \"...\",\n  \"agentRuntimeVersion\": \"...\",\n  \"createdAt\": \"...\",\n  \"status\": \"...\"\n}"}
    - {"language":"json","code":"{\n  \"agentRuntimeArn\": \"...\",\n  \"workloadIdentityDetails\": {\n    \"workloadIdentityArn\": \"...\"\n  },\n  \"agentRuntimeId\": \"...\",\n  \"agentRuntimeVersion\": \"...\",\n  \"createdAt\": \"...\",\n  \"status\": \"...\"\n}"}
    - {"language":"text","code":"export PAYLOAD='{ \"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"tools/list\",\n  \"params\": { \"_meta\": { \"progressToken\": 1 }}}'\n\naws bedrock-agentcore invoke-agent-runtime \\\n  --agent-runtime-arn \"<AGENT_RUNTIME_ARN>\" \\\n  --content-type \"application/json\" \\\n  --accept \"application/json, text/event-stream\" \\\n  --payload \"$(echo -n \"$PAYLOAD\" | base64)\" output.json"}
    - {"language":"text","code":"export PAYLOAD='{ \"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"tools/list\",\n  \"params\": { \"_meta\": { \"progressToken\": 1 }}}'\n\naws bedrock-agentcore invoke-agent-runtime \\\n  --agent-runtime-arn \"<AGENT_RUNTIME_ARN>\" \\\n  --content-type \"application/json\" \\\n  --accept \"application/json, text/event-stream\" \\\n  --payload \"$(echo -n \"$PAYLOAD\" | base64)\" output.json"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_search\",\n    \"arguments\": { \"query\": \"latest AI news\", \"max_results\": 10 }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_search\",\n    \"arguments\": { \"query\": \"latest AI news\", \"max_results\": 10 }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_extract\",\n    \"arguments\": { \"urls\": [\"www.tavily.com\"] }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_extract\",\n    \"arguments\": { \"urls\": [\"www.tavily.com\"] }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_crawl\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_crawl\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_map\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
    - {"language":"json","code":"{\n  \"jsonrpc\": \"2.0\",\n  \"id\": \"1\",\n  \"method\": \"tools/call\",\n  \"params\": {\n    \"name\": \"tavily_map\",\n    \"arguments\": { \"url\": \"www.tavily.com\" }\n  }\n}"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/5NP947bTr_pJ-R0f/images/partnerships/aws/tavilymcppurchase.gif?s=af9c9d2acf4c3a844b038fe441edee68","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_3.gif","alt":"Tavily MCP Server listing on the AWS Marketplace","title":""}
    - {"src":"https://mintcdn.com/tavilyai/5NP947bTr_pJ-R0f/images/partnerships/aws/launchpage.gif?s=5502a869711cfbaa9d8d445669f44157","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_4.gif","alt":"Select Amazon Bedrock AgentCore as the deployment target","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_5.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_6.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_7.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_8.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
    - {"src":"https://mintcdn.com/tavilyai/5NP947bTr_pJ-R0f/images/partnerships/aws/launchpage.gif?s=5502a869711cfbaa9d8d445669f44157","localPath":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_9.gif","alt":"Select Amazon Bedrock AgentCore as the deployment target","title":""}
  charts:
    - {"type":"svg","index":1,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":15,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_15.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":17,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_17.png","width":12,"height":12}
    - {"type":"svg","index":18,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_22.png","width":14,"height":12}
    - {"type":"svg","index":23,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_23.png","width":14,"height":12}
    - {"type":"svg","index":24,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_24.png","width":14,"height":12}
    - {"type":"svg","index":25,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_25.png","width":14,"height":12}
    - {"type":"svg","index":27,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_27.png","width":14,"height":12}
    - {"type":"svg","index":29,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_29.png","width":14,"height":12}
    - {"type":"svg","index":30,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_32.png","width":14,"height":12}
    - {"type":"svg","index":33,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_33.png","width":16,"height":16}
    - {"type":"svg","index":34,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_35.png","width":16,"height":16}
    - {"type":"svg","index":36,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_37.png","width":14,"height":12}
    - {"type":"svg","index":38,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_38.png","width":16,"height":16}
    - {"type":"svg","index":39,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_41.png","width":16,"height":16}
    - {"type":"svg","index":42,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_44.png","width":16,"height":16}
    - {"type":"svg","index":45,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_48.png","width":14,"height":12}
    - {"type":"svg","index":49,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_49.png","width":14,"height":14}
    - {"type":"svg","index":50,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_50.png","width":14,"height":14}
    - {"type":"svg","index":51,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_51.png","width":14,"height":14}
    - {"type":"svg","index":56,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_56.png","width":20,"height":20}
    - {"type":"svg","index":57,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_57.png","width":20,"height":20}
    - {"type":"svg","index":58,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_58.png","width":20,"height":20}
    - {"type":"svg","index":59,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_59.png","width":20,"height":20}
    - {"type":"svg","index":60,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_60.png","width":49,"height":14}
    - {"type":"svg","index":61,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_61.png","width":16,"height":16}
    - {"type":"svg","index":62,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_62.png","width":16,"height":16}
    - {"type":"svg","index":63,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_63.png","width":16,"height":16}
    - {"type":"svg","index":73,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_73.png","width":16,"height":16}
    - {"type":"svg","index":74,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_74.png","width":14,"height":14}
    - {"type":"svg","index":75,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_75.png","width":16,"height":16}
    - {"type":"svg","index":76,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_76.png","width":12,"height":12}
    - {"type":"svg","index":77,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_77.png","width":14,"height":14}
    - {"type":"svg","index":78,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_78.png","width":16,"height":16}
    - {"type":"svg","index":79,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_79.png","width":12,"height":12}
    - {"type":"svg","index":80,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_80.png","width":14,"height":14}
    - {"type":"svg","index":81,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_82.png","width":12,"height":12}
    - {"type":"svg","index":83,"filename":"Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_83.png","width":14,"height":14}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "article"
    confidence: 45
    signals:
      - "article-like"
      - "api-doc-like"
  tabsAndDropdowns: []
  dateFilters: []
---

# Amazon Bedrock AgentCore

## 源URL

https://docs.tavily.com/documentation/partnerships/amazon

## 描述

Integrate Tavily MCP Server with Amazon Bedrock AgentCore for scalable AI agent deployment on AWS.

## 内容

### Overview

### Prerequisites

- [AWS account](https://aws.amazon.com/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and [configured](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)
- [Tavily API Key](https://app.tavily.com/home) for authenticating the Tavily MCP Server
- An IAM role with a trust policy allowing `bedrock-agentcore.amazonaws.com` to assume the role

### Setup

Subscribe on the AWS Marketplace

Select Amazon Bedrock AgentCore

Create an IAM Role

```text
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Deploy the Agent Runtime

- `<AGENT_NAME>`: A name of your choice
- `<AGENT_DESCRIPTION>`: A description of your choice
- `<AGENT_ROLE_ARN>`: The ARN of the IAM role created in the previous step
- `<your-tavily-api-key>`: Your [Tavily API key](https://app.tavily.com/home)

```text
aws bedrock-agentcore-control create-agent-runtime \
  --region us-east-1 \
  --agent-runtime-name "<AGENT_NAME>" \
  --description "<AGENT_DESCRIPTION>" \
  --agent-runtime-artifact '{
    "containerConfiguration": {
      "containerUri": "709825985650.dkr.ecr.us-east-1.amazonaws.com/tavily/tavily-mcp:v6"
    }
  }' \
  --role-arn "<AGENT_ROLE_ARN>" \
  --network-configuration '{
    "networkMode": "PUBLIC"
  }' \
  --protocol-configuration '{
    "serverProtocol": "MCP"
  }' \
  --environment-variables '{
    "TAVILY_API_KEY": "<your-tavily-api-key>"
  }'
```

```text
{
  "agentRuntimeArn": "...",
  "workloadIdentityDetails": {
    "workloadIdentityArn": "..."
  },
  "agentRuntimeId": "...",
  "agentRuntimeVersion": "...",
  "createdAt": "...",
  "status": "..."
}
```

Invoke the Agent Runtime

```text
export PAYLOAD='{ "jsonrpc": "2.0", "id": 1, "method": "tools/list",
  "params": { "_meta": { "progressToken": 1 }}}'

aws bedrock-agentcore invoke-agent-runtime \
  --agent-runtime-arn "<AGENT_RUNTIME_ARN>" \
  --content-type "application/json" \
  --accept "application/json, text/event-stream" \
  --payload "$(echo -n "$PAYLOAD" | base64)" output.json
```

```text
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "tavily_search",
    "arguments": { "query": "latest AI news", "max_results": 10 }
  }
}
```

```text
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "tavily_extract",
    "arguments": { "urls": ["www.tavily.com"] }
  }
}
```

```text
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "tavily_crawl",
    "arguments": { "url": "www.tavily.com" }
  }
}
```

```text
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "tavily_map",
    "arguments": { "url": "www.tavily.com" }
  }
}
```

### Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-toolkit.html)
- [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Tavily MCP Documentation](https://docs.tavily.com/documentation/mcp)
- [Tavily API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)

## 图片

![light logo](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_1.svg)

![dark logo](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_2.svg)

![Tavily MCP Server listing on the AWS Marketplace](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_3.gif)

![Select Amazon Bedrock AgentCore as the deployment target](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_4.gif)

![light logo](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_5.svg)

![dark logo](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_6.svg)

![tavily-logo](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_7.png)

![Powered by Onetrust](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_8.svg)
*Powered by OneTrust Opens in a new Tab*

![Select Amazon Bedrock AgentCore as the deployment target](Amazon_Bedrock_AgentCore_-_Tavily_Docs/image_9.gif)

## 图表

![SVG图表 1](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 15](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_15.png)
*尺寸: 16x16px*

![SVG图表 16](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 17](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_17.png)
*尺寸: 12x12px*

![SVG图表 18](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 22](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_22.png)
*尺寸: 14x12px*

![SVG图表 23](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_23.png)
*尺寸: 14x12px*

![SVG图表 24](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_24.png)
*尺寸: 14x12px*

![SVG图表 25](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_25.png)
*尺寸: 14x12px*

![SVG图表 27](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_27.png)
*尺寸: 14x12px*

![SVG图表 29](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_29.png)
*尺寸: 14x12px*

![SVG图表 30](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 32](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_32.png)
*尺寸: 14x12px*

![SVG图表 33](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_33.png)
*尺寸: 16x16px*

![SVG图表 34](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_35.png)
*尺寸: 16x16px*

![SVG图表 36](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_37.png)
*尺寸: 14x12px*

![SVG图表 38](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_38.png)
*尺寸: 16x16px*

![SVG图表 39](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_41.png)
*尺寸: 16x16px*

![SVG图表 42](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_44.png)
*尺寸: 16x16px*

![SVG图表 45](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_48.png)
*尺寸: 14x12px*

![SVG图表 49](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_49.png)
*尺寸: 14x14px*

![SVG图表 50](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_50.png)
*尺寸: 14x14px*

![SVG图表 51](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_51.png)
*尺寸: 14x14px*

![SVG图表 56](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_56.png)
*尺寸: 20x20px*

![SVG图表 57](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_57.png)
*尺寸: 20x20px*

![SVG图表 58](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_58.png)
*尺寸: 20x20px*

![SVG图表 59](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_59.png)
*尺寸: 20x20px*

![SVG图表 60](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_60.png)
*尺寸: 49x14px*

![SVG图表 61](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_61.png)
*尺寸: 16x16px*

![SVG图表 62](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_62.png)
*尺寸: 16x16px*

![SVG图表 63](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_63.png)
*尺寸: 16x16px*

![SVG图表 73](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_73.png)
*尺寸: 16x16px*

![SVG图表 74](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_74.png)
*尺寸: 14x14px*

![SVG图表 75](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_75.png)
*尺寸: 16x16px*

![SVG图表 76](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_76.png)
*尺寸: 12x12px*

![SVG图表 77](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_77.png)
*尺寸: 14x14px*

![SVG图表 78](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_78.png)
*尺寸: 16x16px*

![SVG图表 79](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_79.png)
*尺寸: 12x12px*

![SVG图表 80](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_80.png)
*尺寸: 14x14px*

![SVG图表 81](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_82.png)
*尺寸: 12x12px*

![SVG图表 83](Amazon_Bedrock_AgentCore_-_Tavily_Docs/svg_83.png)
*尺寸: 14x14px*
