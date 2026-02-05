
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    pokemon_id as unique_field,
    count(*) as n_records

from "pokemon"."main"."fct_pokemon"
where pokemon_id is not null
group by pokemon_id
having count(*) > 1



  
  
      
    ) dbt_internal_test