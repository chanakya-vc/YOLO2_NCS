import os, cv2, math


colornum = 12
colors = [(128,128,128),(128,0,0),(192,192,128),(255,69,0),(128,64,128),(60,40,222),(128,128,0),(192,128,128),(64,64,128),(64,0,128),(64,64,0),(0,128,192),(0,0,0)];
door_locs=[[220,110],[112,445]] # reprsents the x and y cordinates of the centroid of the doors
prob_threshold=0.033
def Visualize(img, results):
	img_cp = img.copy()
	detectedNum = len(results)
	if detectedNum > 0:
            for i in range(detectedNum):
                
                clr = colors[results[i].objType % colornum]
                txt = results[i].name

                left = results[i].left
                top = results[i].top
                right = results[i].right
                bottom = results[i].bottom

                cv2.rectangle(img_cp, (left,top), (right,bottom), clr, thickness=3)
                cv2.rectangle(img_cp, (left,top-20),(right,top),(255,255,255),-1)
                cv2.putText(img_cp,txt,(left+5,top-7),cv2.FONT_HERSHEY_SIMPLEX,0.5,clr,1)

	return img_cp


def distance_metric(left, right, top, bottom,door_locs):
    centroid_coorx=abs(right-left)/2
    centroid_coory=abs(bottom-top)/2
    rect_dist=[]
    for door in door_locs:
        dist=math.sqrt((door[0]-centroid_coorx)**2+(door[1]-centroid_coory)**2)
        rect_dist.append(dist)
    min_dist=min(rect_dist)
    door_id=rect_dist.index(min_dist)+1
    return door_id


    


def IOU(results, object_list):
    detectedNum = len(results) 
    if detectedNum > 0 and detectedNum<=len(object_list):
        for temp1 in object_list:
            temp_list=[]
            for i in range(detectedNum):
                if(results[i].name=="person" or results[i].name=="Person"):
                    union_area=abs((results[i].right-results[i].left)*(results[i].top-results[i].bottom)) + abs((temp1.left-temp1.right)*(temp1.top-temp1.bottom))
                    x_span = min(results[i].right, temp1.right)-max(results[i].left,temp1.left)
                    y_span = min(results[i].bottom, temp1.bottom)-max(results[i].top, temp1.top) # y coordinates measured from the top
                    print ("x_span:"+ str(x_span) +"  y_span:"+ str(y_span))
                    if x_span>0 and y_span>0 :
                        intersect=x_span*y_span
                    else :
                        intersect=0
                    prob=float(intersect/union_area)
                    temp_list.append(prob)
            max_prob=max(temp_list)
            object_id=temp_list.index(max_prob)
            if max_prob>prob_threshold :
                val=object_list.index(temp1)
                print ("The object with object_id:" +str(val)+ "still remains")
                temp1.update_coor(results[object_id].left,results[object_id].right,results[object_id].top,results[object_id].bottom)
            else :
                door_id=distance_metric(temp1.left,temp1.right, temp1.bottom, temp1.top, door_locs)
                print(" The object with" + str(object_id) + "has left the frame from door number"+ str(door_id) ) # Implement the nearest door. 
                val=object_list.index(temp1)
                del object_list[val]

    elif detectedNum > 0 and detectedNum > len(object_list) and len(object_list)!=0:
        for i in range(detectedNum):
            if(results[i].name=="person" or results[i].name=="Person"):
                temp_list=[]
                for temp1 in object_list:                
                    union_area=abs((results[i].right-results[i].left)*(results[i].top-results[i].bottom)) + abs((temp1.left-temp1.right)*(temp1.top-temp1.bottom))
                    x_span = min(results[i].right, temp1.right)-max(results[i].left,temp1.left)
                    y_span = min(results[i].top, temp1.top) -max(results[i].bottom, temp1.bottom)
                    if x_span>0 and y_span>0 :
                        intersect=x_span*y_span
                    else :
                        intersect=0
                    prob=float(intersect/union_area)
                    temp_list.append(prob)
                max_prob=max(temp_list)
                if max_prob>prob_threshold :
                    object_id=temp_list.index(max_prob)
                    temp1.update_coor(results[object_id].left,results[object_id].right,results[object_id].top,results[object_id].bottom)

                else :
                    object_id=len(object_list)
                    print("A new object with object_id"+ str(object_id) + "Has entered the frame" ) # Create a new object and add it to the object_list. 
                    temp2=homo_sapiens(results[i].left,results[i].right,results[i].top,results[i].bottom,object_id)
                    object_list.append(temp2)
    elif detectedNum >0 and len(object_list)==0 : 
        for i in range(detectedNum):
            if(results[i].name=="person" or results[i].name=="Person"):
                object_id=len(object_list)
                print("A new object with object_id"+ str(object_id) + "Has entered the frame" ) # Create a new object and add it to the object_list. 
                temp2=homo_sapiens(results[i].left,results[i].right,results[i].top,results[i].bottom,object_id)
                object_list.append(temp2)
    elif detectedNum ==0 and len(object_list)!=0 : 
        for temp1 in object_list :  
            object_id=object_list.index(temp1)
            door_id=distance_metric(temp1.left,temp1.right, temp1.bottom, temp1.top, door_locs)
            print(" The object with" + str(object_id) + "has left the frame from door number"+ str(door_id) )
            val=object_list.index(temp1)
            del object_list[val]                    


                
                
                
class homo_sapiens:
    def __init__(self, left, right, top, bottom, object_id):
        self.object_id=object_id
        self.left=int (left)
        self.top=int (top)
        self.bottom=int (bottom)
        self.right=int (right)
    def update_coor(self, left, right, top, bottom):
        self.left=left
        self.top=top
        self.bottom=bottom
        self.right=right