{{
    config(
        materialized='table'
    )
}}

with pokemon_stats as (
    select * from {{ ref('stg_pokemon_stats') }}
),

pokemon_base as (
    select 
        pokemon_id,
        pokemon_name
    from {{ ref('stg_pokemon') }}
),

stat_rankings as (
    select
        ps.pokemon_id,
        p.pokemon_name,
        ps.stat_name,
        ps.base_stat,
        row_number() over (partition by ps.stat_name order by ps.base_stat desc) as stat_rank,
        median(ps.base_stat) over (partition by ps.stat_name) as median_stat,
        avg(ps.base_stat) over (partition by ps.stat_name) as avg_stat
    from pokemon_stats ps
    join pokemon_base p on ps.pokemon_id = p.pokemon_id
)

select
    pokemon_id,
    pokemon_name,
    stat_name,
    base_stat,
    stat_rank,
    round(median_stat, 2) as median_stat,
    round(avg_stat, 2) as avg_stat,
    case
        when base_stat >= avg_stat + (median_stat * 0.5) then 'Exceptional'
        when base_stat >= avg_stat then 'Above Average'
        when base_stat >= avg_stat - (median_stat * 0.5) then 'Average'
        else 'Below Average'
    end as stat_tier,
    current_timestamp as transformed_at
from stat_rankings
order by stat_name, stat_rank
