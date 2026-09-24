import streamlit as st
from prompt.prompt import prompt
from output.output import OP
from model.model import ai, aii
from eval.test001 import resume
from eval.text002 import job
from loader.doc import doc_loading
from loader.pdf import pdf_loading



# text = prompt.invoke({
#     "EXTRACTED_TEXT": resume
# })

# resu = aii.invoke(text)
# print(resu.email)
# print(resu.name)

# print(text)


# load = pdf_loading("/home/ahmad/workshop/AI-powered-resume-analyzer/component/CV.pdf")
# text = load.text()

# load2 = doc_loading("/home/ahmad/workshop/AI-powered-resume-analyzer/component/Ahmad resume .docx")
# text2 = load2.text()


command = prompt.invoke({"EXTRACTED_TEXT":resume, "JOB_DESC":job})


result = aii.invoke(command)
print(result)

# print(resume)