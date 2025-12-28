import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import Functions_set
import Db_utility
import pathlib as path

from acnt_ai_agent.Db_utility import Db_utility

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

MODEL = "gpt-4o-mini"
openai = OpenAI()

ddl_document = []
dbutil = Db_utility('nonprod')

def read_ddls(ddl_files):
    for file in ddl_files:
        file_obj = path.Path(file)
        doc_type = file_obj.name
        with open(file_obj.absolute(), 'r') as fl:
            ddl_document.append({"type": doc_type, "text": fl.read()})
    return ddl_document

def runQuery(query):
    query = query.replace("```sql", "").replace("```", "")

    df = dbutil.run_query_asDF(query=query)
    return df


def generate_sql(data_model, query_model):
    print("Generating SQL")
    ddl_document = read_ddls(data_model)
    system_prompt = """
    Your task is to create high performance SQL query by using the following two details 
    first is table ddl and second is the question statement. Do not provide any explanation other than occasional comments. 
    """
    user_prompt = f""" Use the ddl as {ddl_document[0]['text']} and question statement as {query_model}. """
    messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content



with gr.Blocks() as ui:
    with gr.Row():
        data_model = gr.Files(label="DDL Files")
        query_model = gr.Textbox(label="Query", lines=15, value="Enter Query")
    with gr.Row():
        sqlOutput = gr.Textbox(label="SQL", lines=15, value="Sql")
        genSql = gr.Button("Generate SQL")
        runSql = gr.Button("Run SQL")
        outputDf = gr.DataFrame()
    genSql.click(generate_sql, inputs=[data_model, query_model], outputs=[sqlOutput])
    runSql.click(runQuery, inputs=[sqlOutput], outputs=[outputDf])
ui.launch(inbrowser=False)