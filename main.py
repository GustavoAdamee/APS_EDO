import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random

# Radius of the pendulum balls
BALL_RADIUS = 0.05

def make_plot(array_penduluns, i):
    # loop over the pendulums and plot the results for each time i
    for pendulum in array_penduluns:

        ax.plot([0, pendulum.x1[i], pendulum.x2[i]], [0, pendulum.y1[i], pendulum.y2[i]], lw=2, c='k')
        #Pendulum fixed anchor point
        c0 = Circle((0, 0), BALL_RADIUS/2, fc='k', zorder=10)
        #Pendulum balls
        c1 = Circle((pendulum.x1[i], pendulum.y1[i]), BALL_RADIUS, fc='b', ec='b', zorder=10)
        c2 = Circle((pendulum.x2[i], pendulum.y2[i]), BALL_RADIUS, fc='r', ec='r', zorder=10)
        
        # ax.add_patch(c0)
        ax.add_patch(c1)
        ax.add_patch(c2)

    # Centralize the plot
    ax.set_xlim(-array_penduluns[0].L1-array_penduluns[0].L2-BALL_RADIUS, array_penduluns[0].L1+array_penduluns[0].L2+BALL_RADIUS)
    ax.set_ylim(-array_penduluns[0].L1-array_penduluns[0].L2-BALL_RADIUS, array_penduluns[0].L1+array_penduluns[0].L2+BALL_RADIUS)
    ax.set_aspect('equal', adjustable='box')
    # Save the images to a folder
    plt.axis('off')
    plt.savefig('frames/_img{:04d}.png'.format(i//di), dpi=72)
    plt.cla()

# Maximum time, time point spacings and the time grid (all in s).
tmax, dt = 30, 0.01
t = np.arange(0, tmax+dt, dt)

# Make an image every di time points, corresponding to a frame rate of fps
fps = 20
di = int(1/fps/dt)
fig = plt.figure(figsize=(8.3333, 6.25), dpi=72)
ax = fig.add_subplot(111)


import pendulum as p

# Create the pendulums array
array_penduluns = []

# Set the pendulums initial conditions
# Here we have 5 pendulums with different initial conditions
for i in range(0, 6):
    # Add some random angle to the initial conditions variating from -0.001 to 0.001 (very small changes)
    random_angle_1 = random.uniform(-0.001, 0.001)
    random_angle_2 = random.uniform(-0.001, 0.001)
    array_penduluns.append(p.pendulum(3*np.pi/7+random_angle_1, 3*np.pi/4+random_angle_2))

# Solve the pendulums equations
for pendulum in array_penduluns:
    pendulum.solve()

# Make the plots of each penduluns for each di and save the images
for i in range(0, t.size, di):
    print(i // di, '/', t.size // di)
    make_plot(array_penduluns, i)

# Make the gif
import glob
from PIL import Image

def make_gif(frame_folder):
    # Set the images to a list
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]
    # Sort the frames by the number in the filenames
    frames.sort(key=lambda x: int(x.filename.split("_img")[1].split(".")[0]))
    frame_one = frames[0]
    # Save the gif
    frame_one.save("pendulum.gif", format="GIF", append_images=frames,
               save_all=True, duration=60, loop=0)
    print("Gif saved!")
    
make_gif("frames")