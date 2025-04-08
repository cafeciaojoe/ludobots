import os
import time
from datetime import datetime
import shutil

def replay_simulation():
    # Define the directory containing the replays
    replays_dir = "replays"

    # List all folders in the replays directory
    if not os.path.exists(replays_dir):
        print(f"Directory '{replays_dir}' does not exist!")
        return

    # Sort folders alphabetically
    replay_folders = sorted([folder for folder in os.listdir(replays_dir) if os.path.isdir(os.path.join(replays_dir, folder))])
    if not replay_folders:
        print("No replays available!")
        return

    print("Available replays:")
    for idx, folder in enumerate(replay_folders):
        print(f"{idx + 1}. {folder}")

    # Ask the user to select a replay
    try:
        selection = int(input("Select a replay to replay (enter the number): ").strip())
        if selection < 1 or selection > len(replay_folders):
            print("Invalid selection!")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    selected_folder = replay_folders[selection - 1]
    selected_dir = os.path.join(replays_dir, selected_folder)

    # Check for required files in the selected directory
    urdf_file = None
    sdf_file = None
    nndf_file = None

    for file in os.listdir(selected_dir):
        if file.endswith(".urdf"):
            urdf_file = os.path.join(selected_dir, file)
        elif file.endswith(".sdf"):
            sdf_file = os.path.join(selected_dir, file)
        elif file.endswith(".nndf"):
            nndf_file = os.path.join(selected_dir, file)

    # Ensure all required files are present
    if not urdf_file or not sdf_file or not nndf_file:
        print(f"Missing required files in '{selected_folder}' directory!")
        print(f"URDF file: {urdf_file}")
        print(f"SDF file: {sdf_file}")
        print(f"NNDF file: {nndf_file}")
        return
    
    # Temporarily replace constants.py
    root_constants_file = "constants.py"
    selected_constants_file = os.path.join(selected_dir, "_constants.py")
    backup_constants_file = None

    if os.path.exists(selected_constants_file):
        # Backup the original constants.py in the root directory
        if os.path.exists(root_constants_file):
            backup_constants_file = root_constants_file + ".backup"
            shutil.copy(root_constants_file, backup_constants_file)

        # Replace the root constants.py with the one from the selected folder
        shutil.copy(selected_constants_file, root_constants_file)

    # Copy the files to the root directory
    os.system(f"cp {urdf_file} ./")
    os.system(f"cp {sdf_file} ./")
    os.system(f"cp {nndf_file} ./")

    # Extract the ID from the URDF file name (assuming the format is body<ID>.urdf)
    file_name = os.path.basename(urdf_file)
    file_id = file_name.replace("body", "").replace(".urdf", "")

    try:
        # Run the simulation using the copied files
        print(f"Replaying simulation with ID: {file_id}")
        os.system(f"python3 simulate.py GUI {file_id}")
    finally:
        # Ensure the original constants.py is restored
        if backup_constants_file and os.path.exists(backup_constants_file):
            # Restore the original constants.py from the backup
            shutil.move(backup_constants_file, root_constants_file)
        elif os.path.exists(root_constants_file):
            # Remove the replaced constants.py if no backup exists
            os.remove(root_constants_file)

        # Clean up the copied files from the root directory
        if os.path.exists(f"body{file_id}.urdf"):
            os.remove(f"body{file_id}.urdf")
        if os.path.exists(f"world{file_id}.sdf"):
            os.remove(f"world{file_id}.sdf")
        if os.path.exists(f"brain{file_id}.nndf"):
            os.remove(f"brain{file_id}.nndf")

        print("Cleanup complete")

    # If the selected folder is '_last_best', ask if the user wants to save the replay
    if selected_folder == "_last_best":
        while True:
            save_replay = input("Do you want to save this replay? (y/n): ").strip().lower()
            if save_replay in ['y', 'n']:
                break
            print("Invalid input! Please enter 'y' or 'n'.")

        if save_replay == 'y':
            comment = input("Enter a comment for this replay: ").strip().replace(" ", "_")
            timestamp = datetime.now().strftime(f"{comment}_%H-%M-%S_%Y-%m-%d")
            replay_folder = os.path.join(replays_dir, timestamp)
            os.makedirs(replay_folder)

            # Copy the files to the replay folder
            shutil.copy(urdf_file, replay_folder)
            shutil.copy(sdf_file, replay_folder)
            shutil.copy(nndf_file, replay_folder)

            print(f"Replay saved to: {replay_folder}")

if __name__ == "__main__":
    replay_simulation()