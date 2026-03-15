"""
ParaView visualization: Neural Network Loss Landscape.
Renders a 3D surface colored by loss value with gradient magnitude overlay,
styled to resemble research-quality loss landscape plots.
"""
from paraview.simple import *
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJ_DIR, "data")
OUT_DIR = os.path.join(PROJ_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

paraview.simple._DisableFirstRenderCameraReset()

reader = XMLStructuredGridReader(FileName=[os.path.join(DATA_DIR, "loss_landscape.vts")])
reader.UpdatePipeline()

renderView = CreateRenderView()
renderView.ViewSize = [1920, 1080]
renderView.UseColorPaletteForBackground = 0
renderView.Background = [0.05, 0.05, 0.12]
renderView.OrientationAxesVisibility = 0

display = Show(reader, renderView)
ColorBy(display, ("POINTS", "Loss"))

lossLUT = GetColorTransferFunction("Loss")
lossLUT.ApplyPreset("Cool to Warm (Extended)", True)
lossLUT.RescaleTransferFunction(-3.0, 4.0)

lossPWF = GetOpacityTransferFunction("Loss")
lossPWF.RescaleTransferFunction(-3.0, 4.0)

display.SetRepresentationType("Surface")
display.Specular = 0.3
display.SpecularPower = 40
display.Ambient = 0.15

colorBar = GetScalarBar(lossLUT, renderView)
colorBar.Title = "Loss Value"
colorBar.ComponentTitle = ""
colorBar.TitleFontSize = 18
colorBar.LabelFontSize = 14
colorBar.Visibility = 1

renderView.CameraPosition = [6.0, -6.0, 7.0]
renderView.CameraFocalPoint = [0.0, 0.0, 0.0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]

renderView.Update()
Render()

out_path = os.path.join(OUT_DIR, "loss_landscape.png")
SaveScreenshot(out_path, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path}")

# --- Secondary view: gradient magnitude ---
ColorBy(display, ("POINTS", "GradientMagnitude"))
gradLUT = GetColorTransferFunction("GradientMagnitude")
gradLUT.ApplyPreset("Inferno", True)

gradBar = GetScalarBar(gradLUT, renderView)
gradBar.Title = "Gradient Magnitude"
gradBar.ComponentTitle = ""
gradBar.TitleFontSize = 18
gradBar.LabelFontSize = 14
gradBar.Visibility = 1

colorBar.Visibility = 0

renderView.Update()
Render()

out_path2 = os.path.join(OUT_DIR, "loss_landscape_gradient.png")
SaveScreenshot(out_path2, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path2}")

Delete(reader)
del reader
