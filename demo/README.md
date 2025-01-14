## **Quick start**

Don't want to install anything on your computer, we have set up a quick demo on [Google Colab](https://colab.research.google.com/drive/10aJ_kQMXNRb9srB-YD0OPJpE8GOvgQlU?usp=share_link).

---

## **Content**

1. [Installation](#installation)
2. [Extraction](#extract)
3. [Rate](#rate)
   - [Superficial Scald](#scald)
   - [Cross-section Starch](#starch)
   - [Pear Color Analysis](#pear)

---

## <a name="installation"></a> **Installation**

Want to try on your dataset? You can install our model to get started. First, it is recommended to use a package manager such as [conda](https://www.anaconda.com/) or [virtualenv](https://pypi.org/project/virtualenv/) to create a seperate, independent environment for **Granny**. An description of the package installation using conda is provided below.

Due to the limitation of TensorFlow 1.15, it is required to have Python version be **less than or equal** to 3.7

```bash
conda create -n <venv> python==3.7 -y
```

where `<venv>` is the name of the virtual environment

To activate the environment:

```bash
conda activate <venv>
```

Inside the environment, run the following to set up command line interfaces:

```bash
pip install --upgrade granny
```

---

## <a name="extract"></a> **EXTRACTION**

In order to rate each instance, each fruit will have to be extracted from the full-tray image.

Here is a demonstration on an apple tray, consisting of 18 apples (this also works for cross-sections and pears):

<div align="center">
  <img src="granny_smith_images/apple_tray/apple_demo_image.JPG" width="500px" />
  <p>Granny Smith apples</p>
</div>

In the command line, run Granny

```bash
granny --action extract --image_dir granny_smith_images/apple_tray/apple_demo_image.JPG --num_instances 18
```

to get a full-tray masked image (helpful to know what instances are extracted):

<div align="center">
  <img src="granny_smith_images/full_masked_images/apple_demo_image.png" width="500px" />
  <p> </p>
</div>

... and extracted individual images:

1st row:

<p float="left">
    <img src="granny_smith_images/segmented_images/apple_demo_image_4.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_3.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_2.png" width="100" /> 
    <img src="granny_smith_images/segmented_images/apple_demo_image_1.png" width="100" />
</p>

2nd row:

<p float="left">
    <img src="granny_smith_images/segmented_images/apple_demo_image_9.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_8.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_7.png" width="100" /> 
    <img src="granny_smith_images/segmented_images/apple_demo_image_6.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_5.png" width="100" />
</p>

3rd row:

<p float="left">
    <img src="granny_smith_images/segmented_images/apple_demo_image_13.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_12.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_11.png" width="100" /> 
    <img src="granny_smith_images/segmented_images/apple_demo_image_10.png" width="100" />
</p>

4th row:

<p float="left">
    <img src="granny_smith_images/segmented_images/apple_demo_image_18.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_17.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_16.png" width="100" /> 
    <img src="granny_smith_images/segmented_images/apple_demo_image_15.png" width="100" />
    <img src="granny_smith_images/segmented_images/apple_demo_image_14.png" width="100" />
</p>

---

## <a name="rate"></a> **RATE**

### <a name="scald"></a> **Superficial Scald**

With individual apples extracted to your "results", run Granny with a "scald" action

```bash
granny --action scald --image_dir ./results/segmented_images/ --num_instances 2
```

to get the following images, and a `ratings.csv` file containing scald rating for each instance.

1st row:

<p float="left">
    <img src="granny_smith_images/binarized_images/apple_demo_image_4.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_3.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_2.png" width="100" /> 
    <img src="granny_smith_images/binarized_images/apple_demo_image_1.png" width="100" />
</p>

2nd row:

<p float="left">
    <img src="granny_smith_images/binarized_images/apple_demo_image_9.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_8.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_7.png" width="100" /> 
    <img src="granny_smith_images/binarized_images/apple_demo_image_6.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_5.png" width="100" />
</p>

3rd row:

<p float="left">
    <img src="granny_smith_images/binarized_images/apple_demo_image_13.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_12.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_11.png" width="100" /> 
    <img src="granny_smith_images/binarized_images/apple_demo_image_10.png" width="100" />
</p>

4th row:

<p float="left">
    <img src="granny_smith_images/binarized_images/apple_demo_image_18.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_17.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_16.png" width="100" /> 
    <img src="granny_smith_images/binarized_images/apple_demo_image_15.png" width="100" />
    <img src="granny_smith_images/binarized_images/apple_demo_image_14.png" width="100" />
</p>

---

### <a name="starch"></a> **Iodine-stained Cross-section Starch**

If you have a full-tray image of cross-sections, similarly to apples, you can run the [Extraction](#extract) step on the image(s) to get each individual cross-section. This is an example on a tray:

<div align="center">
  <img src="cross_section_images/cross_section_tray/cross_section_demo_image.jpeg" width="400px" class="rotate"/>
  <p>Cross-sections</p>
</div>

1st row:

<p float="left">
    <img src="cross_section_images/segmented_images/cross_section_demo_image_1.png" width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_2.png" width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_3.png" width="100" /> 
    <img src="cross_section_images/segmented_images/cross_section_demo_image_4.png" width="100" />
</p>

2nd row:

<p float="left">
    <img src="cross_section_images/segmented_images/cross_section_demo_image_9.png" width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_8.png" width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_7.png" width="100" /> 
    <img src="cross_section_images/segmented_images/cross_section_demo_image_6.png" width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_5.png" width="100" />
</p>

3rd row:

<p float="left">
    <img src="cross_section_images/segmented_images/cross_section_demo_image_13.png"  width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_12.png"  width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_11.png"  width="100" /> 
    <img src="cross_section_images/segmented_images/cross_section_demo_image_10.png"  width="100" />
</p>

4th row:

<p float="left">
    <img src="cross_section_images/segmented_images/cross_section_demo_image_18.png"  width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_17.png"  width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_16.png"  width="100" /> 
    <img src="cross_section_images/segmented_images/cross_section_demo_image_15.png"  width="100" />
    <img src="cross_section_images/segmented_images/cross_section_demo_image_14.png"  width="100" />
</p>

#### How to install

To calculate the total starch area of each individual cross-section, you will have to install a separate application, [Fiji](https://imagej.net/software/fiji/), to run our macros. The installation is fairly straight-forward, and that would be everything you need to install. Here is the instructions:

1. Install [Fiji](https://imagej.net/software/fiji/)
2. Download our [macros](https://github.com/SystemsGenetics/granny/tree/master/GRANNY/Starch_Macros)
3. Launch Fiji
   - Open the macros downloaded from step 2
   - Click Run
4. Select input and output folder as prompted.
5. Check your selected output folder

#### Output

Inside your [output](https://github.com/SystemsGenetics/granny/tree/master/demo/cross_section_images/output) folder, there are:

1. Processed images of iodine stained cross-sections
2. A `"Results.csv"` file which stores the ratings and the total starch area

For any input image, below are the processed images:

<div align="left">
    <img src="cross_section_images/segmented_images/cross_section_demo_image_1.png" width="200" />
  <img src="cross_section_images/output/cross_section_demo_image_1.pngstarch.jpg" width="200px"/>
  <img src="cross_section_images/output/cross_section_demo_image_1.pngtotal_area.jpg" width="200px"/>
  <p> Cross-section image (a) stained with iodine and used as input for the starch analysis macro, (b) resulting identifying starch threshold image, and (c) resulting full cross-sectional area threshold </p>
</div>

---

### <a name="pear"></a> **Pear Color**

Similar to apples, you can use [Extraction](#extract) to extract pear images from a tray:

<div align="center">
  <img src="pear_images/full_masked_images/pear_demo_image.png" width="500px"/>
  <p>Pears</p>
</div>

1st row:

<p float="left">
    <img src="pear_images/segmented_images/pear_demo_image_1.png" width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_2.png" width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_3.png" width="100" /> 
    <img src="pear_images/segmented_images/pear_demo_image_4.png" width="100" />
</p>

2nd row:

<p float="left">
    <img src="pear_images/segmented_images/pear_demo_image_9.png" width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_8.png" width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_7.png" width="100" /> 
    <img src="pear_images/segmented_images/pear_demo_image_6.png" width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_5.png" width="100" />
</p>

3rd row:

<p float="left">
    <img src="pear_images/segmented_images/pear_demo_image_13.png"  width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_12.png"  width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_11.png"  width="100" /> 
    <img src="pear_images/segmented_images/pear_demo_image_10.png"  width="100" />
</p>

4th row:

<p float="left">
    <img src="pear_images/segmented_images/pear_demo_image_18.png"  width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_17.png"  width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_16.png"  width="100" /> 
    <img src="pear_images/segmented_images/pear_demo_image_15.png"  width="100" />
    <img src="pear_images/segmented_images/pear_demo_image_14.png"  width="100" />
</p>

To analyze pear's peel color, run Granny with a "pear" action

```bash
granny --action pear --image_dir ./results/segmented_images/ --num_instances 2
```

The pear's color will be extracted and mapped to the closest referenced color on the card below. The results are written to a file named "peel_colors.csv", including

    a. the file name
    b. the closest-matched bin
    c. a rating from 0-1
    d. LAB channel values of the image

<div align="center">
  <img src="pear_images/color_preference/pear_color_card.JPG" width="500px"/>
  <p>Color preferences</p>
</div>


