import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from template import BASIC_TEMPLATE,SQL_TEMPLATE

def generate_response(memory, question,model_type="百川"):
    if model_type == "百川":
        llm = ChatOpenAI(
            openai_api_key="sk-cfdf885592540e8f76134c1cfd962dd0",
            base_url="https://api.baichuan-ai.com/v1",
            model="Baichuan3-Turbo",
        )
    elif model_type == "智谱":
        llm = ChatOpenAI(
            openai_api_key="9d46dc29be6a3ea5da64efaf9a7caa41.IMe2UoaxYA4Lrhap",
            base_url= "https://open.bigmodel.cn/api/paas/v4/",
            model="glm-4",
        )
    elif model_type == "你自己的选择":
        llm = ChatOpenAI(
            openai_api_key=st.session_state.model_api_keys["你自己的选择"],
            base_url=st.session_state.model_urls["你自己的选择"],
            model=st.session_state.model_names["你自己的选择"],
        )
    else:
        raise ValueError(f"未知的模型类型: {model_type}")

    prompt = PromptTemplate.from_template(BASIC_TEMPLATE)
    
    username = 'root'
    password = '1433223aaa'
    host = 'localhost'
    dbname = 'doctor'

    connection_uri = f"mysql+mysqlconnector://{username}:{password}@{host}/{dbname}"
    db = SQLDatabase.from_uri(connection_uri)

    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm,db)

    # Define the steps for querying the database and getting LLM responses
    def query_database(query):
        try:
            result = execute_query(query)
            if result.split(":")[0]=="Error":
                result=None
            return result if result else None
        except Exception as e:
            print(f"Database query failed: {e}")
            return None
    if model_type == "百川":
        query = write_query.invoke({"question": question}).split("\n")[0].replace('SQLQuery: ','')
    elif model_type == "智谱":
        query = write_query.invoke({"question": question}).strip().replace('sql', '').replace('SQLResult:', '').replace('```','')
    else:
        query = write_query.invoke({"question": question})
    result = query_database(query)

    
    
    if result:
        my_prompt=PromptTemplate.from_template(SQL_TEMPLATE.replace('{query}',query).replace('{result}',result))
        inputs = question
        chain = LLMChain(
            llm=llm,
            prompt=my_prompt,
            verbose=True,
            memory=memory,
        )
    else:
        inputs = question
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )

    response = chain.invoke(inputs)
    return response
