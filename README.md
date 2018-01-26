# YOLOv2 for Intel/Movidius Neural Compute Stick (NCS)

	
### Step 1. Compile Python Wrapper
```make clean```
```make ```
### Step 2. Convert Caffe to NCS
```
mvNCCompile ./models/caffemodels/yoloV2Tiny20.prototxt -w ./models/caffemodels/yoloV2Tiny20.caffemodel -s 12
```


### Step 3. Run tests
```	
python3 ./detectionExample/Main.py --video /dev/video0
```
/dev/video0 is the webacam, please change accordingly to the camera you attach. 
