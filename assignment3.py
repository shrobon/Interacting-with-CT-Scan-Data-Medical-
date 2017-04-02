# Name : Shrobon Biswas
# Student ID : 1505851
# VTK Assignment 3
# Submission Date : 4/4/2016
import vtk
dir_ = r"CT" #Directory that contains CT dataset of the heart


# Read the CT dataset from the 'CT' folder
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

# Initializing up VTK render window and interactor
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# Defining suitable colur transfer functions 
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Opacity Transfer Functions::: 
# The tissues we are not interested in, we put the opacity as 0.0
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

# Instantiate necessary classes and create VTK pipeline
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
ren.SetViewport(0,0,0.6,1)
ren.SetBackground(0.1,0.2,0.4)
ren.AddVolume(volume)

#The colors used to the planeWidget
RGB_tuples = [(1, 0, 0), (0, 1, 0), (0, 0, 1)] 


# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
volume.Update()

renWin.AddRenderer(ren)
renWin.Render()

#Information about the volume rendered is obtained by the picker
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

# Define plane widget
planeWidgetX = vtk.vtkImagePlaneWidget() 

 

# Setting the plane properties
planeWidgetX.SetInputConnection(reader.GetOutputPort(0))
planeWidgetX.SetPlaneOrientation(0)
planeWidgetX.DisplayTextOn()
planeWidgetX.SetSliceIndex(100)
planeWidgetX.SetPicker(picker)
planeWidgetX.SetKeyPressActivationValue("x")
planeWidgetX.GetPlaneProperty().SetColor(RGB_tuples[0])



# Place plane widget and set interactor

planeWidgetX.SetCurrentRenderer(ren)
planeWidgetX.SetInteractor(iren)
planeWidgetX.PlaceWidget()
planeWidgetX.On()


#code for sliced portion
image = planeWidgetX.GetResliceOutput()
image.Modified()

actor = vtk.vtkImageActor()
actor.GetMapper().SetInputData(image) 
actor.Update()

# Add the volume to the renderer
ren2 = vtk.vtkRenderer()
ren2.SetBackground(0,0,0)
ren2.AddActor(actor)
ren2.SetViewport(0.6,0.5,1,1)
ren2.ResetCamera()
renWin.AddRenderer(ren2)
renWin.Render()

plot = vtk.vtkXYPlotActor()
plot.SetLabelFormat("%g")
plot.SetXTitle("Pixel Intensity")
plot.SetYTitle("Frequency")
plot.SetXValuesToValue()


ren3 = vtk.vtkRenderer()
ren3.SetViewport(0.6,0,1,0.5)
ren3.SetBackground(0,0,0)
renWin.AddRenderer(ren3)
renWin.Render()

#Set Histogram 
histogram = vtk.vtkImageAccumulate()
histogram.AddInputData(image)
(x,y)=image.GetScalarRange()
histogram.SetComponentExtent(int(x),int(y),0,0,0,0);
histogram.SetInputData(image)
histogram.Modified()


plot.AddDataSetInputConnection(histogram.GetOutputPort(0))
ren3.AddActor(plot)
ren3.ResetCamera()
renWin.AddRenderer(ren3)
renWin.Render()
renWin.SetSize(800,800)

# Render the scene
renWin.Render()

#Saving the render window as a JPEG image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()
 
writer = vtk.vtkJPEGWriter()
writer.SetFileName("Output_Assignment3.jpeg")
writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()
iren.Initialize()
iren.Start()


