{{
    config(
        materialized='view'
    )
}}

with source_abilities as (
    select * from {{ source('raw', 'pokemon_abilities') }}
),

cleaned as (
    select
        pokemon_id,
        pokemon_name,
        ability_slot,
        ability_name,
        is_hidden,
        extracted_at
    from source_abilities
)

select * from cleaned
