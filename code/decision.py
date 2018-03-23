import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    #Count up when the rover appears to be stuck
    if Rover.throttle > 0 and Rover.vel < 0.2:
        Rover.stuck_count += 1
    #Go into reverse mode
    if Rover.stuck_count > 100 or Rover.mode == 'reverse':
        if Rover.mode == 'forward':
            Rover.steer = np.sign(np.random.rand()) * -15
        Rover.mode = 'reverse'
        Rover.stuck_count = 0
        print('************************************* **************** ****************')
        print('************************************* STUCK, REVERSING ****************')
        print('************************************* **************** ****************')
        Rover.throttle = -0.2
        Rover.reverse_count += 1
        if Rover.reverse_count > 50:
            Rover.reverse_count = 0
            Rover.mode = 'stop'
        return Rover

    #reset stuck count if the rover gets up to speed of 1.0
    if Rover.vel > 1.0:
        Rover.stuck_count = 0

    if Rover.nav_angles is not None:
        #If rover sees a rock (this may noe work right if it can see two rocks at the s
        #                      same time, if this becomes problem, consider clustering)
        if len(Rover.rock_angles) > 0:
            if len(Rover.nav_angles) > 0:
                print('############################### Rock',len(Rover.nav_angles), np.mean(Rover.nav_angles), np.mean(Rover.nav_dists), Rover.mode)
                print('############################### Rock', np.mean(Rover.rock_angles), np.mean(Rover.rock_dists))
            # Check for Rover.mode status
            if Rover.mode == 'forward':
                # Check the extent of navigable terrain
                if np.mean(Rover.rock_dists) >= Rover.slow_rock:
                    # If mode is forward, navigable terrain looks good
                    # and velocity is below max, then throttle
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                    else:  # Else coast
                        Rover.throttle = 0
                    Rover.brake = 0
                    # Set steering to average angle clipped to the range +/- 15
                    Rover.steer = np.clip(np.mean(Rover.rock_angles * 180 / np.pi), -15, 15)
                # If there's a lack of navigable terrain pixels then go to 'stop' mode
                elif np.mean(Rover.rock_dists) < Rover.slow_rock and np.mean(Rover.rock_dists) > Rover.pickup_dist:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SLOWING DOWN !!!!!!!!')
                    # If mode is forward, navigable terrain looks good
                    # and velocity is below max, then throttle
                    if Rover.vel > Rover.pickup_slowdown_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = 0
                        Rover.brake = Rover.brake_set/2
                    elif Rover.vel <Rover.pickup_slowdown_vel:  # Inch Up To Rock
                        Rover.throttle = Rover.throttle_set/4
                        Rover.brake = 0
                    else:  # Else coast
                        Rover.throttle = 0
                        Rover.brake = 0
                    # Set steering to average angle clipped to the range +/- 15
                    Rover.steer = np.clip(np.mean(Rover.rock_angles * 180 / np.pi), -15, 15)
                elif np.mean(Rover.rock_dists) < Rover.pickup_dist:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! STOPPING !!!!!!!!')
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set *5
                    Rover.steer = 0
                    Rover.mode = 'stop'

            # If we're already in "stop" mode then make different decisions
            elif Rover.mode == 'stop':
                # If we're in stop mode but still moving keep braking
                if Rover.vel > 0.1:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                # If we're not moving (vel < 0.2) then do something else
                elif Rover.vel <= 0.1:
                    # Now we're stopped and we have vision data to see if there's a path forward
                    if Rover.near_sample:
                        Rover.throttle = 0
                        # Release the brake to allow turning
                        Rover.brake = 0
                        # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    # If we're stopped but see sufficient navigable terrain in front then go!
                    if np.mean(Rover.rock_dists) >= Rover.pickup_dist:
                        # Set throttle back to stored value
                        Rover.throttle = Rover.throttle_set
                        # Release the brake
                        Rover.brake = 0
                        # Set steer to mean angle
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15)
                        Rover.mode = 'forward'
        else:
            if len(Rover.nav_angles) > 0:
                print('############################### Nav',len(Rover.nav_angles), np.mean(Rover.nav_angles), np.mean(Rover.nav_dists), Rover.mode)
            # Check for Rover.mode status
            if Rover.mode == 'forward':
                # Check the extent of navigable terrain
                if len(Rover.nav_angles) >= Rover.stop_forward:
                    # If mode is forward, navigable terrain looks good
                    # and velocity is below max, then throttle
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                    else: # Else coast
                        Rover.throttle = 0
                    Rover.brake = 0
                    # Set steering to average angle clipped to the range +/- 15
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                # If there's a lack of navigable terrain pixels then go to 'stop' mode
                elif len(Rover.nav_angles) < Rover.stop_forward:
                        # Set mode to "stop" and hit the brakes!
                        Rover.throttle = 0
                        # Set brake to stored brake value
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0
                        Rover.mode = 'stop'

            # If we're already in "stop" mode then make different decisions
            elif Rover.mode == 'stop':
                # If we're in stop mode but still moving keep braking
                if Rover.vel > 0.2:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                # If we're not moving (vel < 0.2) then do something else
                elif Rover.vel <= 0.2:
                    # Now we're stopped and we have vision data to see if there's a path forward
                    if len(Rover.nav_angles) < Rover.go_forward:
                        Rover.throttle = 0
                        # Release the brake to allow turning
                        Rover.brake = 0
                        # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                        np.sign(np.mean(Rover.nav_angles))
                        Rover.steer = 15
                    # If we're stopped but see sufficient navigable terrain in front then go!
                    if len(Rover.nav_angles) >= Rover.go_forward:
                        # Set throttle back to stored value
                        Rover.throttle = Rover.throttle_set
                        # Release the brake
                        Rover.brake = 0
                        # Set steer to mean angle
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                        Rover.mode = 'forward'
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

