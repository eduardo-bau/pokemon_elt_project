# Quick Start Guide

## Installation & Setup (5 minutes)

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   dbt --version
   python --version
   ```

## Running the Pipeline (3-5 minutes)

### Option 1: Run Everything
```bash
python run_pipeline.py
```

This will:
- Extract 151 Pokemon from PokeAPI (~2-3 minutes)
- Load data into DuckDB
- Run dbt transformations
- Run data quality tests
- Generate documentation

### Option 2: Use Make commands
```bash
# Install dependencies
make install

# Run complete pipeline
make run

# Run tests
make test

# View documentation
make docs
```

## Exploring the Data

### Option 1: Run Analysis Script
```bash
python analyze_data.py
```

### Option 2: Query Directly
```bash
duckdb data/pokemon.duckdb
```

```sql
-- Top 10 strongest Pokemon
SELECT pokemon_name, total_stats 
FROM marts.fct_pokemon 
ORDER BY total_stats DESC 
LIMIT 10;

-- Type distribution
SELECT * FROM marts.dim_type_analysis;

-- Exit
.quit
```

### Option 3: View dbt Documentation
```bash
cd transform/pokemon_dbt
dbt docs serve
```
Then open http://localhost:8080

## Understanding the Output

After running the pipeline, you'll have:

### Raw Data (schema: `raw`)
- Original data from PokeAPI
- Tables: `pokemon`, `pokemon_types`, `pokemon_abilities`, `pokemon_stats`

### Staging Models (schema: `staging`)
- Cleaned and standardized data
- Views that reference raw tables
- Calculated fields (height_meters, weight_kg, BMI)

### Analytics Models (schema: `marts`)
- `fct_pokemon` - Complete Pokemon fact table
- `dim_type_analysis` - Type-based analysis
- `fct_stat_rankings` - Stat rankings and tiers

## Next Steps

1. **Explore the data** with the analysis script
2. **Write your own queries** against the marts schema
3. **View the dbt docs** to understand the lineage
4. **Modify dbt models** to add your own transformations
5. **Add more Pokemon** by changing the limit in `extract_pokemon.py`

## Common Commands

```bash
# Run just extraction
python extract/extract_pokemon.py

# Run just dbt transformations
cd transform/pokemon_dbt && dbt run

# Run dbt tests
cd transform/pokemon_dbt && dbt test

# Clean everything
make clean

# Help
make help
```

## Troubleshooting

**No module named 'duckdb'**
```bash
pip install duckdb --break-system-packages
```

**dbt command not found**
```bash
pip install dbt-core dbt-duckdb --break-system-packages
```

**API rate limiting**
- Increase the delay in `extract_pokemon.py` (line with `time.sleep`)

## What You've Built

✅ Complete ELT pipeline  
✅ Data warehouse with DuckDB  
✅ Automated transformations with dbt  
✅ Data quality tests  
✅ Documentation  
✅ Sample analytics  

Enjoy exploring Pokemon data! 🎮
