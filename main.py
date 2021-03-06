import speech_recognition as sr
from komut import komutlar, Veritabani
from PyQt5 import QtWidgets, uic, QtGui, QtCore, QtMultimedia
import sys
from responsive_voice import ResponsiveVoice
import threading
import time
from os import remove,environ,getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import webbrowser
import sounddevice as sd
from numpy.linalg import norm
from multiprocessing import Process

r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
r.dynamic_energy_threshold = False
r.energy_threshold -= 100



class listenThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(object)

    def run(self):
        r.energy_threshold += 250
        try:
            with sr.Microphone() as source:
                audio = r.listen(source,timeout=3)
            r.energy_threshold -= 250
            if window.listenAktif:
                window.Tip_Label.setText("Konuşmak için butona tıklayın")
                window.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
                window.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
                window.ttsIptal = False
                window.listenAktif = False
                window.animasyon = False
                text = r.recognize_google(audio, language='tr-tr')
                if "Merih" in text:
                    text = text.replace("Merih","Mary")
                if "Melih" in text:
                    text = text.replace("Melih","Mary")
                if "Meri" in text:
                    text = text.replace("Meri","Mary")
                if "Mery" in text:
                    text = text.replace("Mery","Mary")
                if window.listenAktif == False:
                    window.Kelime_Label.setText(text)
                    komut = komutlar(text)
                    komut.islemBul(window.yapilanislem)
                    window.yapilanislem = komut.yapilanislem
                    pozisyon = 100
                    self.soundPath = window.voiceEngine.get_mp3(komut.seslendirilecektext)
                    try:
                        url = QtCore.QUrl.fromLocalFile(self.soundPath)
                    except:
                        pass
                    window.soundPlayer.setMedia(QtMultimedia.QMediaContent(url))
                    window.soundPlayer.play()
                    self.signal.emit(komut)
                    for i in range(20):
                        if pozisyon > 0:
                            pozisyon -= 5
                            window.Yanit_Layout.setContentsMargins(0, 0, 0, pozisyon)
                            time.sleep(0.01)
                    window.backgroundListen = True
                    while window.ttsIptal != True:
                            time.sleep(0.05)
                    window.soundPlayer.stop()
            self.quit()

        except sr.UnknownValueError:
            print("Ne dediğini anlayamadım.")
            window.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
            window.Kelime_Label.setText("Anlaşılmadı")
            window.listenAktif = False
            window.backgroundListen = True
            self.quit()

        except sr.RequestError:
            print("İnternet bağlanıtısı kurulamadı.")
            window.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
            window.listenAktif = False
            window.backgroundListen = True
            self.quit()

        except sr.WaitTimeoutError:
            print("Timeout")
            window.Tip_Label.setText("Konuşmak için butona tıklayın")
            window.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
            window.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(window.dosyakonumu))
            window.listenAktif = False
            window.backgroundListen = True
            self.quit()

        except Exception as code:
            print(code)
            window.yapilanislem = ""
            window.Yanit_Label.setText("Bir hata oluştu bunun için üzgünüm")
            window.voiceEngine.say("Bir hata oluştu bunun için üzgünüm")
            self.quit()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('iwsss.ui', self)
        self.setDefaultUi()
        self.show()


    def setDefaultUi(self):
        self.version = self.findChild(QtWidgets.QLabel, 'version')
        self.version.setText("Mary 1.0.04")
        self.micButton = self.findChild(QtWidgets.QPushButton, 'micButton')
        self.Kelime_Label = self.findChild(QtWidgets.QLabel,'Kelime_Label')
        self.Yanit_Label = self.findChild(QtWidgets.QLabel,'Yanit_Label')
        self.Tip_Label = self.findChild(QtWidgets.QLabel,'Tip_Label')
        self.Yanit_Layout = self.findChild(QtWidgets.QLayout, 'horizontalLayout_2')
        self.Image_Label = self.findChild(QtWidgets.QLabel, 'Image_Label')
        self.sitelink1 = self.findChild(QtWidgets.QLabel, 'sitelink1')
        self.sitelink2 = self.findChild(QtWidgets.QLabel, 'sitelink2')
        self.sitelink3 = self.findChild(QtWidgets.QLabel, 'sitelink3')
        self.sitebaslik1 = self.findChild(QtWidgets.QLabel, 'sitebaslik1')
        self.sitebaslik2 = self.findChild(QtWidgets.QLabel, 'sitebaslik2')
        self.sitebaslik3 = self.findChild(QtWidgets.QLabel, 'sitebaslik3')
        self.sitebaslik1.setOpenExternalLinks(True)
        self.sitebaslik2.setOpenExternalLinks(True)
        self.sitebaslik3.setOpenExternalLinks(True)
        self.siteaciklama1 = self.findChild(QtWidgets.QLabel, 'siteaciklama1')
        self.siteaciklama2 = self.findChild(QtWidgets.QLabel, 'siteaciklama2')
        self.siteaciklama3 = self.findChild(QtWidgets.QLabel, 'siteaciklama3')
        self.web_sonuc1 = self.findChild(QtWidgets.QLayout, 'web_sonuc1')
        self.web_sonuc2 = self.findChild(QtWidgets.QLayout, 'web_sonuc2')
        self.web_sonuc3 = self.findChild(QtWidgets.QLayout, 'web_sonuc3')
        self.web_sonuc1.setSpacing(0)
        self.web_sonuc2.setSpacing(0)
        self.web_sonuc3.setSpacing(0)
        self.web_sonuc1.setContentsMargins(0 ,0 ,0 ,0)
        self.web_sonuc2.setContentsMargins(0, 0, 0, 0)
        self.web_sonuc3.setContentsMargins(0, 0, 0, 0)
        self.micButton.clicked.connect(self.micButtonPressed)
        self.setWindowIcon(QtGui.QIcon('image/mary.png'))
        self.animasyon = False
        self.ttsIptal = False
        self.listenAktif = False
        self.micButtonClickable = True
        self.Image_Label.show()
        self.aktifThreadler = 0
        self.dosyakonumu = getcwd()
        self.soundPlayer = QtMultimedia.QMediaPlayer()
        self.soundPlayer.stateChanged.connect(self.soundPlayerState)
        #Tray icon
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("image/mary.png"))
        self.tray_icon.activated.connect(self.trayDoubleClick)
        show_action = QtWidgets.QAction("Göster", self)
        quit_action = QtWidgets.QAction("Çıkış yap", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.closeApp)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        for i in range(10):
            self.dosyakonumu = self.dosyakonumu.replace("\\","/")
        i = "border-image: url('{}/image/background.png');".format(self.dosyakonumu)
        stylesheet = "#centralwidget{"+i+"}"
        self.setStyleSheet(stylesheet)
        self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(self.dosyakonumu))
        self.yapilanislem = ""
        self.backgroundListen = True
        self.voiceEngine = ResponsiveVoice(lang=ResponsiveVoice.TURKISH, gender=ResponsiveVoice.FEMALE, pitch=0.52, rate=0.53,key="8FCWWns8",vol=0.97)
        threading.Thread(target=self.sesanimasyon,daemon=True).start()
        threading.Thread(target=self.background,daemon=True).start()
        self.db = Veritabani()
        if self.db.ad() == "":
            self.yapilanislem = "ilkacilis"
            threading.Thread(target=self.ilkCalistirma,daemon=True).start()

    def closeApp(self):
        self.hide()
        sys.exit()

    def closeEvent(self, event):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Mary - Sesli asistan",
                "Sesli asistan simge durumuna küçültüldü",
                QtWidgets.QSystemTrayIcon.Information,
                2000
            )
    
    def trayDoubleClick(self, reason):
            if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
                self.show()

    def backgroundCallBack(self,audio):
        if self.backgroundListen:
            try:
                text = r.recognize_google(audio, language='tr-tr')
                liste = ["Merih","Melih","Meri","Mery","MARIO","Mary","emery","h&m"]
                for i in liste:
                    if i in text:
                        text = i.replace(i,"Mary")
                if "MARY" in text.upper():
                    self.notification = QtCore.QUrl.fromLocalFile("{}/notification.mp3".format(self.dosyakonumu))
                    self.soundPlayer.setMedia(QtMultimedia.QMediaContent(self.notification))
                    self.soundPlayer.play()
                    self.listenAktif = True
                    self.ttsIptal = True
                    self.animasyon = True
                    self.backgroundListen = False
                    self.Tip_Label.setText("Dinleniyor")
                    self.micButton.setStyleSheet("border-image: url('{}/image/mic_2.png');".format(self.dosyakonumu))
                    self.Tip_Label.setStyleSheet("background-color:#ff0000;color: rgb(255, 255, 255);")
                    self.show()
                    self.dinle = listenThread(parent=window)
                    self.dinle.start()
                    self.dinle.signal.connect(self.setUi)
                    self.backgroundListen = False
                else:
                    print(text)
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            else:
                print(text)
        SystemExit

    def background(self):
        while True:
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source,timeout=2,phrase_time_limit=2)
                    threading.Thread(target=self.backgroundCallBack,args={audio}).start()
            except sr.WaitTimeoutError:
                pass

    def ilkCalistirma(self):
        self.micButton.setMaximumSize(0, 0)
        self.micButton.setMinimumSize(0, 0)
        self.backgroundListen = False
        self.Tip_Label.setText("")
        threading.Thread(target=self.setYanitLabel, args={"Hoşgeldin, Adım Mary. Ben senin sesli asistanınım."},daemon=True).start()
        self.voiceEngine.say("Hoşgeldin, Adım Mary.\nBen senin sesli asistanınım.")
        threading.Thread(target=self.setYanitLabel,args={"Öncelikle adını öğrenebilir miyim?\nAdını söylemek için lütfen butona tıkla"},daemon=True).start()
        self.voiceEngine.say("Öncelikle adını öğrenebilir miyim? Adını söylemek için lütfen butona tıkla")
        self.micButton.setMaximumSize(80, 80)
        self.micButton.setMinimumSize(80, 80)
        self.Tip_Label.setText("Konuşmak için butona tıklayın")
        while True:
            time.sleep(0.1)
            if self.db.ad() != "":
                time.sleep(5)
                self.setYanitLabel("")
                self.Image_Label.show()
                self.Image_Label.setStyleSheet("border-image: url('{}/image/neler_yapabilirsin.png');".format(self.dosyakonumu))
                self.Image_Label.setMaximumSize(630, 270)
                self.Image_Label.setMinimumSize(630, 270)
                self.voiceEngine.say(f"Yapabileceklerimin bazıları şunlar {self.db.ad()}. Şimdi başlayabilirsin")
                break
        sys.exit()

    def micButtonPressed(self):
        print("micButton Basıldı")
        if self.listenAktif:
            self.micButtonClickable = False
            self.micButton.setEnabled(False)
            self.ttsIptal = True
            self.listenAktif = False
            self.animasyon = False
            self.Tip_Label.setText("Konuşmak için butona tıklayın")
            self.Tip_Label.setStyleSheet("color: rgb(255, 255, 255);")
            self.micButton.setStyleSheet("border-image: url('{}/image/mic_1.png');".format(self.dosyakonumu))
            def i():
                time.sleep(2)
                self.micButtonClickable = True
                self.micButton.setEnabled(True)
                self.backgroundListen = True
                SystemExit
            threading.Thread(target=i,daemon=True).start()
        else:
            if self.micButtonClickable:
                self.listenAktif = True
                self.ttsIptal = True
                self.animasyon = True
                self.backgroundListen = False
                self.Tip_Label.setText("Dinleniyor")
                self.micButton.setStyleSheet("border-image: url('{}/image/mic_2.png');".format(self.dosyakonumu))
                self.Tip_Label.setStyleSheet("background-color:#ff0000;color: rgb(255, 255, 255);")
                self.dinle = listenThread(parent=window)
                self.dinle.start()
                self.dinle.signal.connect(self.setUi)
    @staticmethod
    def sesanimasyon():
        def sound(indata, outdata, frames, time, status):
            volume_norm = norm(indata) * 20
            if window.animasyon:
                window.Tip_Label.setMinimumSize(70+volume_norm, 0)
        while True:
            with sd.Stream(callback=sound):
                sd.sleep(1000000)

    def setYanitLabel(self,yazi,foto=False):
        self.Yanit_Label.setWordWrap(False)
        QtCore.QMetaObject.invokeMethod(self.Yanit_Label, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,yazi))
        yaziBoyutu = QtGui.QFont()
        yaziBoyutu.setPointSize(22)
        if foto:
            self.Yanit_Label.setWordWrap(True)
            self.Yanit_Label.setAlignment(QtCore.Qt.AlignLeft)
        else:
            self.Yanit_Label.setAlignment(QtCore.Qt.AlignCenter)
        if len(yazi)<=40:
            print("40'dan küçük")
            yaziBoyutu.setPointSize(22)
            self.Yanit_Label.setMaximumSize(1000, 99999)

        elif len(yazi)>=40 and len(yazi)<=50:
            print("40-50")
            yaziBoyutu.setPointSize(20)

        elif len(yazi)>=50 and len(yazi)<=60:
            print("50-60")
            yaziBoyutu.setPointSize(18)

        elif len(yazi)>=60 and len(yazi)<=70:
            print("60-70")
            yaziBoyutu.setPointSize(17)
            if foto:
                self.Yanit_Label.setMaximumSize(600, 99999)
            else:
                self.Yanit_Label.setMaximumSize(800, 99999)

        elif len(yazi)>=70 and len(yazi)<=130:
            print("70-130")
            if foto:
                self.Yanit_Label.setMaximumSize(800, 99999)
                self.Yanit_Label.setWordWrap(True)
                yaziBoyutu.setPointSize(18)
            else:
                self.Yanit_Label.setMaximumSize(1000, 99999)
                self.Yanit_Label.setWordWrap(True)
                yaziBoyutu.setPointSize(18)
        else:
            print(len(yazi))
            print("130 üstü")
            yaziBoyutu.setPointSize(14)
            if foto:
                self.Yanit_Label.setMaximumSize(400, 99999)
                self.Yanit_Label.setWordWrap(True)
            else:
                self.Yanit_Label.setMaximumSize(600, 99999)
                self.Yanit_Label.setWordWrap(True)
        self.Yanit_Label.setFont(yaziBoyutu)

    def labelClear(self):
        self.siteaciklama1.setText("")
        self.siteaciklama2.setText("")
        self.siteaciklama3.setText("")
        self.sitebaslik1.setText("")
        self.sitebaslik2.setText("")
        self.sitebaslik3.setText("")
        self.sitelink1.setText("")
        self.sitelink2.setText("")
        self.sitelink3.setText("")
        self.siteaciklama1.hide()
        self.siteaciklama2.hide()
        self.siteaciklama3.hide()
        self.sitebaslik1.hide()
        self.sitebaslik2.hide()
        self.sitebaslik3.hide()
        self.sitelink1.hide()
        self.sitelink2.hide()
        self.sitelink3.hide()
        self.web_sonuc1.setSpacing(0)
        self.web_sonuc2.setSpacing(0)
        self.web_sonuc3.setSpacing(0)
        self.web_sonuc1.setContentsMargins(0, 0, 0, 0)
        self.web_sonuc2.setContentsMargins(0, 0, 0, 0)
        self.web_sonuc3.setContentsMargins(0, 0, 0, 0)
        self.Image_Label.setAlignment(QtCore.Qt.AlignLeft)

    def setUi(self,komut):
        self.labelClear()
        if komut.yapilanislem == "neyapabilirsin":
            self.Image_Label.show()
            self.Image_Label.setStyleSheet("border-image: url('{}/image/neler_yapabilirsin.png');".format(self.dosyakonumu))
            self.Yanit_Label.setText("")
            self.Image_Label.setMinimumSize(630, 270)
            self.Image_Label.setMinimumSize(630, 270)
            self.Yanit_Layout.setSpacing(0)
            self.yapilanislem = ""
        elif komut.yapilanislem == "websiteSonuc":
            self.Image_Label.hide()
            self.sitebaslik1.setCursor(QtCore.Qt.PointingHandCursor)
            self.sitebaslik2.setCursor(QtCore.Qt.PointingHandCursor)
            self.sitebaslik3.setCursor(QtCore.Qt.PointingHandCursor)
            self.web_sonuc1.setContentsMargins(0, 15, 0, 15)
            self.web_sonuc2.setContentsMargins(0, 0, 0, 15)
            self.web_sonuc3.setContentsMargins(0, 0, 0, 15)
            self.web_sonuc1.setSpacing(3)
            self.web_sonuc2.setSpacing(3)
            self.web_sonuc3.setSpacing(3)
            self.siteaciklama1.show()
            self.siteaciklama2.show()
            self.siteaciklama3.show()
            self.sitebaslik1.show()
            self.sitebaslik2.show()
            self.sitebaslik3.show()
            self.sitelink1.show()
            self.sitelink2.show()
            self.sitelink3.show()
            self.Yanit_Label.setText("")
            self.sitelink1.setText(komut.linktext1)
            self.sitelink2.setText(komut.linktext2)
            self.sitelink3.setText(komut.linktext3)
            QtCore.QMetaObject.invokeMethod(self.sitebaslik1, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link1,komut.linktext1)))
            QtCore.QMetaObject.invokeMethod(self.sitebaslik2, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link2,komut.linktext2)))
            QtCore.QMetaObject.invokeMethod(self.sitebaslik3, "setText", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str,"<a href='{}'><font color=white>{}</font></a>".format(komut.link3,komut.linktext3)))
            self.siteaciklama1.setText(komut.aciklama1)
            self.siteaciklama2.setText(komut.aciklama2)
            self.siteaciklama3.setText(komut.aciklama3)
            self.yapilanislem = ""
        elif komut.foto:
            self.Image_Label.show()
            self.Image_Label.setStyleSheet("border-image: url('{}/image/image.jpg');".format(self.dosyakonumu))
            self.Image_Label.setMinimumSize(komut.width, komut.height)
            self.Image_Label.setMaximumSize(komut.width, komut.height)
            if komut.yapilanislem == "havadurumu":
                self.Yanit_Label.setAlignment(QtCore.Qt.AlignLeft)
                QtCore.QMetaObject.invokeMethod(self.Yanit_Label, "setText", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, komut.labelText))
                self.Yanit_Layout.setSpacing(15)
                self.Image_Label.setAlignment(QtCore.Qt.AlignBottom)
                self.sitebaslik1.setText(komut.detay1)
                self.sitebaslik2.setText(komut.detay2)
                self.sitebaslik3.setText(komut.detay3)
                self.sitebaslik1.show()
                self.sitebaslik2.show()
                self.sitebaslik3.show()
                self.sitebaslik1.setCursor(QtCore.Qt.ArrowCursor)
                self.sitebaslik2.setCursor(QtCore.Qt.ArrowCursor)
                self.sitebaslik3.setCursor(QtCore.Qt.ArrowCursor)
                self.yapilanislem = ""
            else:
                self.Yanit_Layout.setSpacing(30)
                self.setYanitLabel(komut.labelText,foto=True)
        else:
            self.Image_Label.setStyleSheet("")
            self.Image_Label.setMinimumSize(0, 0)
            self.Image_Label.setMaximumSize(0, 0)
            self.Image_Label.hide()
            self.Yanit_Layout.setSpacing(6)
            self.setYanitLabel(komut.labelText)

    def soundPlayerState(self,state):
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            pass
        elif state == QtMultimedia.QMediaPlayer.StoppedState:
            try:
                remove(self.soundPath)
                print("Text to speech bitti")
                self.ttsIptal = True
            except Exception as code:
                pass


    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())