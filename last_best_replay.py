import os
import time

def replay_simulation():
    # Define the directory containing the files
    last_best_dir = "last_best"

    # Check if the directory exists
    if not os.path.exists(last_best_dir):
        print(f"Directory '{last_best_dir}' does not exist!")
        return

    # Check for required files in the directory
    urdf_file = None
    sdf_file = None
    nndf_file = None

    for file in os.listdir(last_best_dir):
        if file.endswith(".urdf"):
            urdf_file = os.path.join(last_best_dir, file)
        elif file.endswith(".sdf"):
            sdf_file = os.path.join(last_best_dir, file)
        elif file.endswith(".nndf"):
            nndf_file = os.path.join(last_best_dir, file)

    # Ensure all required files are present
    if not urdf_file or not sdf_file or not nndf_file:
        print("Missing required files in 'last_best' directory!")
        print(f"URDF file: {urdf_file}")
        print(f"SDF file: {sdf_file}")
        print(f"NNDF file: {nndf_file}")
        return

    # Copy the files to the root directory
    os.system(f"cp {urdf_file} ./")
    os.system(f"cp {sdf_file} ./")
    os.system(f"cp {nndf_file} ./")

    # Extract the ID from the URDF file name (assuming the format is body<ID>.urdf)
    file_name = os.path.basename(urdf_file)
    file_id = file_name.replace("body", "").replace(".urdf", "")

    # Run the simulation using the copied files
    print(f"Replaying simulation with ID: {file_id}")
    os.system(f"python3 simulate.py GUI {file_id}")

    # Clean up the copied files from the root directory
    os.remove(f"body{file_id}.urdf")
    os.remove(f"world{file_id}.sdf")
    os.remove(f"brain{file_id}.nndf")

    print("Replay complete and temporary files cleaned up.")

if __name__ == "__main__":
    replay_simulation()