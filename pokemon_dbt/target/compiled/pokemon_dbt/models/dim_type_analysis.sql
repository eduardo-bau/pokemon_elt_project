

with pokemon_types as (
    select * from "pokemon"."main"."stg_pokemon_types"
),

pokemon_base as (
    select * from "pokemon"."main"."stg_pokemon"
),

type_stats as (
    select
        pt.type_name,
        count(distinct pt.pokemon_id) as pokemon_count,
        avg(p.weight_kg) as avg_weight_kg,
        avg(p.height_meters) as avg_height_meters,
        avg(p.base_experience) as avg_base_experience
    from pokemon_types pt
    join pokemon_base p on pt.pokemon_id = p.pokemon_id
    group by pt.type_name
)

select
    type_name,
    pokemon_count,
    round(avg_weight_kg, 2) as avg_weight_kg,
    round(avg_height_meters, 2) as avg_height_meters,
    round(avg_base_experience, 2) as avg_base_experience,
    current_timestamp as transformed_at
from type_stats
order by pokemon_count desc