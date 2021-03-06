import numpy as np
from physics_sim import PhysicsSim

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, init_pose=None, init_velocities=None, 
        init_angle_velocities=None, runtime=5., target_pos=None):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime)
        self.action_repeat = 3
        
        self.action_low = 200
        self.action_high = 600
        self.action_size = 4

        self.state_size = self.action_repeat * 6
        

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) 

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        
        # first initialize the reward by how close the quadcopter is to target,
        # and a penalty by the stability of angles while taking off
        reward = 0
        
        # The penalty would be the sum of the angles, to keep the quadcopter going straight up
        stability_penalty = abs(self.sim.pose[3:6]).sum()
        stability_penalty += abs(self.sim.pose[0] - self.target_pos[0])
        stability_penalty += abs(self.sim.pose[1] - self.target_pos[1])
        # also a penalty for how far the quadcopter is from the target
        
        distance_penalty = abs(self.sim.pose[2] - self.target_pos[2])
        
        penalty = distance_penalty + stability_penalty
        # and for the reward it should be the Euclidean distance
        distance = np.sqrt((self.sim.pose[0] - self.target_pos[0]) ** 2 + 
                           (self.sim.pose[1] - self.target_pos[1]) ** 2 + 
                           (self.sim.pose[2] - self.target_pos[2]) ** 2)
#         distance = abs(self.sim.pose[2] - self.target_pos[2])

        if distance < 2.0: # If the Agent is close by a threshold to the target, he is a good boy and should get his reward 
            reward += 100.0
        else: # otherwise he should get a smaller one to keep him going
            reward += 10.0 
        
        # and Now combine the reward with the penalty
#         return np.tanh(reward - (penalty * 0.005))
        return reward - (penalty * 0.005)

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities
            reward += self.get_reward() 
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat) 
        return state