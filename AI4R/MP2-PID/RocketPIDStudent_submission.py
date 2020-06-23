# Optimize your PID parameters here:
pressure_tau_p = 0.
pressure_tau_d = 0.

rocket_tau_p = 0.
rocket_tau_i = 0.
rocket_tau_d = 0.


def pressure_pd_solution(delta_t, current_pressure, target_pressure, data):
    """Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t (float): Time step length.
        current_pressure (float): Current pressure level of the turbopump.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    """
    alpha = 0.16
    beta = 1
    # TODO: remove naive solution
    #adjust_pressure = current_pressure

    # TODO: implement PD solution here
    ErrorP = target_pressure - current_pressure
    ErrorD = (ErrorP - data['ErrorP'])/delta_t
    adjust_pressure =  alpha * ErrorP + beta * ErrorD
    data['ErrorP'] = ErrorP
    data['ErrorD'] = ErrorD

    return adjust_pressure, data


def rocket_pid_solution(delta_t, current_velocity, optimal_velocity, data):
    """Student solution for maintaining rocket throttle through out the launch based on an optimal flight path

    Args:
        delta_t (float): Time step length.
        current_velocity (float): Current velocity of rocket.
        optimal_velocity (float): Optimal velocity of rocket.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Throttle to set, data dictionary to be passed through run.
    """

    # TODO: remove naive solution
    #throttle = optimal_velocity - current_velocity

    # TODO: implement PID Solution here
    alpha = 47#47
    beta = -10#-10
    gamma = 0.005#0.005
    ErrorP = optimal_velocity - current_velocity
    ErrorD = (ErrorP - data['ErrorP'])/delta_t
    ErrorI = data['ErrorI']
    ErrorI += ErrorP

    throttle = alpha * ErrorP + beta * ErrorD + gamma * ErrorI

    data['ErrorP'] = ErrorP
    data['ErrorD'] = ErrorD
    data['ErrorI'] = ErrorI

    
    return throttle, data
