# app.py
import streamlit as st
from streamlit_sortables import sort_items  # pip install streamlit-sortables

st.set_page_config(page_title="Mini Trello", layout="wide")

# Initialize board state
if "board" not in st.session_state:
    st.session_state.board = {
        "To Do": ["Setup project", "Create UI mockups"],
        "In Progress": ["Write backend APIs"],
        "Done": ["Create repo"]
    }

st.title(" Mini Trello-like Task Manager")

# Add new task
with st.form("add_task"):
    col1, col2 = st.columns([3,1])
    new_task = col1.text_input("New Task", placeholder="Enter task name...")
    target_list = col2.selectbox("List", list(st.session_state.board.keys()))
    submitted = st.form_submit_button(" Add")
    if submitted and new_task:
        st.session_state.board[target_list].append(new_task)
        st.success(f"Added '{new_task}' to {target_list}")

# Layout: 3 columns (lists)
cols = st.columns(len(st.session_state.board))

for idx, (list_name, tasks) in enumerate(st.session_state.board.items()):
    with cols[idx]:
        st.subheader(list_name)
        # Drag-and-drop widget
        items = sort_items(tasks, direction="vertical", key=list_name)
        st.session_state.board[list_name] = items

# Progress tracking
total = sum(len(tasks) for tasks in st.session_state.board.values())
done = len(st.session_state.board["Done"])
progress = 0 if total == 0 else done / total

st.markdown("### Progress")
st.progress(progress)
st.write(f"Completed: {done}/{total} tasks")

