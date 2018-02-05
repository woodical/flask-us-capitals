DROP TABLE IF EXISTS list_of_us_state_capitals;
CREATE table list_of_us_state_capitals (
	State TEXT, 
	Abbreviation TEXT, 
	Year_of_Statehood INT, 
	Capital TEXT, 
	Area REAL, 
	Population INT
);
.mode csv
.import  list_of_us_state_capitals.csv list_of_us_state_capitals
SELECT * from list_of_us_state_capitals LIMIT 10;
SELECT COUNT(*) from list_of_us_state_capitals;
