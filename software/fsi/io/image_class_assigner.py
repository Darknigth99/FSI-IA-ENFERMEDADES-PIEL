# In this file we assign a label to each type of skin disease by
# navigating the different directories and saving each image name in a dictionary with its label.
import datetime
import os
import shutil
from sys import maxsize as infinity

from software.fsi.io.convert_functions import convert_to_tuple

# Default route to the dataset (it must contain 'train' and 'test' subfolders to work)
default_route = os.path.join(os.path.join(os.path.expanduser("~"), "Downloads"), "SkinDisease")
prefix = 0

def manager_io_images(
        amount_of_diseases=infinity,
        route=default_route,
        create_dir_with_all_images=True,
        dir_name="All_Images",
        write_info_text=True,
        name_info_file="Info",
        move_images_into_all_images_dir=True,
        dir_target=default_route
    ):

    try:

        dir_with_all_images = None

        trl = None
        tel = None
        ml = None

        if create_dir_with_all_images:
           dir_with_all_images = create_directory(dir_name, route)

        trl, tel, ml = (create_labels
                        (amount_of_diseases,
                         route,
                         dir_with_all_images,
                         move_images_into_all_images_dir,
                         dir_target=dir_target))

        if write_info_text:
            write_text_file(name_info_file, route, ml, trl, tel)

        return trl, tel, ml

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")



def create_labels(limited, route, all_images_dir, copy_images=True, dir_target=default_route):
    """
        Generates dictionaries mapping image filenames to their numerical label.

        Parameters:
        - limited (int): limits how many disease classes are processed (default = all)
        - route (str): path to the main dataset directory (should end with 'SkinDisease')

        Returns:
        tuple[dict, dict, dict]

        A tuple containing:
        - train_labels : dict[str, int]
            Maps each training image filename to its numerical label.
        - test_labels : dict[str, int]
            Maps each test image filename to its numerical label.
        - meaning_labels : dict[int, str]
            Maps each numerical label to its corresponding disease name.

    """

    # Validate if the route works
    os.listdir(route)

    # Validate route
    if os.path.basename(route) != "SkinDisease":
        raise FileNotFoundError("La ruta pasada es inválida, debe apuntar al directorio 'SkinDisease'")

    train_labels = dict()
    test_labels = dict()
    meaning_labels = dict()
    added_diseases = 0

    training_dir_with_all_images = None
    test_dir_with_all_images = None

    test_route = os.path.join(route, "test")
    train_route = os.path.join(route, "train")

    if copy_images:
        # In the directory with all images, we create 2 subdirectories for test and training
        training_dir_with_all_images = create_directory("Training", all_images_dir)
        test_dir_with_all_images = create_directory("Test", all_images_dir)

    # Iterate inside the train directory to get subdirectories names
    for disease_name in os.listdir(train_route):
        temp_route_train = os.path.join(train_route, disease_name)
        temp_route_test = os.path.join(test_route, disease_name)

        # for current disease, we add a label for train images and test iamges
        add_current_label(added_diseases, temp_route_train, train_labels)
        add_current_label(added_diseases, temp_route_test, test_labels)

        if copy_images:
            copy_images_to_all_images_directory(temp_route_train, training_dir_with_all_images)
            copy_images_to_all_images_directory(temp_route_test, test_dir_with_all_images)

        # also, we create a meaning label in case user want to know what it means the number
        meaning_labels[added_diseases] = disease_name

        added_diseases += 1

        if added_diseases >= limited:
           break

    return train_labels, test_labels, meaning_labels


def add_current_label(current_label, route, labels):
    """
        Adds all image filenames in the given directory to the labels dictionary,
        assigning them the provided label.
    """

    for _, image in enumerate(os.listdir(route)):
        labels[image] = current_label

    return labels


def create_directory(name, route):
    """
    :param name:str  Directory name.
    :param route:str Directory route.
    :return: str Directory route created, None in case something went wrong
    """

    final_route = os.path.join(route, name)

    # In case directory exists, we delete it
    if os.path.exists(final_route):
        shutil.rmtree(final_route)

    os.makedirs(final_route)

    return final_route

def write_text_file(name, route, meaning_label, trl, tel):
    """
    :param name: str Name of the file
    :param route: str Route of the file
    :param meaning_label:dict Dictionary with the meaning of the labels
    :param trl:dict Dictionary with the labels of the training images
    :param tel:dict Dictionary with the labels of the test images
    """

    actual_route = os.path.join(route, f"{name}.txt")

    with open(actual_route, "w") as f:
        f.write(f"Amount of diseases added = {len(meaning_label)}, total images of the directory = {len(trl) + len(tel)}.\n"
               f"Date of the data: {datetime.datetime.now()}.\n"
               f"Meaning of the label = {meaning_label}.\n\n")

        for key, value in trl.items():
            f.write(f"Label = {value}, image_name = {key}\n")

        f.write("\n\n----------------------------------------------\n")
        f.write("END OF THE TRAINING LABELS, BEGIN TEST LABELS\n")
        f.write("----------------------------------------------\n\n")

        for key, value in tel.items():
            f.write(f"Label = {value}, image_name = {key}")

        f.write("\n\n----------------------------------------------\n")
        f.write("END OF THE TEST LABELS, END OF THE FILE\n")

    return

def copy_images_to_all_images_directory(current_dir, target_dir):
    global prefix

    """
        Copies all images from the current_dir into the target_dir.
         This images will have a given number to avoid collisions as a prefix
    """
    for image in os.listdir(current_dir):
        temp_route = os.path.join(current_dir, image)
        shutil.copy2(temp_route, os.path.join(target_dir, f"{prefix}_{image}"))
        prefix += 1
    return


# If you want to test the code, execute this block.
# Change variables if necessary.
if __name__ == "__main__":

    print(convert_to_tuple(ml))
