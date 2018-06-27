-- SQLite only
-- Plugin loader configuration
INSERT INTO configuration ( key, description, value )
     VALUES ( 'SEND_PR_3',
              'HTTP North Plugin',
              ' { "plugin" : { "type" : "string", "value" : "http_north", "default" : "http_north", "description" : "Module that HTTP North Plugin will load" } } '
            );

INSERT INTO destinations ( id, description)
    VALUES ( 2, 'HTTP north' );

INSERT INTO streams ( id, destination_id, description, last_object )
    VALUES ( 3, 2, 'HTTP north', 0 );

-- Statistics
INSERT INTO statistics (key, description, value, previous_value)
    VALUES('SENT_3', 'Readings data sent via HTTP north', 0, 0);

-- Process to schedule
INSERT INTO scheduled_processes ( name, script )
    VALUES ( 'North HTTP', '["tasks/north", "--stream_id", "3", "--debug_level", "1"]' );
