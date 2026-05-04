-- View 1: Cohort Analysis by Enrollment Quarter
CREATE OR REPLACE VIEW vw_cohort_analysis AS
SELECT 
    CONCAT(YEAR(enrollment_date), '-Q', QUARTER(enrollment_date)) as enrollment_quarter,
    country_name,
    sector_name,
    COUNT(*) as cohort_size,
    AVG(placed) as placement_rate,
    AVG(still_employed_6m) as retention_6m_rate,
    AVG(monthly_income_usd) as avg_income,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) * 100.0 / COUNT(*) as female_percentage
FROM fact_program_performance f
JOIN dim_country c ON f.country_key = c.country_key
JOIN dim_sector s ON f.sector_key = s.sector_key
GROUP BY enrollment_quarter, country_name, sector_name;

-- View 2: Leadership Executive Scorecard
CREATE OR REPLACE VIEW vw_leadership_scorecard AS
SELECT 
    c.country_name,
    COUNT(*) as total_youth,
    AVG(placed) as overall_placement_rate,
    AVG(CASE WHEN gender = 'Female' THEN placed END) as female_placement_rate,
    AVG(still_employed_6m) as retention_rate,
    AVG(monthly_income_usd) as avg_monthly_income,
    STDDEV(monthly_income_usd) as income_variation
FROM fact_program_performance f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.country_name;