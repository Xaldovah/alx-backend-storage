-- Create a stored procedure ComputeAverageWeightedScoreForUsers
-- Calculate and update the total weight
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE done INT DEFAULT 0;
	DECLARE user_id INT;

	DECLARE total_score FLOAT DEFAULT 0;
	DECLARE total_weight FLOAT DEFAULT 0;

	DECLARE users_cursor CURSOR FOR SELECT id FROM users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

	OPEN users_cursor;
	users_loop: LOOP

		FETCH users_cursor INTO user_id;
		IF done THEN
			LEAVE users_loop;
		END IF;

		SELECT SUM(c.score * p.weight) INTO total_score
		FROM corrections c
		JOIN projects p ON c.project_id = p.id
		WHERE c.user_id = user_id;

		SELECT SUM(weight) INTO total_weight
		FROM projects;

		UPDATE users
		SET average_score = total_score / total_weight
		WHERE id = user_id;
	END LOOP;

	CLOSE users_cursor;
END //


DELIMITER ;
