import sys
import csv
import re
import pandas as pd
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy, QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QResizeEvent, QPainter, QIcon
from PyQt5 import QtWidgets

width = 1100
height = 750
edgesDictionary = {}
idToNames = {}
idToIdSorted = {}
nameToId = {}
validateFiles1 = False
validateFiles2 = False

def set_background_image(self, image_path, opacity=1.0):
    # Create a QPixmap from the image file
    pixmap = QPixmap(image_path)

    # Resize the pixmap to fit the window size
    pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

    # Create a new QPixmap with the desired opacity
    opacity_pixmap = QPixmap(pixmap.size())
    opacity_pixmap.fill(Qt.transparent)

    # Set the opacity by manipulating the alpha channel
    painter = QPainter(opacity_pixmap)
    painter.setOpacity(opacity)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    # Set the pixmap as the QLabel's background
    self.backgroundLabel.setPixmap(opacity_pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI form from the .ui file
        self.load_ui()
        self.validate1 = False
        self.validate2 = False
        self.visibleLabel1Page1.setVisible(False)
        self.visibleLabel2Page1.setVisible(False)
        # Set the window icon
        # Connect the exitButtonPage1 clicked signal to the application quit
        self.exitButtonPage1.clicked.connect(QApplication.quit)
        self.loadTrainedDataPage1.clicked.connect(self.load_trained_data)
        self.loadDatasetPage1.clicked.connect(self.load_dataset)
        # Set the background image
        set_background_image(self, "images/robotic_arm.jpg", opacity=0.65)
        self.setFixedSize(width, height)
        # Connect the next button clicked signal to the next page function
        self.nextButtonPage1.clicked.connect(self.switch_to_page2)

    def load_ui(self):
        from PyQt5 import uic
        uic.loadUi("ui_files/page1.ui", self)

    def load_trained_data(self):
        # Functions that load the data into a dictionaries
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            # df = pd.read_csv(file_path)
            self.visibleLabel2Page1.setVisible(True)

            self.validate1 = True
            LoadData(file_path)

    def load_dataset(self):
        # Functions that load the data into a dictionaries
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            # df = pd.read_csv(file_path)
            self.visibleLabel1Page1.setVisible(True)

            self.validate2 = True
            ReadPapersName(file_path)

    def switch_to_page2(self):
        if self.validate1 and self.validate2:
            loading_message = "Loading data...\nPlease be patient for another popup window"
            QMessageBox.information(self, "Data Loading", loading_message)
            CreatePapersDictionary()
            QMessageBox.information(self, "Data Loading", "Data loaded successfully!")
            page2 = Page2()
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.addWidget(page2)
            widget.removeWidget(self)
        else:
            QMessageBox.information(self, "No files selected", "Please select csv files to continue.")


class Page2(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI form from the .ui file
        self.load_ui()
        set_background_image(self, "images/robotic_arm.jpg", opacity=0.65)
        self.setFixedSize(width, height)
        self.searchButtonPage2.clicked.connect(self.switch_to_page3)
        self.homeButtonPage2.setIcon(QIcon("images/home_button.png"))
        self.homeButtonPage2.clicked.connect(self.switch_to_page1)
        # Connect the returnPressed signal of the line edit to the click slot of the search button
        self.lineEditPage2.returnPressed.connect(self.searchButtonPage2.click)

        # Connect the exitButtonPage1 clicked signal to the application quit
        self.exitButtonPage2.clicked.connect(QApplication.quit)

    def load_ui(self):
        from PyQt5 import uic
        uic.loadUi("ui_files/page2.ui", self)

    def switch_to_page3(self):
        text_to_transfer = self.lineEditPage2.text()
        # print("text to transfer", text_to_transfer)
        if len(text_to_transfer) == 0:
            QMessageBox.information(self, "No Text Found", "No text found in the search bar.")
            return
        page3 = Page3(text_to_transfer)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.addWidget(page3)
        widget.removeWidget(self)

    def switch_to_page1(self):
        mainWindow = MainWindow()
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.addWidget(mainWindow)
        widget.removeWidget(self)


class Page3(QMainWindow):
    def __init__(self, transferred_text):
        super().__init__()
        self.transferred_text = transferred_text
        # Load the UI form from the .ui file
        self.load_ui()
        set_background_image(self, "images/robotic_arm.jpg", opacity=0.65)
        self.setFixedSize(width, height)
        self.homeButtonPage3.setIcon(QIcon("images/home_button.png"))
        self.homeButtonPage3.clicked.connect(self.switch_to_page1)
        # Connect the exitButtonPage1 clicked signal to the application quit
        self.exitButtonPage3.clicked.connect(QApplication.quit)
        self.searchButtonPage3.clicked.connect(self.switch_to_page2)
        self.updateResults()

    def load_ui(self):
        from PyQt5 import uic
        uic.loadUi("ui_files/page3.ui", self)
        # print(self.transferred_text)

    def switch_to_page2(self):
        page2 = Page2()
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.addWidget(page2)
        widget.removeWidget(self)

    def switch_to_page1(self):
        mainWindow = MainWindow()
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.addWidget(mainWindow)
        widget.removeWidget(self)

    def updateResults(self):
        # Search for ID corresponding to the transferred_text
        id_ = None
        for name, id_value in nameToId.items():
            if self.transferred_text.lower() in name.lower():
                id_ = id_value
                break
        if id_ is not None:
            if id_ == "325497":
                print("IM HERE")
            result_names = []
            # Get the sorted IDs list corresponding to the found ID
            sorted_ids = idToIdSorted.get(id_)
            if sorted_ids is not None:
                for sorted_id in reversed(sorted_ids):
                    # Get the name corresponding to each sorted ID
                    if idToNames.get(sorted_id) is not None:
                        name = idToNames.get(sorted_id)
                    if name is not None:
                        result_names.append(name)
                        name = None
            if not result_names:
                self.textEditPage3.append("No papers found.")
            for name in result_names:
                name = re.sub(r'"|,$', '', name)
                new_text = name.rsplit(',', 1)[0] + '.'
                new_text = new_text.replace("..", ".")
                self.textEditPage3.append(new_text + '\n')
        else:
            self.textEditPage3.append("No papers found.")


def LoadData(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)

        # Skip the header row
        next(reader)

        for row in reader:
            edge = eval(row[0])
            count = int(row[1])
            edgesDictionary[edge] = count

    # print(edgesDictionary)


def ReadPapersName(file_path):

    # filename = "csv_files/paper_names_id.csv"
    # filename = input_file

    with open(file_path, "r", newline="") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the first row (header)

        for row in csv_reader:
            if len(row) >= 2:
                id_ = row[0]
                name = row[1]
                idToNames[id_] = name
                nameToId[name] = id_


    # print(nameToId)
    # print(namesDictionary)


def CreatePapersDictionary():
    for id_, name in idToNames.items():
        matching_names = []
        for key, value in edgesDictionary.items():
            if str(key[0]) == id_:
                matching_names.append(str(key[1]) + ',' + str(value))
            if str(key[1]) == id_:
                matching_names.append(str(key[0]) + ',' + str(value))
        idToIdSorted[id_] = matching_names

    for key, value in idToIdSorted.items():
        # Sort the list in ascending order based on the integer value after ','
        sorted_list = sorted(value, key=lambda x: int(x.split(',')[1]))
        idToIdSorted[key] = sorted_list

    for key, value in idToIdSorted.items():
        # Remove '0' values and delete the characters after ','
        cleaned_list = [item.split(',')[0] for item in value if item.split(',')[1] != '0']
        idToIdSorted[key] = cleaned_list

    # print(idToIdSorted)



# # Functions that load the data into a dictionaries
# LoadData()
# ReadPapersName()
# CreatePapersDictionary()


# Run the App\GUI
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
window = MainWindow()
icon = QIcon("images/icon.png")
widget.setWindowIcon(icon)
widget.setWindowTitle("Final Project")
widget.addWidget(window)
widget.setFixedSize(width, height)
widget.show()
sys.exit(app.exec_())
