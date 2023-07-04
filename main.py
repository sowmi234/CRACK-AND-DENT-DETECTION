import streamlit as st

def main():
    st.title("CRACK AND DENT DETECTION 🤖")
    # Display video from a local file
    image_path = "assets/main.png"
    st.image(image_path)

if __name__ == '__main__':
    main()