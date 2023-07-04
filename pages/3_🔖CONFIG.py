from pathlib import Path
import PIL
import mysql.connector
import io

# External packages
import streamlit as st

# Local Modules
import settings
import helper

def show_slider_page(confidence, model):
    # Establish database connection
    cnx = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Sowmi@123",
        database="storage"
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Model Options
    model_type = st.selectbox(
        "Select Task", ['Detection', 'Segmentation', 'New Model'])

    # Selecting Detection, Segmentation, or New Model
    if model_type == 'Detection':
        model_path = Path(settings.DETECTION_MODEL)
    elif model_type == 'Segmentation':
        model_path = Path(settings.SEGMENTATION_MODEL)
    elif model_type == 'New Model':
        model_path = Path(settings.NEW_MODEL)
    else:
        st.error("Please select a valid model type!")
        return

    # Load Pre-trained ML Model
    try:
        model = helper.load_model(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)
        return

    source_radio = st.radio(
        "Select Source", settings.SOURCES_LIST)

    source_img = None
    # If image is selected
    if source_radio == settings.IMAGE:
        source_img = st.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

        if source_img is not None:
            try:
                uploaded_image = PIL.Image.open(source_img)

                col1, col2 = st.columns(2)

                with col1:
                    st.image(source_img, caption="Uploaded Image",
                             use_column_width=True)

                with col2:
                    pass

                if st.button('Detect Flaws'):
                    with col2:
                        res = model.predict(uploaded_image, conf=confidence)
                        boxes = res[0].boxes
                        res_plotted = res[0].plot()[:, :, ::-1]
                        st.image(res_plotted, caption='Detected Image',
                                 use_column_width=True)
                        try:
                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.data)
                        except Exception as ex:
                            st.write("No image is uploaded yet!")

                        # Convert the image to bytes
                        computer_vision_bytes = io.BytesIO()
                        PIL.Image.fromarray(res_plotted).save(computer_vision_bytes, format='PNG')
                        computer_vision_bytes = computer_vision_bytes.getvalue()
                        # Store the image data in the database
                        query = "INSERT INTO computer_vision (images) VALUES (%s)"
                        cursor.execute(query, (computer_vision_bytes,))
                        cnx.commit()

            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)

    elif source_radio == settings.VIDEO:
        helper.play_stored_video(confidence, model)

    elif source_radio == settings.WEBCAM:
        helper.play_webcam(confidence, model)

    else:
        st.error("Please select a valid source type!")

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()

# Setting page layout
st.set_page_config(
    page_title="CRACKS AND DENTS DETECTION",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("CRACKS AND DENTS DETECTION 🤖 ")

confidence = float(st.slider("Select Model Confidence", 25, 100, 40)) / 100
show_slider_page(confidence, model=None)
