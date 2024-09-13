# #example 1
# from master import call_for_rest_fetch, PaginatedFetcher

# def main():
#     # Test with a different paginated API (JSONPlaceholder mock API)
#     api_url = "https://jsonplaceholder.typicode.com/posts"  # A mock API with pagination

#     output_csv = "output_paginated_new.csv"

#     call_for_rest_fetch(
#         fetcher_class=PaginatedFetcher,
#         url=api_url,
#         filename=output_csv,
#         headers=None,
#         access_token=None,
#         page_param='_page',  # JSONPlaceholder uses '_page' for pagination
#         per_page=10,         # Limit to 10 results per page
#         data_key=None        # The response is directly the data, no need for 'data_key'
#     )

# if __name__ == "__main__":
#     main()


#example 2
from master import call_for_rest_fetch, PaginatedFetcher

def main():
    api_url = "https://swapi.dev/api/people/"  # SWAPI for people data

    output_csv = "output_starwars_paginated.csv"

    call_for_rest_fetch(
        fetcher_class=PaginatedFetcher,
        url=api_url,
        filename=output_csv,
        headers=None,
        access_token=None,
        page_param='page',  # SWAPI uses 'page' for pagination
        per_page=10,        # SWAPI doesn't use 'per_page', but setting to 10 as default
        data_key='results'  # SWAPI returns data under 'results'
    )

if __name__ == "__main__":
    main()
