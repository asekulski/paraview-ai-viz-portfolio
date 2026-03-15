"""
ParaView visualization: CNN Activation Volume Rendering.
Renders a 3D volume of synthetic neural network activations
using volume rendering with custom transfer functions.
"""
from paraview.simple import *
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJ_DIR, "data")
OUT_DIR = os.path.join(PROJ_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

paraview.simple._DisableFirstRenderCameraReset()

reader = XMLImageDataReader(FileName=[os.path.join(DATA_DIR, "activation_volume.vti")])
reader.PointArrayStatus = ["Activation", "Entropy"]
reader.UpdatePipeline()

renderView = CreateRenderView()
renderView.ViewSize = [1920, 1080]
renderView.UseColorPaletteForBackground = 0
renderView.Background = [0.0, 0.0, 0.05]
renderView.OrientationAxesVisibility = 0

# --- Volume Rendering of Activations ---
display = Show(reader, renderView)
display.SetRepresentationType("Volume")
ColorBy(display, ("POINTS", "Activation"))

actLUT = GetColorTransferFunction("Activation")
actLUT.ApplyPreset("Cool to Warm (Extended)", True)
actLUT.RescaleTransferFunction(0.0, 1.0)

actPWF = GetOpacityTransferFunction("Activation")
actPWF.Points = [0.0, 0.0, 0.5, 0.0,
                 0.15, 0.0, 0.5, 0.0,
                 0.3, 0.05, 0.5, 0.0,
                 0.5, 0.15, 0.5, 0.0,
                 0.7, 0.4, 0.5, 0.0,
                 1.0, 0.9, 0.5, 0.0]

colorBar = GetScalarBar(actLUT, renderView)
colorBar.Title = "Activation Intensity"
colorBar.ComponentTitle = ""
colorBar.TitleFontSize = 18
colorBar.LabelFontSize = 14
colorBar.Visibility = 1

renderView.CameraPosition = [6.0, 5.0, 4.0]
renderView.CameraFocalPoint = [0.0, 0.0, 0.0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]

renderView.Update()
Render()

out_path = os.path.join(OUT_DIR, "activation_volume.png")
SaveScreenshot(out_path, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path}")

# --- Iso-surface view of high activations ---
contour = Contour(Input=reader)
contour.ContourBy = ["POINTS", "Activation"]
contour.Isosurfaces = [0.3, 0.5, 0.7, 0.9]
contour.UpdatePipeline()

Hide(reader, renderView)

contourDisplay = Show(contour, renderView)
ColorBy(contourDisplay, ("POINTS", "Activation"))
contourDisplay.Opacity = 0.6
contourDisplay.Specular = 0.4
contourDisplay.SpecularPower = 30

renderView.Update()
Render()

out_path2 = os.path.join(OUT_DIR, "activation_isosurfaces.png")
SaveScreenshot(out_path2, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path2}")

Delete(contour)
Delete(reader)
