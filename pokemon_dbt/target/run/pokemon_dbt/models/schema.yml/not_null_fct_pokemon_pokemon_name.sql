
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pokemon_name
from "pokemon"."main"."fct_pokemon"
where pokemon_name is null



  
  
      
    ) dbt_internal_test