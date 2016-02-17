--Sample daily trends (based on a 7 day average)
with agg_views as (
Select date,
	sum(count) as totalView,
	countries,
        geom 
from
	public.monthjan
group by date,countries,geom
)
   
select 
	date,
	countries,
	totalView,
	avg,
	zscore,
	geom
from (
	Select
		date,
		countries,
		totalView,
		avg(totalView) over(partition by countries) as avg,
		(totalView-avg(totalView) over(PARTITION BY countries order by date rows between 6 preceding and current row ))/NULLIF((stddev(totalView) over(PARTITION BY countries order by date rows between 6 preceding and current row)),0) as zscore,
		geom
	from (        	
		Select  date::date,
			coalesce(totalView,0) as totalView,
			countries, 
			geom
		from agg_views
		right join
		(
			(
			select distinct countries
			from agg_views
			) c
			cross join
			generate_series ( '2016-01-26'::date-'6 day'::interval,
				'2016-01-26'::date,
				'1 day'
			    ) gs(date)
		) s using (countries, date)
		) as d
	)as zscoresValues
where zscore>=1.65 and date='2016-01-26'
order by zscore desc 
limit 50