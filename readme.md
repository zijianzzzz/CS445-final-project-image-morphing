<h1 align="center">Enhanced image morphing and useful applications</h1>

<p align="center">
  <strong>2026 Spring CS445 Course Project</strong><br>
</p>

---

### Project effect: 
Affine transformation + Laplacian pyramid blending + Auto landmark and triangulation + Multi-image bulk morphing:
<!-- <strong>Sample ouput:</strong> -->

<!-- <img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/3207051d-6e26-4a34-b652-da9665d8486f" /> -->
<img width="300" height="300" alt="output" src="https://github.com/user-attachments/assets/ffa70be3-dd75-46e5-9d0f-87322feb007c" />
<!-- <img width="610" height="612" alt="image" src="https://github.com/user-attachments/assets/3207051d-6e26-4a34-b652-da9665d8486f" />
<img width="610" height="612" alt="output" src="https://github.com/user-attachments/assets/ffa70be3-dd75-46e5-9d0f-87322feb007c" /> -->
<!-- <img width="410" height="412" alt="image" src="https://github.com/user-attachments/assets/3207051d-6e26-4a34-b652-da9665d8486f" />
<img width="410" height="412" alt="output" src="https://github.com/user-attachments/assets/ffa70be3-dd75-46e5-9d0f-87322feb007c" /> -->
<!-- <img width="300" height="300" alt="output" src="https://github.com/user-attachments/assets/e0c62f97-3173-4ed5-88bd-2731ee747aeb" /> -->
<!-- <img width="300" height="300" alt="output-5M" src="https://github.com/user-attachments/assets/487bf053-9f43-4db9-a5da-ebc20de29554" /> -->
<img width="300" height="300" alt="output-5m" src="https://github.com/user-attachments/assets/842790cf-af68-4106-8f48-eee77d2ee2d7" />

<p> TPS transformation + Laplacian pyramid blending + Auto landmark and triangulation + Multi-image bulk morphing: </p>

<img width="300" height="300" alt="output-4 5M" src="https://github.com/user-attachments/assets/a80187b3-396c-47e8-be5a-5c4a60bac24f" />

---


## Project overview:
<p>Image morphing is a digital image processing technique that creates a smooth and continuous transformation from one image to another. Unlike simple crossfading (which only blends pixel intensities), morphing combines geometric warping and color interpolation to produce a visually coherent transition where shapes, structures, and textures appear to evolve naturally over time. The basic techniques used in image morphing are: Linear cross-dissolve blending, Delaunay Triangulation, and Affine transformation. In this project, we will explore the advanced techniques which can enrich and enhance image morphing functionalities.</p>
<p>Firstly, the images are divided into several parts by selecting different points on them. These points
on the image are called control points. The control points are used to apply the Delaunay
triangulation as well as the geometric transformation to the images. </p>
<p>Morphing is primarily used in animation and special effects. In the present day,
there exist many software programs like After Effects, Nuke, etc. This software can also be used by people
who don’t know coding.</p>

## We focus on:
<p> We focus on advanced techniques that can enhance the morphing effect. For example, advanced geometric transformation, advanced image intensity blending, automatic landmark selecting and triangulation, supporting multiple input images bulk morphing, etc.</p>

## Implementation:

|   🔷 Basic image morphing       |          🔷 Enhanced image morphing                           |
|---------------------------------|---------------------------------------------------------------|
| Linear cross-dissolve blending  | Multi-band Gaussian-Laplacian pyramid blending                |
| Affine transformation           | Advanced TPS (Thin Plate Splines) transformation              |
| Manual control points selection | Automatic feature point/landmark detection and triangulation  |
| Two image morphing              | Support multi-input images' bulk morphing                     |


## Image morphing applications:
1. [Hybrid image using image morphing](https://github.com/johnlee2898-2/CS445-final-project-image-morphing/tree/main/morphing_applications/hybrid_image_with_morphing)
2. [Multi-image face averaging](https://github.com/johnlee2898-2/CS445-final-project-image-morphing/tree/main/morphing_applications/multi_img_processing)
3. [Expression transfer](https://github.com/johnlee2898-2/CS445-final-project-image-morphing/tree/main/morphing_applications/application3)
4. Application 4

---

## Instructions to use the code

This file contains the steps on how to execute the file.

### Main command options

`main.py` supports these options for the two-image morphing flow:

| Option | Values | Description |
|--------|--------|-------------|
| `--correspondence` | `manual`, `auto`, `compare` | Choose manual point clicking, automatic face landmark correspondences, or manual-vs-auto evaluation. |
| `--transform` | `affine`, `tps` | Choose affine triangle warping or Thin Plate Spline warping. |
| `--blend` | `linear`, `laplacian` | Choose linear cross-dissolve or Gaussian-Laplacian pyramid blending. |
| `--frames` | integer | Number of intermediate frames to generate, excluding the source and destination images. |
| `--total-frames` | integer | Total number of output frames, including source and destination endpoints. |
| `--no-display` | flag | Save outputs without opening OpenCV display windows. Useful for automatic runs. |
| `--save-correspondences` | optional path | Save the selected correspondence points to JSON. |

Note: TPS mode uses `--frames`. Do not use `--total-frames` with `--transform tps`. TPS also opens a small face-border selection step even when automatic correspondences are used, so do not pass `--no-display` for TPS runs.


---
### Manual Correspondence Examples

<strong>Step-1</strong> Open the command line or terminal and enter the following -
```text
$ python3 main.py img1.png img2.png --correspondence manual --transform affine --blend linear --frames 100
$ python3 main.py img1.png img2.png --correspondence manual --transform affine --blend laplacian --frames 100
```
Here, img1 refers to the source image and img2 refers to the destination image.

<strong>Step-2</strong> Enter the control points on img1 using mouse click and press escape after entering all points. Do the same for img2, but the order of points should remain the same.

The program now automatically adds boundary anchor points around the image border (corners plus quarter-edge anchors), so you only need to click the meaningful feature points manually.

After doing so, the system will display and save the triangulated images.

<strong>Step-3</strong> Enter the number of intermediate images you want to see, or pass it directly with `--frames`.

The morphing method is selected from the command line. Use `--transform affine` or `--transform tps`, and use `--blend linear` or `--blend laplacian`.

The code will take some time to create and save the desired number of intermediates. We have directly saved the images to save time.

Output folders:

```text
generated-images/manual-linear-dissolve/
generated-images/manual-laplacian-pyramid-blending/
```

---
### Automatic Correspondence Examples

Automatic correspondence uses face landmarks, so it works best when each input image contains a clear face.

```text
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --blend linear --frames 30 --no-display
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --blend laplacian --frames 30 --no-display
```

To generate a full 100-frame sequence where `inter_1.jpg` is the source image and `inter_100.jpg` is the destination image:

```text
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --blend linear --total-frames 100 --no-display
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --blend laplacian --total-frames 100 --no-display
```

Automatic correspondence outputs are saved to:

```text
generated-images/auto-linear-dissolve/
generated-images/auto-laplacian-pyramid-blending/
```

To save the automatically detected points and reuse them later:

```text
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --save-correspondences generated-images/auto_correspondences.json --total-frames 100 --no-display
$ python3 main.py img1.png img2.png --correspondence auto --transform affine --auto-correspondences generated-images/auto_correspondences.json --total-frames 100 --no-display
```

To evaluate manual vs. automatic correspondences, first save a manual correspondence file, then run compare mode:

```text
$ python3 main.py img1.png img2.png --correspondence manual --transform affine --blend laplacian --total-frames 100 --save-correspondences generated-images/manual_correspondences.json
$ python3 main.py img1.png img2.png --correspondence compare --transform affine --blend linear --total-frames 100 --manual-correspondences generated-images/manual_correspondences.json --no-display
$ python3 main.py img1.png img2.png --correspondence compare --transform affine --blend laplacian --total-frames 100 --manual-correspondences generated-images/manual_correspondences.json --no-display
```

The comparison metrics and figures are saved to:

```text
evaluation-results/manual-vs-auto/linear_metrics.csv
evaluation-results/manual-vs-auto/laplacian_metrics.csv
evaluation-results/manual-vs-auto/linear_side_by_side_frame_2.png
evaluation-results/manual-vs-auto/linear_side_by_side_frame_51.png
evaluation-results/manual-vs-auto/linear_side_by_side_frame_99.png
evaluation-results/manual-vs-auto/laplacian_side_by_side_frame_2.png
evaluation-results/manual-vs-auto/laplacian_side_by_side_frame_51.png
evaluation-results/manual-vs-auto/laplacian_side_by_side_frame_99.png
```


---
### TPS Transformation Examples

Thin Plate Spline transformation is selected with `--transform tps`. It can be combined with manual or automatic correspondences and either blending method. After the key correspondences are chosen, TPS asks for a rectangular face border on each image: click two opposite corners around the face/head boundary, then press Enter. Press `R` to reset the rectangle if needed. The code generates several border rings from that rectangle to reduce edge distortion.

```text
$ python3 main.py img1.png img2.png --correspondence manual --transform tps --blend linear --frames 30
$ python3 main.py img1.png img2.png --correspondence manual --transform tps --blend laplacian --frames 30
$ python3 main.py img1.png img2.png --correspondence auto --transform tps --blend laplacian --frames 30
```

Output folders:

```text
generated-images/manual-linear-dissolve/
generated-images/manual-laplacian-pyramid-blending/
generated-images/auto-linear-dissolve/
generated-images/auto-laplacian-pyramid-blending/
generated-images/tps-linear-dissolve/
generated-images/tps-laplacian-pyramid-blending/
```

Note: `--multi-image ""` is not needed for normal two-image morphing. Leave `--multi-image` out unless you want to run the multi-image feature.

The command below is the corrected version of the auto-correspondence plus Laplacian example. It uses the default affine transform and runs the two-image flow:

```text
$ python3 main.py img1.png img2.png --blend laplacian --correspondence auto --frames 30 --no-display
```


---
## Multi Image Morphing

this capability allows morphing multiple images when the initial code only allowed 2.
the functionality can be split into two parts

<Strong> Sequential image morphing</Strong>    

this involves morphing the first image to the second, the second to the third and so on, making a sequential number of morphs  

<Strong> Image averaging </Strong>

this functionaliy finds the average morph posistion between all of the images, and averages the images together to create an average image.

<Strong> Use case </Strong>


this capability adds three new flags to the cli
```text
--multi-image {location of the directory of images}'
```
will automaticaly add all the images in said directory to the process

```text
--multi-image-trigs saved
```
will use any previously manually entered points to mark the morphing triangles

the program defaults to sequential image morphing and will ask you how many frames you would like to generate between images, but you can add the flag 
```text
'--multi-image-proccess avg' 
```
to run the average image morphing instead

```text
$ python3 main.py img1.png img8.png --multi-image ./multi-input-images/ --blend linear --correspondence manual --frames 10
$ python3 main.py img1.png img8.png --multi-image ./multi-input-images/ --blend laplacian --correspondence manual --frames 10
```

### Multi-Image TPS Demo

Use `--transform tps` to run Thin Plate Spline warping through the whole multi-image sequence. It can be combined with `--blend linear` or `--blend laplacian`. Manual mode uses the saved or newly clicked control points for each image. TPS also asks for a two-click rectangular face border for each image, even in automatic correspondence mode.

```text
$ python3 main.py img1.png img8.png --multi-image ./multi-input-images/ --correspondence manual --transform tps --blend linear --frames 10
$ python3 main.py img1.png img8.png --multi-image ./multi-input-images/ --correspondence manual --transform tps --blend laplacian --frames 10
```

For an overall demo that combines multi-image morphing, automatic correspondence, TPS transformation, and Laplacian pyramid blending:

```text
$ python3 main.py img1.png img8.png --multi-image ./multi-input-images/ --correspondence auto --transform tps --blend laplacian --frames 10
```

Output folders:

```text
generated-images/multi-input-linear-dissolve/
generated-images/multi-input-laplacian-pyramid-blending/
generated-images/multi-input-tps-linear-dissolve/
generated-images/multi-input-tps-laplacian-pyramid-blending/
```

<strong>Step-4</strong> Open the command line or terminal and enter the following to generate mp4 video or gif with all the intermediate images generated in step-3:


## install ffmpeg
```text
$ sudo apt update
$ sudo apt install ffmpeg
$ ffmpeg -version
```

## generate mp4 or gif
```text
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/manual-linear-dissolve/inter_%d.jpg generated-images/manual-linear-dissolve/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/manual-linear-dissolve/inter_%d.jpg generated-images/manual-linear-dissolve/output.mp4

$ ffmpeg -framerate 15 -start_number 1 -i generated-images/manual-laplacian-pyramid-blending/inter_%d.jpg generated-images/manual-laplacian-pyramid-blending/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/manual-laplacian-pyramid-blending/inter_%d.jpg generated-images/manual-laplacian-pyramid-blending/output.mp4

$ ffmpeg -framerate 15 -start_number 1 -i generated-images/auto-linear-dissolve/inter_%d.jpg generated-images/auto-linear-dissolve/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/auto-linear-dissolve/inter_%d.jpg generated-images/auto-linear-dissolve/output.mp4

$ ffmpeg -framerate 15 -start_number 1 -i generated-images/auto-laplacian-pyramid-blending/inter_%d.jpg generated-images/auto-laplacian-pyramid-blending/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/auto-laplacian-pyramid-blending/inter_%d.jpg generated-images/auto-laplacian-pyramid-blending/output.mp4

$ ffmpeg -framerate 15 -start_number 1 -i generated-images/tps-linear-dissolve/inter_%d.jpg generated-images/tps-linear-dissolve/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/tps-linear-dissolve/inter_%d.jpg generated-images/tps-linear-dissolve/output.mp4

$ ffmpeg -framerate 15 -start_number 1 -i generated-images/tps-laplacian-pyramid-blending/inter_%d.jpg generated-images/tps-laplacian-pyramid-blending/output.gif
$ ffmpeg -framerate 15 -start_number 1 -i generated-images/tps-laplacian-pyramid-blending/inter_%d.jpg generated-images/tps-laplacian-pyramid-blending/output.mp4

$ ffmpeg -framerate 15 -i generated-images/multi-input-laplacian-pyramid-blending/inter_%d.jpg generated-images/multi-input-laplacian-pyramid-blending/output.gif
$ ffmpeg -framerate 15 -i generated-images/multi-input-laplacian-pyramid-blending/inter_%d.jpg generated-images/multi-input-laplacian-pyramid-blending/output.mp4
$ ffmpeg -framerate 15 -i generated-images/multi-input-linear-dissolve/inter_%d.jpg generated-images/multi-input-linear-dissolve/output.gif
$ ffmpeg -framerate 15 -i generated-images/multi-input-linear-dissolve/inter_%d.jpg generated-images/multi-input-linear-dissolve/output.mp4
$ ffmpeg -framerate 15 -i generated-images/multi-input-tps-linear-dissolve/inter_%d.jpg generated-images/multi-input-tps-linear-dissolve/output.gif
$ ffmpeg -framerate 15 -i generated-images/multi-input-tps-linear-dissolve/inter_%d.jpg generated-images/multi-input-tps-linear-dissolve/output.mp4
$ ffmpeg -framerate 15 -i generated-images/multi-input-tps-laplacian-pyramid-blending/inter_%d.jpg generated-images/multi-input-tps-laplacian-pyramid-blending/output.gif
$ ffmpeg -framerate 15 -i generated-images/multi-input-tps-laplacian-pyramid-blending/inter_%d.jpg generated-images/multi-input-tps-laplacian-pyramid-blending/output.mp4
```


---
<strong>Note: Please follow the project structure to add more files </strong>
## Project Structure

```text
CS445-final-project-image-morphing/

│── morphing-applications           # Directory for all morphing useful applications
│        ├── hybrid_image_with_morphing
│        ├── multi_img_processing   # average and sequential multi image processing
│        |        ├── multi-input-generated-imgs
|        |        ├── multi-input-triangulated-imgs
|        |        ├── trig-files
|        |        └── utils.py
│        ├── expression_transfer
│        └── application4
│
├── utils
│    └── image_utils.py             # Directory for all utils files
│
│── Triangulated Images             # Directory for generated triangulated images
│        ├── Triangulated Image_src.jpg
│        └── Triangulated Image_dest.jpg
│
├── generated-images                # Directory saving all generated intermediate morphing images and generated MP4 and GIF files
│        ├── manual-laplacian-pyramid-blending         # Laplacian pyramid blending
│        │        ├── inter_1.jpg
│        │        ├── inter_2.jpg
│        │        ├── ..........
│        │        ├── inter_100.jpg
│        │        ├── output.gif
│        │        └── output.mp4
│        ├── manual-linear-dissolve                    # Linear cross-dissolve blending
│        │        ├── inter_1.jpg
│        │        ├── inter_2.jpg
│        │        ├── ..........
│        │        ├── inter_100.jpg
│        │        ├── output.gif
│        │        └── output.mp4
│        ├── auto-laplacian-pyramid-blending            # Automatic correspondence
│        ├── auto-linear-dissolve
│        ├── multi-input-laplacian-pyramid-blending     # Multiple input images case
│        ├── multi-input-linear-dissolve
│        ├── multi-input-tps-linear-dissolve            # Multiple input images with TPS
│        ├── multi-input-tps-laplacian-pyramid-blending # Multiple input images with TPS and Laplacian blending
│        ├── tps-laplacian-pyramid-blending             # Tps transformation
│        └── tps-linear-dissolve
|
│
├── evaluation-results
│        ├── manual-vs-auto
│        └── matplotlib-cache
│
├── main.py                         # This is the entrance Python file
│
├── input-images                    # Directory for two input images
│       ├── img1.png 
│       └── img2.png
│
├── morph                           # Morphing related source code
│       ├── blend.py
│       ├── correspondences.py
│       ├── triangulation.py
│       ├── evaluation.py
│       ├── tps.py
│       └── warp.py
│
├── multi-input-images              # Directory for multiple input images, which will be used to generate multiple continuous morphing effects
│       ├── multi-image1.png
│       ├── multi-image2.png
│       ├── multi-image3.png
│       └── .........
│
├── requirements.txt                # Document
│
└── README.md

```

