# Pokemon Analysis Notebook
# This script demonstrates how to query the transformed data

import duckdb

# Connect to the database
conn = duckdb.connect('data/pokemon.duckdb')

print("="*70)
print("POKEMON ELT PIPELINE - DATA ANALYSIS")
print("="*70)

# Query 1: Top 10 Strongest Pokemon
print("\n1. TOP 10 STRONGEST POKEMON (by total stats)")
print("-"*70)
result = conn.execute("""
    SELECT 
        pokemon_name,
        primary_type,
        secondary_type,
        total_stats,
        attack,
        defense,
        speed
    FROM fct_pokemon
    ORDER BY total_stats DESC
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]:15} | {row[1]:10} | {row[2] or 'None':10} | Total: {row[3]:3} | Atk: {row[4]:3} | Def: {row[5]:3} | Spd: {row[6]:3}")

# Query 2: Type Distribution
print("\n2. TYPE DISTRIBUTION")
print("-"*70)
result = conn.execute("""
    SELECT 
        type_name,
        pokemon_count,
        ROUND(avg_weight_kg, 1) as avg_weight,
        ROUND(avg_height_meters, 1) as avg_height
    FROM dim_type_analysis
    ORDER BY pokemon_count DESC
""").fetchall()

for row in result:
    print(f"{row[0]:12} | Count: {row[1]:3} | Avg Weight: {row[2]:5} kg | Avg Height: {row[3]:4} m")

# Query 3: Fastest Pokemon
print("\n3. TOP 10 FASTEST POKEMON")
print("-"*70)
result = conn.execute("""
    SELECT 
        pokemon_name,
        base_stat as speed,
        stat_tier
    FROM fct_stat_rankings
    WHERE stat_name = 'speed'
    ORDER BY stat_rank
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]:15} | Speed: {row[1]:3} | {row[2]}")

# Query 4: Heaviest Pokemon by Type
print("\n4. HEAVIEST POKEMON BY TYPE")
print("-"*70)
result = conn.execute("""
    WITH ranked_pokemon AS (
        SELECT 
            primary_type,
            pokemon_name,
            weight_kg,
            ROW_NUMBER() OVER (PARTITION BY primary_type ORDER BY weight_kg DESC) as rn
        FROM fct_pokemon
    )
    SELECT 
        primary_type,
        pokemon_name,
        ROUND(weight_kg, 1) as weight_kg
    FROM ranked_pokemon
    WHERE rn = 1
    ORDER BY weight_kg DESC
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]:12} | {row[1]:15} | {row[2]:6} kg")

# Query 5: Dual Type Combinations
print("\n5. MOST COMMON DUAL-TYPE COMBINATIONS")
print("-"*70)
result = conn.execute("""
    SELECT 
        primary_type || ' / ' || secondary_type as type_combo,
        COUNT(*) as pokemon_count,
        ROUND(AVG(total_stats), 1) as avg_total_stats
    FROM fct_pokemon
    WHERE secondary_type IS NOT NULL
    GROUP BY primary_type, secondary_type
    ORDER BY pokemon_count DESC
    LIMIT 10
""").fetchall()

for row in result:
    print(f"{row[0]:25} | Count: {row[1]:2} | Avg Stats: {row[2]}")

# Query 6: Stats Summary
print("\n6. OVERALL STATISTICS")
print("-"*70)
result = conn.execute("""
    SELECT 
        COUNT(*) as total_pokemon,
        COUNT(DISTINCT primary_type) as total_types,
        ROUND(AVG(total_stats), 1) as avg_total_stats,
        MAX(total_stats) as max_total_stats,
        MIN(total_stats) as min_total_stats
    FROM fct_pokemon
""").fetchone()

print(f"Total Pokemon:     {result[0]}")
print(f"Total Types:       {result[1]}")
print(f"Avg Total Stats:   {result[2]}")
print(f"Max Total Stats:   {result[3]}")
print(f"Min Total Stats:   {result[4]}")

# Close connection
conn.close()

print("\n" + "="*70)
print("Analysis complete!")
print("="*70)
