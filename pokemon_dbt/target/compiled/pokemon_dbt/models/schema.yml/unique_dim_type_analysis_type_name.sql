
    
    

select
    type_name as unique_field,
    count(*) as n_records

from "pokemon"."main"."dim_type_analysis"
where type_name is not null
group by type_name
having count(*) > 1


