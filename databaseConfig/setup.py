import psycopg2


class PSQLDatabaseSetup:
    def __init__(self, connection, database_table, channel,drop_function_if_exists=False):
        """
        :param connection psycopg2.connection:
        :param database_table:
        :param channel:
        :param drop_function_if_exists:
        """
        self.function_name = 'notify_event'
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.channel = channel
        self.drop_function = drop_function_if_exists
        self.table = database_table

    def create_notify_event(self):
        query_string_if_exists_function = "select exists( select * from pg_proc where proname = '{function_name}');".format(function_name=self.function_name)

        query_string_create_function="""
        CREATE OR REPLACE FUNCTION {function_name}() RETURNS TRIGGER AS $$
        
            DECLARE
                data json;
                notification json;
        
            BEGIN
        
                -- Convert the old or new row to JSON, based on the kind of action.
                -- Action = DELETE?             -> OLD row
                -- Action = INSERT or UPDATE?   -> NEW row
                IF (TG_OP = 'DELETE') THEN
                    data = row_to_json(OLD);
                ELSE
                    data = row_to_json(NEW);
                END IF;
        
                -- Contruct the notification as a JSON string.
                notification = json_build_object(
                                  'table',TG_TABLE_NAME,
                                  'action', TG_OP,
                                  'data', data);
        
        
                -- Execute pg_notify(channel, notification)
                PERFORM pg_notify({channel},notification::text);
        
                -- Result is ignored since this is an AFTER trigger
                RETURN NULL;
            END;
        
        $$ LANGUAGE plpgsql;
        
        """.format(function_name=self.function_name, channel=self.channel)

        query_string_drop_function="drop function if exists {function_name};".format(function_name=self.function_name)

        self.cursor.execute(query_string_if_exists_function)

        if self.cursor.fetchone()[0]:
            self.add_trigger_to_table()

    def add_trigger_to_table(self):
        query_string_if_trigger_exists =\
            "select exists( select * from pg_trigger where tgname = '{table_name}_{function_name}');".format(
                table_name=self.table,
                function_name=self.function_name
            )
        self.cursor.execute(query_string_if_trigger_exists)
        if self.cursor.fetchone()[0]:
            pass
