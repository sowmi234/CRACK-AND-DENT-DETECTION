import streamlit as st

def main():
    st.title("CONTACT")
    # Display video from a local file
    image_path = "assets/contact_us.png"
    st.image(image_path, caption="Contact Image")

if __name__ == '__main__':
    main()
