import math

def transform(wgLat, wgLng):
    mgLat = 0
    mgLng = 0
    rad = 6378245.0
    ee = 0.00669342162296594323

    if outOfChina(wgLat, wgLng):
        mgLat = wgLat
        mgLng = wgLng
    else:
        dLat = transformLat(wgLng - 105.0, wgLat - 35.0);  
        dLng = transformLng(wgLng - 105.0, wgLat - 35.0);  
        radLat = wgLat / 180.0 * math.pi;  
        magic = math.sin(radLat);  
        magic = 1 - ee * magic * magic;  
        sqrtMagic = math.sqrt(magic);  
        dLat = (dLat * 180.0) / ((rad * (1 - ee)) / (magic * sqrtMagic) * math.pi);  
        dLng = (dLng * 180.0) / (rad / sqrtMagic * math.cos(radLat) * math.pi);  
        mgLat = wgLat + dLat;  
        mgLng = wgLng + dLng;

    return mgLat, mgLng

def outOfChina(lat, lng):
    if lng < 73.4904 or lng > 134.7773:
        return True
    if lat < 17.9993 or lat > 53.5609:
        return True

    if (lng > 125.3237 and lng < 136.4173) and (lat > 29.6093 and lat < 43.24):
        return True

    if (lng > 73.3237 and lng < 78.4573) and (lat > 7.53 and lat < 32.33):
        return True
    
    if (lng > 80.3237 and lng < 97.81) and (lat < 28.00):
        return True

    if (lng > 97.81 and lng < 108.02) and (lat < 21.00):
        return True

    return False

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))  
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0  
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0  
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0  
    return ret  

def transformLng(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))  
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0  
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0  
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0  
    return ret

from os import listdir
from os.path import isfile, join
from PIL import Image
from .getGPS import get_lat_lon_dt

if __name__ == "__main__":

    # mypath = '/Users/happy/Django/ohtto/media/drive/aa'
    # for file in listdir(mypath):
    #     if isfile(join(mypath, file)):
    #         fullpath = join(mypath,file)
    #         print(fullpath)

    #         if fullpath != '/Users/happy/Django/ohtto/media/drive/aa/.DS_Store':
    fullpath = '/Users/happy/Django/ohtto/blog/aa.jpg'
    image = Image.open(fullpath)
    lat, lng, dt = get_lat_lon_dt(image)
    # print("Lat : ", lat, " Lng : ", lng, " Taken Time : ", dt)

    if lat != 0.0:
        mgLat, mgLng = transform(lat, lng)
        # print("Lat : ", mgLat, " Lng : ", mgLng, " Taken Time : ", dt)
        # print("")

