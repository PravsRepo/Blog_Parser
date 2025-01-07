# README for Blog Parser

## INSTALLATION

> Create virtual environment

    $ python -m venv venv

> Activate the environment

    $ source venv/bin/activate

> pip install -r requirements.txt

## Configuration details

    config.ini - contains the all input and output paths

## Folder structure

    - html
        - css
        - template
    - images
        - large
        - thumbnails
    - src
    - venv (Virtual environment)
    - README.md
    - requirements.txt

## How to Run?

    $ python src/blog_parser.py <file.HTML>

    example:
    $ python src/blog_parser.py sampleblog.html

    * Note: This script creates an output file named <file_pics.html> in the output folder

## Notes

    $ The title text is determined based on the name of the input HTML file.
    example:
    $ input file name - sampleblog.html
    $ Title text - sampleblog


    $ The image names should be same in both the {input}.html file and the images directory. 
    example:
    $ test.html - The image name {{image1.jpg}}
                                 --------------
    $ images directory - The image name {{image1.jpg}}
                                        ---------------   