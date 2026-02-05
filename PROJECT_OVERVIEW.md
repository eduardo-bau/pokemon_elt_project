# Pokemon ELT Pipeline - Project Overview

## 📋 Project Summary

This is a production-ready ELT (Extract, Load, Transform) pipeline that:
- Extracts Pokemon data from the PokeAPI
- Loads it into a DuckDB data warehouse
- Transforms it using dbt for analytics

## 🏗️ Architecture

```
PokeAPI → Python → DuckDB (Raw) → dbt → DuckDB (Marts) → Analytics
```

## 📁 Project Structure

```
pokemon_elt/
├── extract/                    # Extract & Load
│   └── extract_pokemon.py     # Pulls data from PokeAPI
├── transform/                  # Transform
│   └── pokemon_dbt/           # dbt project
│       ├── models/
│       │   ├── staging/       # Cleaned views
│       │   └── marts/         # Analytics tables
│       ├── dbt_project.yml
│       └── profiles.yml
├── data/                       # Database location
│   └── pokemon.duckdb
├── run_pipeline.py            # Main orchestrator
├── analyze_data.py            # Sample queries
├── requirements.txt           # Python deps
├── Makefile                   # Shortcuts
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick start guide
└── architecture.mermaid      # Visual diagram
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Pipeline
```bash
python run_pipeline.py
```

### 3. Explore Data
```bash
python analyze_data.py
```

## 📊 Data Models

### Raw Layer (`raw` schema)
- `pokemon` - Base Pokemon data
- `pokemon_types` - Type mappings
- `pokemon_abilities` - Ability mappings
- `pokemon_stats` - Stat values

### Staging Layer (`staging` schema)
- `stg_pokemon` - Cleaned with calculations (BMI, conversions)
- `stg_pokemon_types` - Cleaned types
- `stg_pokemon_abilities` - Cleaned abilities
- `stg_pokemon_stats` - Cleaned stats

### Marts Layer (`marts` schema)
- `fct_pokemon` - Complete Pokemon fact table (pivoted stats, aggregated attributes)
- `dim_type_analysis` - Pokemon grouped by type
- `fct_stat_rankings` - Pokemon ranked by each stat

## 🔧 Key Features

✅ **Full ELT Pipeline**
- Automated extraction from PokeAPI
- Raw data storage in DuckDB
- Modular dbt transformations

✅ **Data Quality**
- dbt tests for validation
- Schema enforcement
- Referential integrity checks

✅ **Analytics Ready**
- Pre-built fact and dimension tables
- Calculated metrics (total stats, BMI, rankings)
- Optimized for queries

✅ **Documentation**
- Auto-generated dbt docs with lineage
- Comprehensive README
- Quick start guide
- Sample queries

✅ **Developer Experience**
- Makefile for common tasks
- Modular, maintainable code
- Clear separation of concerns
- Orchestration script

## 📈 Sample Queries

### Top 10 Strongest Pokemon
```sql
SELECT pokemon_name, total_stats, primary_type
FROM marts.fct_pokemon
ORDER BY total_stats DESC
LIMIT 10;
```

### Type Distribution
```sql
SELECT type_name, pokemon_count, avg_weight_kg
FROM marts.dim_type_analysis
ORDER BY pokemon_count DESC;
```

### Fastest Pokemon
```sql
SELECT pokemon_name, base_stat, stat_tier
FROM marts.fct_stat_rankings
WHERE stat_name = 'speed'
ORDER BY stat_rank
LIMIT 10;
```

## 🛠️ Technologies Used

- **Python** - Extraction & orchestration
- **DuckDB** - Embedded analytical database
- **dbt** - Data transformation framework
- **PokeAPI** - RESTful Pokemon data source

## 📝 Make Commands

```bash
make install     # Install dependencies
make extract     # Run extraction only
make transform   # Run dbt only
make run         # Run complete pipeline
make test        # Run dbt tests
make docs        # Generate and serve dbt docs
make clean       # Clean generated files
make help        # Show all commands
```

## 🎯 Use Cases

This pipeline demonstrates:

1. **ELT Best Practices**
   - Raw data preservation
   - Incremental transformations
   - Separation of concerns

2. **Data Warehousing**
   - Dimensional modeling
   - Fact and dimension tables
   - Slowly changing dimensions (ready for enhancement)

3. **Analytics Engineering**
   - dbt modeling patterns
   - Data quality testing
   - Documentation generation

4. **Real-World Skills**
   - API integration
   - SQL transformations
   - Pipeline orchestration
   - Error handling

## 🔄 Pipeline Flow

1. **Extract**: Python script calls PokeAPI endpoints
2. **Load**: Raw JSON data inserted into DuckDB tables
3. **Transform**: dbt models create cleaned views and analytical tables
4. **Test**: dbt validates data quality
5. **Document**: Auto-generated lineage and documentation

## 📦 Output

After running the pipeline, you'll have:

- **151 Pokemon** with complete attributes
- **6 types** of analysis-ready tables
- **Data quality tests** passed
- **Documentation** with full lineage
- **Sample queries** to explore data

## 🎓 Learning Outcomes

By exploring this project, you'll learn:

- How to build production ELT pipelines
- DuckDB for analytical workloads
- dbt for SQL transformations
- API data extraction patterns
- Data modeling best practices
- Pipeline orchestration

## 🚀 Next Steps

1. Run the pipeline with the quick start guide
2. Explore the data with sample queries
3. View dbt documentation for lineage
4. Modify models to add your own transformations
5. Scale to more Pokemon (up to 1000+)

## 📚 Additional Resources

- Full README with detailed documentation
- Quick start guide for immediate setup
- Architecture diagram (Mermaid format)
- Sample analysis script with queries
- Complete dbt project structure

---

**Built with ❤️ using Python, DuckDB, and dbt**
