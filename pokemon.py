import requests


def get_pokemon(pokemon: str | int) -> dict:
    """
    Busca informações de um Pokémon na PokéAPI.

    Args:
        pokemon: Nome ou ID do Pokémon (ex: "pikachu" ou 25)

    Returns:
        Dicionário com os dados do Pokémon

    Raises:
        ValueError: Se o Pokémon não for encontrado
        requests.HTTPError: Para outros erros HTTP
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{str(pokemon).lower()}"
    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError(f"Pokémon '{pokemon}' não encontrado.")

    response.raise_for_status()
    return response.json()


def print_pokemon_info(data: dict) -> None:
    """Exibe as informações principais de um Pokémon."""
    name = data["name"].capitalize()
    pokemon_id = data["id"]
    height = data["height"] / 10  # decímetros → metros
    weight = data["weight"] / 10  # hectogramas → kg
    types = [t["type"]["name"] for t in data["types"]]
    abilities = [a["ability"]["name"] for a in data["abilities"]]

    print(f"Nome:        {name}")
    print(f"ID:          #{pokemon_id}")
    print(f"Tipos:       {', '.join(types)}")
    print(f"Altura:      {height} m")
    print(f"Peso:        {weight} kg")
    print(f"Habilidades: {', '.join(abilities)}")


if __name__ == "__main__":
    import sys

    pokemon = sys.argv[1] if len(sys.argv) > 1 else "pikachu"

    try:
        data = get_pokemon(pokemon)
        print_pokemon_info(data)
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)
