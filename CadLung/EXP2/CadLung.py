'''
SELU - CAR System -- LBRN 2020 Virtual Summer Program
Mentor: Dr. Omer Muhammet Soysal
Last Modified on: August 27 2020

Authors: William Brown
Date:
Distribution: Participants of SELU - CAR System -- LBRN 2020 Virtual Summer Program

CODING NOTES
- Use relative path
- Be sure your code is optimized as much as possible.
- Read the coding standarts and best practice notes.
~~~~ HELP  ~~~~
- Main File
'''
import NasFcAnn
import PlaneDataProcess
import keras
from keras.metrics import AUC

#Parameters
DataSet_xy = 'data_balanced_6Slices_1orMore_xy.bin'
DataSet_xz = 'data_balanced_6Slices_1orMore_xz.bin'
DataSet_yz = 'data_balanced_6Slices_1orMore_yz.bin'

xySliceTrainPredPath = 'OUTPUT/xySliceTrainPredictions.tf'
xySliceTestPredPath = 'OUTPUT/xySliceTestPredictions.tf'

xyPlaneInputPath = 'CadLung/INPUT/PLANE/xyPlaneInput.npz'
###

# XY Slice Model
xySliceModel = NasFcAnn.NasFcAnn(dataPath=DataSet_xy, type='slice',
                              name='xySlice', regRate=0.001, positiveRegion='y',
                              normalize='zs')

xySliceModel.loadData()
xySliceModel.doPreProcess()

xySliceModel.loadModel()
xySliceModel.testModel()
xySliceModel.exportPredict()
print('XY Slice Model Evaluation:')
xySliceModel.evaluate()

xySliceModel.exportTrainPred()
###

# XY Plane Pre Process
xyPlanePreProcess = PlaneDataProcess.PlaneDataProcess('xySlice')
xyPlaneTrainSet = xyPlanePreProcess.readTrainData(xySliceTrainPredPath)      #Training Set
xyPlaneTrainLabel = xyPlanePreProcess.convertTrainingLabels(DataSet_xy)[0]   #Training Labels
xyPlaneTestSet = xyPlanePreProcess.readTrainData(xySliceTestPredPath)        #Test Set
xyPlaneTestLabel = xyPlanePreProcess.convertTrainingLabels(DataSet_xy)[1]    #Test Labels

xyPlanePreProcess.exportPlaneInputs(xyPlaneInputPath, xyPlaneTrainSet, xyPlaneTrainLabel, xyPlaneTestSet, xyPlaneTestLabel)
###

# XY Plane Model
xyPlaneModel = NasFcAnn.NasFcAnn(dataPath=xyPlaneInputPath, type='plane',
                              name='xyPlane', regRate=0.001, positiveRegion='n',
                              normalize='zs')

xyPlaneModel.loadData()
xyPlaneModel.doPreProcess()

xyPlaneModel.loadModel()
xyPlaneModel.testModel()
xyPlaneModel.exportPredict()
print('XY Plane Model Evaluation:')
xyPlaneModel.evaluate()

xyPlaneModel.exportTrainPred()
###

print('done!')
