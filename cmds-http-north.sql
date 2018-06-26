-- Plugin loader configuration
INSERT INTO foglamp.configuration ( key, description, value )
     VALUES ( 'SEND_PR_3',
              'HTTP North Plugin',
              ' { "plugin" : { "type" : "string", "value" : "http", "default" : "http", "description" : "Module that HTTP North Plugin will load" } } '
            );


INSERT INTO foglamp.scheduled_processes ( name, script ) VALUES ( 'North HTTP', '["tasks/north", "--stream_id", "3", "--debug_level", "1"]' );

--- Run the sending process using HTTP North translator every 15 seconds
INSERT INTO foglamp.schedules ( id, schedule_name, process_name, schedule_type,
                                schedule_time, schedule_interval, exclusive, enabled )
       VALUES ( '81bdf749-8aa0-468e-b229-9ff695668e8c', -- id
                'HTTP Sender',                          -- schedule_name
                'North HTTP',                           -- process_name
                3,                                      -- schedule_type (interval)
                NULL,                                   -- schedule_time
                '00:00:30',                             -- schedule_interval
                't',                                    -- exclusive
                't'                                     -- enabled
              );

-- Statistics
INSERT INTO foglamp.statistics (key, description, value, previous_value)
    VALUES('SENT_3', 'Readings data sent via HTTP north', 0, 0);

-- Destination & Stream For Sending Process
INSERT INTO foglamp.destinations ( id, description, ts )
    VALUES ( 2, 'HTTP north', now() );
INSERT INTO foglamp.streams ( id, destination_id, description, last_object, ts )
    VALUES ( 3, 2, 'HTTP north', 0, now() );
