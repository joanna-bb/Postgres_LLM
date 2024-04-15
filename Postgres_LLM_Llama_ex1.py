import os
import openai
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Text,
    DateTime,
    select,
    inspect
)
from llama_index.core import SQLDatabase, ServiceContext, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from sqlalchemy import insert
from sqlalchemy import text
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
openai.api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm)

engine = create_engine("postgresql://{username}:{password}@{host}:{port}/{mydatabase}")

# load all table definitions
metadata_obj = MetaData()
metadata_obj.reflect(engine)

sql_database = SQLDatabase(engine)
query_engine=NLSQLTableQueryEngine(sql_database=sql_database,tables=["patients","diagnosis","patient_diagnosis","patient_procedures","procedures"],llm=llm)

query_str="Find all male patients and their ICD10 procedures and diagnoses"
response=query_engine.query(query_str)
print(response)
print(response.metadata)