import os
import re
import time

import requests
from requests.auth import HTTPBasicAuth

def check_response_status(response, url):
    if response.status_code != 200:
        print(f'{url} didn\'t give a 200 response', response.status_code)

username = os.getenv('ATLASSIAN_USER')
token = os.getenv('ATLASSIAN_API_TOKEN')
space_key = os.getenv('ATLASSIAN_SPACE_KEY')
auth = HTTPBasicAuth(username, token)

# Get the space_id
url = f'https://erasmus.atlassian.net/wiki/rest/api/space/{space_key}'
response = requests.get(url=url, auth=auth, headers={'Accept': 'application/json'})
check_response_status(response, url)
space_id = response.json()['id']

# Get all pages in the space
url = 'https://erasmus.atlassian.net/wiki/api/v2/pages'
response = requests.get(url=url, auth=auth, params={'space-id': space_id, 'limit': 250}, headers={'Accept': 'application/json'})
pageIds = []
check_response_status(response, url)
for pageId in response.json()['results']:
    if pageId['title'] != '':
        pageIds.append([pageId['id'], re.sub(r'[^\w\s\-\.\_]', ' ', pageId['title'])])

# Loop through all pages and download the pdf file into the app
for pageId in pageIds:
    print(pageId[1])

    # Get the task and cloud id's for generating the pdf link
    url = 'https://erasmus.atlassian.net/wiki/spaces/flyingpdf/pdfpageexport.action'
    response = requests.get(url=url, auth=auth, params={'pageId': pageId[0]}, headers={'X-Atlassian-Token': 'no-check'})
    check_response_status(response, url)

    # Define the regex patterns
    task_id_pattern = re.compile(r'<meta name="ajs-taskId" content="([^"]+)">')
    cloud_id_pattern = re.compile(r'<meta name="ajs-cloud-id" content="([^"]+)">')

    # Search for the patterns in the response text
    match_task_id = task_id_pattern.search(response.text)
    match_cloud_id = cloud_id_pattern.search(response.text)

    # Extract the matched groups
    task_id = match_task_id.group(1) if match_task_id else None
    cloud_id = match_cloud_id.group(1) if match_cloud_id else None

    # Get the download url
    url = 'https://erasmus.atlassian.net/wiki/services/api/v1/download/pdf'
    response = requests.get(url=url, auth=auth, params={'taskId': task_id, 'cloudId': cloud_id},
                            headers={'Accept': 'application/json'})
    check_response_status(response, url)
    download_url = response.text

    # Check the progress of the pdf generation, and repeat until 100% generated
    url = f'https://erasmus.atlassian.net/wiki/services/api/v1/task/{task_id}/progress'
    response = requests.get(url=url, auth=auth, headers={'Accept': 'application/json'})
    check_response_status(response, url)
    while response.json()['progress'] < 100:
        # Wait until the pdf has been generated
        print(response.json()['progress'])
        time.sleep(2)
        response = requests.get(url=url, auth=auth, headers={'Accept': 'application/json'})

    # Download the pdf's
    pdf_content = requests.get(url=download_url, headers={'Accept': 'application/json'})
    check_response_status(response, url)
    with open(f"data/QM/{pageId[1]}.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_content.content)

print('success')