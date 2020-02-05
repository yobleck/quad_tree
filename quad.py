from PIL import Image;
import sys; #fileinput for picking image
sys.setrecursionlimit(1000); #might be neccesary depending on how deep the tree goes

im_og = Image.open("./images/VNN.jpg");
im = im_og.copy();
im_og.close(); #avoid overwriting source image
#im.show();
#print(im.getpixel((0,0)));

width, height = im.size;

bsp_array = []; #array that holds the values of the quad tree. index format: [tier, [x,y], [r,g,b]]
                #tier = how deep down the tree the square is     x,y = coor of upper left corner   rgb=color


def quad_tree(start,div,tier):
    for y in range(0,2): #these 2 for loops iterate over the 4 nodes of that tier in the tree
        for x in range(0,2):
            #print("tier:", tier);
            notmono = False; #monochromatic
            
            startx = start[0]+x*div[0];
            starty = start[1]+y*div[1];
            divx = div[0]+x*div[0];
            divy = div[1]+y*div[1];
            #print("start stuff:", startx, starty, divx, divy);
            #try: #crashing on subdivide of lower right quadrant
            test_pix = im.getpixel((startx,starty)); #top left pixel used to check if all pixels in node are same color
            #print(test_pix);
            
            for wid in range(startx,divx): #these 2 for loops iterate over pixels in node
                for hit in range(starty,divy):
                    #print(wid,hit);
                    if im.getpixel((wid,hit)) != test_pix:
                        notmono = True;
            if notmono == True:
                print("branching...");
                temp_tier = tier + 1;
                quad_tree([startx,starty],[int(div[0]/2),int(div[1]/2)],temp_tier);
            else:
                print("adding leaf node to array"); #add rgb to nested array or dict or quad tree class or something
                bsp_array.append([tier, [startx,starty], test_pix]); #this is temporary
            #except:
                #pass;
    #print(bsp_array);


quad_tree([0,0], [int(width/2), int(height/2)], 0);
print(bsp_array);

#TODO: reconstruct image to verify
