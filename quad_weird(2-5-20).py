#this version makes really small squares in top left that progressively get bigger and fuzzier towards the bottom right
#its a bug where the recursive function only works properly in the first quadrant of each node tire
#but it looks cool so im keeping it here
from PIL import Image, ImageDraw;
import sys; #fileinput for picking image
sys.setrecursionlimit(5000); #might be neccesary depending on how deep the tree goes

im_og = Image.open("./images/Untitled3.png");
im = im_og.copy();
im_og.close(); #avoid overwriting source image
#im.show();
#print(im.getpixel((0,0)));

width, height = im.size;

bsp_array = []; #array that holds the values of the quad tree. index format: [tier, [x,y], [r,g,b]]
                #tier = how deep down the tree the square is     x,y = coor of upper left corner   rgb=color
#NOT AN ACTUAL QUAD TREE. Only contains a list of leaf noes from top left to bottom right

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
#print(bsp_array[1]);
#print(bsp_array[1][2]);
#print(bsp_array[1][2][0]);

#TODO: reconstruct image to verify
remake = Image.new("RGBA", (width,height), color=None);
draw = ImageDraw.Draw(remake);
#draw.rectangle([0,0,10,10],fill="rgb(0,255,0)",outline="rgb(255,0,0)",width=1);
#"""
for i in range(0,len(bsp_array)):  #[x0,y0,x1,y1]
    draw.rectangle([bsp_array[i][1][0], bsp_array[i][1][1], bsp_array[i][1][0]+int(width/2**(bsp_array[i][0]+1)), bsp_array[i][1][1]+int(height/2**(bsp_array[i][0]+1))], 
                   fill=(bsp_array[i][2][0], bsp_array[i][2][1], bsp_array[i][2][2]), #rgb value
                   outline=None, width=0); #optional outline
#"""
remake.save("./images/Untitled3_weird_remake.png",format="png");
