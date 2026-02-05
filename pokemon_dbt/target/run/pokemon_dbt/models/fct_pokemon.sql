
  
    
    

    create  table
      "pokemon"."main"."fct_pokemon__dbt_tmp"
  
    as (
      

with pokemon_base as (
    select * from "pokemon"."main"."stg_pokemon"
),

pokemon_stats_pivoted as (
    select
        pokemon_id,
        max(case when stat_name = 'hp' then base_stat end) as hp,
        max(case when stat_name = 'attack' then base_stat end) as attack,
        max(case when stat_name = 'defense' then base_stat end) as defense,
        max(case when stat_name = 'special-attack' then base_stat end) as special_attack,
        max(case when stat_name = 'special-defense' then base_stat end) as special_defense,
        max(case when stat_name = 'speed' then base_stat end) as speed
    from "pokemon"."main"."stg_pokemon_stats"
    group by pokemon_id
),

pokemon_types_agg as (
    select
        pokemon_id,
        max(case when type_slot = 1 then type_name end) as primary_type,
        max(case when type_slot = 2 then type_name end) as secondary_type,
        count(*) as type_count
    from "pokemon"."main"."stg_pokemon_types"
    group by pokemon_id
),

pokemon_abilities_agg as (
    select
        pokemon_id,
        count(*) as ability_count,
        sum(case when is_hidden then 1 else 0 end) as hidden_ability_count
    from "pokemon"."main"."stg_pokemon_abilities"
    group by pokemon_id
),

final as (
    select
        p.pokemon_id,
        p.pokemon_name,
        p.height,
        p.weight,
        p.height_meters,
        p.weight_kg,
        p.bmi,
        p.base_experience,
        
        -- Types
        t.primary_type,
        t.secondary_type,
        t.type_count,
        
        -- Abilities
        a.ability_count,
        a.hidden_ability_count,
        
        -- Stats
        s.hp,
        s.attack,
        s.defense,
        s.special_attack,
        s.special_defense,
        s.speed,
        
        -- Calculated stats
        (s.hp + s.attack + s.defense + s.special_attack + s.special_defense + s.speed) as total_stats,
        
        -- Metadata
        p.extracted_at,
        current_timestamp as transformed_at
        
    from pokemon_base p
    left join pokemon_stats_pivoted s on p.pokemon_id = s.pokemon_id
    left join pokemon_types_agg t on p.pokemon_id = t.pokemon_id
    left join pokemon_abilities_agg a on p.pokemon_id = a.pokemon_id
)

select * from final
order by pokemon_id
    );
  
  