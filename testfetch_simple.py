from master import call_for_rest_fetch, SimpleFetcher

def main():
    api_url = "https://restcountries.com/v3.1/all"
    
    output_csv = "output_simple.csv"
    
    call_for_rest_fetch(
        fetcher_class=SimpleFetcher,  
        url=api_url,                  
        filename=output_csv,          
        headers=None,                 # No specific headers needed for this API
        access_token=None             # No access token required for this API
    )

if __name__ == "__main__":
    main()
