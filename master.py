#the master script to be called as per the rest api's factors

import csv
import requests
import json
import logging
import time
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIFetcher(ABC):
    def __init__(self, url, headers=None, access_token=None, retries=3, backoff_factor=0.3):
        self.url = url
        self.headers = headers or {}
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'
        self.retries = retries
        self.backoff_factor = backoff_factor

    @abstractmethod
    def fetch_data(self):
        pass

    def make_request(self, params=None):
        """Makes an HTTP GET request with retries."""
        for attempt in range(self.retries):
            try:
                logging.info(f"Fetching data from {self.url} with params {params}, attempt {attempt + 1}")
                response = requests.get(self.url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as http_err:
                logging.error(f"HTTP error occurred: {http_err}")
            except requests.exceptions.ConnectionError as conn_err:
                logging.error(f"Connection error occurred: {conn_err}")
            except requests.exceptions.Timeout as timeout_err:
                logging.error(f"Timeout error occurred: {timeout_err}")
            except requests.exceptions.RequestException as req_err:
                logging.error(f"General error occurred: {req_err}")
            time.sleep(self.backoff_factor * (2 ** attempt))  # Exponential backoff
        logging.error(f"Failed to fetch data after {self.retries} attempts.")
        return None

class PaginatedFetcher(APIFetcher):
    def fetch_data(self, page_param='page', per_page=100, data_key=None):
        """
        General pagination logic for any REST API. Keeps fetching pages until no more data is returned.
        
        :param page_param: The parameter name for the page number.
        :param per_page: The number of items per page.
        :param data_key: Optional key to specify where the actual data is in the response.
                         If None, the response itself is assumed to be the data.
        :return: A list of all fetched data across multiple pages.
        """
        data = []
        page = 1
        while True:
            params = {page_param: page, 'per_page': per_page}
            response = self.make_request(params)
            
            if not response:  # Stop if no response
                break

            # If there's a specific data_key, use it; otherwise, assume the entire response is the data
            if data_key and data_key in response:
                fetched_data = response[data_key]
            else:
                fetched_data = response  # Assume the full response is the data
            
            if not fetched_data:  # Stop if no data is returned in the current page
                break

            data.extend(fetched_data)

            # If fewer than per_page items are returned, assume this is the last page
            if len(fetched_data) < per_page:
                break

            page += 1  # Move to the next page

        return data

class OffsetBasedFetcher(APIFetcher):
    def fetch_data(self, offset_param='offset', limit=100):
        data = []
        offset = 0
        while True:
            params = {offset_param: offset, 'limit': limit}
            response = self.make_request(params)
            if not response or 'data' not in response:
                break
            data.extend(response['data'])
            if len(response['data']) < limit:
                break
            offset += limit
        return data

class CursorBasedFetcher(APIFetcher):
    def fetch_data(self, cursor_param='cursor'):
        data = []
        cursor = None
        while True:
            params = {cursor_param: cursor} if cursor else {}
            response = self.make_request(params)
            if not response or 'data' not in response:
                break
            data.extend(response['data'])
            cursor = response.get('next_cursor')
            if not cursor:
                break
        return data

class SimpleFetcher(APIFetcher):
    def fetch_data(self):
        return self.make_request()

class LargeJSONFetcher(APIFetcher):
    def fetch_data(self, data_key='data'):
        response = self.make_request()
        if response and data_key in response:
            return response[data_key]
        return response

def flatten_json(y):
    """
    Flatten JSON object to a single level dictionary.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def write_to_csv(data, filename):
    """
    Writes data to a CSV file.
    Dynamically handles fields and nested structures.
    """
    # Determine all possible keys in the dataset for the CSV header
    all_keys = set()
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                all_keys.update(entry.keys())
    elif isinstance(data, dict):
        all_keys.update(data.keys())
    
    # Sort keys to have consistent column order
    all_keys = sorted(all_keys)
    
    # Open CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_keys)
        writer.writeheader()

        # Write data rows
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict):
                    # Write row with all fields
                    writer.writerow({key: entry.get(key, None) for key in all_keys})
        elif isinstance(data, dict):
            writer.writerow({key: data.get(key, None) for key in all_keys})


def call_for_rest_fetch(fetcher_class, url, headers=None, access_token=None, filename='output.csv', **fetcher_params):
    fetcher = fetcher_class(url, headers=headers, access_token=access_token)
    data = fetcher.fetch_data(**fetcher_params)
    if data:
        write_to_csv(data, filename)
        logging.info(f"Data successfully written to {filename}.")
    else:
        logging.error("No data fetched.")


# Example of running the script with a Paginated API
# if __name__ == "__main__":
#     call_for_rest_fetch(
#         PaginatedFetcher,
#         "https://api.example.com/data",
#         headers={"Custom-Header": "value"},
#         access_token="your_access_token",
#         filename="output.csv",
#         page_param='page',
#         per_page=50
#     )

#simple's example
def main():
    api_url = "https://restcountries.com/v3.1/all"
    
    output_csv = "output_data2.csv"
    
    call_for_rest_fetch(
        SimpleFetcher,                 # Use SimpleFetcher as there is no pagination
        url=api_url,                  # API URL
        filename=output_csv,          # Output CSV file
        headers=None,                 # No specific headers needed for this API
        access_token=None             # No access token required for this API
    )

if __name__ == "__main__":
    main()
