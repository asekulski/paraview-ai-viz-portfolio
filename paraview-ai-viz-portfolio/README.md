# AI Research Visualization Suite — ParaView Portfolio

Scientific visualizations built with **ParaView 6.1** and its Python scripting API, demonstrating techniques for understanding deep learning models through 3D rendering, volume visualization, and vector field analysis.

> Built as a portfolio piece for scientific visualization (ParaView) specialist roles in AI research.

---

## Visualizations

| Visualization | Description | VTK Techniques |
|---|---|---|
| **Loss Landscape** | 3D surface of a multi-modal loss function with local minima | StructuredGrid, Surface Rendering, Color Mapping |
| **Gradient Flow Field** | Streamlines showing optimizer trajectories through parameter space | ImageData, StreamTracer, Tube, Iso-surfaces |
| **CNN Activation Volume** | Volume rendering of synthetic 3D neural network activations | Volume Rendering, Opacity Transfer Functions, Contour |
| **Embedding Point Cloud** | Clustered 3D embeddings (t-SNE/UMAP style) with confidence | PolyData, Glyph (Sphere), Categorical Color Maps |

---

## Project Structure

```
paraview-ai-viz-portfolio/
├── scripts/
│   ├── generate_data.py              # Synthetic dataset generation (NumPy → VTK XML)
│   ├── generate_data_standalone.py   # Run with standard Python (no ParaView needed)
│   ├── viz_loss_landscape.py         # ParaView: loss landscape rendering
│   ├── viz_gradient_field.py         # ParaView: gradient vector field
│   ├── viz_activation_volume.py      # ParaView: CNN activation volume rendering
│   ├── viz_embedding_cloud.py        # ParaView: embedding point cloud
│   └── copy_images_to_docs.py        # Copy renders to docs/ for GitHub Pages
├── data/                             # Generated VTK datasets (git-ignored)
├── output/                           # Rendered PNG images
├── docs/
│   ├── index.html                    # GitHub Pages gallery
│   └── images/                       # Images served by GitHub Pages
├── run_all.py                        # Master pipeline script
├── requirements.txt
└── README.md
```

---

## Requirements

- **ParaView 6.x** (tested with 6.1.0) — [Download](https://www.paraview.org/download/)
- **NumPy** (bundled with ParaView's Python, or install separately)

---

## How to Run

### Step 1: Generate Data + Render (Full Pipeline)

Run everything with a single command using ParaView's built-in Python:

```bash
# Windows (adjust path to your ParaView installation)
"C:\Program Files\ParaView 6.1.0\bin\pvpython.exe" run_all.py

# Linux / macOS
pvpython run_all.py
```

### Step 2: Generate Data Only (No ParaView Required)

If you just want to create the VTK datasets:

```bash
python scripts/generate_data_standalone.py
```

### Step 3: Render Only (Data Already Exists)

```bash
pvpython run_all.py --render
```

### Step 4: Copy Images to GitHub Pages

```bash
python scripts/copy_images_to_docs.py
```

Then commit and push — the gallery will be live at your GitHub Pages URL.

---

## Hosting on GitHub Pages

1. Create a GitHub repository and push this project
2. Go to **Settings → Pages**
3. Set source to **Deploy from a branch**, branch `main`, folder `/docs`
4. Your gallery will be live at `https://YOUR_USERNAME.github.io/paraview-ai-viz-portfolio/`

---

## Opening in ParaView GUI

All generated `.vti`, `.vts`, and `.vtp` files in `data/` can be opened directly in the ParaView desktop application for interactive exploration:

1. **File → Open** → navigate to the `data/` folder
2. Select any dataset and click **Apply**
3. Use the Properties panel to adjust color maps, representations, and filters

---

## Technical Highlights

- **Fully scripted pipeline** — every visualization is reproducible via `pvpython`
- **Custom VTK XML writers** — datasets generated from pure NumPy without VTK library dependency
- **Research-relevant** — visualizations address real concepts in deep learning interpretability
- **Production rendering** — 1920×1080 output with custom lighting, backgrounds, and color bars
- **Multiple VTK data types** — ImageData, StructuredGrid, PolyData
- **Advanced filters** — StreamTracer, Contour, Glyph, Tube, Volume Rendering

---

## License

MIT
