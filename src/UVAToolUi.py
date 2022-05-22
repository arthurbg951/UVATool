from PyQt5.QtWidgets import QApplication
from forms.FormUVATool import FormUVATool

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FormUVATool()
    window.show()
    app.exec()
