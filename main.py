import jinja2
import pygments
from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QTextEdit, QSplitter, QPushButton, QVBoxLayout, \
    QFileDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

TEMPLATE = '''
<!DOCTYPE html>
<html> 
  <head>
    <title>Processing.JS inside Webpages: Template</title> 
  </head>
  <body>
    <!--This draws the canvas on the webpage -->
    <canvas id="mycanvas"></canvas> 
  </body>
 
  <!-- Include the processing.js library -->
  <!-- See https://khanacademy.zendesk.com/hc/en-us/articles/202260404-What-parts-of-ProcessingJS-does-Khan-Academy-support- for differences -->
  <script src="https://cdn.jsdelivr.net/processing.js/1.4.8/processing.min.js"></script> 
  <script>
  var programCode = function(processingInstance) { 
    with (processingInstance) { 
      {{content}} 
    }};

  // Get the canvas that ProcessingJS will use
  var canvas = document.getElementById("mycanvas"); 
  // Pass the function to ProcessingJS constructor
  var processingInstance = new Processing(canvas, programCode); 
  </script>
</html>
'''

DEFAULT_CODE = '''
      size(400, 400); 
      frameRate(30);
        
      // Paste code from Khan Academy here:
      fill(255, 255, 0);
      ellipse(200, 200, 200, 200);
      noFill();
      stroke(0, 0, 0);
      strokeWeight(2);
      arc(200, 200, 150, 100, 0, PI);
      fill(0, 0, 0);
      ellipse(250, 200, 10, 10);
      ellipse(153, 200, 10, 10);
'''


def main():
    app = QApplication([])
    text_box = QTextEdit()
    text_box.setFontFamily("Courier New")
    web = QWebEngineView()
    web.setUrl(QUrl("file:///test.html"))

    def update_text(text):
        text_box.setText(text)

    update_text(DEFAULT_CODE)

    file_label = QLabel()

    save_button = QPushButton("&Save")
    load_button = QPushButton("&Load")

    parent = QSplitter()
    controls_widget = QWidget()
    file_buttons_layout = QHBoxLayout()
    file_buttons_layout.addWidget(save_button)
    file_buttons_layout.addWidget(load_button)

    controls_layout = QVBoxLayout()
    controls_layout.addWidget(text_box)
    controls_layout.addWidget(file_label)
    controls_layout.addLayout(file_buttons_layout)
    controls_widget.setLayout(controls_layout)

    main_layout = QHBoxLayout()
    main_layout.addWidget(controls_widget)
    main_layout.addWidget(web)

    parent.setLayout(main_layout)
    parent.show()

    prev_filename = ""

    def save():
        nonlocal prev_filename
        file_name = QFileDialog.getSaveFileName(
            parent,
            "Save...", prev_filename, "JS Files (*.js)")
        if file_name:
            prev_filename = file_name[0]
            file_label.setText(prev_filename)
            with open(prev_filename, 'w') as f:
                f.write(text_box.toPlainText())

    def load():
        nonlocal prev_filename
        file_name = QFileDialog.getOpenFileName(
            parent,
            "Load...", prev_filename, "JS Files (*.js)")
        if file_name:
            prev_filename = file_name[0]
            file_label.setText(prev_filename)
            with open(prev_filename) as f:
                update_text(f.read())

    def set_web_content():
        html = jinja2.Template(TEMPLATE).render(content=text_box.toPlainText())
        web.setContent(html.encode(), mimeType="text/html", baseUrl=QUrl("https://cdn.jsdelivr.net"))

    save_button.clicked.connect(save)
    load_button.clicked.connect(load)
    text_box.textChanged.connect(set_web_content)

    app.exec()


if __name__ == "__main__":
    main()
