import math as m

def compute_motor_parameters(winding, torque_nm, speed_rad):
    # Motor Constants (AKE80-8)
    R_phase = 0.870  # Ohms (Phase Resistance)
    #L_phase = 990e-6  # Henry (Phase Inductance) #Ignored
    k_e = 0.315  # V/(rad/s) (Back EMF Constant)
    k_t = 0.32  # Nm/A (Torque Constant)
    
    # Compute Back EMF
    back_emf = k_e * speed_rad
    
    # Compute Phase Current (I_phase = T / k_t)
    I_phase_peak = torque_nm / k_t
    
    # Compute Resistive Voltage Drop
    resistive_drop = R_phase * I_phase_peak
    
    # Assuming steady-state operation (negligible L dI/dt term)
    V_phase_peak = back_emf + resistive_drop

    #Calculate line to line RMS value
    if winding == "wye":
        V_phase_line_RMS = V_phase_peak/m.sqrt(2)
        I_phase_line_RMS = I_phase_peak/m.sqrt(2)
        P_RMS = 3 * V_phase_line_RMS * I_phase_line_RMS


    if winding == "delta":
        V_phase_line_RMS = V_phase_peak/m.sqrt(2)
        I_phase_line_RMS = m.sqrt(3)/m.sqrt(2)*I_phase_peak
        P_RMS = m.sqrt(3)*V_phase_line_RMS * I_phase_line_RMS
    
    return [
        V_phase_peak,
        I_phase_peak,
        V_phase_line_RMS,
        I_phase_line_RMS,
        P_RMS
    ]

def compute_battery_parameters(P_DC,V_OC,impedance):
    #Battery model with internal resistance

    I_DC = (V_OC - m.sqrt(V_OC**2-4*impedance*P_DC))/(2*impedance)
    V_Bat = P_DC/I_DC
    V_Drop = V_OC-V_Bat

    return{ 
        "I_DC":I_DC,
        "V_Bat":V_Bat,
        "V_Drop":V_Drop
    }


if __name__ == "__main__":
    print(compute_motor_parameters("delta",1,100))
    print(compute_battery_parameters(100,36,0.01))
