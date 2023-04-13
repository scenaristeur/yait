from glob import glob
import os
from PIL import Image
import json

print(os.name)
print (os.sep)
#exit()


"""list folders"""
folders = glob("./cifar2png/cifar100png/train/*/", recursive = True)

cpt = 0 # nbr of folders to explore
step = 1
float_precision = 5 # default 17


for folder in folders:
  if cpt < 3:
    file_cpt = 0
    cpt = cpt + 1
    print("\n")
    print(folder) 
    label = folder.split(os.sep)[1]
    print("label '% s:'" % label)
    dir_path = folder+'*.*'
    files = glob(dir_path)
    
    for file in files:
      print(label, file)
      image_representation = {}
      image_representation['label'] = label
      image_representation['points'] = []
      file_cpt = file_cpt + 1
      im = Image.open(file) # Can be many different formats.
      pix = im.load()
      size = im.size
      #print (im.size)  # Get the width and hight of the image for iterating over
      demi_largeur = int(size[0]/2)
      demi_hauteur = int(size[1]/2)
      center = (demi_largeur, demi_hauteur )
      #print (center)
      pix_center = pix[center]
      #print (pix_center)  # Get the RGBA Value of the a pixel of an image
      
      progression = 0
     
      point_representation = {}
      normalized_center_point = (center[0]/size[0], center[1]/size[1])
      normalized_center_pixel = (round(pix_center[0]/255, float_precision), round(pix_center[1]/255, float_precision), round(pix_center[2]/255, float_precision))
      point_representation['x'] = normalized_center_point[0]
      point_representation['y'] = normalized_center_point[1]
      point_representation['r'] = normalized_center_pixel[0]
      point_representation['g'] = normalized_center_pixel[1]
      point_representation['b'] = normalized_center_pixel[2]
      image_representation['points'].append(point_representation)

      while progression < demi_largeur :
        progression = progression + step
        print("-- '% s'" % progression)
        
        up = (center[0],center[1]-progression)
        up_right = (center[0]+progression,center[1]-progression)
        right = (center[0]+progression,center[1])
        down_right = (center[0]+progression,center[1]+progression)
        down = (center[0],center[1]+progression)
        down_left = (center[0]-progression,center[1]+progression)
        left = (center[0]-progression,center[1])
        up_left = (center[0]-progression,center[1]-progression)
        matrice = (up, up_right, right, down_right, down, down_left, left, up_left )
        #print(matrice)
        for point in matrice:
          point_representation = {}
          if point[0] > 0 and point[0] < size[0] and point[1] > 0 and point[1] < size[1] :
            #print(point)
            pixel = pix[point]
            #print(point, pixel)
            #normalize all values to be between 0 and 1
            #x_norm = (x-np.min(x))/(np.max(x)-np.min(x))
            normalized_point = (point[0]/size[0], point[1]/size[1])
            normalized_pixel = (round(pixel[0]/255, float_precision), round(pixel[1]/255, float_precision), round(pixel[2]/255, float_precision))
            print(normalized_point, normalized_pixel)
            #json = '{"x":'+normalized_point[0]+',"y":'+normalized_point[1]+',"r":'+normalized_pixel[0]+',"g":'+normalized_pixel[1]+',"b":'+normalized_pixel[2]+'}'
            #print(json)
            point_representation['x'] = normalized_point[0]
            point_representation['y'] = normalized_point[1]
            point_representation['r'] = normalized_pixel[0]
            point_representation['g'] = normalized_pixel[1]
            point_representation['b'] = normalized_pixel[2]

            image_representation['points'].append(point_representation)
      print(image_representation)

      #create image
      new_label = image_representation['label']
      new_points = image_representation['points']
      new_size = (32,32)
      im_new = Image.new(mode="RGBA", size = new_size)
      pix_new = im_new.load()
      for p in new_points:
        print(p)
        x = int(p['x']*size[0])
        y = int(p['y']*size[1])
        r = int(p['r']*255)
        g = int(p['g']*255)
        b = int(p['b']*255)
        #a = 255

        pix_new[x,y] = (r,g,b)
        print(x,y,r,g,b)
        path = './out/'+new_label+'/'
        isExist = os.path.exists(path)
      if not isExist:
      # Create a new directory because it does not exist
       os.makedirs(path)
      im_new.save(path+str(file_cpt)+'.png')

      #pix[x,y] = value  # Set the RGBA Value of the image (tuple)
      #im.save('alive_parrot.png')  # Save the modified pixels as .png 

      
      """for i in range(0, demi_largeur+1, step) :
        print(i)
        left = (center[0]-i*step,center[1])

        print(left)"""
