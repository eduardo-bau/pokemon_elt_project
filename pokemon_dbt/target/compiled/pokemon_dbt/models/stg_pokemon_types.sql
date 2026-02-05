

with source_types as (
    select * from "pokemon"."raw"."pokemon_types"
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