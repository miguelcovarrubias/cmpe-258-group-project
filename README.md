### labels should have the following format
<object-class> <x> <y> <width> <height>  
* <object-class> - integer number of object from 0 to (classes-1)    
* <x> <y> <width> <height> - float values relative to width and height of image, it can be equal from 0.0 to 1.0  
* for example: 2 points represent the box in the picture, (x1, y1) and (x2, y2). Note that the y values start from top to bottom.
* width = x2 - x1
* height = y2 - y1 
* x = ((x1 - x1)/2) + x1 
* x = ((x1 - x1)/2) + x1 

* attention: <x> <y> - are center of rectangle (are not top-left corner)  

### to train the model without initial weights 
./darknet detector train cfg/coco.data cfg/yolov3-tiny.cfg 

### to train the model with initial weights 
./darknet detector train cfg/coco.data cfg/yolov3-tiny.cfg  darknet53.conv.74

### to train with from backup
./darknet detector train cfg/coco.data cfg/yolov3-tiny.cfg scripts/coco/backup/yolov3-tiny.backup  darknet53.conv.74 

