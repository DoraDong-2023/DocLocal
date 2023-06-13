import os, sys, markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QTextBrowser, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFrame, QFrame, QLineEdit, QPushButton, QTreeWidgetItem, QTabWidget
from PyQt5.QtCore import Qt, QUrl, QModelIndex
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QDesktopServices, QStandardItemModel, QStandardItem
from getlink import *
import argparse

parser = argparse.ArgumentParser(description='Search using Google or download file.')
parser.add_argument('--search_engine', default='google', help='search using Google')
args = parser.parse_args()

class MarkdownViewer(QMainWindow):
    def __init__(self,folder_path):
        super().__init__()

        self.folder_path = folder_path

        self.setWindowTitle("DocLocal")
        self.resize(800, 500)
        # left
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Github/Google/Bing/DuckDuckgo")
        self.search_edit.returnPressed.connect(self.on_search_Github)
        self.google_button = QPushButton("S")
        self.google_button.clicked.connect(lambda:self.on_search_engine(args.search_engine))
        self.google_button.setFixedSize(40, 30)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.google_button)
        search_layout.setContentsMargins(3, 0, 0, 0)
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        # left down
        
        self.tree_view = QTreeView(self)
        self.renew_tree()
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
        self.text_browser.setMinimumWidth(400)
        self.text_browser.setMinimumHeight(300)
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
    def renew_tree(self,):
        model = QStandardItemModel()
        root_item = QStandardItem('Github')
        root_item.setFlags(root_item.flags() & ~Qt.ItemIsEditable)
        model.appendRow(root_item)
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".md") or file.endswith(".rst"):
                    file_item = QStandardItem(os.path.basename(root)+'/'+file)
                    file_item.setData(os.path.join(root, *dirs, file), role=Qt.UserRole)
                    file_item.setCheckable(False)
                    file_item.setFlags(root_item.flags() & ~Qt.ItemIsEditable)
                    root_item.appendRow(file_item)
        self.tree_view.setModel(model)
        #index = model.index(0, 0, QModelIndex())
        #self.tree_view.setRowHidden(index.row(), QModelIndex(), False)
        
    def on_search_Github(self,):
        self.text_browser.setText('Getting Files from Github...')
        search_text = self.search_edit.text()
        reback = save_readme_from_url(search_text)
        self.text_browser.setText('Getting Files from Github...'+'\n'+reback+'\n'+'Now you can load content under filepath.')
        self.renew_tree()
        # go to page 1
        self.tabs.setCurrentIndex(0)
    def on_search_engine(self,search_engine="google"):
        search_text = self.search_edit.text()
        if search_engine=='google':
            if search_text:
                url = "https://www.google.com/search?q=" + search_text
            else:
                url = "https://www.google.com"
            self.browser.load(QUrl(url))
        elif search_engine=='bing':
            if search_text:
                url = "https://www.bing.com/search?q=" + search_text
            else:
                url = "https://www.bing.com"
            self.browser.load(QUrl(url))
        elif search_engine=='duckduckgo':
            if search_text:
                url = "https://duckduckgo.com/html/?q=" + search_text
            else:
                url = "https://duckduckgo.com"
            self.browser.load(QUrl(url))
        # go to page 2
        self.tabs.setCurrentIndex(1)
    def on_clicked(self, index):
        file_path = index.data(role=Qt.UserRole)
        if isinstance(file_path,str):
            self.show_markdown(file_path)
    def show_markdown(self,path):
        if os.path.isfile(path) and path.endswith(".md"):
            with open(path, "r", encoding="utf-8") as f:
                md_text = f.read()
                html_text = markdown.markdown(md_text)
                self.text_browser.setHtml(html_text)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MarkdownViewer(os.path.abspath(os.getcwd()))
    viewer.show()
    sys.exit(app.exec_())
