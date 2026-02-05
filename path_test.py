from pathlib import Path



project_root = Path(__file__).parent
extract_script = project_root / "extract" / "extract_pokemon.py"
dbt_project = project_root / "pokemon_dbt"


print(dbt_project)

