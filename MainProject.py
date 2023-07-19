#Code Made by TRIADS 
#ECE 2nd Years 


import cv2
from object_detection import ObjectDetection
import Voiceit
import math
import datetime
import Mailer


crt = datetime.datetime.now().strftime("%H:%M")
print('Current time : ', crt)                                              #prints current time
Voiceit.speak('Hello all, Motion detection program starting up Made by team TRIADS')
#Voiceit.telltime()
#Voiceit.tdate()


#Initialize Object detection
od = ObjectDetection()

#Capture  the video from the source
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("D:\\Study\\AAVARTANPROJECT\\PROJECT\\videoplayback.mp4")
#cap = cv2.VideoCapture("D:\\Study\\AAVARTANPROJECT\\PROJECT\\TestVideo1.mp4")
#cap = cv2.VideoCapture("D:\\Study\\AAVARTANPROJECT\\PROJECT\\Cars_test.mp4")
count=0                                                                     #stores the number of frames processed
up=0                                                                        #stores the count of people left
down=int(input(("Enter the number of people already in the shop: ")))       #stores the count of people inside
numb=0                                                                      #stores the number of people inside the store 
font = cv2.FONT_HERSHEY_SIMPLEX
center_points_prev_frame = []

tracking_objects = {}                                                       #Dictory of center points of objects with ids
track_id = 0                                                                #keeps the id 

ls=0

#implement the main prog
while True:
    #v2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Frame',1600,900)

    total=0
    isframe,frame = cap.read(1)
    count+=1

    if not isframe:                                                          #Breaks the while loop when no frame is received
        break
    
    # Points on current frame
    center_points_cur_frame = []

    #Detect object on the frame and put a rectangle on it
    (class_ids,scores,boxes) = od.detect(frame)                                #class_ids return the object detected, scores gives the accuracy of the detected object, boxes gives the location
    #print(class_ids,'\n',scores,'\n',boxes)

    for it in class_ids:
        if it==0:
            for box in boxes:
                total+=1
                c=str(total)
                (x,y,w,h)=box
                cx = int((x+w+x)/2)
                cy = int((y+h+y)/2)
                center_points_cur_frame.append((cx, cy))
                cv2.rectangle(frame, (x,y) , (x+w , y+h) , (0,255,0),2) 

            #For the first two frames check the locating centers of the of the object and declare them the same if the distance between themselves in both the fram is less than 30px
            if count <= 2:
                for pt in center_points_cur_frame:
                    for pt2 in center_points_prev_frame:
                        distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                        if distance < 30:
                            tracking_objects[track_id] = pt
                            ls=center_points_cur_frame.index(pt)
                            track_id += 1

            #once the basic tracking is done keep the check on the objects, create new and remove lost objects
            else:
                tracking_objects_copy = tracking_objects.copy()
                center_points_cur_frame_copy = center_points_cur_frame.copy()

                try:
                    for object_id, pt2 in tracking_objects_copy.items():
                        object_exists = False
                        for pt in center_points_cur_frame_copy:
                            distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                            

                            # Update IDs position
                            if distance < 30:
                                tracking_objects[object_id] = pt
                                object_exists = True
                                ls=center_points_cur_frame_copy.index(pt)
                                if pt in center_points_cur_frame:
                                    center_points_cur_frame.remove(pt)
                                continue
                        
                        ct=center_points_cur_frame_copy[ls]
                        if (pt2[1]<300 and ct[1]>300):
                            down+=1
                        if (pt2[1]>300 and ct[1]<300):
                            up+=1

                        # Remove IDs lost
                        if not object_exists:
                            tracking_objects.pop(object_id)

                except Exception as e:
                    continue

                # Add new IDs found
                for pt in center_points_cur_frame:
                    tracking_objects[track_id] = pt
                    track_id += 1

            #puting an id on the object in the frame 
            for object_id, pt in tracking_objects.items():
                cv2.circle(frame, pt, 5, (0, 255, 0), -1)
                #cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'Person', (pt[0], pt[1] - 7), 0, 1, (0, 255, 0), 2)


            
        else:
            i=0
            for box in boxes:
                if scores[i]>0.9:
                    c=str(total)
                    (x,y,w,h)=box
                    cx = int((x+w+x)/2)
                    cy = int((y+h+y)/2)
                    center_points_cur_frame.append((cx, cy))
                    cv2.rectangle(frame, (x,y) , (x+w , y+h) , (0,0,255),2) 
                    cv2.putText(frame, 'Alert',(x+w , y+h), 0, 1, (0, 0, 255), 2)
                i+=1

    numb=down-up
    #coun="Total objects detected: "+str(track_id)
    #cv2.putText(frame,coun,(20,50),font,1,(255,255,0),2)
    coun="Out: "+str(up)
    cv2.putText(frame,coun,(20,100),font,1,(255,255,0),2)
    coun="In: "+str(down)
    cv2.putText(frame,coun,(20,150),font,1,(255,255,0),2)
    coun="People inside: "+str(numb)
    cv2.putText(frame,coun,(20,200),font,1,(255,255,0),2)
    cv2.putText(frame,'____________________________________________________________________________________________________________________',(0,300),font,1,(0,0,0),5)
    


    if numb>100:
        coun='OVERLOAD ALERT !!!'
        cv2.putText(frame,coun,(150,100),font,1,(0,0,255),2)
        Voiceit.speak('OVERLOAD ALERT!!!')
        #print('ALERT !!!')

    crt = datetime.datetime.now().strftime("%H:%M")                         #checks time. If time > 20hrs then prints alert for object detected 
    if (crt[0]+crt[1])>'20':
        if center_points_cur_frame != []:
            #print('ALERT !!!')
            coun='TIME ALERT !!!'
            cv2.putText(frame,coun,(150,100),font,1,(0,0,255),2)
            Mailer.sendmail()                                               #Sends mail to the owner
            #Voiceit.speak('GET OUT OF THE AREA OR ELSE POLICE WILL BE CALLED')
            continue
    
    cv2.imshow("Motion Detector",frame)                                               #outputs the window to user
    key = cv2.waitKey(1)                                                    #Gives the number of sec delay between the reading of each frame
    
    #escape from loop to end program press 'Esc'
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
coun="Up: "+str(up)
print(coun)
coun="Down: "+str(down)
print(coun)
print('Thanks for using Motion detection program. Press enter to exit')
Voiceit.speak('Thanks for using Motion detection program made by TRIADS.')
input()