import pytesseract as tess
from PIL import Image	

import urllib.request
from PIL import Image

async def imageToText(url):
	# get the image from the url, setting to a known browser agent 
	# because of mod_security or some similar server security feature
	# which blocks known spider/bot user agents 
	class AppURLopener(urllib.request.FancyURLopener):
		version = "Mozilla/5.0"

	opener = AppURLopener()
	response = opener.open(url)

	img = Image.open(response)

	#access tesseract module
	tess.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract-OCR/tesseract.exe'
	result = tess.image_to_string(img)
	#remove an auto added character at the beginning of the string if the image had no text
	print("analuyzying")
	print(result)

	return  result[:-1]