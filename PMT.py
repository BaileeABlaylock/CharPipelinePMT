from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtGui import *
import shutil

import os
import re
import sys

class PMT(QMainWindow):
    def __init__(self, base_directory,path, path2):
        super(PMT, self).__init__()
        uic.loadUi("PMT.ui", self)

        self.base_directory = base_directory

        self.model = QFileSystemModel()  # creates the file system model
        self.model.setRootPath('C:/Temp')  # Sets the root of the file system module
        index = self.model.index('C:/Temp')  # Gets the index of the root

        self.tree = self.DirTreeView
        self.tree.setModel(self.model)  # Set the tree model to the file system
        self.tree.setRootIndex(index)  # Set the tree root view to the root path
        self.tree.setSortingEnabled(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openAsset)

        self.tree.setColumnHidden(1, True)  # Hide size
        self.tree.setColumnHidden(2, True)  # Hide Type
        self.tree.setColumnHidden(3, True)  # Hide date

        self.tree2 = self.assetTreeView
        self.tree2.setModel(self.model)  # Set the tree model to the file system t
        self.tree2.setRootIndex(index)  # Set the tree root view to the root path

        self.tree2.setColumnHidden(1, True)  # Hide size
        self.tree2.setColumnHidden(2, True)  # Hide Type
        self.tree2.setColumnHidden(3, True)  # Hide date

        # Connect our buttons to their functions
        self.CPbutton.clicked.connect(self.createProject)
        self.CAbutton.clicked.connect(self.createAsset)
        self.DPbutton.clicked.connect(self.deleteProject)
        self.DAbutton.clicked.connect(self.deleteAsset)
        self.OAbutton.clicked.connect(self.openAsset)

        self.SPcomboBox.currentIndexChanged.connect(self.on_selection_changed)
        self.populate_combobox(path, path2)

    def createAsset(self):
        base = self.NAlineEdit.text()
        filename = self.NAlineEdit.text()
        msg = QMessageBox()
        error_message = "Please use camelCase!"
        selected_option = self.SPcomboBox.currentText()
        selected_department = self.SDAcomboBox.currentText()
        print(path)

        if filename and self.MeshCheckBox.isChecked() and selected_option:
            if not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', filename):
                QMessageBox.critical(self, 'Error', error_message, QMessageBox.Ok)
                return

            if not filename.endswith("Mesh.ma"):
                filename += "Mesh.ma"

            try:
                with open(f"C:/Temp/{selected_department}/projects/{selected_option}/assets/{filename}", 'w') as file:

                    # Write some content to the file
                    file.write("This is the content of the .ma file.")

                msg.setText(f"'{filename}' saved successfully!")
                msg.exec_()

            except IOError:
                print(f"Error: Could not write to the file '{filename}'")

            filename = base

        if filename and self.RigCheckBox.isChecked() and selected_option:
            if not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', filename):
                QMessageBox.critical(self, 'Error', error_message, QMessageBox.Ok)
                return

            if not filename.endswith("Rig.ma"):
                filename += "Rig.ma"

            try:
                with open(f"C:/Temp/{selected_department}/projects/{selected_option}/assets/{filename}", 'w') as file:

                    # Write some content to the file
                    file.write("This is the content of the .ma file.")

                msg.setText(f"'{filename}' saved successfully!")
                msg.exec_()

            except IOError:
                print(f"Error: Could not write to the file '{filename}'")

        filename = base

        if filename and self.AnimCheckBox.isChecked() and selected_option:
            if not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', filename):
                QMessageBox.critical(self, 'Error', error_message, QMessageBox.Ok)
                return

            if not filename.endswith("Anim.ma"):
                filename += "Anim.ma"

            try:
                with open(f"C:/Temp/{selected_department}/projects/{selected_option}/assets/{filename}", 'w') as file:

                    # Write some content to the file
                    file.write("This is the content of the .ma file.")

                msg.setText(f"'{filename}' saved successfully!")
                msg.exec_()

            except IOError:
                print(f"Error: Could not write to the file '{filename}'")

    def createProject(self):
        project_name = self.PNlineEdit.text()
        error_message = "Please use camelCase!"
        selected_option = self.SDcomboBox.currentText()
        subfolders = ["assets", "tools", "config"]

        if project_name and selected_option == "theOtherOnesGames":
            path = os.path.join('C:/Temp/theOtherOnesGames/projects', project_name, *subfolders)

            if not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', project_name):
                QMessageBox.critical(self, 'Error', error_message, QMessageBox.Ok)
                return

            try:
                os.makedirs(path)
                print(f'Folder "{project_name}" created successfully in the "Projects" folder.')

                # clears the type box once the user successfully creates the project folder
                self.PNlineEdit.clear()

                # Takes the created project names and adds them to the 'Select Project' combo box
                self.SPcomboBox.addItem(project_name)

            except FileExistsError:
                print(f'Folder "{project_name}" already exists in the "Projects" folder.')


        if project_name and selected_option == "theOtherOnesFilms":
            path = os.path.join('C:/Temp/theOtherOnesFilms/projects', project_name, *subfolders)

            if not re.match(r'^[a-z]+(?:[A-Z][a-z]+)*$', project_name):
                QMessageBox.critical(self, 'Error', error_message, QMessageBox.Ok)
                return

            try:
                os.makedirs(path)
                print(f'Folder "{project_name}" created successfully in the "Projects" folder.')

                # clears the type box once the user successfully creates the project folder
                self.PNlineEdit.clear()

                # Takes the created project names and adds them to the 'Select Project' combo box
                self.SPcomboBox.addItem(project_name)

            except FileExistsError:
                print(f'Folder "{project_name}" already exists in the "Projects" folder.')

    # Function that deletes the selected Project
    def deleteProject(self):
        index = self.DirTreeView.currentIndex()
        filePath = self.model.filePath(index)
        shutil.rmtree(filePath)

    def openAsset(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.openFile)
        cursor = QtGui.QCursor
        menu.exec_(cursor.pos())

    def openFile(self):
        index = self.assetTreeView.currentIndex()
        filePath = self.model.filePath(index)
        os.startfile(filePath)

    def deleteAsset(self):
        index = self.assetTreeView.currentIndex()
        filePath = self.model.filePath(index)
        os.remove(filePath)


    def create_folder_directory(self, folder_structure):
        # Create the base directory if it doesn't exist
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)

        # Create the folder directory structure inside the base directory
        tree_widget = QTreeWidget()
        tree_widget.setColumnCount(1)
        self.create_folders(self.base_directory, folder_structure, tree_widget)
        return tree_widget

    def create_folders(self, current_directory, folder_structure, tree_widget, parent_item=None):
        for folder_name, subfolders in folder_structure.items():
            folder_path = os.path.join(current_directory, folder_name)

            # Check if the folder already exists
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                print(f"Created folder: {folder_path}")

            # Add the folder to the QTreeWidget
            item = QTreeWidgetItem(parent_item, [folder_name])
            tree_widget.addTopLevelItem(item)

            if subfolders:
                self.create_folders(folder_path, subfolders, tree_widget, item)

    def populate_combobox(self, path, path2):
        if not os.path.exists(path) or not os.path.isdir(path):
            print("Invalid path!")
            return

        # Get the list of folders in the specified path
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

        # Add the folders to the QComboBox
        self.SPcomboBox.addItems(folders)

        if not os.path.exists(path2) or not os.path.isdir(path2):
            print("Invalid path!")
            return

        # Get the list of folders in the specified path
        folders = [folder for folder in os.listdir(path2) if os.path.isdir(os.path.join(path2, folder))]

        # Add the folders to the QComboBox
        self.SPcomboBox.addItems(folders)

    def on_selection_changed(self, index):
        selected_folder = self.SPcomboBox.itemText(index)
        print(f'Selected folder: {selected_folder}')

# Specifies the base directory where the folders will be created
base_directory = "C:/Temp"

if not os.path.exists(base_directory):
    os.makedirs(base_directory)
    print(f"Directory '{base_directory}' created successfully.")
else:
    print(f"Directory '{base_directory}' already exists.")

folder_directory = {
    "theOtherOnesFilms": {
        "projects": {
            "defaultFilmProject": {
                "assets": {
                    "meshes": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        }
                    },
                    "rigs": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        }
                    },
                    "animation": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        }
                    },
                },
                "temp": {},
                "tools": {
                    "config": {},
                }
            },
            "temp": {},
            "tools": {
                "config": {},
            },
        },
        "temp": {},
        "tools": {
            "config": {},
        },
    },
    "theOtherOnesGames": {
        "projects": {
            "defaultGameProject": {
                "assets": {
                    "meshes": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        },
                    },
                    "rigs": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        },
                    },
                    "animations": {
                        "temp": {},
                        "tools": {
                            "config": {},
                        },
                    },
                },
                "temp": {},
                "tools": {
                    "config": {},
                },
            },
            "temp": {},
            "tools": {
                "config": {}
            }
        },
        "temp": {},
        "tools": {
            "config": {},
        },
    },
}

if __name__ == '__main__':
    app = QApplication([])
    path = 'C:/Temp/theOtherOnesFilms/projects'
    path2 = 'C:/Temp/theOtherOnesGames/projects'
    window = PMT(base_directory,path, path2)
    window.create_folder_directory(folder_directory)
    window.show()
    app.exec_()
    sys.exit(app.exec_())

