# Python commands in this file are executed on Slicer startup

# Examples:
#
# Load a scene file
# slicer.util.loadScene('c:/Users/SomeUser/Documents/SlicerScenes/SomeScene.mrb')
#
# Open a module (overrides default startup module in application settings / modules)
# slicer.util.mainWindow().moduleSelector().selectModule('SegmentEditor')
#

# Pre-populate the scene with measurements
# From slicerScript repo - https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#pre-populate-the-scene-with-measurements
# sliceNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")

pointList = [
                'GreaterTuberosity',
                'LesserTuberosity',
                'IntertubercularGroove',
                'MedialEpicondyle',
                'LateralEpicondyle'
                ]
curveList = [
                'DeltoidInsertion'
                'CorticalInner_20%',
                'CorticalInner_40%',
                ]
planeList = ['OsteotomyPlane']

# Function used populate the scene with all desired measurements
def createMeasurements():
    # populate curve measurements
    for closedCurveNodeName in curveList:
        closedCurveNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsClosedCurveNode", closedCurveNodeName)
        closedCurveNode.CreateDefaultDisplayNodes()
        print(f'point created for: {closedCurveNodeName} \n')
    # populate point measurements
    for pointNodeName in pointList:
        pointListNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", pointNodeName)
        pointListNode.CreateDefaultDisplayNodes()
        print(f'point created for: {pointNodeName} \n')
    # populate plane measurements
    for planeNodeName in planeList:
        planeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsPlaneNode", planeNodeName)
        planeNode.CreateDefaultDisplayNodes()

shortcut1 = qt.QShortcut(slicer.util.mainWindow())
shortcut1.setKey(qt.QKeySequence("Ctrl+n"))
shortcut1.connect( 'activated()', createMeasurements)

# Copy all measurements in the scene to Excel
# From slicerscript repo - https://slicehttps://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#copy-all-measurements-in-the-scene-to-excelr.readthedocs.io/en/latest/developer_guide/script_repository.html#copy-all-measurements-in-the-scene-to-excel
def copyLineMeasurementsToClipboard():
    measurementsListHeader = '\t'.join(['MeasurementName', 'X', 'Y', 'Z'])
    measurementsList = []

    # Coordinates - Curves
    closedCurveListNodes = getNodesByClass('vtkMRMLMarkupsClosedCurveNode')
    for closedCurveNode in closedCurveListNodes:
        print(f'type pointNode: {type(closedCurveNode)}')
        
        # Individual points
        numberFiducials = closedCurveNode.GetNumberOfControlPoints()
        for i in range(numberFiducials):
            measurementName = closedCurveNode.GetName()
            x, y, z = closedCurveNode.GetNthControlPointPosition(i)
            measurementsList.append('\t'.join([f'{measurementName}_{i}', str(x), str(y), str(z)]))

    # Coordinates - Fiducials
    pointListNodes = getNodesByClass('vtkMRMLMarkupsFiducialNode')
    for pointNode in pointListNodes:
        print(f'type pointNode: {type(pointNode)}')

        # Individual points      
        numberFiducials = pointNode.GetNumberOfControlPoints()
        print(f'{numberFiducials} control points')
        for i in range(numberFiducials):
            measurementName = pointNode.GetName()
            # print(f'type coord: {type(pointNode.GetNthControlPointPosition(i))} \t len: {len(pointNode.GetNthControlPointPosition(i))}')
            print(f'coordinates: {pointNode.GetNthControlPointPosition(i)}')
            x, y, z = pointNode.GetNthControlPointPosition(i)
            measurementsList.append('\t'.join([f'{measurementName}_{i}', str(x), str(y), str(z)]))

    # Plane Normal Vectors
    planeListNodes = getNodesByClass('vtkMRMLMarkupsPlaneNode')
    for planeNode in planeListNodes:
        measurementName = planeNode.GetName()
        x, y, z = planeNode.GetNormal()
        print(f'normal vector: {planeNode.GetNormal()}')
        measurementsList.append('\t'.join([measurementName + '_normal', str(x), str(y), str(z)]))

    # Copy all measurements to clipboard (to be pasted into Excel)
    if measurementsList:
        slicer.app.clipboard().setText("\n".join(measurementsList))
        slicer.util.delayDisplay(f"Copied {len(measurementsList)} length measurements to the clipboard.")
    else:
        print(f'Unable to collect point coordinates')

shortcut2 = qt.QShortcut(slicer.util.mainWindow())
shortcut2.setKey(qt.QKeySequence("Ctrl+m"))
shortcut2.connect( 'activated()', copyLineMeasurementsToClipboard)