# teach_a_quadcopter_to_flight
Deep Reinforcement learning agent to teach a quadcopter to flight


The task taught to the agent is Taking Off the ground up to 10 meters ( or whatever unit is used along z axis )

The Agent uses DDPG Network Architecture with an Actor of 3 Hidder layers of size 32, 64, 32 and a relu activation layer while the Critic 
uses 2 Dense Layers of size 32, 64 and a relu activation function.

The reward is defined by how close the agent is to the target position and penalized by the unstability of the take off ( Sum of the 
Euler angles of the quadcopter ) and the difference alogn the x and y axis.

This project is part of Udacity's Deep Learning Nanodegree Program
