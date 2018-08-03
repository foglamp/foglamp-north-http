-- SQLite only
-- Plugin loader configuration
INSERT INTO destinations ( id, description)
    VALUES ( 2, 'HTTP North' );

INSERT INTO streams ( id, destination_id, description, last_object )
    VALUES ( 3, 2, 'HTTP North', 0 );

-- Statistics
INSERT INTO statistics (key, description, value, previous_value)
    VALUES('SENT_3', 'Readings data sent via HTTP North', 0, 0);
