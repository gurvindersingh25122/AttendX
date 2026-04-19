import streamlit as st
import pandas as pd
import subprocess
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Attendance",
    page_icon="📊",
    layout="wide"
)

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
button[kind="primary"] {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("📊 Smart Attendance Dashboard")
st.caption("Fast • Clean • Face Recognition System")

# ---------- LAYOUT ----------
col1, col2, col3 = st.columns(3)

# ---------- REGISTER ----------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Register Student")

    with st.form("register_form"):
        name = st.text_input("Student Name")
        submit = st.form_submit_button("Capture Face")

        if submit:
            if name:
                with st.spinner("Capturing faces..."):
                    subprocess.run(["python", "capture_faces.py", name])
                st.success("✅ Capture Complete")
            else:
                st.warning("Enter name first")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TRAIN ----------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Train Model")

    if st.button("Train Now"):
        with st.spinner("Training model..."):
            subprocess.run(["python", "train_model.py"])
        st.success("✅ Model Trained")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RECOGNITION ----------
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎥 Start Recognition")

    if st.button("Start Camera"):
        with st.spinner("Running recognition..."):
            subprocess.run(["python", "recognize_faces_knn.py"])

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ATTENDANCE TABLE ----------
st.markdown("## 📅 Attendance Records")


def load_data():
    if os.path.exists("attendance/attendance.csv"):
        return pd.read_csv(
            "attendance/attendance.csv",
            names=["Name", "Date", "Time"]
        )
    return pd.DataFrame()

data = load_data()
if not data.empty:
    # st.dataframe(data, use_container_width=True)
    st.dataframe(data,width='stretch')
else:
    st.info("No attendance records yet")
