from pykeeb import *
from math import *

print('plates')

########################MAIN PLATE#######################
rows=5
columns=6
plate = Keyboard_matrix(5, 6, 0, 0, 1, [0,0,7], 0,11,0, 20,20,'mx')

#arc rows and columns with specified radii in mm
plate.arc_rows(75)
plate.arc_cols(220)

#ignore bottom inside key
plate.ik[0][0]=True


#y-axis column translations
#shift 3rd column from the left forward by 2mm
plate.cm[2][1]=plate.cm[2][1]+2
#shift 2 right most columns backward by 6mm
plate.cm[4][1]=plate.cm[4][1]-6
plate.cm[5][1]=plate.cm[5][1]-6

#z-axis column translations
#shift middle 2 columns down by specified dist in mm
plate.cm[2][2]=plate.cm[2][2]-5 
plate.cm[3][2]=plate.cm[3][2]-2
#shift 3 right most columns up by specified dist in mm
plate.cm[3][2]=plate.cm[3][2]+1.8
plate.cm[4][2]=plate.cm[4][2]+3
plate.cm[5][2]=plate.cm[5][2]+3
#generate
plate.generate()

##################THUMB CLUSTER##########################

plate2 = Keyboard_matrix(3, 3, 0, 0, 10, [-21,3,14], 12,14,0, 20,20,'mx')

#ignore keys to make room for 2u keys
plate2.ik[2][2]=True
plate2.ik[1][2]=True
plate2.ik[1][1]=True
#arc cols by specified radii
plate2.arc_rows(90)
plate2.arc_cols(350)

#shift bottom 1u sockets up by 0.5u to make room for 2u caps
keyshift=10
plate2.im[0][2][1]=plate2.im[0][2][1]+keyshift
plate2.im[0][1][1]=plate2.im[0][1][1]+keyshift

#shift 2u keys up by 5mm
plate2.im[0][2][2]=plate2.im[0][2][2]-0.9
plate2.im[0][1][2]=plate2.im[0][1][2]-0.9

plate2.im[0][2][3]=plate2.im[0][2][3]+5
plate2.im[0][1][3]=plate2.im[0][1][3]+5

#generate
plate2.generate()

#rotate thumbcluster by 13 degrees
thumbangle=13

#########HULLS CONNECTING TWO PLATES########

#hulls connecting thumb and matrix
print('plate hulls')
#hull 2u key to 1u keys around them
plate2.column_hulls[0][0].disable()
conn=(plate2.sm[2][1].get_back()+plate2.sm[0][1].get_front()+plate2.sm[1][0].get_corner('fr',0.01,12,0.01,0.01)).hull()
conn+=(plate2.sm[0][1].get_left()+\
       plate2.sm[1][0].get_corner('br',0.01,12,0.01,0.01)+\
      plate2.sm[0][0].get_corner('fr',0.01,12,0.01,0.01)).hull()
#extend 2u keys down to make border of cluster
conn+=(plate2.sm[0][1].get_back(0.01,extrude=keyshift)+\
      plate2.sm[0][2].get_back(0.01,extrude=keyshift)).hull()
#hull extensions to bottom left
conn+=(plate2.sm[0][1].get_corner('bl', 0,0,0.01, keyshift)+\
       plate2.sm[1][1].get_left()+\
       plate2.sm[0][0].get_right()).hull()
#rotate cluster
conn=conn.rotate(thumbangle)
#hull right 2u key to keywell
conn+=(plate2.sm[0][2].get_right().rotate(thumbangle)+\
       plate.sm[0][1].get_left()+\
       plate.sm[0][1].get_corner('bl',0,0,0.01,0.01)).hull()
#hull top right 1u key to keywell
conn+=(plate2.sm[2][1].get_right(extrude=2).rotate(thumbangle)+\
       plate.sm[1][0].get_left(0.01,0)+\
       plate.sm[2][0].get_corner('bl',0,0,0.01,0.01)).hull()
#hull middle of cluster to keywell
conn+=(plate2.sm[0][2].get_front().rotate(thumbangle)+\
       plate2.sm[2][1].get_corner('br', 2, 3, 2, 3).rotate(thumbangle)+\
       plate2.sm[0][1].get_corner('fr', 2, 3, 2, 3).rotate(thumbangle)+\
       plate.sm[1][0].get_back()).hull()

plate.left_wall[1].disable()
plate.left_wall_hulls[0].disable()
plate.corner_hulls[0][0].disable()

#########HULLS CONNECTING TWO CASES########

print('case hulls')


#create front wall for cluster (needs elegant solution)
largefront=((plate2.sm[0][1].get_back(0.01,extrude=keyshift+3)+\
         plate2.sm[0][2].get_back(0.01,extrude=keyshift+3)).hull())
smallfront=((((plate2.sm[0][1].get_back(0.01,extrude=9.5)+\
         plate2.sm[0][2].get_back(0.01,extrude=9.5)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull())

smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=keyshift)+\
         plate2.sm[0][2].get_back(0.01,extrude=keyshift)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([0,0,1])
smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=keyshift)+\
         plate2.sm[0][2].get_back(0.01,extrude=keyshift)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([0,0,-1])
smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=keyshift)+\
         plate2.sm[0][2].get_back(0.01,extrude=keyshift)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([-1,0,0])
smallfront+=((((plate2.sm[0][1].get_back(0.01,extrude=keyshift)+\
         plate2.sm[0][2].get_back(0.01,extrude=keyshift)+\
        (plate2.sm[0][1].get_back(0.01,extrude=-1)+\
         plate2.sm[0][2].get_back(0.01,extrude=-1))))).hull()).translate([1,0,0])

caconn=project((plate2.sm[0][0].get_corner('br',0,0,0.01,3)+(largefront-smallfront)).hull())


#rotate thumbcluster
caconn=caconn.rotate(thumbangle)


#hull front of cluster case to main case
caconn+=project((plate2.sm[2][1].get_corner('fr', 2, 3, 2, 3).rotate(thumbangle)+plate.sm[2][0].get_corner('bl', 2, 3, 2, 3)).hull())

caconn+=project((plate.sm[0][1].get_corner('bl', 0, 0, 0.01,0.01)+\
               plate2.sm[0][2].get_corner('br', 0, 0, 2, 3).rotate(thumbangle)+\
               plate2.sm[0][2].get_corner('br', 0, 0, 2,keyshift+3).rotate(thumbangle)).hull())   

plate2.right_wall[0].disable()
plate2.right_wall_hulls[0].disable()

plate2.front_right_corner.disable()
plate2.back_right_corner.disable()

plate2.back_wall[1].disable()
plate2.back_wall[2].disable()

plate2.back_wall_hulls[1].disable()
plate2.back_wall_hulls[0].disable()

plate2.right_wall_hulls[1].disable()

#########EXTRUDE LIPS INSIDE OF CASE FOR PLATE TO REST ON##########

print('mounts')
for c in range(columns):
    for r in range(rows):
        if c==0 and r==0:
            mount=plate.sm[r][c].get_left(thickness=0.8,extrude=False).translate([0,0,-3])
        elif c==0 and r==1:
            None
        elif c==0:
            mount+=plate.sm[r][c].get_left(thickness=0.8,extrude=False).translate([0,0,-3])
        elif c==columns-1:
            mount+=plate.sm[r][c].get_right(thickness=0.8,extrude=False).translate([0,0,-3])
        if r==0:
            mount+=plate.sm[r][c].get_back(thickness=0.8,extrude=False).translate([0,0,-3])
        elif r==rows-1:
            mount+=plate.sm[r][c].get_front(thickness=0.8,extrude=False).translate([0,0,-3])
            
for c in range(3):
    for r in range(3):
        if c==0 and r==0:
            mount2=plate2.sm[r][c].get_left(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
            mount2+=plate2.sm[r][c].get_back(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
        elif c==0:
            mount2+=plate2.sm[r][c].get_left(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])
        elif c>0 and r==0:
            mount2+=plate2.sm[r][c].get_back(thickness=0.8,extrude=False).translate([0,-9.5,-3]).rotate(thumbangle)
            
        elif r==3-1:
            mount2+=plate2.sm[r][c].get_front(thickness=0.8,extrude=False).rotate(thumbangle).translate([0,0,-3])            


#########GET KEY CAPS##########

print('keys')
keys=[]
for row in range(rows):
    for column in range(columns):
        if row+column>0:
        #plate.sm[row][column].get_keyswitch()
            keys.append(plate.sm[row][column].get_keycap())

keys.append(plate2.sm[0][0].get_keycap().rotate(thumbangle))   
keys.append(plate2.sm[0][1].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[0][2].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[1][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][0].get_keycap().rotate(thumbangle))        
keys.append(plate2.sm[2][1].get_keycap().rotate(thumbangle))        


cable_hole = Cylinder(30, 7, center=True).rotate([90,0,0])
cable_hole = (cable_hole + cable_hole.translate([10,0,0])).hull().translate([26,100,0]).color("Blue")


#bring it all together
print('unions')
right_hand=plate.get_matrix()+plate2.get_matrix().rotate(thumbangle)+conn+mount2+caconn#+keys
pl=plate2.get_plate().rotate(thumbangle)+plate.get_plate()+conn#+keys
ca=plate2.get_walls().rotate(thumbangle)+plate.get_walls()+mount2+caconn
    
	
print('writing')
(pl).write(r"things\pydactyl_plate.scad")
(ca-pl).write(r"things\pydactyl_case.scad")
((right_hand)).write(r"things\pydactyl.scad")
