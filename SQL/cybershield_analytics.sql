SELECT *
FROM incidents
LIMIT 10;



SELECT 
    attack_type,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY attack_type
ORDER BY total_incidents DESC;



SELECT 
    target_industry,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY target_industry
ORDER BY total_incidents DESC;



SELECT 
    risk_level,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY risk_level
ORDER BY total_incidents DESC;



SELECT 
    attack_type,
    ROUND(AVG(financial_loss_million), 2) AS average_financial_loss_million
FROM incidents
GROUP BY attack_type
ORDER BY average_financial_loss_million DESC;



SELECT 
    target_industry,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM incidents
GROUP BY target_industry
ORDER BY average_risk_score DESC;


SELECT 
    year,
    COUNT(*) AS total_incidents
FROM incidents
GROUP BY year
ORDER BY year ASC;



SELECT 
    incident_id,
    country,
    year,
    attack_type,
    target_industry,
    financial_loss_million,
    affected_users,
    risk_score
FROM incidents
WHERE risk_level = 'High'
ORDER BY risk_score DESC
LIMIT 10;

SELECT 
    country,
    COUNT(*) AS total_incidents,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM incidents
GROUP BY country
ORDER BY average_risk_score DESC;

SELECT 
    attack_type,
    COUNT(*) AS total_incidents,
    ROUND(SUM(financial_loss_million), 2) AS total_financial_loss_million
FROM incidents
GROUP BY attack_type
ORDER BY total_financial_loss_million DESC
LIMIT 5;


SELECT 
    target_industry,
    COUNT(*) AS high_risk_incidents
FROM incidents
WHERE risk_level = 'High'
GROUP BY target_industry
ORDER BY high_risk_incidents DESC;


SELECT 
    attack_type,
    ROUND(AVG(resolution_time_hours), 2) AS average_resolution_time_hours
FROM incidents
GROUP BY attack_type
ORDER BY average_resolution_time_hours DESC;


SELECT 
    incident_id,
    country,
    year,
    attack_type,
    target_industry,
    financial_loss_million,
    affected_users,
    resolution_time_hours,
    risk_score,
    risk_level
FROM incidents
ORDER BY 
    risk_score DESC,
    financial_loss_million DESC,
    affected_users DESC
LIMIT 10; 
