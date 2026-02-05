
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pokemon_count
from "pokemon"."main"."dim_type_analysis"
where pokemon_count is null



  
  
      
    ) dbt_internal_test