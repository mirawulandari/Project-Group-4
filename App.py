import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import io
import os
import math

# Path to the university logo
logo_path = "university_logo.png"  # Adjust with your file location

# Path to member photos
foto_mira = "mira_wulandari.jpg"  # Adjust with Mira's photo path
foto_yohanes = "yohanes_priyoko.jpg"  # Adjust with Yohanes' photo path

# Menu navigation
menu = st.sidebar.radio("Select a page", ["Home", "Member Group 4", "Image Transformations"])

# Display university logo on all menus (without the caption below)
if os.path.exists(logo_path):
    st.image(logo_path, width=200, use_container_width=False, output_format="auto")
else:
    st.error(f"Logo not found at {logo_path}")

# Custom font styling for markdown content
st.markdown("""
    <style>
    .title {
        font-family: 'Arial', sans-serif;
        font-size: 36px;
        text-align: center;
        color: #333;
    }
    .subheader {
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        color: #444;
    }
    .paragraph {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Menu 1: Home
if menu == "Home":
    # Display title as "Linear Algebra Group 4" with a border frame
    st.markdown(
        """
        <div style='border-top: 3px solid black; border-right: none; border-left: none; border-bottom: 3px solid black; 
                    width: fit-content; padding: 10px; margin-left: 0;'>
            <h1 style="margin: 0;">Linear Algebra Group 4</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.subheader("Welcome to Group 4's Project on Image Processing.")
    
    # Paragraph with larger font size
    st.markdown(
        "<p class='paragraph'>This Streamlit application showcases the contributions of Group 4 in the Image Processing course. Explore the page to learn more about us, view various examples, and delve into the concepts we have worked on.</p>", 
        unsafe_allow_html=True
    )

    st.write("Study Program: *Industrial Engineering*")
    st.write("Faculty: *Engineering*")

# Menu 2: Member Group 4
elif menu == "Member Group 4":
    st.title("Member Group 4")
    st.markdown("### Meet Our Team:")

    # Display member names with buttons
    if st.button("Mira Wulandari"):
        # Show photo only after button is clicked
        if os.path.exists(foto_mira):
            st.image(foto_mira, caption="Mira Wulandari", width=200)
        else:
            st.error("Mira Wulandari's photo not found.")
    
    if st.button("Yohanes Surya Priyoko"):
        # Show photo only after button is clicked
        if os.path.exists(foto_yohanes):
            st.image(foto_yohanes, caption="Yohanes Surya Priyoko", width=200)
        else:
            st.error("Yohanes Surya Priyoko's photo not found.")

# Menu 3: Image Transformations
elif menu == "Image Transformations":
    st.title("Image Transformation Application")
    st.write("Upload your image and choose the desired effect.")

    # Upload image file
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png", "pdf"])
    if uploaded_file:
        try:
            # Open the uploaded image
            image = Image.open(io.BytesIO(uploaded_file.read()))
            st.image(image, caption="Original Image", width=200)

            # Choose image effect
            option = st.selectbox(
                "Choose image effect:",
                ["Rotation", "Scaling", "Translation", "Skew", "Distortion", "Contours", "Greyscale"]
            )

            # Apply selected effect
            if option == "Rotation":
                # Rotation: control for rotation angle
                angle = st.slider("Select Rotation Angle (degrees)", -180, 180, 0)
                processed_image = image.rotate(angle)

            elif option == "Scaling":
                # Scaling: control for scaling in x and y axis
                scale_x = st.slider("Select Scaling Factor (X axis)", 0.1, 3.0, 1.0)
                scale_y = st.slider("Select Scaling Factor (Y axis)", 0.1, 3.0, 1.0)

                # Calculate new size based on scaling factors
                new_size = (int(image.width * scale_x), int(image.height * scale_y))
                processed_image = image.resize(new_size)

            elif option == "Translation":
                # Translation: control for translation (shifting) along x and y axes
                translate_x = st.slider("Select Translation (X axis)", -image.width, image.width, 0)
                translate_y = st.slider("Select Translation (Y axis)", -image.height, image.height, 0)

                # Apply translation (shifting)
                translation_matrix = [1, 0, translate_x, 0, 1, translate_y]
                processed_image = image.transform(image.size, Image.AFFINE, translation_matrix)

            elif option == "Skew":
                # Skew: control for skew (shearing) effect along x and y axis
                skew_x = st.slider("Select Skew Factor (X axis)", -50, 50, 0)
                skew_y = st.slider("Select Skew Factor (Y axis)", -50, 50, 0)

                # Apply skew (shearing)
                skew_matrix = [
                    1, math.tan(math.radians(skew_x)), 0, 
                    math.tan(math.radians(skew_y)), 1, 0
                ]
                processed_image = image.transform(image.size, Image.AFFINE, skew_matrix)

            elif option == "Distortion":
                # Control for distortion level
                blur_radius = st.slider("Blur Level (radius)", 0, 10, 5)
                processed_image = image.filter(ImageFilter.GaussianBlur(blur_radius))

            elif option == "Contours":
                # Contour effect using ImageFilter.CONTOUR
                processed_image = image.filter(ImageFilter.CONTOUR)

            elif option == "Greyscale":
                # Convert image to greyscale
                processed_image = image.convert("L")

            # Display processed image
            st.image(processed_image, caption="Processed Image", width=200)

            # Convert image to byte format for download
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Download button
            download_format = st.selectbox("Choose download format:", ["PNG", "JPG", "PDF"])
            file_extension = download_format.lower()
            st.download_button(
                label="Download Image",
                data=byte_im,
                file_name=f"processed_image.{file_extension}",
                mime=f"image/{file_extension}"
            )
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.warning("Please upload an image first!")
