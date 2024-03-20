duckdb
--.open 'C:\\Project_Files\\bigquery_duckdb\\duckdb\\gdelt.duckdb'
.open 'C:\\Project_Files\streamlit_gdelt\\duckdb\\gdelt.duckdb'

create or replace table upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024 (
    date date,
    USA int,
    Germany int,
    Poland int,
    Hungary int,
    France int,
    China int,
    UK int);

insert into upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024 
select * from read_csv('streamlit_data.csv');

from upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024;

copy from database 'C:\\Project_Files\\bigquery_duckdb\\duckdb\\gdelt.duckdb' as db1 to 'C:\\Project_Files\streamlit_gdelt\\duckdb\\gdelt.duckdb' as db2;
from upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024;

PRAGMA import_database('C:\Project_Files\bigquery_duckdb\duckdb\gdelt.duckdb');

show tables;

COPY upd_multiple_countriesS_sum_of_criticsim_russia_2020_2024 TO 'streamlit_data.csv' (DELIMITER ',');