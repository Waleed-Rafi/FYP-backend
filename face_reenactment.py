import os
from scripts import align_68, prepare_testing_files
from experiments import runner
import time


def apply_reenactment(
    input_image_path, input_pose_src_path, input_audio_src_path, output_path
):
    """
    (input_image_path, input_pose_src_path, input_audio_src_path, output_path)
    """
    input_image_folder_path = input_image_path[:-9]
    # input_image_folder_path="fr_modules/misc/Input/0001"

    # Image Alignment
    if os.path.isdir(input_image_folder_path):
        home_path = "/".join(input_image_folder_path.split("/")[:-1])
        save_image_path = os.path.join(
            home_path, input_image_folder_path.split("/")[-1] + "_cropped"
        )
        os.makedirs(save_image_path, exist_ok=True)
        # print(save_image_path) --> fr_modules/misc/Input/0001_cropped

        align_68.align_folder(input_image_folder_path, save_image_path)

    time.sleep(60)
    # Prepare Test Data
    # src_pose_path = './misc/Pose_Source/00473.mp4'
    # src_audio_path = './misc/Audio_Source/00015.mp4'
    # src_input_path = './misc/Input/00098.mp4'
    # csv_path = ./misc/demo2.csv'
    src_pose_path = input_pose_src_path
    src_audio_path = input_audio_src_path
    src_input_path = "misc/Input/0001_cropped/0001.jpg"  # input_image_path
    csv_path = output_path

    prepare_testing_files.pre_processing(
        src_pose_path, src_audio_path, src_input_path, csv_path
    )

    # Inference
    # !bash fr_modules/experiments/demo_vox.sh
    runner.run_inference()


# apply_reenactment("", "", "", "")


# import os
# from scripts import align_68, prepare_testing_files
# from experiments import runner


# def apply_reenactment(
#     input_image_path, input_pose_src_path, input_audio_src_path, output_path
# ):
#     """
#     (input_image_path, input_pose_src_path, input_audio_src_path, output_path)
#     """
#     input_image_folder_path = input_image_path[:-9]
#     # input_image_folder_path="fr_modules/misc/Input/0001"

#     # Image Alignment
#     if os.path.isdir(input_image_folder_path):
#         home_path = "/".join(input_image_folder_path.split("/")[:-1])
#         save_image_path = os.path.join(
#             home_path, input_image_folder_path.split("/")[-1] + "_cropped"
#         )
#         os.makedirs(save_image_path, exist_ok=True)
#         # print(save_image_path) --> fr_modules/misc/Input/0001_cropped

#         align_68.align_folder(input_image_folder_path, save_image_path)

#     print("Image Alignment Completed!")

#     # Prepare Test Data
#     # src_pose_path = './misc/Pose_Source/00473.mp4'
#     # src_audio_path = './misc/Audio_Source/00015.mp4'
#     # src_input_path = './misc/Input/00098.mp4'
#     # csv_path = ./misc/demo2.csv'
#     src_pose_path = input_pose_src_path
#     src_audio_path = input_audio_src_path
#     src_input_path = output_path  # "misc/Input/0001_cropped/0001.jpg"
#     csv_path = output_path

#     prepare_testing_files.pre_processing(
#         src_pose_path, src_audio_path, src_input_path, csv_path
#     )
#     print("Test data Prepared!")

#     # Inference
#     # !bash fr_modules/experiments/demo_vox.sh
#     runner.run_inference()
#     print("Inference Completed!")


# # apply_reenactment("", "", "", "")
