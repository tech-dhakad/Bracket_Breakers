import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Mini Social Media", layout="wide")

# ---------------- Init session state ----------------
if "users" not in st.session_state:
    st.session_state.users = {}  # username -> {password, bio}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "posts" not in st.session_state:
    st.session_state.posts = []  # list of dicts


# ---------------- Helper functions ----------------
def create_post(author, content):
    post = {
        "id": random.randint(1000, 9999),
        "author": author,
        "content": content,
        "likes": set(),
        "comments": [],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.posts.insert(0, post)


def add_comment(post_id, author, text):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["comments"].append(
                {"author": author, "text": text, "time": datetime.now().strftime("%H:%M")}
            )
            break


def toggle_like(post_id, user):
    for post in st.session_state.posts:
        if post["id"] == post_id:
            if user in post["likes"]:
                post["likes"].remove(user)
            else:
                post["likes"].add(user)


# ---------------- Sidebar (Login/Register) ----------------
st.sidebar.title("👤 Account")

if st.session_state.current_user:
    st.sidebar.success(f"Logged in as {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
else:
    choice = st.sidebar.radio("Choose", ["Login", "Register"])
    uname = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")

    if choice == "Register":
        bio = st.sidebar.text_area("Bio")
        if st.sidebar.button("Register"):
            if uname in st.session_state.users:
                st.sidebar.error("Username already exists!")
            else:
                st.session_state.users[uname] = {"password": pwd, "bio": bio}
                st.sidebar.success("Registered! Now login.")
    else:
        if st.sidebar.button("Login"):
            if (
                uname in st.session_state.users
                and st.session_state.users[uname]["password"] == pwd
            ):
                st.session_state.current_user = uname
            else:
                st.sidebar.error("Invalid credentials")

# ---------------- Main Dashboard ----------------
st.title("📱 Mini Social Platform")

if not st.session_state.current_user:
    st.info("Login to see & create posts.")
else:
    # New post form
    with st.form("new_post"):
        content = st.text_area("What's on your mind?", "")
        posted = st.form_submit_button("Post")
        if posted and content.strip():
            create_post(st.session_state.current_user, content)
            st.success("Posted!")

    st.markdown("---")

    # Display posts
    for post in st.session_state.posts:
        with st.container():
            st.write(f"**{post['author']}** · {post['timestamp']}")
            st.write(post["content"])

            # Like & comment actions
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(
                    f"❤️ {len(post['likes'])}",
                    key=f"like_{post['id']}",
                ):
                    toggle_like(post["id"], st.session_state.current_user)
            with col2:
                comment_text = st.text_input(
                    "Write a comment...",
                    key=f"cmt_in_{post['id']}",
                    placeholder="Type and press Enter",
                )
                if comment_text:
                    add_comment(post["id"], st.session_state.current_user, comment_text)
                    st.experimental_rerun()

            # Show comments
            for c in post["comments"]:
                st.caption(f"💬 {c['author']} ({c['time']}): {c['text']}")
            st.markdown("---")
