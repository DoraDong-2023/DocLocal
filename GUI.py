import os, sys, markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QTextBrowser, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFrame, QFrame, QLineEdit, QPushButton, QTreeWidgetItem, QTabWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QDesktopServices, QStandardItemModel, QStandardItem
from getlink import *


class MarkdownViewer(QMainWindow):
    def __init__(self,folder_path):
        super().__init__()

        self.folder_path = folder_path

        self.setWindowTitle("Markdown Viewer")
        self.resize(800, 600)
        # left
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search on Google/Bing")
        self.search_edit.returnPressed.connect(self.on_search_Github)
        self.google_button = QPushButton("G")
        self.google_button.clicked.connect(lambda:self.on_search_engine("google"))
        self.google_button.setFixedSize(40, 30)
        self.bing_button = QPushButton("B")
        self.bing_button.clicked.connect(lambda:self.on_search_engine("bing"))
        self.bing_button.setFixedSize(40, 30)
        self.ggd_button = QPushButton("D")
        self.ggd_button.clicked.connect(lambda:self.on_search_engine("duckduckgo"))
        self.ggd_button.setFixedSize(40, 30)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.google_button)
        search_layout.addWidget(self.bing_button)
        search_layout.addWidget(self.ggd_button)
        search_layout.setContentsMargins(3, 0, 0, 0)
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        # left down
        model = QStandardItemModel()
        root_item = QStandardItem(os.path.basename(folder_path))
        root_item.setCheckable(False)
        model.appendRow(root_item)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    file_item = QStandardItem(os.path.basename(root)+'/'+file)
                    file_item.setData(os.path.join(root, *dirs, file), role=Qt.UserRole)
                    file_item.setCheckable(False)
                    root_item.appendRow(file_item)
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(model)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.AscendingOrder)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setExpandsOnDoubleClick(True)
        self.tree_view.clicked.connect(self.on_clicked)


        # right
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.anchorClicked.connect(QDesktopServices.openUrl)
        self.text_browser.setFrameStyle(QFrame.NoFrame)
        self.text_browser.setReadOnly(True)
        self.text_browser.setContextMenuPolicy(Qt.NoContextMenu)
        self.text_browser.setMinimumWidth(600)
        self.text_browser.setMinimumHeight(600)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.text_browser)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        left_layout = QVBoxLayout()
        #left_layout.addWidget(search_layout)
        left_layout.addWidget(self.tree_view)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        splitter00 = QSplitter(Qt.Vertical)
        splitter00.addWidget(search_widget)
        splitter00.addWidget(left_widget)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(splitter00)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("https://www.bing.com"))
        browse_layout = QVBoxLayout()
        browse_layout.addWidget(self.browser)
        websearch_widget = QWidget()
        websearch_widget.setLayout(browse_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(right_widget, "Markdown Viewer")
        self.tabs.addTab(websearch_widget, "Web Search")

        splitter.addWidget(self.tabs)
        splitter.setSizes([200, 600])
        self.setCentralWidget(splitter)
    def on_search_Github(self,):
        self.text_browser.setText('Getting Files from Github...')
        search_text = self.search_edit.text()
        reback = save_readme_from_url(search_text)
        # TODO:直接显示markdown
        # notification
        self.text_browser.setText('Getting Files from Github...'+'\n'+reback+'\n'+'Now you can load content under filepath.')
        self.update_directory()
        self.update()
        self.repaint()
    def on_search_engine(self,name="google"):
        search_text = self.search_edit.text()
        if name=='google':
            if search_text:
                url = "https://www.google.com/search?q=" + search_text
            else:
                url = "https://www.google.com"
            self.browser.load(QUrl(url))
        elif name=='bing':
            if search_text:
                url = "https://www.bing.com/search?q=" + search_text
            else:
                url = "https://www.bing.com"
            self.browser.load(QUrl(url))
        elif name=='duckduckgo':
            if search_text:
                url = "https://duckduckgo.com/html/?q=" + search_text
            else:
                url = "https://duckduckgo.com"
            self.browser.load(QUrl(url))
    

    def on_clicked(self, index):
        #path = self.file_system_model.filePath(index)
        file_path = index.data(role=Qt.UserRole)
        if isinstance(file_path,str):
            self.show_markdown(file_path)
    def show_markdown(self,path):
        if os.path.isfile(path) and path.endswith(".md"):
            with open(path, "r", encoding="utf-8") as f:
                md_text = f.read()
                html_text = markdown.markdown(md_text)
                self.text_browser.setHtml(html_text)
    def update_directory(self):
        model = QStandardItemModel()
        root_item = QStandardItem(os.path.basename(self.folder_path))
        root_item.setCheckable(False)
        model.appendRow(root_item)
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".md"):
                    file_item = QStandardItem(os.path.basename(root)+'/'+file)
                    file_item.setData(os.path.join(root, *dirs, file), role=Qt.UserRole)
                    file_item.setCheckable(False)
                    root_item.appendRow(file_item)
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(model)
                

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    viewer = MarkdownViewer("/Users/doradong/Doc/code_idea/Dash_self/code")
    viewer.show()
    sys.exit(app.exec_())



"""
pyqt5做一个GUI页面，左边栏里最上方为搜索框，搜索框右边有两个按钮G,B。左边栏下方自动展示当前路径下的所有md文件目录，名称为路径。右边窗口选择对应名称可以显示md文件为markdown，并可以滚动窗口拖动看内容
"""