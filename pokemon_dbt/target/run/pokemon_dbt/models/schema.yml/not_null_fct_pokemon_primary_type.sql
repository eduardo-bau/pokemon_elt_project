
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select primary_type
from "pokemon"."main"."fct_pokemon"
where primary_type is null



  
  
      
    ) dbt_internal_test