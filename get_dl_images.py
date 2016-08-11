baseUrl = 'http://deeplocal.com'
cssUrl = 'http://www.deeplocal.com/assets/style/css/main.css'

# Supports python 2 and 3
from six.moves import urllib

response = urllib.request.urlopen(baseUrl)
html = response.read()

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
Looks through the current html setup and determines which classes are used
'''
def retrieve_used_classes():
  # TODO: Implement
  return []

'''
Takes a dictionary representing key and keyCount and returns a formatted
string representing the number of times each key was tallied
'''
def list_types(image_types):
  # TODO: Implement
  return '(type count not implemented)'
# =============== #
# = Main Script = #
# =============== #

# Retrieve the relevant information about images and which are used
images = generate_image_dictionary()
used_classes = retrieve_used_classes()

# Empty line before printing found images
print ''

image_types = dict()
for used_class in used_classes:
  if images[used_class]:
    print baseUrl + images[used_class]

print '\n' + str(len(used_classes)) + ' images found ' + list_types(image_types)