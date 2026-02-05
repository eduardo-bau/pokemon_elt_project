# Pokemon ELT Pipeline

A complete ELT (Extract, Load, Transform) pipeline using PokeAPI as a data source, DuckDB as the data warehouse, and dbt for transformations.

## Architecture

```
PokeAPI → Python Extractor → DuckDB (Raw) → dbt → DuckDB (Analytics)
```

### Pipeline Phases

1. **Extract (Python)**: Fetches Pokemon data from PokeAPI
2. **Load (Python + DuckDB)**: Loads raw data into DuckDB tables
3. **Transform (dbt)**: Creates staging and mart models for analytics

## Project Structure

```
pokemon_elt/
├── data/                           # DuckDB database file
│   └── pokemon.duckdb
├── extract/                        # Extraction scripts
│   └── extract_pokemon.py         # Main extraction script
├── transform/                      # dbt project
│   └── pokemon_dbt/
│       ├── models/
│       │   ├── staging/           # Staging models (views)
│       │   │   ├── stg_pokemon.sql
│       │   │   ├── stg_pokemon_types.sql
│       │   │   ├── stg_pokemon_abilities.sql
│       │   │   ├── stg_pokemon_stats.sql
│       │   │   └── sources.yml
│       │   └── marts/             # Analytics models (tables)
│       │       ├── fct_pokemon.sql
│       │       ├── dim_type_analysis.sql
│       │       ├── fct_stat_rankings.sql
│       │       └── schema.yml
│       ├── dbt_project.yml
│       └── profiles.yml
├── requirements.txt
├── run_pipeline.py                 # Pipeline orchestrator
└── README.md
```

## Prerequisites

- Python 3.8+
- pip

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation**:
   ```bash
   python extract/extract_pokemon.py --help
   dbt --version
   ```

## Usage

### Run Complete Pipeline

```bash
python run_pipeline.py
```

This will:
1. Extract Pokemon data from PokeAPI
2. Load into DuckDB raw tables
3. Run dbt transformations
4. Run dbt tests
5. Generate documentation

### Run Individual Phases

**Extract only**:
```bash
python extract/extract_pokemon.py
```

**Transform only** (requires extracted data):
```bash
cd transform/pokemon_dbt
dbt run
dbt test
```

**Skip phases**:
```bash
# Skip extraction (use existing data)
python run_pipeline.py --skip-extract

# Skip transformation
python run_pipeline.py --skip-transform
```

## Data Models

### Raw Layer (schema: `raw`)

- `raw.pokemon` - Base Pokemon information
- `raw.pokemon_types` - Pokemon type mappings
- `raw.pokemon_abilities` - Pokemon abilities
- `raw.pokemon_stats` - Pokemon base stats

### Staging Layer (schema: `staging`)

- `stg_pokemon` - Cleaned Pokemon with calculated metrics (height_meters, weight_kg, BMI)
- `stg_pokemon_types` - Cleaned type data
- `stg_pokemon_abilities` - Cleaned ability data
- `stg_pokemon_stats` - Cleaned stats data

### Marts Layer (schema: `marts`)

- `fct_pokemon` - Complete Pokemon fact table with all stats pivoted
- `dim_type_analysis` - Analysis by Pokemon type
- `fct_stat_rankings` - Pokemon ranked by individual stats with tiers

## Example Queries

### Top 10 Strongest Pokemon (by total stats)
```sql
SELECT 
    pokemon_name,
    primary_type,
    secondary_type,
    total_stats,
    attack,
    defense
FROM marts.fct_pokemon
ORDER BY total_stats DESC
LIMIT 10;
```

### Type Distribution
```sql
SELECT 
    type_name,
    pokemon_count,
    avg_weight_kg,
    avg_height_meters
FROM marts.dim_type_analysis
ORDER BY pokemon_count DESC;
```

### Top Attackers
```sql
SELECT 
    pokemon_name,
    stat_name,
    base_stat,
    stat_rank,
    stat_tier
FROM marts.fct_stat_rankings
WHERE stat_name = 'attack'
ORDER BY stat_rank
LIMIT 10;
```

### Dual-Type Pokemon
```sql
SELECT 
    pokemon_name,
    primary_type,
    secondary_type,
    total_stats
FROM marts.fct_pokemon
WHERE secondary_type IS NOT NULL
ORDER BY total_stats DESC;
```

## dbt Documentation

Generate and serve documentation:

```bash
cd transform/pokemon_dbt
dbt docs generate
dbt docs serve
```

Then open http://localhost:8080 in your browser.

## Configuration

### Modify Number of Pokemon

Edit `extract/extract_pokemon.py`:

```python
# Extract all available Pokemon
extractor.run_extraction(limit=1000)

# Extract only first generation (151)
extractor.run_extraction(limit=151)
```

### Change Database Location

Edit `transform/pokemon_dbt/profiles.yml`:

```yaml
pokemon_dbt:
  outputs:
    dev:
      type: duckdb
      path: '/path/to/your/pokemon.duckdb'
```

## Testing

Run dbt tests to validate data quality:

```bash
cd transform/pokemon_dbt
dbt test
```

Tests include:
- Uniqueness checks
- Not null validations
- Referential integrity

## Troubleshooting

### API Rate Limiting

If you hit rate limits, increase the delay:

```python
extractor.run_extraction(limit=151, delay=0.5)  # 500ms delay
```

### DuckDB Connection Issues

Ensure the database path is correct and accessible:

```bash
# Check database file
ls -la data/pokemon.duckdb

# Connect manually
duckdb data/pokemon.duckdb
```

### dbt Errors

Check dbt debug output:

```bash
cd transform/pokemon_dbt
dbt debug
```

## Performance

- **Extraction**: ~2-3 minutes for 151 Pokemon
- **Transformation**: <10 seconds for all models
- **Total Pipeline**: ~3-4 minutes

## Future Enhancements

- [ ] Incremental loads for large datasets
- [ ] Add more Pokemon attributes (moves, evolution chains)
- [ ] Create data quality dashboard
- [ ] Add CI/CD with GitHub Actions
- [ ] Implement SCD Type 2 for historical tracking
- [ ] Add more advanced analytics (type effectiveness, team building)

## License

MIT

## Resources

- [PokeAPI Documentation](https://pokeapi.co/docs/v2)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
