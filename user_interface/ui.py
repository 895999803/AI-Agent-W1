import os
import sys
import streamlit as st
import pandas as pd
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import tools.tools_calling as tc
st.set_page_config(layout="wide")

# st.title("Multi-stage Streamlit App")

# Initialize session state variables
if 'show_5x5_table' not in st.session_state:
    st.session_state.show_5x5_table = False
if 'show_3x5_table' not in st.session_state:
    st.session_state.show_3x5_table = False
if 'clicked_5x5_button_index' not in st.session_state:
    st.session_state.clicked_5x5_button_index = None
if 'papers' not in st.session_state:
    st.session_state.papers = None
if 'keyword' not in st.session_state:
    st.session_state.keyword = None
if 'number' not in st.session_state:
    st.session_state.number = None


# --- Stage 1: Initial Button ---
if not st.session_state.show_5x5_table:
    st.subheader("论文调研助手")
    st.session_state.keyword = st.text_input("关键词")
    st.session_state.number = st.number_input("期待推荐的论文数量（最少5篇）", step=1, value=5)
    if st.button("查询", key="initial_button"):
        st.session_state.show_5x5_table = True
        st.rerun()

# --- Stage 2: 5x5 Table with Buttons ---
# Only show 5x5 table if show_5x5_table is True AND show_3x5_table is False
if st.session_state.show_5x5_table and not st.session_state.show_3x5_table:
    st.subheader("论文推荐列表")

    query = "请帮我推荐" + str(st.session_state.number) + "篇与" + st.session_state.keyword + "相关的论文。"
    response = tc.tool_calling(query)
    # print(response)
    data = json.loads(response)
    # print(data)

    for i in range(len(data)):
        authors = ""
        for author in data[i]['authors']:
            authors += author + "\n"
        data[i]['authors'] = authors

    st.session_state.papers = data
    df_5x5 = pd.DataFrame(data)
    column_widths = []
    for key in data[0]:
        column_widths.append(1)
    column_widths.append(0.5)

    # Create columns for the table, including one for the button
    # We need 4 columns for data + 1 for the button = 5 columns
    cols_5x5 = st.columns(column_widths)

    # Display headers for 5x5 table
    for i, col_name in enumerate(df_5x5.columns):
        with cols_5x5[i]:
            st.write(f"**{col_name}**")
    with cols_5x5[-1]: # The last column for the button header
        st.write(f"**Action**")

    st.markdown("---") # Separator

    # Display data rows and buttons for 5x5 table
    for index_5x5, row_5x5 in df_5x5.iterrows():
        row_cols_5x5 = st.columns(column_widths)
        for i, col_name in enumerate(df_5x5.columns):
            with row_cols_5x5[i]:
                st.write(row_5x5[col_name])
        with row_cols_5x5[-1]:  # The last column for the button
            if st.button(f"论文精读", key=f"5x5_button_{index_5x5}"):
                st.session_state.show_3x5_table = True
                st.session_state.clicked_5x5_button_index = index_5x5
                st.rerun()

# --- Stage 3: 3x5 Data Table (displayed on current page) ---
# Only show 3x5 table if show_3x5_table is True
if st.session_state.show_3x5_table:
    # st.markdown("--- # Separator")
    # st.info(f"您点击了 5x5 表格中的第 {st.session_state.clicked_5x5_button_index + 1} 个按钮，现在显示其对应的数据。")
    paper = st.session_state.papers[st.session_state.clicked_5x5_button_index]

    st.subheader(f"论文精读: {paper["title"]}")
    paper_url = paper["url"]
    paper_content = tc.arxiv_paper_calling(paper_url)

    st.write(paper_content)

    if st.button("返回论文推荐", key="back_to_5x5"):
        st.session_state.show_3x5_table = False
        st.session_state.clicked_5x5_button_index = None
        st.rerun()
