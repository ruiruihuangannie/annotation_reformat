Collect & Re-format Segmentation Images
===
## Overview
This program aims to format collected segmentation images using OpenCV. 
The program can read collected images and convert them into an ML-friendly format.  
⚠️  This script must be run on a computer connected to a functioning MTM.
## Requirements
For first time users, please make sure to correctly set up the environment by following all steps and links below:

### 1. Setup [AMBF](https://github.com/WPI-AIM/ambf/wiki)
### 2. Setup [surgical_robotics_challenge](https://github.com/collaborative-robotics/surgical_robotics_challenge)
Once the repository is cloned and setup properly, when you navigate to the directory `~/surgical_robotics_challenge`, you should be able to run `./run_environment.sh` to launch the scene.
### 3. Setup [dVRK](https://github.com/jhu-dvrk/sawIntuitiveResearchKit/wiki/CatkinBuild) 
Once the repository is cloned and setup properly, you should be able to run `roscd dvrk_config`, which will land you from whichever folder you were in to `~/catkin_ws/src/cisst-saw/sawIntuitiveResearchKit/share`
### 4. Setup [ROS video recorder](https://github.com/Cartucho/dvrk_record_video)
In the `config.yaml` file, change the `output_dir` to the following code block, so that the recorded dataset will be numbered in ways compatible for future application:
```yaml
output_dir: "~/annotation_reformat/recordings/recxx" # with xx be whichever record you are working on 
```

Change `rostopic` to subscribe to AMBF rostopics to subscribe to left ECM and its corresponding annotation video:
```yaml
rostopic:
  cam1: "/ambf/env/cameras/cameraL/ImageData" # left ECM video
  cam2: "/ambf/env/cameras/cameraL2/ImageData" # left annotation video
```

Move the repository to your catkin workspace and re-build it with the new repository
```shell
mv dvrk_record_video ~/catkin_ws/src
catkin build --summary
```

### 5. Copy the current repo
```shell
git clone https://github.com/ruiruihuangannie/annotation_reformat
```

## Features
|           Feature            | Description                                                                                   |
|:----------------------------:|-----------------------------------------------------------------------------------------------|
|  `convert_ambf_standard.py`  | python script that converts ambf annotation video to match those from the public open dataset |
|          `image.py`          | python script that defines a customized image class                                           |


# Usage
## Step 1
### Terminal #1: `roscore`
```shell
source ~/catkin_ws/devel/setup.bash
roscore
```

### Terminal #2: `dVRK GUI console`
```shell
source ~/catkin_ws/devel/setup.bash
roscd dvrk_config
rosrun dvrk_robot dvrk_console_json -j jhu-daVinci/console-MTML-MTMR.json
```

### Terminal #3: `surgical robotics challenge`
```shell
source ~/ambf/build/devel/setup.bash
cd ~/surgical_robotics_challenge/
./run_environment.sh
```

### Terminal #4: `teleoperation for left MTM`
Note: It is recommended to change the ECM angle to increase the variety of training data.
```shell
source ~/ambf/build/devel/setup.bash
cd ~/surgical_robotics_challenge/scripts/surgical_robotics_challenge/teleoperation
python3 mtm_multi_psm_control.py --mtm MTML -c mtml --one 1 --two 0
```

### Terminal #5: `teleoperation for right MTM`
```shell
source ~/ambf/build/devel/setup.bash
cd ~/surgical_robotics_challenge/scripts/surgical_robotics_challenge/teleoperation
python3 mtm_multi_psm_control.py --mtm MTMR -c mtmr --one 0 --two 1
```

### Terminal #6: `video recorder`
```shell
source ~/catkin_ws/devel/setup.bash
cd ~/catkin_ws/src/dvrk_record_video/scripts
python3 node_dvrk_record_video.py
```
When data collection begins, the following `[Info]` should be displayed in the terminal. When finish recording data, press `ctrl+c` to exit the recorder.  
<img src=Media/recorder_info.png> 

### Check
When successfully launched, 5 separate application windows should appear, which includes:

|     Application     |                            Example                             |
|:-------------------:|:--------------------------------------------------------------:|
|    dvRK console     |        <img src=Media/dvrk_console.png width = "480" />        |
|   AMBF simulator    |       <img src=Media/ambf_launch_scene.png width="480"/>       |
|  MTM GUI <br>(L/R)  |     <img src = Media/mtm_control_gui.png width = "480" />      |
|    dvrk recorder    |  <img src = Media/recorder_double_screen.png width = "480" />  |

**Note**: At this point, the AMBF simulator should be projected onto the MTM console screen. If not, potential problems might include:
1. Not properly installing AMBF, dVRK, surgical robotics challenge, or the video recorder
2. Not properly sourcing the environment
3. If homing failed when launching the dVRK console, try `qlacommand -c close-relays` before launching again.

## Step 2 Check raw images
Navigate to the folder that now contains the recorded images and videos, which should contain:
1. one .mkv video
2. multiple .png segmentation images
3. one .txt timestamp file

## Step 3 Start image processing
The raw image data will then be processed with the following goals in mind:
1. the annotation video will be selected in 1 out of 10 to make sure that every frame is slightly different from the previous ones.
2. annotation #1: black-white (PSM arms/grippers, needle, thread = white), the rest are black
3. annotation #2: black-3 colors (PSM arms/grippers = white, needle = red, thread = green), the rest are black
4. annotation #3: black-4 colors (PSM arms = white, PSM grippers = blue, needle = red, thread = green), the rest are black

```shell
cd ~/annotation_reformat/ # Navigate to the folder that contains the current repo
python3 convert_ambf_standard.py -i ~/data/rec01 # Change it to point to whatever folder that contains the images
```
If applicable, repeat the above steps for all recordings.

## Step 4 Check segmented images
In each folder that now contains processed segmented images, each image should correspond to 4 segmented images, example:

|    Raw Image     | <img src=Media/ambf_raw.png width = "480" />  |
|:----------------:|:---------------------------------------------:|
| AMBF annotation  |   <img src=Media/ambf.png width = "480" />    |
|  annotation #1   |     <img src=Media/1.png width = "480" />     |
|  annotation #2   |     <img src=Media/2.png width = "480" />     |
|  annotation #3   |     <img src=Media/3.png width = "480" />     |


## Conclusion
This program provides a simple way to streamline collected segmentation images from AMBF using OpenCV. I hope this is helpful!