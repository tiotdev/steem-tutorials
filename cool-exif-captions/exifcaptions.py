"""
Configuration: Adjust these variables
"""
path = '00steemit' # Path to folder that contains image files
postaccount = 'yoursteemaccount' # Your Steem account name previously set up in the beem CLI wallet
"""
Configuration end
"""
import os
from beem import Steem
from beem.imageuploader import ImageUploader
from PIL import Image
from PIL.ExifTags import TAGS
from fractions import Fraction
walletpw = os.environ.get('UNLOCK') # Remember to set the UNLOCK environment variable before running the script

def get_exif (exif,field) :
  for (k,v) in exif.items():
     if TAGS.get(k) == field:
        return v

def process_image(imgurl):
    try:
        """ 
        Reading the Exif-Data with Pillow
        """
        img = Image.open(path+"/"+imgurl)
        exif = img._getexif()
        tmp_exp = get_exif(exif,'ExposureTime')
        tmp_focal = get_exif(exif,'FocalLength')
        tmp_fstop = get_exif(exif,'FNumber')
        ISO = "ISO "+str(get_exif(exif,'ISOSpeedRatings'))
        """
        Formatting the EXIF-Data
        """
        try:
                ExposureTime = str(Fraction(tmp_exp[0]/tmp_exp[1]).limit_denominator())+"s"
        except:
                ExposureTime = "None"
        try:
                FocalLength = str(int(tmp_focal[0]/tmp_focal[1]))+"mm"
        except: 
                FocalLength = "None"
        try: 
                FNumber = "f/"+str(tmp_fstop[0]/tmp_fstop[1])
        except:
                FNumber = "None"
        settings = "" if ExposureTime == "None" or FocalLength == "None" or FNumber == "None" or ISO == "None" else ExposureTime+"; "+FocalLength+"; "+FNumber+"; "+ISO
        """
        Uploading to steemitimages using beem
        """
        steem = Steem()
        iu = ImageUploader(steem_instance=steem)
        steem.wallet.unlock(walletpw)
        postimage = iu.upload(path+"/"+imgurl, postaccount)
        """
        Optional: Adding a watermark with Pillow
        --- Config
        watermarkedpath = '00steemit'
        watermarkpath = 'watermark.png'
        --- Config end
        watermark = Image.open(watermarkpath)
        destination = img.copy()
        position = ((destination.width - watermark.width - 32), (destination.height - watermark.height - 30))
        destination.paste(watermark, position, watermark)
        waterimgurl = watermarkedpath+'/'+imgurl
        destination.save(waterimgurl)
        postimage = iu.upload(waterimgurl, postaccount)
        """
        """ 
        Printing out the result
        """
        print("<center><img src='"+postimage['url']+".jpg' /><br><sup>"+settings+"</sup></center>")
    except Exception as error:
        print("Error during image processing "+repr(error))

if __name__ == '__main__':
    """
    Queueing all files
    """
    for image in os.listdir(path):
        process_image(image)
    print("Finished")
