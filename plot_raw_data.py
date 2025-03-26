import pandas as pd
import matplotlib.pyplot as plt

import data_import

if __name__ == "__main__":
    # Example usage
    directory_path = "data"  # Replace with your actual directory path
    df_dict = data_import.load_all_csv_in_directory(directory_path)

    # Example: Print first few rows of each dataframe
    for file_name, df in df_dict.items():
        print(f"\n{file_name}:")
        print(df.head())

#Knee joint velocity
    fig = plt.figure(figsize=(8, 5))  # Set figure size
    ax1 = fig.add_subplot(111)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fr_knee_w"], label = "charlotte_fr_knee", color='r', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fl_knee_w"], label = "charlotte_fl_knee", color='g', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_mr_knee_w"], label = "charlotte_mr_knee", color='b', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_ml_knee_w"], label = "charlotte_ml_knee", color='c', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_br_knee_w"], label = "charlotte_br_knee", color='m', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_bl_knee_w"], label = "charlotte_bl_knee", color='y', alpha=0.7)
    plt.legend(loc='upper left')
    plt.xlabel("Time (sec)")
    plt.ylabel("Angular Velocity (Rad/s)")
    plt.title("Knee Angular Velocity")
    plt.axhline(y=1.98, color='r', linestyle='--', linewidth=2, label="Speed Limit") #30V/ 0.315 (ke) / (6*8) (reduction)
    plt.axhline(y=-1.98, color='r', linestyle='--', linewidth=2, label="Speed Limit")
    plt.grid(True)
    plt.savefig("Knee Angular Velocity", dpi=300, bbox_inches="tight")

#Hip joint vertical velocity
    fig = plt.figure(figsize=(8, 5))  # Set figure size
    ax1 = fig.add_subplot(111)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fr_hip_ver_w"], label = "charlotte_fr_hip_ver", color='r', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fl_hip_ver_w"], label = "charlotte_fl_hip_ver", color='g', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_mr_hip_ver_w"], label = "charlotte_mr_hip_ver", color='b', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_ml_hip_ver_w"], label = "charlotte_ml_hip_ver", color='c', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_br_hip_ver_w"], label = "charlotte_br_hip_ver", color='m', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_bl_hip_ver_w"], label = "charlotte_bl_hip_ver", color='y', alpha=0.7)
    plt.legend(loc='upper left')
    plt.xlabel("Time (sec)")
    plt.ylabel("Angular Velocity (Rad/s)")
    plt.title("Hip Vertical Angular Velocity")
    plt.axhline(y=1.19, color='r', linestyle='--', linewidth=2, label="Speed Limit") #30/0.315/(10*8) 
    plt.axhline(y=-1.19, color='r', linestyle='--', linewidth=2, label="Speed Limit")
    plt.grid(True)
    plt.savefig("Hip Vertical Angular Velocity", dpi=300, bbox_inches="tight")

#Hip joint lateral velocity
    fig = plt.figure(figsize=(8, 5))  # Set figure size
    ax1 = fig.add_subplot(111)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fr_hip_lat_w"], label = "charlotte_fr_hip_lat", color='r', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_fl_hip_lat_w"], label = "charlotte_fl_hip_lat", color='g', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_mr_hip_lat_w"], label = "charlotte_mr_hip_lat", color='b', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_ml_hip_lat_w"], label = "charlotte_ml_hip_lat", color='c', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_br_hip_lat_w"], label = "charlotte_br_hip_lat", color='m', alpha=0.7)
    ax1.scatter(df_dict["joint_velocity"]["Time"], df_dict["joint_velocity"]["charlotte_bl_hip_lat_w"], label = "charlotte_bl_hip_lat", color='y', alpha=0.7)
    plt.legend(loc='upper left')
    plt.xlabel("Time (sec)")
    plt.ylabel("Angular Velocity (Rad/s)")
    plt.title("Hip Lateral Angular Velocity")
    plt.axhline(y=11.9, color='r', linestyle='--', linewidth=2, label="Speed Limit") #30/0.315/8
    plt.axhline(y=-11.9, color='r', linestyle='--', linewidth=2, label="Speed Limit")
    plt.grid(True)
    plt.savefig("Hip Lateral Angular Velocity", dpi=300, bbox_inches="tight")

    plt.show()