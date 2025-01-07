import os
import sys
import logging
import usage

from makeblog import HtmlParser
from configparser import ConfigParser


src_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
parser = ConfigParser()
parser.read(['config.ini', src_dir+'/config.ini'])
config = parser['Settings']

# Create and configure logger
logging.basicConfig(filename=config['LOG_FILE'], format='%(levelname)s  |   %(message)s %(asctime)s',
                    datefmt='%d/%m/%Y %I:%M:%S %p', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)


l = len(sys.argv)
if l != 2:
    print("\nERROR: Please add filename in the args\n")
    exit()
filename = sys.argv[1]
output_filename = os.path.splitext(filename)[0]

# argparse main function
if __name__ == "__main__":
    usage.main()


parser = HtmlParser(filename, config, logger)
parser.parse()
soup, body = parser.get_header()
body = parser.get_body(body)
logger.info('The body tag has been separated from the html parse tree.')
soup = parser.blog_title(soup, body, output_filename)
piwik = parser.get_piwik(config['TEMPLATE_DIR']+'piwik.html')
image_detail_large, image_detail_thumbnail = parser.get_all_image_details()
parser.copy_css_to_output()
css_link = parser.create_css_link(soup)
ptag = parser.create_ptag(soup)
replace_body = parser.get_imagename_in_body(body, ptag, image_detail_large, image_detail_thumbnail)
html_soup = parser.insert_piwik_css(soup, piwik, css_link, replace_body)
parser.write_html(str(html_soup), file_name=config['OUTPUT_DIR']+output_filename+'_pics.html')