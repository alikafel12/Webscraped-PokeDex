# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pokedex.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

connection = sqlite3.connect("pokemon.db")

cursor = connection.cursor()

def get_names():
    # names for dropdown
    sql_command = """SELECT Name FROM pokemon;"""
    cursor.execute(sql_command)
    names = [name[0] for name in cursor.fetchall()]
    return names

def get_pokemon_data(pokemon_name):
    # get a pokemon's data from table
    sql_command = """SELECT Name, Type, HP, Attack, Sp_Atk, Defense, Sp_Def, Speed, Total, Image FROM pokemon WHERE Name = ?;"""
    cursor.execute(sql_command, (pokemon_name,))
    data = cursor.fetchall()
    return data

class Ui_PokeDex(object):

    def setupUi(self, PokeDex):
        PokeDex.setObjectName("PokeDex")
        PokeDex.resize(500, 250)

        # labels
        self.gridLayout = QtWidgets.QGridLayout(PokeDex)
        self.gridLayout.setObjectName("gridLayout")
        self.total = QtWidgets.QLabel(PokeDex)
        self.total.setObjectName("total")
        self.gridLayout.addWidget(self.total, 9, 0, 1, 1)
        self.defense = QtWidgets.QLabel(PokeDex)
        self.defense.setObjectName("defense")
        self.gridLayout.addWidget(self.defense, 6, 0, 1, 1)
        self.name = QtWidgets.QLabel(PokeDex)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 0, 1, 1)
        self.sp_attack = QtWidgets.QLabel(PokeDex)
        self.sp_attack.setObjectName("sp_attack")
        self.gridLayout.addWidget(self.sp_attack, 5, 0, 1, 1)
        self.sp_defense = QtWidgets.QLabel(PokeDex)
        self.sp_defense.setObjectName("sp_defense")
        self.gridLayout.addWidget(self.sp_defense, 7, 0, 1, 1)
        self.speed = QtWidgets.QLabel(PokeDex)
        self.speed.setObjectName("speed")
        self.gridLayout.addWidget(self.speed, 8, 0, 1, 1)
        self.type = QtWidgets.QLabel(PokeDex)
        self.type.setObjectName("type")
        self.gridLayout.addWidget(self.type, 2, 0, 1, 1)
        self.hp = QtWidgets.QLabel(PokeDex)
        self.hp.setObjectName("hp")
        self.gridLayout.addWidget(self.hp, 3, 0, 1, 1)
        self.attack = QtWidgets.QLabel(PokeDex)
        self.attack.setObjectName("attack")
        self.gridLayout.addWidget(self.attack, 4, 0, 1, 1)

        # dropdown menu
        self.dropdown = QtWidgets.QComboBox(PokeDex)
        self.dropdown.setEnabled(True)
        self.dropdown.setObjectName("dropdown")
        self.names = get_names()
        self.dropdown.addItems(self.names)
        self.gridLayout.addWidget(self.dropdown, 0, 0, 1, 2)

        # image label
        self.image = QtWidgets.QLabel(PokeDex)
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 1, 1, 9, 2)

        # search button
        self.searchbtn = QtWidgets.QPushButton(PokeDex)
        self.searchbtn.setObjectName("searchbtn")
        self.searchbtn.clicked.connect(lambda: self.run_search())
        self.gridLayout.addWidget(self.searchbtn, 0, 2, 1, 1)

        self.retranslateUi(PokeDex)
        QtCore.QMetaObject.connectSlotsByName(PokeDex)

    def retranslateUi(self, PokeDex):
        _translate = QtCore.QCoreApplication.translate
        PokeDex.setWindowTitle(_translate("PokeDex", "PokeDex"))
        self.total.setText(_translate("PokeDex", "Total:"))
        self.defense.setText(_translate("PokeDex", "Defense:"))
        self.name.setText(_translate("PokeDex", "Name:"))
        self.sp_attack.setText(_translate("PokeDex", "Sp. Attack:"))
        self.sp_defense.setText(_translate("PokeDex", "Sp. Defense:"))
        self.speed.setText(_translate("PokeDex", "Speed:"))
        self.type.setText(_translate("PokeDex", "Type:"))
        self.searchbtn.setText(_translate("PokeDex", "Search"))
        self.hp.setText(_translate("PokeDex", "HP:"))
        self.attack.setText(_translate("PokeDex", "Attack:"))

    def run_search(self):
        # method, gets pokemon data and display results
        pokemon_name = self.dropdown.currentText()
        pokemon_data = get_pokemon_data(pokemon_name)
        pixmap = QtGui.QPixmap(pokemon_data[0][9])
        self.image.setPixmap(pixmap)

        self.name.setText('Name: \t\t' + pokemon_data[0][0])
        self.type.setText('Type: \t\t' + pokemon_data[0][1])
        self.hp.setText('HP: \t\t' + str(pokemon_data[0][2]))
        self.attack.setText('Attack: \t\t' + str(pokemon_data[0][3]))
        self.sp_attack.setText('Sp. Attack: \t' + str(pokemon_data[0][4]))
        self.defense.setText('Defense: \t' + str(pokemon_data[0][5]))
        self.sp_defense.setText('Sp. Defense: \t' + str(pokemon_data[0][6]))
        self.speed.setText('Speed: \t\t' + str(pokemon_data[0][7]))
        self.total.setText('Total: \t\t' + str(pokemon_data[0][8]))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PokeDex = QtWidgets.QDialog()
    ui = Ui_PokeDex()
    ui.setupUi(PokeDex)
    PokeDex.show()
    sys.exit(app.exec_())


