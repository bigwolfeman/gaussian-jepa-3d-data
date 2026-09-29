# Source attribution

- Google Scanned Objects by Google Research supplied the scanned object meshes and textures. The source dataset uses CC BY 4.0: https://research.google/blog/scanned-objects-by-google-research-a-dataset-of-3d-scanned-common-household-items/ . We rendered these assets into new videos and fitted 3D Gaussian models to those renders. This project is not endorsed by Google.
- Poly Haven supplied HDRI backgrounds and lighting. Its assets use CC0: https://polyhaven.com/license .
- Kubric supplied the MOVi scene generator. Its code uses Apache 2.0: https://github.com/google-research/kubric . We modified the render and export pipeline to produce 768 × 768 videos and object, camera, and Gaussian training data.
- gsplat supplied the Gaussian rasterizer and fit implementation: https://github.com/nerfstudio-project/gsplat .

The generated data in this archive is licensed CC BY 4.0. `LICENSE-CODE` covers only the original utility code in this archive. It does not relicense Kubric, gsplat, or any source assets.
