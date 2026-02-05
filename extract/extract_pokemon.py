"""
Extract Pokemon data from PokeAPI and load into DuckDB
This script extracts data from the PokeAPI and loads it into raw tables in DuckDB
"""
import requests
import duckdb
import json
from datetime import datetime
from typing import List, Dict, Any
import time


class PokeAPIExtractor:
    """Extract data from PokeAPI"""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self, db_path: str = "data/pokemon.duckdb"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._setup_raw_schema()
    
    def _setup_raw_schema(self):
        """Create raw schema and tables"""
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
        
        # Raw Pokemon table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw.pokemon (
                id INTEGER,
                name VARCHAR,
                height INTEGER,
                weight INTEGER,
                base_experience INTEGER,
                is_default BOOLEAN,
                order_num INTEGER,
                extracted_at TIMESTAMP,
                raw_data JSON
            )
        """)
        
        # Raw Pokemon Types table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw.pokemon_types (
                pokemon_id INTEGER,
                pokemon_name VARCHAR,
                type_slot INTEGER,
                type_name VARCHAR,
                extracted_at TIMESTAMP
            )
        """)
        
        # Raw Pokemon Abilities table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw.pokemon_abilities (
                pokemon_id INTEGER,
                pokemon_name VARCHAR,
                ability_slot INTEGER,
                ability_name VARCHAR,
                is_hidden BOOLEAN,
                extracted_at TIMESTAMP
            )
        """)
        
        # Raw Pokemon Stats table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw.pokemon_stats (
                pokemon_id INTEGER,
                pokemon_name VARCHAR,
                stat_name VARCHAR,
                base_stat INTEGER,
                effort INTEGER,
                extracted_at TIMESTAMP
            )
        """)
        
        print("✓ Raw schema and tables created")
    
    def extract_pokemon_list(self, limit: int = 151) -> List[str]:
        """Extract list of Pokemon URLs"""
        print(f"Fetching list of {limit} Pokemon...")
        response = requests.get(f"{self.BASE_URL}/pokemon?limit={limit}")
        response.raise_for_status()
        
        pokemon_list = response.json()['results']
        print(f"✓ Found {len(pokemon_list)} Pokemon")
        return [p['url'] for p in pokemon_list]
    
    def extract_pokemon_details(self, url: str) -> Dict[str, Any]:
        """Extract detailed Pokemon data"""
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def load_pokemon_data(self, pokemon_data: Dict[str, Any]):
        """Load Pokemon data into raw tables"""
        extracted_at = datetime.now()
        
        # Load main Pokemon data
        self.conn.execute("""
            INSERT INTO raw.pokemon VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            pokemon_data['id'],
            pokemon_data['name'],
            pokemon_data['height'],
            pokemon_data['weight'],
            pokemon_data.get('base_experience'),
            pokemon_data.get('is_default', True),
            pokemon_data.get('order'),
            extracted_at,
            json.dumps(pokemon_data)
        ])
        
        # Load Pokemon types
        for type_info in pokemon_data.get('types', []):
            self.conn.execute("""
                INSERT INTO raw.pokemon_types VALUES (?, ?, ?, ?, ?)
            """, [
                pokemon_data['id'],
                pokemon_data['name'],
                type_info['slot'],
                type_info['type']['name'],
                extracted_at
            ])
        
        # Load Pokemon abilities
        for ability_info in pokemon_data.get('abilities', []):
            self.conn.execute("""
                INSERT INTO raw.pokemon_abilities VALUES (?, ?, ?, ?, ?, ?)
            """, [
                pokemon_data['id'],
                pokemon_data['name'],
                ability_info['slot'],
                ability_info['ability']['name'],
                ability_info.get('is_hidden', False),
                extracted_at
            ])
        
        # Load Pokemon stats
        for stat_info in pokemon_data.get('stats', []):
            self.conn.execute("""
                INSERT INTO raw.pokemon_stats VALUES (?, ?, ?, ?, ?, ?)
            """, [
                pokemon_data['id'],
                pokemon_data['name'],
                stat_info['stat']['name'],
                stat_info['base_stat'],
                stat_info['effort'],
                extracted_at
            ])
    
    def run_extraction(self, limit: int = 151, delay: float = 0.1):
        """Run full extraction process"""
        print(f"\n{'='*60}")
        print("Starting Pokemon ELT Pipeline - Extract Phase")
        print(f"{'='*60}\n")
        
        # Clear existing data (full refresh)
        print("Clearing existing raw data...")
        self.conn.execute("DELETE FROM raw.pokemon")
        self.conn.execute("DELETE FROM raw.pokemon_types")
        self.conn.execute("DELETE FROM raw.pokemon_abilities")
        self.conn.execute("DELETE FROM raw.pokemon_stats")
        print("✓ Raw tables cleared\n")
        
        # Extract Pokemon list
        pokemon_urls = self.extract_pokemon_list(limit)
        
        # Extract and load each Pokemon
        print(f"\nExtracting detailed data for {len(pokemon_urls)} Pokemon...")
        for i, url in enumerate(pokemon_urls, 1):
            try:
                pokemon_data = self.extract_pokemon_details(url)
                self.load_pokemon_data(pokemon_data)
                
                if i % 10 == 0:
                    print(f"  Processed {i}/{len(pokemon_urls)} Pokemon...")
                
                # Be nice to the API
                time.sleep(delay)
                
            except Exception as e:
                print(f"  ✗ Error processing {url}: {e}")
                continue
        
        print(f"\n✓ Extraction complete! Loaded {len(pokemon_urls)} Pokemon")
        
        # Show summary
        self._print_summary()
    
    def _print_summary(self):
        """Print extraction summary"""
        print(f"\n{'='*60}")
        print("Extraction Summary")
        print(f"{'='*60}")
        
        pokemon_count = self.conn.execute("SELECT COUNT(*) FROM raw.pokemon").fetchone()[0]
        types_count = self.conn.execute("SELECT COUNT(*) FROM raw.pokemon_types").fetchone()[0]
        abilities_count = self.conn.execute("SELECT COUNT(*) FROM raw.pokemon_abilities").fetchone()[0]
        stats_count = self.conn.execute("SELECT COUNT(*) FROM raw.pokemon_stats").fetchone()[0]
        
        print(f"Pokemon:    {pokemon_count:>6}")
        print(f"Types:      {types_count:>6}")
        print(f"Abilities:  {abilities_count:>6}")
        print(f"Stats:      {stats_count:>6}")
        print(f"{'='*60}\n")
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Extract first 151 Pokemon (original generation)
    extractor = PokeAPIExtractor(db_path="~/pokemon_elt_project/data/pokemon.duckdb")
    
    try:
        extractor.run_extraction(limit=151, delay=0.1)
    finally:
        extractor.close()
    
    print("✓ Extract phase completed successfully!")
