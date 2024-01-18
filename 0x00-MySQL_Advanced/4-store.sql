-- Create a trigger to decrease the quantity of an item after adding a new order
-- Update the quantity in the items table based on the new order
DELIMITER //


CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
END;


//


DELIMITER ;
