import streamlit as st

# Setting page layout
st.set_page_config(
    page_title="CRACK AND DENT DETECTION",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<link rel="stylesheet" href="assets/styles.css">', unsafe_allow_html=True)

# Main page heading
st.markdown('<div class="title-wrapper"><h1>CRACKS AND DENTS DETECTION 🤖</h1></div>', unsafe_allow_html=True)
# Sidebar
# Home page
st.subheader("Explore the limitless possibilities of computer vision in your own projects.")

st.video("assets/COMPUTER VISION.mp4")

    # Get Started button
if st.button("Get Started"):
        # Add your logic for the desired functionality when the button is clicked
    pass



