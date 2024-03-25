import requests
from datetime import datetime, timedelta

data_provider_url = "http://localhost:8000/api/events/"
end_of_yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
start_of_yesterday = end_of_yesterday - timedelta(days=1)

params = {
        'updated__gte': start_of_yesterday.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'updated__lt': end_of_yesterday.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
response = requests.get(data_provider_url, params=params)
print(response.json(), response.status_code)
