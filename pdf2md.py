import glob
from mdutils.mdutils import MdUtils
import os
from pdf2image import convert_from_path
import shutil


def _mkdir(dir):
    """
    Create or overwrite new directory
    """
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def _get_images(fname):
    """
    Convert multipage pdf to image object with separate images
    """
    return convert_from_path(fname)


def _create_md(fname, title):
    """
    Create empty markdown file
    """
    return MdUtils("out/" + fname, title)


def _fill_md(md, images):
    """
    Fill empty markdown file with title and images
    """
    for i, image in enumerate(images):
        fname = "img" + str(i) + ".jpg"
        path = "img/" + fname
        image.save("out/" + path, "JPEG")
        md.new_line(md.new_inline_image(text="", path=path))
    return md


def _save_md(md):
    """
    Save markdown file
    """
    md.create_md_file()


def _zip(fname):
    return shutil.make_archive(fname, 'zip', "out")


def main():
    _mkdir("out")
    _mkdir("out/img")

    pdf = glob.glob("your_pdf/*.pdf")[0]
    images = _get_images(pdf)

    md = _create_md("file", "Headline")
    md = _fill_md(md, images)
    _save_md(md)
    _zip("out")


if __name__ == "__main__":
    main()
