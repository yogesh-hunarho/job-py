import requests
import json

def test_job_search():
    url = "http://127.0.0.1:8001/api/jobs/search"
    payload = {
        "site_name": ["glassdoor"],
        "search_term": "web developer internship",
        "location": "Mumbai",
        "results_wanted": 5
    }
    
    print(f"Sending request to {url} with payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Found {data.get('count')} jobs")
        # print(json.dumps(data, indent=2))
        if data.get('count') >= 0:
             print("SUCCESS: API returned valid response structure")
        else:
             print("FAILURE: API returned invalid response structure")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response text: {e.response.text}")

if __name__ == "__main__":
    test_job_search()
