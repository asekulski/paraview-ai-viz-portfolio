"""
ParaView visualization: Embedding Space Point Cloud.
Renders clustered 3D point cloud resembling t-SNE/UMAP projections
of high-dimensional embeddings from a neural network.
"""
from paraview.simple import *
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJ_DIR, "data")
OUT_DIR = os.path.join(PROJ_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

paraview.simple._DisableFirstRenderCameraReset()

reader = XMLPolyDataReader(FileName=[os.path.join(DATA_DIR, "embedding_cloud.vtp")])
reader.PointArrayStatus = ["ClusterLabel", "Confidence"]
reader.UpdatePipeline()

renderView = CreateRenderView()
renderView.ViewSize = [1920, 1080]
renderView.UseColorPaletteForBackground = 0
renderView.Background = [0.03, 0.03, 0.1]
renderView.OrientationAxesVisibility = 0

# --- Glyph each point as a sphere ---
glyph = Glyph(Input=reader, GlyphType="Sphere")
glyph.ScaleArray = ["POINTS", "Confidence"]
glyph.ScaleFactor = 0.15
glyph.GlyphMode = "All Points"
glyph.GlyphType.ThetaResolution = 12
glyph.GlyphType.PhiResolution = 12
glyph.UpdatePipeline()

display = Show(glyph, renderView)
ColorBy(display, ("POINTS", "ClusterLabel"))

labelLUT = GetColorTransferFunction("ClusterLabel")
labelLUT.ApplyPreset("Turbo", True)
labelLUT.RescaleTransferFunction(0.0, 7.0)
labelLUT.NumberOfTableValues = 8
labelLUT.Discretize = 1

display.Specular = 0.3
display.Ambient = 0.2

colorBar = GetScalarBar(labelLUT, renderView)
colorBar.Title = "Cluster ID"
colorBar.ComponentTitle = ""
colorBar.TitleFontSize = 18
colorBar.LabelFontSize = 14
colorBar.Visibility = 1

renderView.CameraPosition = [10.0, -8.0, 8.0]
renderView.CameraFocalPoint = [0.0, 0.5, 0.0]
renderView.CameraViewUp = [0.0, 0.0, 1.0]

renderView.Update()
Render()

out_path = os.path.join(OUT_DIR, "embedding_cloud.png")
SaveScreenshot(out_path, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path}")

# --- Confidence coloring ---
ColorBy(display, ("POINTS", "Confidence"))
confLUT = GetColorTransferFunction("Confidence")
confLUT.ApplyPreset("Viridis", True)
confLUT.RescaleTransferFunction(0.0, 1.0)

confBar = GetScalarBar(confLUT, renderView)
confBar.Title = "Prediction Confidence"
confBar.ComponentTitle = ""
confBar.TitleFontSize = 18
confBar.LabelFontSize = 14
confBar.Visibility = 1
colorBar.Visibility = 0

renderView.Update()
Render()

out_path2 = os.path.join(OUT_DIR, "embedding_confidence.png")
SaveScreenshot(out_path2, renderView, ImageResolution=[1920, 1080],
               TransparentBackground=0)
print(f"Saved: {out_path2}")

Delete(glyph)
Delete(reader)
