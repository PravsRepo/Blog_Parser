'''
    This class is used to create a blog from the sample blog.
    
    Author: praveen@leap.respark.iitm.ac.in
    Date: 31 Aug, 2023
    Version: 1.0
'''

import os
import re
import shutil
import copy

from bs4 import BeautifulSoup
from PIL import Image


class HtmlParser:
    '''
        This class is used to parse the html file.
    '''

    def __init__(self, file_name, config, logger):
        '''
            This is the constructor of the class.
        '''
        self.config = config
        self.logger = logger
        self.file_path = file_name
        self.soup = None

        self.logger.info('The program has started...')
        self.logger.debug('Parsing the html file: %s', self.file_path)
        self.logger.info('Initiated the variables')

    def parse(self):
        '''
            This method is used to parse the html file.
        '''
        try:
            with open(self.file_path, 'r') as file:
                soup = BeautifulSoup(file, 'html.parser')
            self.soup = soup
            self.logger.info(f'{self.file_path} file read successfully and html parse tree has been created.')
        except Exception as e:
            self.logger.error(f'Error reading {self.file_path}: ', e)
            exit()

    def get_header(self):
        '''
            This method is used to get the header of the html file.
        '''
        try:
            # extract the body in the parse tree, leaving the rest of the code intact.
            body_tag = self.soup.body.extract()
            self.logger.info('The body extracted from the parse tree')
            return self.soup, body_tag
        except:
            self.logger.info('Parse tree has no body tag.')
            exit()

    def get_body(self, body):
        '''
            This method is used to get the body of the html file.
        '''
        return body

    def blog_title(self, soup, body, filename):
        '''
            This method is used to change the title tag string in the head tag.
        '''
        title_tag = soup.title
        body_ptag_title = copy.copy(body.find('p', class_='Title'))
        body_ptag_title_text = body_ptag_title.string
        if body_ptag_title:  # If the 'Title' class exist, it uses to replace the title tag string in the <head>
            title_tag.string.replace_with(body_ptag_title_text)
            self.logger.info(
                f'The title of the blog is "{title_tag.string}" added successfully.')
            return soup
        else:  # If the 'Title' class <p> tag not found, uses the input file name to replace the title tag string in the <head>
            title_tag.string.replace_with(filename)
            self.logger.info(
                f'The title of the blog is "{title_tag.string}" added successfully.')
            return soup

    def get_piwik(self, file_path):
        '''
            This method is used to get the piwik code from the piwik.html file.
        '''
        try:
            with open(file_path, 'r') as piwik:
                piwik_soup = BeautifulSoup(piwik, "html.parser")
                self.logger.info(f'{os.path.basename(file_path)} file read successfully.')
            return piwik_soup
        except Exception as e:
            self.logger.error(f'Error reading {file_path}:', e)

    def get_respdiv(self, file_path):
        '''
            This method is used to get the respdiv code from the respdiv.html file.
        '''
        try:
            with open(file_path, 'r') as respdiv:
                respdiv_soup = BeautifulSoup(respdiv, "html.parser")
            self.logger.info(f'{os.path.basename(file_path)} file read successfully.')
            return respdiv_soup
        except Exception as e:
            self.logger.error(f'Error reading {file_path}:', e)
            exit()

    def get_all_image_details(self):
        '''
            This method is used to get the image details from the image_directory.
        '''
        img_extension = ("jpg", "jpeg", "png", "gif", "svg")
        image_detail_large = {}
        image_detail_thumbnail = {}
        # this try is for to get the image details from ../images/large directory
        try: 
            all_files_large = os.listdir(self.config['IMAGE_DIR_LARGE'])
            files_large = [file for file in all_files_large if file.endswith(img_extension)]
            for large in files_large:
                image_detail_large[large] = self.get_image_description(self.config['IMAGE_DIR_LARGE']+large)
    
            self.logger.info("The image details are collected from the LARGE directory.")
        except:
            self.logger.error('Entered large image directory is not found, please check the path.')
            print("\n\nERROR: Large path not found, please check it.\n\n")
            exit()

        # this try is for to get the image details from ../images/thumbnail directory  
        try:
            all_files_thumbnail = os.listdir(self.config['IMAGE_DIR_THUMBNAILS'])
            files_thumbnail = [file for file in all_files_thumbnail if file.endswith(img_extension)]
            for thumbnail in files_thumbnail:
                image_detail_thumbnail[thumbnail] = self.get_image_description(self.config['IMAGE_DIR_THUMBNAILS']+thumbnail)

            self.logger.info("The image details are collected from the thumbnail directory.")
        except:
            self.logger.error('Entered thumbnail image directory is not found, please check the path.')
            print("\n\nERROR: Thumbnail path not found, please check it.\n\n")
            exit()
        return image_detail_large, image_detail_thumbnail
    
    def get_image_description(self, image_file):
        '''
            This method is used to get the image description of all images.
        '''
        image_name = os.path.basename(image_file)
        try:
            image = Image.open(image_file)
            data = image.getexif()
            self.logger.info(f'{image_name}   :   {data[270]}')
            return data[270]
        except Exception as e:
            self.logger.info(f'{image_name}   :   {image_file} This image file do not have description.')
            return image_name

    def copy_css_to_output(self):
        try:
            input_css_dir = self.config['CSS_DIR']
            output_path = self.config['OUTPUT_DIR']
            shutil.copy(input_css_dir+'respgal.css', output_path)
            self.logger.info("Copied respgal.css to the output folder")
            return
        except Exception as e:
            self.logger.info("Error copying the respgal.css", e)

    def create_css_link(self, soup):
        '''
            This method creates a css_link
        '''
        css_link = soup.new_tag('link', href='respgal.css', rel='stylesheet')
        self.logger.info(f'Created CSS file link: {css_link}')
        return css_link

    def create_ptag(self, soup):
        '''
            This method creates a p tag
        '''
        p_tag = soup.new_tag('p', style='clear:both')
        self.logger.info(f'Created p tag: {p_tag}')
        return p_tag

    def get_imagename_in_body(self, body, ptag, image_detail_large, image_detail_thumbnail):
        '''
            This method is used to get the image name inside the curly braces from the body tag.
        '''
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        p_tags = body.find_all(tags)
        search_pattern = r"{{(.*?)}}"
        image_pattern = re.compile(search_pattern)
        body.clear()
        for p_tag in p_tags:
            text = p_tag.get_text()
            if image_pattern.search(text):
                matches = re.findall(search_pattern, text)
                if "|" in str(matches):
                    image_names = []
                    for match in matches:
                        result = match.split("|")
                        image_names.extend(result)
                    matches = image_names.copy()
                span_tag = p_tag.find('span')
                if span_tag:
                    span_tag.clear()
                else:
                    p_tag.clear()
                for match in matches:
                    output = self.image_replace(match.strip(), image_detail_large, image_detail_thumbnail)
                    if span_tag:
                        span_tag.append(output)
                    else:
                        p_tag.append(output)
                p_tag = BeautifulSoup(str(p_tag)+str(ptag), "html.parser")
            body.append(p_tag)
        self.logger.info(
            'Successfully for each image name inside the curly braces has been changed with respdiv.html')
        return body

    def image_replace(self, image_name, image_detail_large, image_detail_thumbnail):
        '''
            This method replaces the image name and description and returns the respdiv.
        '''
        # print("Working...")
        respdiv = self.get_respdiv(self.config['TEMPLATE_DIR']+'respdiv.html')
        a_tag = respdiv.find('a')
        img_tag = respdiv.find('img')
        div_tag = respdiv.find('div', class_="desc")
       
        # check image_name is exist or not
        if image_name != "":
            try:
                description = image_detail_thumbnail[image_name]
                img_tag['src'] = 'images/'+'thumbnails/'+image_name
                div_tag.string = description
            except KeyError:
                print(f'\n\nERROR:The {image_name} is not found in the thumbnail directory\n\n')
                self.logger.ERROR(f'The {image_name} is not found in the thumbnail directory.')
                exit()
                
            try:
                if image_detail_large[image_name]:
                    a_tag['href'] = 'images/'+'large/'+image_name
            except:
                print(f'\n\nERROR:The {image_name} is not found in the large directory\n\n')
                self.logger.ERROR(f'The {image_name} is not found in the large directory.')
                a_tag['href'] = 'images/'+'large/'+'image_name'

            self.logger.info(f'{image_name} and description are replaced in the respdiv.html')
            return respdiv
        else:
            return ""

    def insert_piwik_css(self, soup, piwik, css_link, replace_body):
        '''
            This method inserts the piwik code, css link and the new body tags into the head tag and 
            returns the main html code.
        '''
        head_tag = soup.head
        style_tag = head_tag.style
        style_tag.insert_after(piwik)
        head_tag.append(css_link)
        soup.html.append(replace_body)
        self.logger.info(
            'Successfully inserted the piwik code, css link and body tag and returns the output html code.')
        return soup

    def write_html(self, html_soup, file_name):
        '''
            This method write the html and save the file name as sampleblog_pic.html into the 
            output folder.
        '''
        try:
            with open(file_name, 'w') as output_file:
                output_file.write(html_soup)
            self.logger.info(
                f'The output html code has been written in the {file_name}, and saved in the output folder.')
        except:
            self.logger.error(f'Error writing: {file_name}')
