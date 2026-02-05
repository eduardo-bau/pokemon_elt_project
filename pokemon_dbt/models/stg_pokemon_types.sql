{{
    config(
        materialized='view'
    )
}}

with source_types as (
    select * from {{ source('raw', 'pokemon_types') }}
),

cleaned as (
    select
        pokemon_id,
        pokemon_name,
        type_slot,
        type_name,
        extracted_at
    from source_types
)

select * from cleaned
