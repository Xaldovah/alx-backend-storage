-- Create a stored procedure ComputeAverageScoreForUser that computes
-- and stores the average score for a student
DELIMITER //


CREATE PROCEDURE ComputeAverageScoreForUser(
	IN p_user_id INT
)
BEGIN
	DECLARE total_score FLOAT;
	DECLARE total_projects INT;

	SET total_score = 0;
	SET total_projects = 0;

	SELECT SUM(score), COUNT(DISTINCT project_id)
	INTO total_score, total_projects
	FROM corrections
	WHERE user_id = p_user_id;

	IF total_projects > 0 THEN
		UPDATE users
		SET average_score = total_score / total_projects
		WHERE id = p_user_id;
	END IF;
END;


//


DELIMITER ;
