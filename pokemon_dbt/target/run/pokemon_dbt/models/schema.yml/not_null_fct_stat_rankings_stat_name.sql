
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stat_name
from "pokemon"."main"."fct_stat_rankings"
where stat_name is null



  
  
      
    ) dbt_internal_test