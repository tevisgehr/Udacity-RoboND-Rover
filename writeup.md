## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

![alt text][image1]

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
See jupyter notebook file included in repo.



#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
See jupyter notebook file included in repo. Also see included video.

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

The perception step function was mostly unchanged from the examples given in the lectures.  The main difference can be seen in lines 137-144 where I have excluded worldmap updates from any frames that were received while the sum of pitch and roll exceeds 0.5. This value was found experimentally. This change greatly improved fidelity (now averageing around 80%). Also I used color ranges, rather than color thresholds, which further imporved fidelity.

The most significant changes were made in the decision step. A new root branch of the decision tree was added for frames when a rock is detected. Its functionality is modeled off of the functionality of the original navigation branch. A third main branch was added to detect when the rover is stuck, and to have it enter a new 'reverse' mode for several timesteps. This reverse mode can be seen in action in the video. These changes, some minor logic involving steering, and a lot of parameter tuning were enough to collect three of the rocks and map over 60% of the world with a fidelity of nearly 80%.  

Some minor modifications were made in drive_rover.py and supporting_functions.py. New attributes were added to the Rover() class to support changes to decision.py. Some code was added to supporting functions to help with video generation.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**
FPS: ~ 13 to 30
Graphics: 1024x768, 'Good'

Some of this question was already answered in my answer to question number 1. The main strategy was to have the robot go into separate decision trees depending on whether or not it can see a rock. The functionality for steering and braking was already included in the normal navigation tree. This code was modified for the case of a rock sighting, but the task was accomplished in essentially the same way. I modified the brakeing and steering algorithms to include a new 'slowing' phase once the rover gets close to the rock. Also the steering direction in both the 'stopped' at a wall and 'reverse' because stuck states was changed from a static -15 to a random choice between either +15 of -15. This added robustness to the system and helped prevent getting stuck.  

After doing this, I still have a high failure rate due to the rover getting stuck. Modeling off my own behavior in such cases, I created a 'reverse' mode that gets kicked on once the rover has been unsuccessfuly trying to go forward for some number of steps. 

Results might be improved in the following ways:
1. Continue to tune parameters and tweak the logic of the current decsion tree structure. I did not nessesarily find optimum settings. 

2. Modify funationality and settings for higher speed.

3. Give the rover some knowledge of the map so that it is not just wandering around aimlessly forever. This could be done in a huge number of ways.

