import sys
import datetime
import os
from PyQt5 import QtWidgets, QtCore, QtGui
import codecs
import networkx as nx



class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setFixedSize(1050, 800)
        self.setWindowTitle("Analyze Catan field")
        
        description = QtWidgets.QLabel(self)
        description.setGeometry(20, -50, 280, 300)
        description.setStyleSheet("font: Arial; font-size: 16px;")
        description.setWordWrap(True)
        ###################################
        description.setText(
        " This program calculates probabilities that a random dice roll will result in resource gain for each village position.\n\n"+
        " Enter the board setup and press the button to calculate probabilities.")


        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

        # Background
        pic = QtWidgets.QLabel(self)
        pic.setPixmap(QtGui.QPixmap("data/field_background.png").scaledToHeight(700))
        pic.setGeometry(300, 20, 700, 700)



        # LineEdit fields for resource fields
        f_pos, self.f_vals, v_pos = load_ui_pos()


        self.f_nam = sorted(list(f_pos.keys()))
        self.field_QLE = {}
        for key in self.f_nam:
            self.field_QLE[key] = QtWidgets.QLineEdit(self)
            self.field_QLE[key].setText(self.f_vals[key])
            self.field_QLE[key].setAttribute(QtCore.Qt.WA_StyledBackground)
            self.field_QLE[key].setGeometry(*f_pos[key], 40, 40)
            self.field_QLE[key].setAlignment(QtCore.Qt.AlignHCenter)
            self.field_QLE[key].setStyleSheet(QLE_style())

        self.v_nam = sorted(list(v_pos.keys()))
        self.village_QL = {}
        for key in self.v_nam:
            self.village_QL[key] = QtWidgets.QLabel(self)
            self.village_QL[key].setText(key)
            self.village_QL[key].setAttribute(QtCore.Qt.WA_StyledBackground)
            self.village_QL[key].setGeometry(*v_pos[key], 35, 30)
            self.village_QL[key].setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.village_QL[key].hide()


        # Save button
        self.b_calc = QtWidgets.QPushButton(self)
        self.b_calc.setGeometry(50, 670, 170, 70)
        self.b_calc.setFont(font_btn())
        self.b_calc.setText("Calculate \nprobabilities!")
        # self.b_calc.setWordWrap(True)
        self.b_calc.clicked.connect(self.calc_probs)

        self.show()


    def calc_probs(self):
        # ########################################################################################################
        probs = {
                0:   0.0,
                2:   0.027777778,
                3:   0.055555556,
                4:   0.083333333,
                5:   0.111111111,
                6:   0.138888889,
                7:   0.166666667,
                8:   0.138888889,
                9:   0.111111111,
                10:  0.083333333,
                11:  0.055555556,
                12:  0.027777778}

        G_board = nx.Graph()
        G_board.add_nodes_from(self.f_nam)
        G_board.add_nodes_from(self.v_nam)
        G_board.add_edges_from(get_links())

        # calc probabilities for each village
        v_vals = {}
        for village in self.v_nam:
            # value = 0
            value = set()
            for field in G_board.neighbors(village):
                try:
                    field_dice = int(self.field_QLE[field].text())
                except:
                    field_dice = 0
                value.add(field_dice)

                probability = sum([probs[x] for x in value])

                # if field_dice in probs:
                    # value += probs[field_dice]
            v_vals[village] = "%3.1f"%(100 * probability)

        for elem in self.village_QL:
            # print(elem)
            self.village_QL[elem].setText(v_vals[elem])
            self.village_QL[elem].setStyleSheet(L_style()+get_colors(v_vals[elem]))
            self.village_QL[elem].show()





    
def QLE_style():
    return """color: rgb(0, 0, 0);
            background-color: rgb(255, 255, 255); 
            border-width: 1px; 
            border-style: solid; 
            border-radius: 20px;
            font: Arial;
            font-size: 24px;
            """

def L_style():
    return """color: rgb(0, 0, 0);
            border-radius: 15px;
            font: bold Arial;
            font-size: 16px;
            """

def load_ui_pos():
    import json
    with open('data/ui_positions.json', 'r') as fp:
        [f_pos, f_vals, v_pos] = json.load(fp)
    return f_pos, f_vals, v_pos
    

def font_btn():
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(14)
    font.setBold(True)
    # font.setWeight(75)
    # font.wrap(75)
    return font

def get_links(finp="data/network_edges.csv"):
    links = []
    with codecs.open(finp, "rb") as finp:
        for line in finp:
            line = line.decode().strip()
            res = line.split(";")
            pos = res[0]
            ff = res[1:]
            for field in ff:
                if field != '-':
                    links.append((pos, field))
    return links


def get_colors(val):
    val = float(val)
    r = 0
    g = 0
    if val < 5.0:
        r = 255
        g = 0
    elif (val >= 5.0) and (val < 20.0):
        r = 255
        g = int(255 * (val - 5) / 15)
    elif (val >= 20.0) and (val < 35.0):
        r = int(255 * (35 - val) / 15)
        g = 255
    elif val >= 35.0:
        r = 0
        g = 255
   
    return "background-color: rgba(%3d, %3d, 0);"%(r,g)
    


app = QtWidgets.QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
a_window = Window()
app.exec_()
    