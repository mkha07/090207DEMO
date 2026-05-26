from PIL import Image

logo = Image.open('Icon.JPG')
logo.save('Icon.ico', format='ICO', sizes=[(255, 255)])