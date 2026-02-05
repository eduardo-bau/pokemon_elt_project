
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pokemon_id
from "pokemon"."raw"."pokemon_stats"
where pokemon_id is null



  
  
      
    ) dbt_internal_test