
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select stat_rank
from "pokemon"."main"."fct_stat_rankings"
where stat_rank is null



  
  
      
    ) dbt_internal_test