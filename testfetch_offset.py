from master import call_for_rest_fetch, OffsetBasedFetcher

def main():
    # Test with PokeAPI which uses offset and limit for pagination
    api_url = "https://pokeapi.co/api/v2/pokemon"

    output_csv = "output_pokemon_offset.csv"

    call_for_rest_fetch(
        fetcher_class=OffsetBasedFetcher,
        url=api_url,
        filename=output_csv,
        headers=None,
        access_token=None,
        offset_param='offset',    # PokeAPI uses 'offset' for pagination
        limit_param='limit',      # PokeAPI uses 'limit' to set the number of results per page
        limit=20,                 # Fetch 20 Pokémon per request
        data_key='results'        # The response contains a 'results' key with the Pokémon data
    )

if __name__ == "__main__":
    main()
