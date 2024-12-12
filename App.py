import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import io
import os
import math

# Path ke logo universitas
logo_path = "university_logo.png"  # Sesuaikan dengan lokasi file Anda

# Sidebar untuk navigasi menu dan logo
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, caption="President University", use_column_width=True)
else:
    st.sidebar.error(f"Logo tidak ditemukan di {logo_path}")

menu = st.sidebar.radio("Pilih Menu", ["About Group 4", "Application"])

# Menu 1: About Group 4
if menu == "About Group 4":
    st.title("Project Group 4")
    st.subheader("Linear Algebra")
    st.write("Study Program: *Industrial Engineering*")
    st.write("Faculty: *Engineering*")
    st.markdown("### Member Group 4:")
    st.write("1. Mira Wulandari")
    st.write("2. Yohanes Surya Priyoko")

    # Menampilkan foto anggota kelompok
    foto_mira = "mira_wulandari.jpg"  # Ganti dengan path foto Mira
    foto_yohanes = "yohanes_priyoko.jpg"  # Ganti dengan path foto Yohanes

    if os.path.exists(foto_mira) and os.path.exists(foto_yohanes):
        st.image([foto_mira, foto_yohanes], caption=["Mira Wulandari", "Yohanes Surya Priyoko"], width=200)
    else:
        st.error("Foto anggota kelompok tidak ditemukan.")

# Menu 2: Application
elif menu == "Application":
    with st.container():
        st.title("Aplikasi Pemrosesan Gambar")
        st.write("Unggah gambar Anda dan pilih efek pemrosesan yang diinginkan.")

        # Upload file gambar
        uploaded_file = st.file_uploader("Unggah gambar Anda", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            # Membuka gambar
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar Asli", use_container_width=True)

            # Pilihan efek pemrosesan
            option = st.selectbox(
                "Pilih efek gambar:",
                ["Rotasi", "Translasi", "Skala", "Distorsi", "Kontur", "Greyscale", "Kemiringan"]
            )

            # Terapkan efek
            if option == "Rotasi":
                angle = st.slider("Pilih Sudut Rotasi (derajat)", -180, 180, 0)
                processed_image = image.rotate(angle)

            elif option == "Kemiringan":
                skew_angle = st.slider("Pilih Sudut Kemiringan (derajat)", -45, 45, 0)

                # Mengonversi derajat ke radian
                skew_radian = math.radians(skew_angle)

                # Matriks transformasi affine untuk kemiringan
                transform_matrix = (1, math.tan(skew_radian), 0, 0, 1, 0)

                # Terapkan transformasi ke gambar
                processed_image = image.transform(image.size, Image.AFFINE, transform_matrix, resample=Image.NEAREST)

            elif option == "Translasi":
                # Kontrol untuk translasi
                x_shift = st.slider("Geser Horizontal (px)", -500, 500, 0)
                y_shift = st.slider("Geser Vertikal (px)", -500, 500, 0)
                # Translasi menggunakan transformasi afine
                processed_image = image.transform(
                    image.size,
                    Image.AFFINE,
                    (1, 0, x_shift, 0, 1, y_shift),
                    resample=Image.NEAREST
                )

            elif option == "Skala":
                # Kontrol untuk skala
                scale_factor = st.slider("Faktor Skala", 0.1, 3.0, 1.0)
                width, height = image.size
                new_size = (int(width * scale_factor), int(height * scale_factor))
                processed_image = image.resize(new_size)

            elif option == "Distorsi":
                # Kontrol untuk tingkat distorsi
                blur_radius = st.slider("Tingkat Blur (radius)", 0, 10, 5)
                processed_image = image.filter(ImageFilter.GaussianBlur(blur_radius))

            elif option == "Kontur":
                # Efek Kontur menggunakan ImageFilter.CONTOUR
                processed_image = image.filter(ImageFilter.CONTOUR)

            elif option == "Greyscale":
                # Efek Greyscale untuk mengubah gambar menjadi hitam-putih
                processed_image = image.convert("L")

            # Tampilkan hasil
            st.image(processed_image, caption="Gambar Diproses", use_container_width=True)

            # Konversi gambar ke format byte untuk unduhan
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Tombol unduh
            download_format = st.selectbox("Pilih format unduhan:", ["PNG", "JPG", "JPEG"])
            file_extension = download_format.lower()
            st.download_button(
                label="Unduh Gambar",
                data=byte_im,
                file_name=f"processed_image.{file_extension}",
                mime=f"image/{file_extension}"
            )
        else:
            st.warning("Harap unggah gambar terlebih dahulu!")
