# In this file we assign a label to each type of skin disease by
# navigating the different directories and saving each image name in a dictionary with its label.
import os
from sys import maxsize as infinity

# Default route to the dataset (it must contain 'train' and 'test' subfolders)
default_route = os.path.join(os.path.join(os.path.expanduser("~"), "Downloads"), "SkinDisease")

def create_labels(limited=infinity, route=default_route):
    """
        Generates dictionaries mapping image filenames to their numerical label.

        Parameters:
        - limited (int): limits how many disease classes are processed (default = all)
        - route (str): path to the main dataset directory (should end with 'SkinDisease')

        Returns:
        - (train_labels, test_labels): two dictionaries {image_name: label}
    """
    # We check the route is valid
    if os.path.basename(route) != "SkinDisease":
        print("Ruta inválida. Debe apuntar al directorio 'SkinDisease'")
        return None

    try:
        os.listdir(route)
    except FileNotFoundError:
        print("No se ha podido encontrar la ruta indicada")
        return None

    train_labels = dict()
    test_labels = dict()
    meaning_labels = dict()
    added_diseases = 0

    test_route = os.path.join(route, "test")
    train_route = os.path.join(route, "train")

    for directory in enumerate(os.listdir(train_route)):
        temp_route_train = os.path.join(train_route, directory[1])
        temp_route_test = os.path.join(test_route, directory[1])

        add_current_label(added_diseases, temp_route_train, train_labels)
        add_current_label(added_diseases, temp_route_test, test_labels)

        meaning_labels[added_diseases] = directory[1]

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


# If you want to test the code, execute this block.
# Change variables if necessary.
if __name__ == "__main__":
    tr_labels, te_labels, m = create_labels(5)
    print(m)
    print("fin del programa")
