import pandas as pd
import matplotlib.pyplot as plt

import data_import
import motor_model

def apply_reduction(df_torques,df_velocities):
       
    knee_reduction = float(8*6)
    hip_ver_reduction = float(8*10)
    hip_lat_reduction = float(8*1)

    reductions = {
        "charlotte_fr_knee": knee_reduction,
        "charlotte_fl_knee": knee_reduction,
        "charlotte_mr_knee": knee_reduction,
        "charlotte_ml_knee": knee_reduction,
        "charlotte_br_knee": knee_reduction,
        "charlotte_bl_knee": knee_reduction,
        "charlotte_fr_hip_ver": hip_ver_reduction,
        "charlotte_fl_hip_ver": hip_ver_reduction,
        "charlotte_mr_hip_ver": hip_ver_reduction,
        "charlotte_ml_hip_ver": hip_ver_reduction,
        "charlotte_br_hip_ver": hip_ver_reduction,
        "charlotte_bl_hip_ver": hip_ver_reduction,
        "charlotte_fr_hip_lat": hip_lat_reduction,
        "charlotte_fl_hip_lat": hip_lat_reduction,
        "charlotte_mr_hip_lat": hip_lat_reduction,
        "charlotte_ml_hip_lat": hip_lat_reduction,
        "charlotte_br_hip_lat": hip_lat_reduction,
        "charlotte_bl_hip_lat": hip_lat_reduction
    }

    df_torques = df_torques.rename(columns=lambda x: x.replace("_actuator", ""))

    adjusted_torque_df = df_torques.set_index("Time").div(reductions).reset_index()

    df_velocities=df_velocities.drop(columns=[
                    "charlotte_base_link_wx",
                    "charlotte_base_link_wy",
                    "charlotte_base_link_wz",
                    "charlotte_base_link_vx",
                    "charlotte_base_link_vy",
                    "charlotte_base_link_vz"
                    ])
    
    df_velocities = df_velocities.rename(columns=lambda x: x.replace("_w", ""))

    adjusted_velocity_df = df_velocities.set_index("Time").mul(reductions).reset_index()

    return adjusted_torque_df,adjusted_velocity_df

def compute_parameters_for_row(row,actuator):
    results = [df_dict["joint_torque_reduced"]["Time"][row.name]]
    results.extend(motor_model.compute_motor_parameters(
        "wye",
        df_dict["joint_torque_reduced"][actuator][row.name],  # Torque at same row index
        df_dict["joint_velocity_reduced"][actuator][row.name],   # Velocity at same row index
    ))
    
    return results


if __name__ == "__main__":
    # Example usage
    directory_path = "data"  # Replace with your actual directory path
    df_dict = data_import.load_all_csv_in_directory(directory_path)

    # Example: Print first few rows of each dataframe
    for file_name, df in df_dict.items():
        print(f"\n{file_name}:")
        print(df.head())
    
    df_dict["joint_torque_reduced"], df_dict["joint_velocity_reduced"] = apply_reduction(df_dict["joint_torque"],df_dict["joint_velocity"])

    print("joint_torque_reduced:")
    print(df_dict["joint_torque_reduced"].head())

    print("joint_velocity_reduced:")
    print(df_dict["joint_velocity_reduced"])


#Calculated motor voltage and current based on simulation results
df_motor_values={}
for actuator in list(df_dict["joint_velocity_reduced"])[1:]:
    #Apply function to each row in joint_velocity_reduced DataFrame
    df_results = df_dict["joint_velocity_reduced"].apply(compute_parameters_for_row,args=[actuator], axis=1)

    # Convert list outputs into separate columns
    df_results = pd.DataFrame(df_results.tolist(), columns=["Time","V_phase_peak","I_phase_peak","V_phase_line_RMS","I_phase_line_RMS","P_RMS"], index=df_dict["joint_velocity_reduced"].index)
   
    df_motor_values[actuator] = df_results
    # Display the results
    print(actuator)
    print(df_motor_values[actuator])

# Scatter plots
fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_hip_ver"]["Time"], df_motor_values["charlotte_fr_hip_ver"]["V_phase_peak"], label = "charlotte_fr_hip_ver", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_hip_ver"]["Time"], df_motor_values["charlotte_fl_hip_ver"]["V_phase_peak"], label = "charlotte_fl_hip_ver", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_hip_ver"]["Time"], df_motor_values["charlotte_mr_hip_ver"]["V_phase_peak"], label = "charlotte_mr_hip_ver", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_hip_ver"]["Time"], df_motor_values["charlotte_ml_hip_ver"]["V_phase_peak"], label = "charlotte_ml_hip_ver", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_hip_ver"]["Time"], df_motor_values["charlotte_br_hip_ver"]["V_phase_peak"], label = "charlotte_br_hip_ver", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_hip_ver"]["Time"], df_motor_values["charlotte_bl_hip_ver"]["V_phase_peak"], label = "charlotte_bl_hip_ver", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Voltage (V)")
plt.title("Hip Vertical Voltage (Peak)")
plt.axhline(y=30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.axhline(y=-30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.grid(True)
plt.savefig("Hip Vertical Voltage (Peak)", dpi=300, bbox_inches="tight")

fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_hip_ver"]["Time"], df_motor_values["charlotte_fr_hip_ver"]["I_phase_line_RMS"], label = "charlotte_fr_hip_ver", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_hip_ver"]["Time"], df_motor_values["charlotte_fl_hip_ver"]["I_phase_line_RMS"], label = "charlotte_fl_hip_ver", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_hip_ver"]["Time"], df_motor_values["charlotte_mr_hip_ver"]["I_phase_line_RMS"], label = "charlotte_mr_hip_ver", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_hip_ver"]["Time"], df_motor_values["charlotte_ml_hip_ver"]["I_phase_line_RMS"], label = "charlotte_ml_hip_ver", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_hip_ver"]["Time"], df_motor_values["charlotte_br_hip_ver"]["I_phase_line_RMS"], label = "charlotte_br_hip_ver", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_hip_ver"]["Time"], df_motor_values["charlotte_bl_hip_ver"]["I_phase_line_RMS"], label = "charlotte_bl_hip_ver", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Current (A)")
plt.title("Hip Vertical Current (Line RMS)")
plt.axhline(y=4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.grid(True)
plt.savefig("Hip Vertical Current (Line RMS)", dpi=300, bbox_inches="tight")

fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_hip_lat"]["Time"], df_motor_values["charlotte_fr_hip_lat"]["V_phase_peak"], label = "charlotte_fr_hip_lat", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_hip_lat"]["Time"], df_motor_values["charlotte_fl_hip_lat"]["V_phase_peak"], label = "charlotte_fl_hip_lat", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_hip_lat"]["Time"], df_motor_values["charlotte_mr_hip_lat"]["V_phase_peak"], label = "charlotte_mr_hip_lat", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_hip_lat"]["Time"], df_motor_values["charlotte_ml_hip_lat"]["V_phase_peak"], label = "charlotte_ml_hip_lat", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_hip_lat"]["Time"], df_motor_values["charlotte_br_hip_lat"]["V_phase_peak"], label = "charlotte_br_hip_lat", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_hip_lat"]["Time"], df_motor_values["charlotte_bl_hip_lat"]["V_phase_peak"], label = "charlotte_bl_hip_lat", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Voltage (V)")
plt.title("Hip Lateral Voltage (Peak)")
plt.axhline(y=30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.axhline(y=-30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.grid(True)
plt.savefig("Hip Lateral Voltage (Peak)", dpi=300, bbox_inches="tight")

fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_hip_lat"]["Time"], df_motor_values["charlotte_fr_hip_lat"]["I_phase_line_RMS"], label = "charlotte_fr_hip_lat", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_hip_lat"]["Time"], df_motor_values["charlotte_fl_hip_lat"]["I_phase_line_RMS"], label = "charlotte_fl_hip_lat", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_hip_lat"]["Time"], df_motor_values["charlotte_mr_hip_lat"]["I_phase_line_RMS"], label = "charlotte_mr_hip_lat", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_hip_lat"]["Time"], df_motor_values["charlotte_ml_hip_lat"]["I_phase_line_RMS"], label = "charlotte_ml_hip_lat", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_hip_lat"]["Time"], df_motor_values["charlotte_br_hip_lat"]["I_phase_line_RMS"], label = "charlotte_br_hip_lat", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_hip_lat"]["Time"], df_motor_values["charlotte_bl_hip_lat"]["I_phase_line_RMS"], label = "charlotte_bl_hip_lat", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Current (A)")
plt.title("Hip Lateral Current (Line RMS)")
plt.axhline(y=4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.grid(True)
plt.savefig("Hip Lateral Current (Line RMS)", dpi=300, bbox_inches="tight")

fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_knee"]["Time"], df_motor_values["charlotte_fr_knee"]["V_phase_peak"], label = "charlotte_fr_knee", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_knee"]["Time"], df_motor_values["charlotte_fl_knee"]["V_phase_peak"], label = "charlotte_fl_knee", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_knee"]["Time"], df_motor_values["charlotte_mr_knee"]["V_phase_peak"], label = "charlotte_mr_knee", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_knee"]["Time"], df_motor_values["charlotte_ml_knee"]["V_phase_peak"], label = "charlotte_ml_knee", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_knee"]["Time"], df_motor_values["charlotte_br_knee"]["V_phase_peak"], label = "charlotte_br_knee", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_knee"]["Time"], df_motor_values["charlotte_bl_knee"]["V_phase_peak"], label = "charlotte_bl_knee", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Voltage (V)")
plt.title("Knee Voltage (Peak)")
plt.axhline(y=30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.axhline(y=-30, color='r', linestyle='--', linewidth=2, label="Voltage Limit")
plt.grid(True)
plt.savefig("Knee Voltage (Peak)", dpi=300, bbox_inches="tight")

fig = plt.figure(figsize=(8, 5))  # Set figure size
ax1 = fig.add_subplot(111)
ax1.scatter(df_motor_values["charlotte_fr_knee"]["Time"], df_motor_values["charlotte_fr_knee"]["I_phase_line_RMS"], label = "charlotte_fr_knee", color='r', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_fl_knee"]["Time"], df_motor_values["charlotte_fl_knee"]["I_phase_line_RMS"], label = "charlotte_fl_knee", color='g', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_mr_knee"]["Time"], df_motor_values["charlotte_mr_knee"]["I_phase_line_RMS"], label = "charlotte_mr_knee", color='b', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_ml_knee"]["Time"], df_motor_values["charlotte_ml_knee"]["I_phase_line_RMS"], label = "charlotte_ml_knee", color='c', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_br_knee"]["Time"], df_motor_values["charlotte_br_knee"]["I_phase_line_RMS"], label = "charlotte_br_knee", color='m', alpha=0.7)
ax1.scatter(df_motor_values["charlotte_bl_knee"]["Time"], df_motor_values["charlotte_bl_knee"]["I_phase_line_RMS"], label = "charlotte_bl_knee", color='y', alpha=0.7)
plt.legend(loc='upper left')
plt.xlabel("Time (sec)")
plt.ylabel("Current (A)")
plt.title("Knee Current (Line RMS)")
plt.axhline(y=4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-4.8, color='k', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.axhline(y=-12, color='r', linestyle='--', linewidth=2, label="Current Limit")
plt.grid(True)
plt.savefig("Knee Current (Line RMS)", dpi=300, bbox_inches="tight")

plt.show()





