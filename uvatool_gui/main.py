from PyQt5.QtWidgets import QApplication
from uvatool_gui.forms.UVATool import FormUVATool

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FormUVATool()
    sys.exit(app.exec())
