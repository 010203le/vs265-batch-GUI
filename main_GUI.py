from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from UI import Ui_MainWindow
import os
import sys

if getattr(sys, 'frozen', False):
    PathOfThisFile = os.path.dirname(sys.executable)
elif __file__:
    PathOfThisFile = os.path.dirname(__file__)

x265P = '--crf 14.5 --preset slower --tune lp++ --output-depth 10 --profile main10 --level-idc 4.1 --rd 5 --psy-rd 1.8 --rskip 0 --ctu 32 --limit-tu 2 --cutree-strength 1.75 --no-rect --no-amp --aq-mode 5 --qg-size 8 --aq-strength 0.8 --qcomp 0.65 --cbqpoffs -2 --crqpoffs -2 --vbv-bufsize 30000 --vbv-maxrate 30000 --pbratio 1.2 --hme-range 16,24,40 --merange 38 --bframes 8 --rc-lookahead 60 --ref 4 --min-keyint 1 --no-open-gop --deblock -1:-1 --no-sao --no-strong-intra-smoothing'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
		# in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        # TODO
        self.setWindowTitle('vs265-batch')
        self.ui.toolButton.clicked.connect(self.open_x265)
        self.ui.lineEdit.setText(PathOfThisFile+'\\bin\\x265.exe')
        self.ui.lineEdit_2.setText(x265P)
        self.ui.toolButton_4.clicked.connect(self.open_VSPipe)
        self.ui.lineEdit_3.setText(PathOfThisFile+'\\vapoursynth-R57.A6\\VSPipe.exe')
        self.ui.toolButton_3.clicked.connect(self.open_vpy)
        self.ui.lineEdit_4.setText(PathOfThisFile+'\\main.vpy')
        self.ui.toolButton_7.clicked.connect(self.open_mkvmerge)
        self.ui.lineEdit_5.setText(PathOfThisFile+'\\bin\\mkvtoolnix-64-bit-73.0.0\\mkvmerge.exe')
        self.ui.lineEdit_6.setText(PathOfThisFile+'\\_temp')
        self.ui.lineEdit_7.setText(PathOfThisFile+'\\_source')
        self.ui.lineEdit_8.setText(PathOfThisFile+'\\_encode')
        self.ui.lineEdit_10.setText('lolice-EC')
        self.ui.lineEdit_11.setText('jpn')
        self.ui.lineEdit_12.setText('24000/1001p')
        self.ui.pushButton.clicked.connect(self.run)

    def open_x265(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")
        self.ui.lineEdit.setText(filename)
    
    def open_VSPipe(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")
        self.ui.lineEdit_3.setText(filename)
    
    def open_vpy(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")
        self.ui.lineEdit_4.setText(filename)
    
    def open_mkvmerge(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")
        self.ui.lineEdit_5.setText(filename)

    def run(self):
        # TODO
        mkvCount = 0
        mkvList = []
        mkvNameList = []
        batList = []
        mergeList = []

        for root, dirs, files in os.walk(self.ui.lineEdit_7.text()):
            for file in files:
                if file.endswith('.mkv'):
                    mkvList.append(os.path.join(root, file))
                    mkvNameList.append(file)
                    mkvCount += 1
        
        with open(self.ui.lineEdit_4.text(), 'r') as f:
            vpy = f.read()
            vpy = vpy.split('#BATCH')
            f.close()
        VSPipe = self.ui.lineEdit_3.text()
        x265 = self.ui.lineEdit.text()
        x265P=self.ui.lineEdit_2.text()
        mkvMerge = self.ui.lineEdit_5.text()
        temp = self.ui.lineEdit_6.text()
        outPath = self.ui.lineEdit_8.text()
        trackName = self.ui.lineEdit_10.text()
        videoLang = self.ui.lineEdit_11.text()
        optFileName = self.ui.lineEdit_9.text()
        fps = self.ui.lineEdit_12.text()
        for i in range(mkvCount):
            batList.append('"'+VSPipe+'"'+' "'+os.path.join(temp, 'batch'+str(i+1)+'.vpy')+'" - --y4m | '+'"'+x265+'" '+x265P+' --y4m --output "'+os.path.join(temp, 'batch'+str(i+1)+'_out.hevc')+'" -')
            mergeList.append('"'+mkvMerge+'" -o "'+ outPath +'\\'+mkvNameList[i][:-4]+'_new.mkv" -D "'+mkvList[i]+'" '+'--language 0:"' + videoLang + '" --track-name 0:"' + trackName + '" --default-duration 0:'+fps+' "'+os.path.join(temp, 'batch'+str(i+1)+'_out.hevc')+'"')
            with open(os.path.join(temp, 'batch'+str(i+1)+'.vpy'), 'w') as f:
                f.write(vpy[0]+'\na=r"'+mkvList[i]+'"\n'+vpy[2])
                f.close()
                i=i+1
        with open(optFileName+'_batch.bat', 'w') as f:
            f.write('@echo off\n')
            for i in range(mkvCount):
                f.write(batList[i]+'\n')
                f.write(mergeList[i]+'\n')
                i=i+1
            f.write('\npause')
            f.close()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Done!")
        msg.setWindowTitle("Done")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())