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
        source_route=default_route,
        dir_target=default_route
    ):

    try:
        print("Cargando datos")
        trl, tel, ml = create_labels(amount_of_diseases,
                                     source_route,
                                     dir_target)

        write_text_file("Info", dir_target, ml, trl, tel)

        return trl, tel, ml

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")



def create_labels(limited, source_route, target_dir):
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

    # Validate if the source_route works
    os.listdir(source_route)

    # Validate source_route
    if os.path.basename(source_route) != "SkinDisease":
        raise FileNotFoundError("La ruta pasada es inválida, debe apuntar al directorio 'SkinDisease'")

    train_labels = dict()
    test_labels = dict()
    meaning_labels = dict()

    test_source = os.path.join(source_route, "test")
    train_source = os.path.join(source_route, "train")

    # In the target directory, we create 2 subdirectories for test and training
    training_target = create_directory("Training", target_dir)
    test_target = create_directory("Test", target_dir)

    copy_images_from_to(train_source, training_target, limited, train_labels, meaning_labels)
    copy_images_from_to(test_source, test_target, limited, test_labels)

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

def move_images_to_target_dir(current_dir, target_dir):
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

def copy_images_from_to(source_route, target_route, amount_of_diseases, labels, meaning_label=None):
    directories = [d for d in os.listdir(source_route)]

    # check if there is less diseases than the amount needed
    if len(directories) < amount_of_diseases:
        amount_of_diseases = len(directories)

    added = 0

    # for each disease
    for disease_name in os.listdir(source_route):

        # create a temporary route pointing the disease directory
        temp_route = os.path.join(source_route, disease_name)

        # adding the current image to the label
        add_current_label(added, temp_route, labels)

        # create a new dir with the route of the current target dir and the current disease
        new_route_disease = create_directory(disease_name, target_route)

        # copy the imagess to the target route
        move_images_to_target_dir(temp_route, new_route_disease)

        # if given a dictionary, add a label with the current disease
        if meaning_label:
            meaning_label[disease_name] = added

        added += 1

        if added >= amount_of_diseases:
            break
