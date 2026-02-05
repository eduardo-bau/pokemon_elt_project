
  
  create view "pokemon"."main"."stg_pokemon_stats__dbt_tmp" as (
    

with source_stats as (
    select * from "pokemon"."raw"."pokemon_stats"
),

cleaned as (
    select
        pokemon_id,
        pokemon_name,
        stat_name,
        base_stat,
        effort,
        extracted_at
    from source_stats
)

select * from cleaned
  );
