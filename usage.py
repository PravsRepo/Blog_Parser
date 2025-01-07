import argparse
import sys
import os


def main():
    description = '''

    This script creates a responsive HTML blog from the input HTML file.

    1. Inside the input file, image names should be enclosed within double curly braces, for example, {{image1.jpg}} or {{image2.jpg|image3.jpg}}.
    2. The script selectively extracts image names that are enclosed within the curly braces.
    3. It verifies that the extracted image names correspond to files existing in the designated image directory and retrieves their details for subsequent processing.
    4. Subsequently, these identified images are substituted with div tags to enhance the responsiveness of the blog layout.
    5. Finally, the resulting output file is saved within the current directory.


    ----------------------For further information read README.md-----------------------------
    '''

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', metavar='input_file.HTML', type=str,
                        nargs='?')

    # Parse command-line arguments
    args = parser.parse_args()
    filename = sys.argv[1]
    
    # Check if input_file argument is provided
    if not filename.endswith('.html'):
        print("-----------------------------------------------------------------------------------")
        print(f"\nError: Invalid command-line argument.")
        print("\nThe command line argument format is python src/blog_parser.py input_file.html\n")
        print("-----------------------------------------------------------------------------------")
        sys.exit(1)

    # Check if input_file is exist in the directory
    if not os.path.isfile(filename):
        print("-----------------------------------------------------------------------------------")
        print(f"\nError: Entered Input file '{filename}' does not exist.\n")
        print("-----------------------------------------------------------------------------------")
        sys.exit(1)
