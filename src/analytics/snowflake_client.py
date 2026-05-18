import os
import snowflake.connector
from snowflake.connector import SnowflakeConnection

class SnowflakeClient:
    def __init__(self):
        self.conn = self._get_connection()

    def _get_connection(self) -> SnowflakeConnection:
        """Create a Snowflake connection using environment variables."""
        return snowflake.connector.connect(
            user=os.environ.get('SNOWFLAKE_USER'),
            password=os.environ.get('SNOWFLAKE_PASSWORD'),
            account=os.environ.get('SNOWFLAKE_ACCOUNT'),
            warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
            database=os.environ.get('SNOWFLAKE_DATABASE', 'THREAT_ANALYTICS'),
            schema=os.environ.get('SNOWFLAKE_SCHEMA', 'CLOUDTRAIL')
        )

    def execute_query(self, query: str) -> list[dict]:
        """Execute a query and return results as a list of dicts."""
        try:
            cursor = self.conn.cursor(snowflake.connector.DictCursor)
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
