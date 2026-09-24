import streamlit as st
import pandas as pd

from components.header import start
from components.side import sidebaar
from configuration.configur import image
from prompt.prompt import prompt

from loader.doc import doc_loading
from loader.pdf import pdf_loading

from model.model import aii


####################### SESSION STATE #######################

if "names" not in st.session_state:
    st.session_state.names = []

if "phones" not in st.session_state:
    st.session_state.phones = []

if "emails" not in st.session_state:
    st.session_state.emails = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "is_resume" not in st.session_state:
    st.session_state.is_resume = []

if "wrong_file_reason" not in st.session_state:
    st.session_state.wrong_file_reason = []


if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()


####################### STARTER #########################

c1, c2 = st.columns(2)

with c1:

    st.image(image)

with c2:

    start1 = start()

    start.init()


################### SIDEBAR OPERATIONS #####################

st.sidebar.title("The parameter will be added here")

file = st.sidebar.file_uploader(
    "Please upload the resume here",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

job_desc = st.sidebar.text_area(
    "Write the Job Description here",
    height=350
)

btn = st.sidebar.button("Submit")


####################### EXECUTER ########################

if btn:

    if file:

        # Clear previous results
        st.session_state.names = []
        st.session_state.phones = []
        st.session_state.emails = []
        st.session_state.scores = []
        st.session_state.is_resume = []
        st.session_state.wrong_file_reason = []

        raw_text = []

        # Extract text from every uploaded resume
        for txt in file:

            if txt.name.lower().endswith(".pdf"):

                pdf = pdf_loading(txt)

                raw_text.append(pdf.text())

            else:

                doc = doc_loading(txt)

                raw_text.append(doc.text())


        #################### AI ANALYSIS ####################

        for text in raw_text:

            data = prompt.invoke({
                "EXTRACTED_TEXT": text,
                "JOB_DESC": job_desc
            })

            result = aii.invoke(data)


            #################### STORE RESULTS ####################

            st.session_state.names.append(result.name)

            st.session_state.phones.append(result.phone)

            st.session_state.emails.append(result.email)

            st.session_state.scores.append(result.score)

            st.session_state.is_resume.append(result.is_resume)

            st.session_state.wrong_file_reason.append(
                result.wrong_file_reason
            )


        #################### CREATE DATAFRAME ####################

        st.session_state.df = pd.DataFrame({

            "Name": st.session_state.names,

            "Email": st.session_state.emails,

            "Phone": st.session_state.phones,

            "Score": st.session_state.scores,

            "Is Resume": st.session_state.is_resume,

            "Wrong File Reason": st.session_state.wrong_file_reason

        })


####################### DISPLAY ########################

if not st.session_state.df.empty:

    st.subheader("Resume Analysis")

    st.dataframe(
        st.session_state.df,
        use_container_width=True
    )