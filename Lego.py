#  This code will pixelate an image and export X and Y coordinates, along with a Tableau color palette.
#  The goal of the code is to allow you to then plot the image in Tableau as Legos.
#
#  Written by Ken Flerlage, March, 2020
#
#  This code is in the public domain
#----------------------------------------------------------------------------------------------------------------------------------------

from base64 import b16encode
import math
import sys
import os
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from tkinter import Tk
import PySimpleGUI as sg

#---------------------------------------------------------------------------------------------------------------------------------------- 
# Prompt for the input image file.
#---------------------------------------------------------------------------------------------------------------------------------------- 
def get_image_file():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select Original Image File",filetypes = (("Image Files",".png .jpg .jpeg"),("All Files","*.*")))
    root.withdraw()

    return root.filename 

#---------------------------------------------------------------------------------------------------------------------------------------- 
# Convert RGB to hex
#---------------------------------------------------------------------------------------------------------------------------------------- 
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

#----------------------------------------------------------------------------------------------------------------------------------------
# # Main processing routine.
#----------------------------------------------------------------------------------------------------------------------------------------

# Build simple form to get user input.
form = sg.FlexForm('Lego') 

layout = [
          [sg.Text('How many columns?')],
          [sg.Text('Columns', size=(10, 1)), sg.InputText('25', size=(6,1))],
          [sg.Submit(), sg.Cancel()]
         ]

button, values = form.Layout(layout).Read()

# Check to see if the user canceled, closed the dialog, or entered an invalid value.
if button == "Cancel" or button is None or not(values[0].isdigit()):
    messagebox.showinfo("Error", "You either canceled/closed the dialog or entered an invalid parameter. Exiting the program.")
    sys.exit() 

# Continue processing.
form.Close()
columnCount = int(values[0])

# Initiatlize variables and constants.
colorList = []
tileNum = 1

# Prompt for the image file.
imgin = get_image_file()

if imgin == "":
    messagebox.showinfo("Error", "No file selected. Program will now quit.")
    sys.exit()

# Set output files to write to the same folder.
filepath = os.path.dirname(imgin)
if filepath[-1:] != "/":
    filepath += "/"

outFile = filepath + 'Tiles.csv'
colorFile = filepath + 'Colors.csv'

out = open(outFile,'w') 
outColor = open(colorFile,'w') 

# Write header of the tiles file.
outString = 'ID,X,Y,Color ID'
out.write (outString)
out.write('\n')

# Write header of the color file.
outString = 'Color ID,Hex Color'
outColor.write (outString)
outColor.write('\n')

# Open the image and convert to RGB.
img = Image.open(imgin, 'r')
img = img.convert('RGB')
width = img.size[0] 
height = img.size[1]

# Determine tile size (widht and height) and determine number of rows.
tileSize = width/columnCount
rowCount = int(height/tileSize)

# Loop through columns and rows, find the center point of the tile, and get the color.
for col in range(1, columnCount+1):
    for row in range(1, rowCount+1):
        centerX = (col-1)*tileSize + (tileSize/2)
        centerY = (row-1)*tileSize + (tileSize/2)

        # Get the color of this pixel.
        RGB = img.getpixel((centerX, centerY))
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]

        # Convert the color to hex
        hexColor = rgb_to_hex(RGB)

        # Is this color already in the list?
        try:
            ind = colorList.index(hexColor)
        except ValueError:
            colorList.append(hexColor)

        # Write the tile to the file.
        ind = colorList.index(hexColor)
        outString = str(tileNum) + ',' + str(centerX) + ',' + str(centerY) + ',' + str(ind) 
        out.write (outString)
        out.write('\n')

        tileNum += 1

out.close()

# Write the final color file.
ind = 0
for color in colorList:
    outString = str(ind) + ',<color>#' + color + '</color>'
    outColor.write (outString)
    outColor.write('\n')
    ind += 1

outColor.close()

messagebox.showinfo('Complete', 'Output files--tiles.csv and colors.csv--have been written to the following directory: ' + filepath)
