{{
    config(
        materialized='view'
    )
}}

with source_pokemon as (
    select * from {{ source('raw', 'pokemon') }}
),

cleaned as (
    select
        id as pokemon_id,
        name as pokemon_name,
        height,
        weight,
        base_experience,
        is_default,
        order_num,
        extracted_at,
        -- Convert height from decimeters to meters
        height / 10.0 as height_meters,
        -- Convert weight from hectograms to kilograms
        weight / 10.0 as weight_kg,
        -- Calculate BMI (weight in kg / (height in m)^2)
        case 
            when height > 0 then (weight / 10.0) / power(height / 10.0, 2)
            else null 
        end as bmi
    from source_pokemon
)

select * from cleaned
