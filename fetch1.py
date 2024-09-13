#A script commented by cgpt to understand a basic fetch and print of a simple rest api.

import requests
import csv
import os

def fetch_data_from_api(api_url):
    """
    Fetches data from the given API URL.
    Returns the data if successful, otherwise None.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def write_headers_to_csv(file_path, headers):
    """
    Writes the headers to the CSV file if it doesn't already exist.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

def write_data_to_csv(file_path, data):
    """
    Writes the data rows to the CSV file.
    Each data fragment is written as a row.
    """
    with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item.values())
                else:
                    writer.writerow([item])
        elif isinstance(data, dict):
            writer.writerow(data.values())

def process_api_data(api_url, output_csv):
    """
    Fetch data from API and write it to CSV.
    Detects headers from the data and writes it row by row.
    """
    data = fetch_data_from_api(api_url)
    
    if data:
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            headers = data[0].keys()
            if not os.path.exists(output_csv):
                write_headers_to_csv(output_csv, headers)
        elif isinstance(data, dict):
            headers = data.keys()
            if not os.path.exists(output_csv):
                write_headers_to_csv(output_csv, headers)
        
        write_data_to_csv(output_csv, data)
        print(f"Data successfully written to {output_csv}")

def main():
    """
    Main function to run the program. Defines the API URL and output CSV path.
    """
    api_url = "https://restcountries.com/v3.1/all"
    output_csv = "output_countries_api.csv"
    
    process_api_data(api_url, output_csv)

if __name__ == "__main__":
    main()
