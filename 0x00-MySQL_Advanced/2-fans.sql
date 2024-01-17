-- Import the metal_bands table dump
-- Rank country origins of bands by the number of (non-unique) fans
SELECT origin, SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
