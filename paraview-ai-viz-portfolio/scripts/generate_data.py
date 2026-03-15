"""
Generate synthetic scientific datasets for ParaView visualization.
Produces VTK-compatible files representing AI/ML-relevant phenomena.
"""
import numpy as np
import os
import struct

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def write_vti(filepath, dims, origin, spacing, point_data_arrays):
    """Write a VTK ImageData (.vti) XML file."""
    nx, ny, nz = dims
    ox, oy, oz = origin
    sx, sy, sz = spacing
    npts = nx * ny * nz

    with open(filepath, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="ImageData" version="1.0" byte_order="LittleEndian">\n')
        f.write(f'  <ImageData WholeExtent="0 {nx-1} 0 {ny-1} 0 {nz-1}" '
                f'Origin="{ox} {oy} {oz}" Spacing="{sx} {sy} {sz}">\n')
        f.write(f'    <Piece Extent="0 {nx-1} 0 {ny-1} 0 {nz-1}">\n')
        f.write('      <PointData>\n')
        for name, arr in point_data_arrays.items():
            ncomp = 1 if arr.ndim == 1 else arr.shape[1]
            flat = arr.flatten()
            data_str = " ".join(f"{v:.6f}" for v in flat)
            f.write(f'        <DataArray type="Float64" Name="{name}" '
                    f'NumberOfComponents="{ncomp}" format="ascii">\n')
            f.write(f"          {data_str}\n")
            f.write("        </DataArray>\n")
        f.write("      </PointData>\n")
        f.write("    </Piece>\n")
        f.write("  </ImageData>\n")
        f.write("</VTKFile>\n")


def write_vtp_points(filepath, points, point_data_arrays):
    """Write a VTK PolyData (.vtp) XML file with vertices."""
    npts = len(points)
    pts_str = " ".join(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}" for p in points)
    conn_str = " ".join(str(i) for i in range(npts))
    off_str = " ".join(str(i + 1) for i in range(npts))

    with open(filepath, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="PolyData" version="1.0" byte_order="LittleEndian">\n')
        f.write("  <PolyData>\n")
        f.write(f'    <Piece NumberOfPoints="{npts}" NumberOfVerts="{npts}" '
                f'NumberOfLines="0" NumberOfStrips="0" NumberOfPolys="0">\n')
        f.write("      <PointData>\n")
        for name, arr in point_data_arrays.items():
            ncomp = 1 if arr.ndim == 1 else arr.shape[1]
            flat = arr.flatten()
            data_str = " ".join(f"{v:.6f}" for v in flat)
            f.write(f'        <DataArray type="Float64" Name="{name}" '
                    f'NumberOfComponents="{ncomp}" format="ascii">\n')
            f.write(f"          {data_str}\n")
            f.write("        </DataArray>\n")
        f.write("      </PointData>\n")
        f.write("      <Points>\n")
        f.write('        <DataArray type="Float64" NumberOfComponents="3" format="ascii">\n')
        f.write(f"          {pts_str}\n")
        f.write("        </DataArray>\n")
        f.write("      </Points>\n")
        f.write("      <Verts>\n")
        f.write('        <DataArray type="Int64" Name="connectivity" format="ascii">\n')
        f.write(f"          {conn_str}\n")
        f.write("        </DataArray>\n")
        f.write('        <DataArray type="Int64" Name="offsets" format="ascii">\n')
        f.write(f"          {off_str}\n")
        f.write("        </DataArray>\n")
        f.write("      </Verts>\n")
        f.write("    </Piece>\n")
        f.write("  </PolyData>\n")
        f.write("</VTKFile>\n")


def write_vts(filepath, points_3d, point_data_arrays):
    """Write a VTK StructuredGrid (.vts) XML file."""
    ny, nx, _ = points_3d.shape
    pts_flat = points_3d.reshape(-1, 3)
    pts_str = " ".join(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}" for p in pts_flat)

    with open(filepath, "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="StructuredGrid" version="1.0" byte_order="LittleEndian">\n')
        f.write(f'  <StructuredGrid WholeExtent="0 {nx-1} 0 {ny-1} 0 0">\n')
        f.write(f'    <Piece Extent="0 {nx-1} 0 {ny-1} 0 0">\n')
        f.write("      <PointData>\n")
        for name, arr in point_data_arrays.items():
            ncomp = 1 if arr.ndim == 1 else arr.shape[1]
            flat = arr.flatten()
            data_str = " ".join(f"{v:.6f}" for v in flat)
            f.write(f'        <DataArray type="Float64" Name="{name}" '
                    f'NumberOfComponents="{ncomp}" format="ascii">\n')
            f.write(f"          {data_str}\n")
            f.write("        </DataArray>\n")
        f.write("      </PointData>\n")
        f.write("      <Points>\n")
        f.write('        <DataArray type="Float64" NumberOfComponents="3" format="ascii">\n')
        f.write(f"          {pts_str}\n")
        f.write("        </DataArray>\n")
        f.write("      </Points>\n")
        f.write("    </Piece>\n")
        f.write("  </StructuredGrid>\n")
        f.write("</VTKFile>\n")


# ---------------------------------------------------------------------------
# Dataset 1: Neural Network Loss Landscape (3D surface)
# ---------------------------------------------------------------------------
def generate_loss_landscape():
    """
    Simulate a loss landscape with multiple local minima resembling
    what's seen in deep learning optimization research (Li et al., 2018).
    """
    print("[1/4] Generating loss landscape surface...")
    res = 200
    x = np.linspace(-3, 3, res)
    y = np.linspace(-3, 3, res)
    X, Y = np.meshgrid(x, y)

    Z = (
        0.5 * (X**2 + Y**2)
        - 2.0 * np.exp(-((X - 1)**2 + (Y - 1)**2) / 0.3)
        - 1.5 * np.exp(-((X + 1.2)**2 + (Y + 0.8)**2) / 0.5)
        - 1.0 * np.exp(-((X - 0.5)**2 + (Y + 1.5)**2) / 0.2)
        + 0.3 * np.sin(3 * X) * np.cos(3 * Y)
    )

    grad_x, grad_y = np.gradient(Z, x, y)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)

    points = np.zeros((res, res, 3))
    points[:, :, 0] = X
    points[:, :, 1] = Y
    points[:, :, 2] = Z

    filepath = os.path.join(DATA_DIR, "loss_landscape.vts")
    write_vts(filepath, points, {
        "Loss": Z.flatten(),
        "GradientMagnitude": grad_mag.flatten(),
    })
    print(f"  -> Saved {filepath}")
    return filepath


# ---------------------------------------------------------------------------
# Dataset 2: Gradient Flow Vector Field
# ---------------------------------------------------------------------------
def generate_gradient_field():
    """
    3D vector field representing gradient descent trajectories
    through a parameter space — useful for understanding optimizer behavior.
    """
    print("[2/4] Generating gradient flow vector field...")
    res = 40
    x = np.linspace(-3, 3, res)
    y = np.linspace(-3, 3, res)
    z = np.linspace(-1, 3, res)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    r2 = X**2 + Y**2
    potential = 0.5 * r2 - 2.0 * np.exp(-r2 / 0.8) + 0.1 * Z**2

    Vx = -(X - 2.0 * X * np.exp(-r2 / 0.8) * (-2.0 / 0.8))
    Vy = -(Y - 2.0 * Y * np.exp(-r2 / 0.8) * (-2.0 / 0.8))
    Vz = -(0.2 * Z)

    vel_mag = np.sqrt(Vx**2 + Vy**2 + Vz**2)

    npts = res**3
    vecs = np.column_stack([Vx.flatten(), Vy.flatten(), Vz.flatten()])

    filepath = os.path.join(DATA_DIR, "gradient_field.vti")
    write_vti(filepath, (res, res, res), (-3, -3, -1), (6/(res-1), 6/(res-1), 4/(res-1)), {
        "GradientVelocity": vecs,
        "VelocityMagnitude": vel_mag.flatten(),
        "Potential": potential.flatten(),
    })
    print(f"  -> Saved {filepath}")
    return filepath


# ---------------------------------------------------------------------------
# Dataset 3: CNN Activation Volume (3D scalar field)
# ---------------------------------------------------------------------------
def generate_activation_volume():
    """
    Synthetic 3D activation map mimicking feature responses
    in a convolutional neural network layer.
    """
    print("[3/4] Generating CNN activation volume...")
    res = 80
    x = np.linspace(-2, 2, res)
    y = np.linspace(-2, 2, res)
    z = np.linspace(-2, 2, res)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    np.random.seed(42)
    activation = np.zeros_like(X)
    n_features = 12
    for _ in range(n_features):
        cx, cy, cz = np.random.uniform(-1.5, 1.5, 3)
        sigma = np.random.uniform(0.2, 0.6)
        amp = np.random.uniform(0.5, 1.0)
        activation += amp * np.exp(-((X-cx)**2 + (Y-cy)**2 + (Z-cz)**2) / (2*sigma**2))

    activation += 0.05 * np.random.randn(*activation.shape)
    activation = np.clip(activation, 0, None)
    activation /= activation.max()

    entropy = -activation * np.log(activation + 1e-10) - (1 - activation) * np.log(1 - activation + 1e-10)

    filepath = os.path.join(DATA_DIR, "activation_volume.vti")
    write_vti(filepath, (res, res, res), (-2, -2, -2), (4/(res-1), 4/(res-1), 4/(res-1)), {
        "Activation": activation.flatten(),
        "Entropy": entropy.flatten(),
    })
    print(f"  -> Saved {filepath}")
    return filepath


# ---------------------------------------------------------------------------
# Dataset 4: Embedding Space Point Cloud (clustered)
# ---------------------------------------------------------------------------
def generate_embedding_cloud():
    """
    Simulated 3D embedding space (like t-SNE/UMAP output) with distinct
    clusters representing different classes in a classification task.
    """
    print("[4/4] Generating embedding space point cloud...")
    np.random.seed(123)

    cluster_centers = [
        (2, 2, 1), (-2, 1, -1), (0, -2, 2),
        (3, -1, -2), (-1, 3, 0), (-2, -2, -1),
        (1, 0, 3), (0, 2, -3),
    ]
    points_per_cluster = 500
    all_points = []
    all_labels = []
    all_confidence = []

    for i, center in enumerate(cluster_centers):
        spread = np.random.uniform(0.3, 0.7)
        pts = np.random.randn(points_per_cluster, 3) * spread + np.array(center)
        all_points.append(pts)
        all_labels.append(np.full(points_per_cluster, i, dtype=float))
        dist = np.sqrt(np.sum((pts - np.array(center))**2, axis=1))
        conf = np.exp(-dist / spread)
        all_confidence.append(conf)

    points = np.vstack(all_points)
    labels = np.concatenate(all_labels)
    confidence = np.concatenate(all_confidence)

    filepath = os.path.join(DATA_DIR, "embedding_cloud.vtp")
    write_vtp_points(filepath, points, {
        "ClusterLabel": labels,
        "Confidence": confidence,
    })
    print(f"  -> Saved {filepath}")
    return filepath


if __name__ == "__main__":
    print("=" * 60)
    print("  Generating synthetic datasets for ParaView visualization")
    print("=" * 60)
    generate_loss_landscape()
    generate_gradient_field()
    generate_activation_volume()
    generate_embedding_cloud()
    print("\nAll datasets generated successfully.")
    print(f"Output directory: {DATA_DIR}")
