import mysql.connector
from PIL import Image
import io
import os
import streamlit as st

# Connect to the MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sowmi@123",
    database="storage"
)
st.title("DETECTED IMAGES 🖼️")

# Retrieve all image data from the database
cursor = cnx.cursor()
query = "SELECT images FROM computer_vision"  # Modify the query as per your table structure
cursor.execute(query)
results = cursor.fetchall()

# Create a directory to store the retrieved images
output_dir = "retrieved_images"
os.makedirs(output_dir, exist_ok=True)

# Iterate over the results and display each image in Streamlit
for i, result in enumerate(results):
    image_data = result[0]
    image = Image.open(io.BytesIO(image_data))
    st.image(image, caption=f"Retrieved Image {i+1}")

    # Save the image to the output directory
    image_path = os.path.join(output_dir, f"retrieved_image_{i+1}.png")
    image.save(image_path)

# Close the cursor and the database connection
cursor.close()
cnx.close()

st.success(f"All images retrieved and saved to the {output_dir} directory.")
