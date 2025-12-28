from src.textnode import TextNode, TextType
from src.helpers import clear_dir, copy_directory_contents_recursive, generate_page_recursive

source_path = "./static"
template_path = "./template.html"
dest_path = "./public"

def main():
    clear_dir(dest_path)
    copy_directory_contents_recursive(source_path, dest_path)
    generate_page_recursive(from_path="./content", template_path=template_path, dest_path=dest_path)

if __name__ == "__main__":
    main()