"""
ParaView visualization: Gradient Descent Vector Field.
Renders streamlines and glyphs showing optimizer trajectories
through a parameter space potential field.
"""
from paraview.simple import *
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJ_DIR, "data")
OUT_DIR = os.path.join(PROJ_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

paraview.simple._DisableFirstRenderCameraReset()

reader = XMLImageDataReader(FileName=[os.path.join(DATA_DIR, "gradient_field.vti")])
reader.PointArrayStatus = ["GradientVelocity", "VelocityMagnitude", "Potential"]
reader.UpdatePipeline()

renderView = CreateRenderView()
renderView.ViewSize = [1920, 1080]
renderView.UseColorPaletteForBackground = 0
renderView.Background = [0.02, 0.02, 0.08]
renderView.OrientationAxesVisibility = 0

# --- Streamlines through the gradient field ---
stream = StreamTracer(Input=reader, SeedType="Point Cloud")
stream.Vectors = ["POINTS", "GradientVelocity"]
stream.MaximumStreamlineLength = 8.0
stream.SeedType.Center = [0.0, 0.0, 1.0]
stream.SeedType.Radius = 2.5
stream.SeedType.NumberOfPoints = 300
stream.UpdatePipeline()

streamTube = Tube(Input=stream)
streamTube.Radius = 0.04
streamTube.NumberofSides = 12
streamTube.UpdatePipeline()

streamDisplay = Show(streamTube, renderView)
ColorBy(streamDisplay, ("POINTS", "VelocityMagnitude"))
velLUT = GetColorTransferFunction("VelocityMagnitude")
velLUT.ApplyPreset("Plasma", True)
streamDisplay.Opacity = 0.85

# --- Iso-surfaces of the potential field ---
contour = Contour(Input=reader)
contour.ContourBy = ["POINTS", "Potential"]
contour.Isosurfaces = [0.5, 1.5, 3.0]
contour.UpdatePipeline()

contourDisplay = Show(contour, renderView)
ColorBy(contourDisplay, ("POINTS", "Potential"))
potLUT = GetColorTransferFunction("Potential")
potLUT.ApplyPreset("Cool to Warm", True)
contourDisplay.Opacity = 0.15
contourDisplay.Specular = 0.5

colorBar = GetScalarBar(velLUT, renderView)
colorBar.Title = "Flow Speed"
colorBar.ComponentTitle = ""
colorBar.TitleFontSize = 18
colorBar.LabelFontSize = 14
colorBar.Visibility = 1

renderView.CameraPosition = [8.0, -5.0, 6.0]
renderView.CameraFocalPoint = [0.0, 0.0, 1.0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]

renderView.Update()
Render()

out_path = os.path.join(OUT_DIR, "gradient_field.png")
SaveScreenshot(out_path, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path}")

Delete(contour)
Delete(streamTube)
Delete(stream)
Delete(reader)
