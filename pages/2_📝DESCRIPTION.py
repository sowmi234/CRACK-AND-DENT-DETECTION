import streamlit as st

def main():
    st.title("DESCRIPTION")

    # Display video from a local file
    video_path = "assets/Description.mp4"
    st.video(video_path)

if __name__ == '__main__':
    main()
