from scrapegraph_py import Client 
from scrapegraph_py.logger import sgai_logger 

sgai_logger.set_logging(level = "INFO")

#initialize the client
sgai_client = Client(api_key = '')

#facebook profile url 
fb_profile_url = '[ADD URL HERE]'

#adding fb profile scrapper request
response = sgai_client.smartscraper(
    website_url = fb_profile_url, 
    user_prompt = "Extract the main profile available information such as Name, Gender, Email etc"
)

print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()