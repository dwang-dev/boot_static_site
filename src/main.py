from helpers import copy_directory_contents_recursive, generate_page_recursive
import sys
import os
import shutil

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_directory_contents_recursive(dir_path_static, dir_path_public)
    generate_page_recursive(from_path=dir_path_content, template_path=template_path, dest_path=dir_path_public, basepath=basepath)

if __name__ == "__main__":
    main()