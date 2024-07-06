from PySide2.QtWidgets import QLineEdit, QListView


class FilterWidget(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(FilterWidget, self).__init__(*args, **kwargs)
        self.setPlaceholderText("Filter list")
        self.setClearButtonEnabled(True)
        self.textChanged.connect(self.filter_list)

    def filter_list(self):
        filter = self.text()
        listWidget = self.parentWidget().findChildren(QListView)[0]

        model = listWidget.model()
        if filter != "":
            for index in range(model.rowCount(0)):
                if filter.lower() in model.index(index, 0).data().lower():
                    print(model.index(index, 0).data)
                    listWidget.setRowHidden(index, False)
                else:
                    listWidget.setRowHidden(index, True)
        else:
            for index in range(model.rowCount(0)):
                listWidget.setRowHidden(index, False)
