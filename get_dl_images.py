baseUrl = 'http://deeplocal.com'
cssUrl = 'http://www.deeplocal.com/assets/style/css/main.css'

# Supports python 2 and 3
from six.moves import urllib
from bs4 import BeautifulSoup

response = urllib.request.urlopen(baseUrl)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

response = urllib.request.urlopen(cssUrl)
css = response.read()

# ================== #
# = Helper Methods = #
# ================== #

'''
Given the two relevant lines in a CSS file, add the targeted
css classes as keys mapped to the image url path (without the base url)
'''
def process_image_lines(images, line1, line2):
  #   .class.otherClass.targetClass, .class.otherClass.targetClass2, .class.otherClass.targetClass3 { 
  line1 = line1.strip()
  line1 = line1[:-2] # Remove the ' {'
  classes = line1.split(', ')

  # Get target class
  classes = [c.split('.')[-1] for c in classes]

  #   background-image: url("/assets/imgs/projects/food-truck/excited.jpg"); }
  line2 = line2.split('url("')[1]
  url = line2.split('"')[0]

  for key in classes:
    images[key] = url

'''
Maps css classes to the associated urls found in the css file
'''
def generate_image_dictionary():
  images = dict()

  last_line = ''
  for line in css.split('\n'):
    if 'url("/assets/imgs/' in line:
      process_image_lines(images, last_line, line)
    last_line = line

  return images

'''
Takes a dictionary representing key and keyCount and returns a formatted
string representing the number of times each key was tallied
'''
def list_types(image_types):
  # TODO: Implement
  return '(type count not implemented)'

'''
Takes a dictionary and a key and will add one to the value of the key
or start a tally if none exists
'''
def add_key_tally(d, key):
  if key in d:
    d[key] += 1
  else:
    d[key] = 1

# =============== #
# = Main Script = #
# =============== #

# Retrieve the relevant information about images and which are used
divs = [div for div in soup.find_all('div', 
        attrs = {'class': 'section'}) 
        if 'news' not in div['class']] # news sections do not contain images

images = generate_image_dictionary()
image_types = dict()

def get_div_image_url(div):
  return None

print ''
num_photos = 0

for div in divs:
  url = get_div_image_url(div)
  if url != None:
    print baseUrl + url
    
    file_type = url.split('.')[-1]
    add_key_tally(image_types, file_type)
    num_photos += 1

print '\n' + str(num_photos) + ' images found ' + list_types(image_types)
