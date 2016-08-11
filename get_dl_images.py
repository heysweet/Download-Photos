baseUrl = 'http://deeplocal.com'

# Supports python 2 and 3
from six.moves import urllib

response = urllib.request.urlopen(baseUrl)

html = response.read()

print html