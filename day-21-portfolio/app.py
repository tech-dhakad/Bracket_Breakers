import streamlit as st
from PIL import Image

# ----------------- Page Config -----------------
st.set_page_config(page_title="My Portfolio", page_icon="💻", layout="wide")

# ----------------- Header -----------------
st.title("💻 My Developer Portfolio")
st.write("Welcome to my portfolio! I am a passionate **AI/DS student & developer** 🚀")

# Profile image (optional)
# image = Image.open("profile.jpg")
# st.image(image, width=150)

# ----------------- About Section -----------------
st.header("👨‍💻 About Me")
st.write("""
Hi! I'm **[Your Name]**, a B.Tech AI/DS student at Sagar Institute of Science and Technology.  
I love building full-stack applications, chatbots, and AI-powered tools.  
Currently preparing for **GATE DA** and exploring **Web + AI integrations**.  
""")

# ----------------- Skills -----------------
st.header("⚡ Skills")
cols = st.columns(3)
skills = [
    ["Python", "Streamlit", "Flask"],
    ["Express.js", "React", "Node.js"],
    ["SQL", "MongoDB", "Machine Learning"]
]
for i, col in enumerate(cols):
    with col:
        for skill in skills[i]:
            st.markdown(f"- {skill}")

# ----------------- Projects Showcase -----------------
st.header("🚀 Projects")
projects = [
    {
        "title": "Medi-Bot",
        "desc": "AI-powered chatbot for health tips with medically reviewed info.",
        "link": "https://github.com/yourusername/medi-bot"
    },
    {
        "title": "Pharma-Bot",
        "desc": "Pharmacy assistant chatbot with drug info & dosage reminders.",
        "link": "https://github.com/yourusername/pharma-bot"
    },
    {
        "title": "Swadesh",
        "desc": "Hackathon project for a one-stop platform for study resources.",
        "link": "https://github.com/yourusername/swadesh"
    }
]

for p in projects:
    with st.container():
        st.subheader(p["title"])
        st.write(p["desc"])
        st.markdown(f"[🔗 View Project]({p['link']})")
        st.markdown("---")

# ----------------- Contact Form -----------------
st.header("📬 Contact Me")

contact_form = """
<form action="https://formsubmit.co/YOUR_EMAIL_HERE" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="text" name="name" placeholder="Your Name" required>
    <input type="email" name="email" placeholder="Your Email" required>
    <textarea name="message" placeholder="Your Message Here" required></textarea>
    <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

st.info("Or connect with me on [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)")
