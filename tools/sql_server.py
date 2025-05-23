from fastmcp import FastMCP
from sqlalchemy import create_engine, inspect, text
from datetime import datetime, date

# --- Configuration ---
DB_CONFIGS = {
    "titanic": "sqlite:///resource/titanic.db",
    "chinook": "sqlite:///resource/chinook.db",
}
EXECUTE_QUERY_MAX_CHARS = 4000
TRANSPORT = "streamable-http"

mcp = FastMCP(
    name="SQL Tool",
    instructions="Use the tools to interact with the databases. Each tool is specific to a configured database."
)

def get_engine(db_url, readonly=True):
    return create_engine(
        db_url,
        isolation_level='AUTOCOMMIT',
        execution_options={'readonly': readonly}
    )

def get_db_info(db_url):
    engine = get_engine(db_url, readonly=True)
    with engine.connect():
        url = engine.url
        print(f"Connecting to {url}")
        result = {
            "dialect": engine.dialect.name,
            "version": list(engine.dialect.server_version_info),
            "database": url.database,
            "host": url.host,
            "user": url.username
        }
        return result

# --- Dynamic Tool Registration ---
for db_key, db_url in DB_CONFIGS.items():
    db_info = get_db_info(db_url)
    
    @mcp.tool(name=f"{db_key}_all_table_names", description=f"Return all table names in the database '{db_key}' separated by comma. {db_info}")
    def all_table_names() -> str:
        engine = get_engine(db_url)
        inspector = inspect(engine)
        return ", ".join(inspector.get_table_names())

    @mcp.tool(name=f"{db_key}_filter_table_names", description=f"Return all table names in the database '{db_key}' containing the substring 'q'. {db_info}")
    def filter_table_names(q: str) -> str:
        engine = get_engine(db_url)
        inspector = inspect(engine)
        return ", ".join(x for x in inspector.get_table_names() if q in x)
    
    @mcp.tool(name=f"{db_key}_schema_definitions", description=f"Returns schema and relation information for the given tables. {db_info}")
    def schema_definitions(table_names: list[str]) -> str:
        def format(inspector, table_name):
            columns = inspector.get_columns(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            primary_keys = set(inspector.get_pk_constraint(table_name)["constrained_columns"])
            result = [f"{table_name}:"]

            # Process columns
            show_key_only = {"nullable", "autoincrement"}
            for column in columns:
                if "comment" in column:
                    del column["comment"]
                name = column.pop("name")
                column_parts = (["primary key"] if name in primary_keys else []) + [str(
                    column.pop("type"))] + [k if k in show_key_only else f"{k}={v}" for k, v in column.items() if v]
                result.append(f"    {name}: " + ", ".join(column_parts))

            # Process relationships
            if foreign_keys:
                result.extend(["", "    Relationships:"])
                for fk in foreign_keys:
                    constrained_columns = ", ".join(fk['constrained_columns'])
                    referred_table = fk['referred_table']
                    referred_columns = ", ".join(fk['referred_columns'])
                    result.append(f"      {constrained_columns} -> {referred_table}.{referred_columns}")

            return "\n".join(result)

        engine = get_engine(db_url)
        inspector = inspect(engine)
        return "\n".join(format(inspector, table_name) for table_name in table_names)

    
    def execute_query_description():
        parts = [
            f"Execute a SQL query and return results in a readable format. Results will be truncated after {EXECUTE_QUERY_MAX_CHARS} characters.",
            "IMPORTANT: Always use the params parameter for query parameter substitution (e.g. 'WHERE id = :id' with params={'id': 123}) to prevent SQL injection. Direct string concatenation is a serious security risk.",
            f"Database info: {db_info}",
        ]
        return " ".join(parts)
    
    @mcp.tool(name=f"{db_key}_execute_query", description=execute_query_description())
    def execute_query(query: str, params: dict = {}) -> dict:
        def format_value(val):
            """Format a value for display, handling None and datetime types"""
            if val is None:
                return "NULL"
            if isinstance(val, (datetime, date)):
                return val.isoformat()
            return str(val)

        engine = get_engine(db_url)
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                if query.strip().upper().startswith("SELECT"):
                    rows = result.fetchall()
                    columns = result.keys()
                    return {
                        "columns": list(columns),
                        "rows": [[format_value(val) for val in row] for row in rows]
                    }
                else:
                    return {"status": "ok"}
        except Exception as e:
            return {"error": str(e)}
