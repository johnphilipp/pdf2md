from mdutils.mdutils import MdUtils
import os
import pdf2image
import shutil
import streamlit as st
import tempfile


def get_md_from_path(pdf_path, pdf_fname):
    """
    Return path to `*.zip` from `*.pdf` path.
    Zip includes:
        > `img/` dir with images of each pdf slide
        > `*.md` file with references to images in img/ dir
    Zip built with a temporary dir using the `tempfile`
    library and a nested dir using the standard `os` library.
    The temporary dir is then archived as `*.zip` using the
    `shutil` library for final assembly. The temporary dir is
    deleted upon function return.
    """
    with st.spinner(text="In progress..."):
        pdf_fname = "pdf2md_" + pdf_fname.rstrip(".pdf")
        images = pdf2image.convert_from_path(pdf_path)
        temp_root_dir = tempfile.mkdtemp()
        os.mkdir(temp_root_dir + "/img")
        md = MdUtils(
            file_name=temp_root_dir + "/" + pdf_fname,
            title=pdf_fname
        )
        for i, image in enumerate(images):
            jpg_fname = "img" + str(i) + ".jpg"
            jpg_path = temp_root_dir + "/img/" + jpg_fname
            image.save(jpg_path, "JPEG")
            md.new_line(
                md.new_inline_image(
                    text="",
                    path="img/" + jpg_fname
                ))
        md = md.create_md_file()
        zip = shutil.make_archive(
            base_name=pdf_fname,
            format="zip",
            root_dir=temp_root_dir
        )
        shutil.rmtree(temp_root_dir)
        return zip


def get_md_from_bytes(pdf_file, pdf_fname):
    """
    Return path to `*.zip` from `*.pdf` byte values.
    Function creates a temporary file and calls the
    `get_md_from_path` function for main execution.
    The temporary file is deleted upon function return.
    """
    fh, temp_filename = tempfile.mkstemp()
    try:
        with open(temp_filename, "wb") as f:
            f.write(pdf_file)
            f.flush()
            return get_md_from_path(f.name, pdf_fname)
    finally:
        os.close(fh)
        os.remove(temp_filename)
