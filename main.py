from PySide2.QtWidgets import *
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Evaluate_expression import *
import matplotlib.pyplot as plt

def plot(*args):
	"""
	Plot an expression from a Min value to a Max value
	"""
	# Get the user input`
	expr = expr_entry.text()
	minV = minV_entry.value()
	maxV = maxV_entry.value()

	# remove whitespaces
	expr = re.sub("\s", "", expr)

	if is_valid_input(expr, minV, maxV):
		minV = int(minV)
		maxV = int(maxV)
		if minV < maxV:
			y = []
			x = range(minV, maxV+1)

			# claculate y
			for i in x:
				i_val = re.sub("x|X", "{}".format(i), expr)
				y.append(add_parts(i_val))

			# plot the result
			plotter.clear()
			plotter.plot(x, y)
			plotter.figure.canvas.draw()
		# Min value >= Max value
		else:
			message = 'Min value should be less than Max value'
			msgBox = QMessageBox()
			msgBox.setWindowTitle("Invalid range")
			msgBox.setText(message)
			msgBox.setIcon(QMessageBox.Critical)
			msgBox.exec_()
	# the user input is not valid
	else:
		message = 'The input isn\'t valid, \nPlease make sure that the'\
		   ' function is valid!'
		msgBox = QMessageBox()
		msgBox.setWindowTitle("Invalid function")
		msgBox.setText(message)
		msgBox.setIcon(QMessageBox.Critical)
		msgBox.exec_()

# Initialize a window and title
app = QApplication([]) # Start an application.
window = QWidget() # Create a window.
window.setWindowTitle("Function Plotter")

# Initialize the canvas that contains the figure
static_canvas = FigureCanvas(Figure())
plotter = static_canvas.figure.subplots()


# Initialize a grid layout
layout = QGridLayout() # Create a layout.
h_layout = QHBoxLayout() # Create a layout.

# Entries
expr_entry = QLineEdit()
expr_entry.setText("x+3*5-2")
minV_entry = QSpinBox()
minV_entry.setValue(0)
minV_entry.setRange(-10000, 10000)
maxV_entry = QSpinBox()
maxV_entry.setValue(1)
maxV_entry.setRange(-10000, 10000)

# Add Entries to grid
layout.addWidget(expr_entry, 0, 1)
layout.addWidget(minV_entry, 1, 1)
layout.addWidget(maxV_entry, 2, 1)

# Labels
expr_label = QLabel("Function")
minV_label = QLabel("Min value")
maxV_label = QLabel("Max value")

# Add labels to grid
layout.addWidget(expr_label, 0, 0)
layout.addWidget(minV_label, 1, 0)
layout.addWidget(maxV_label, 2, 0)

# Button
plot_button = QPushButton("Plot")
plot_button.clicked.connect(plot)
expr_entry.returnPressed.connect(plot)

# Add button to grid
layout.addWidget(plot_button, 3, 1)

# combine layouts and add canvas
h_layout.addLayout(layout)
h_layout.addWidget(static_canvas)


window.setLayout(h_layout) # Pass the layout to the window
window.show() # Show window
app.exec_() # Execute the App
