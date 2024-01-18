-- Create a stored procedure AddBonus that adds
-- a new correction for a student
DELIMITER //

CREATE PROCEDURE AddBonus(
	IN p_user_id INT,
	IN p_project_name VARCHAR(255),
	IN p_score INT
)
BEGIN
	DECLARE project_id INT;

	IF NOT EXISTS (SELECT id FROM projects WHERE name = p_project_name) THEN
		INSERT INTO projects (name) VALUES (p_project_name);
	END IF;

	SET project_id = COALESCE((SELECT id FROM projects WHERE name = p_project_name), LAST_INSERT_ID());

	INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, project_id, p_score);

END;

//

DELIMITER ;
