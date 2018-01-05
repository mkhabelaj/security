import psycopg2


class PSQLDatabaseSetup:
    def __init__(self, connection, database_table, channel, function_name='notify_event', drop_if_exists=False):
        """
        :param connection psycopg2.connection:
        :param database_table:
        :param channel:
        :param drop_if_exists:
        """
        self.function_name = function_name
        self.conn = connection
        self.cursor = self.conn.cursor()
        self.channel = channel
        self.table = database_table
        self.drop_if_exists = drop_if_exists

        if self.drop_if_exists:
            self.drop_function_trigger()

    def create_notify_event(self):
        query_string_if_exists_function = \
            "select exists( select * from pg_proc where proname = '{function_name}');".format(
                function_name=self.function_name
            )

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

        self.execute_sql(query_string_if_exists_function, "Checking if Function exists ....")

        if self.cursor.fetchone()[0]:
            print("{function} function already exists".format(function=self.function_name))
        else:
            print("Function does not exist")
            self.execute_sql(query_string_create_function,"creating {function} function".format(
                function=self.function_name
            ))

        self.add_trigger_to_table()

    def add_trigger_to_table(self):
        query_string_if_trigger_exists =\
            "select exists( select * from pg_trigger where tgname = '{table_name}_{function_name}');".format(
                table_name=self.table,
                function_name=self.function_name
            )
        query_create_trigger="""
        CREATE TRIGGER {table}_{function_name} 
        AFTER INSERT OR UPDATE OR DELETE ON {table}
          FOR EACH ROW EXECUTE PROCEDURE {function_name}();
        """.format(
            table=self.table,
            function_name=self.function_name
        )
        self.execute_sql(query_string_if_trigger_exists, "Checking if trigger exists")
        if self.cursor.fetchone()[0]:
            print('Trigger already exists')
        else:
            print('Trigger doest not exist')
            self.execute_sql(query_create_trigger, "creating trigger....")

    def drop_function_trigger(self):
        print("Dropping function {function_name} and trigger {table}_{function_name} if exists".format(
            function_name=self.function_name,
            table=self.table,
        ))
        query_string_drop_function = "DROP FUNCTION IF EXISTS {function_name};".format(function_name=self.function_name)
        query_string_drop_trigger="DROP TRIGGER {table}_{function_name} ON {table}".format(
            function_name=self.function_name,
            table=self.table,
        )
        self.execute_sql(query_string_drop_trigger, "Dropping trigger")
        self.execute_sql(query_string_drop_function, "Dropping function")


    def execute_sql(self, statement, logging_info="Executing sql statement"):
        print('{logging_info}'.format(logging_info=logging_info))
        try:
            self.cursor.execute(statement)
            print("Execution was successful")
        except Exception as e:
            print('Error {ex}'.format(ex=e))
