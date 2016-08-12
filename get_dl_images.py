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
Given a map of class names to urls (without the base url) and a div,
this method will find an image on the carousel's display and return
the url, or None if no image that would be displayed could be found.
'''
def get_div_image_url(images, div):
  # == Print images loaded from the css file == #
  for used_class in div['class']:
    if used_class in images:
      return images[used_class]

  # == Print images loaded from the html file == #
  if 'text-image' in div['class']:
    return div.find_all('img')[0]['src']

  return None

'''
Takes a dictionary representing key and keyCount and returns a formatted
string representing the number of times each key was tallied
'''
def list_types(image_types):
  type_counts = []

  for key in image_types.iterkeys():
    value = image_types[key]
    if value is not 1:
      type_counts.append(str(value) + ' ' + key + 's')
    else:
      type_counts.append('1 ' + key)

  return '(' + ', '.join(type_counts) + ')'

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

print ''
num_photos = 0
urls = []

for div in divs:
  url = get_div_image_url(images, div)
  if url != None:
    urls.append(url)

    file_type = url.split('.')[-1]
    add_key_tally(image_types, file_type)

for url in sorted(urls):
  print baseUrl + url

print '\n' + str(len(urls)) + ' images found ' + list_types(image_types)
