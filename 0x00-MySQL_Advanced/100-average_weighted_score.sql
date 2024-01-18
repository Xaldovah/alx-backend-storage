-- Create a stored procedure ComputeAverageWeightedScoreForUser
 -- Calculate the total weighted score
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE total_score FLOAT DEFAULT 0;
	DECLARE total_weight FLOAT DEFAULT 0;

	SELECT SUM(c.score * p.weight) INTO total_score
	FROM corrections c
	JOIN projects p ON c.project_id = p.id
	WHERE c.user_id = user_id;

	SELECT SUM(weight) INTO total_weight
	FROM projects;

	UPDATE users
	SET average_score = total_score / total_weight
	WHERE id = user_id;
END //


DELIMITER ;
