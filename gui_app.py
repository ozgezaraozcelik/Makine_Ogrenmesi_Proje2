import os
import sys

# --- KRİTİK AYARLAR (EN BAŞTA OLMALI) ---
# Windows'un DLL hatasını engellemek için:
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Sanal ortamdaki torch DLL dosyalarının yolunu elle gösteriyoruz
try:
    current_dir = os.getcwd()
    # "sanal_ortam" klasör isminin senin klasörünle birebir aynı olduğundan emin ol
    dll_path = os.path.join(current_dir, "sanal_ortam", "Lib", "site-packages", "torch", "lib")
    if os.path.exists(dll_path):
        os.add_dll_directory(dll_path)
except Exception as e:
    print(f"DLL Yolu eklenirken hata oluştu (Önemli olmayabilir): {e}")

# --- IMPORT SIRALAMASI ÇOK ÖNEMLİDİR ---
# ÖNCE PyTorch/YOLO yüklenmeli, SONRA OpenCV (cv2) yüklenmeli.
# Yoksa "WinError 1114" hatası alırsın.
from ultralytics import YOLO
import cv2  # YOLO'dan SONRA gelmeli

# PyQt Kütüphaneleri
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, 
                             QTextEdit, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class KiyafetTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLG-407 Kıyafet Tespiti - PRO Sürüm")
        self.setGeometry(100, 100, 1200, 750)

        # 1. Modeli Yükle (best.pt dosyası bu kodla aynı klasörde olmalı)
        model_path = 'best.pt'
        if not os.path.exists(model_path):
            QMessageBox.critical(self, "Hata", "best.pt dosyası bulunamadı! Lütfen dosya yolunu kontrol edin.")
            self.model = None
        else:
            try:
                self.model = YOLO(model_path)
            except Exception as e:
                QMessageBox.critical(self, "Model Hatası", f"Model yüklenirken hata oluştu:\n{e}")
                self.model = None

        self.image_path = None
        self.detected_image = None
        self.initUI()

    def initUI(self):
        # Ana Düzen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # --- SOL TARAFTAKİ PANEL (Resimler) ---
        image_layout = QHBoxLayout()
        
        # Orijinal Resim Alanı
        self.label_original = QLabel("Orijinal Resim")
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setStyleSheet("border: 2px solid gray; background-color: #f0f0f0;")
        self.label_original.setFixedSize(500, 500)
        
        # İşlenmiş (Tagged) Resim Alanı
        self.label_processed = QLabel("Tespit Sonucu")
        self.label_processed.setAlignment(Qt.AlignCenter)
        self.label_processed.setStyleSheet("border: 2px solid gray; background-color: #f0f0f0;")
        self.label_processed.setFixedSize(500, 500)

        image_layout.addWidget(self.label_original)
        image_layout.addWidget(self.label_processed)

        # --- SAĞ TARAFTAKİ PANEL (Butonlar ve Bilgi) ---
        control_layout = QVBoxLayout()

        # Butonlar
        self.btn_select = QPushButton("1. Select Image (Resim Seç)")
        self.btn_select.clicked.connect(self.resim_sec)
        self.btn_select.setStyleSheet("font-size: 14px; padding: 10px;")

        self.btn_detect = QPushButton("2. Test Image (Fotoda Test Et)")
        self.btn_detect.clicked.connect(self.tespit_et)
        self.btn_detect.setStyleSheet("font-size: 14px; padding: 10px; background-color: #4CAF50; color: white;")

        # --- YENİ EKSTRA PUAN BUTONU ---
        self.btn_camera = QPushButton("🔥 Canlı Kamera Testi (Video) 🔥")
        self.btn_camera.clicked.connect(self.kamera_ac)
        self.btn_camera.setStyleSheet("""
            font-size: 14px; padding: 10px; background-color: #FF5722; color: white; font-weight: bold;
        """)

        self.btn_save = QPushButton("3. Save Image (Sonucu Kaydet)")
        self.btn_save.clicked.connect(self.kaydet)
        self.btn_save.setStyleSheet("font-size: 14px; padding: 10px;")

        # Sonuç Listesi (List Widget)
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Tespit edilen nesneler burada listelenecek...\nKamera açıldığında bilgi verilecek.")
        self.result_text.setMaximumHeight(200)

        control_layout.addWidget(self.btn_select)
        control_layout.addWidget(self.btn_detect)
        control_layout.addWidget(self.btn_camera) 
        control_layout.addWidget(self.btn_save)
        control_layout.addWidget(QLabel("Tespit Detayları:"))
        control_layout.addWidget(self.result_text)
        control_layout.addStretch()

        # Ana düzene ekle
        layout_container = QVBoxLayout()
        layout_container.addLayout(image_layout)
        layout_container.addLayout(control_layout)
        central_widget.setLayout(layout_container)

    def resim_sec(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.png *.jpeg)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.label_original.setPixmap(pixmap.scaled(self.label_original.width(), self.label_original.height(), Qt.KeepAspectRatio))
            self.label_processed.setText("Tespit Bekleniyor...")
            self.result_text.clear()
            self.result_text.append(f"Resim yüklendi: {os.path.basename(file_path)}")

    def tespit_et(self):
        if not self.model:
            QMessageBox.warning(self, "Uyarı", "Model yüklenemediği için işlem yapılamıyor.")
            return
        if not self.image_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim seçin!")
            return

        results = self.model(self.image_path)
        result = results[0]
        plotted_image = result.plot()
        plotted_image_rgb = cv2.cvtColor(plotted_image, cv2.COLOR_BGR2RGB)
        
        height, width, channel = plotted_image_rgb.shape
        bytes_per_line = 3 * width
        q_img = QImage(plotted_image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.detected_image = QPixmap.fromImage(q_img)

        self.label_processed.setPixmap(self.detected_image.scaled(self.label_processed.width(), self.label_processed.height(), Qt.KeepAspectRatio))

        self.result_text.clear()
        self.result_text.append(f"--- Fotoğraf Tespiti Sonuçları ---")
        class_counts = {}
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = result.names[cls_id]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        for name, count in class_counts.items():
            self.result_text.append(f"{name}: {count} adet")
        if not class_counts:
             self.result_text.append("Hiçbir nesne tespit edilemedi.")

    # --- YENİ KAMERA FONKSİYONU ---
    def kamera_ac(self):
        if not self.model:
            QMessageBox.warning(self, "Uyarı", "Model yüklenemedi!")
            return

        self.result_text.clear()
        self.result_text.append("Canlı kamera açılıyor... Lütfen bekleyin.\nKapatmak için açılan pencerede 'q' tuşuna basın.")
        QApplication.processEvents() # Arayüzün donmasını engelle

        cap = cv2.VideoCapture(0) # 0 numaralı kamerayı aç
        
        if not cap.isOpened():
            QMessageBox.critical(self, "Hata", "Kamera açılamadı! Bağlantıyı kontrol edin.")
            self.result_text.append("Hata: Kamera açılamadı.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Modeli kullanarak tahmin yap (stream=True daha hızlıdır)
            results = self.model(frame, stream=True, verbose=False)
            
            # Sonucu çizdir
            for result in results:
                annotated_frame = result.plot()

            # Sonucu yeni bir pencerede göster
            cv2.imshow("YOLOv8 Canlı Kıyafet Tespiti (Çıkmak için 'q' bas)", annotated_frame)

            # 'q' tuşuna basılırsa döngüyü kır
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.result_text.append("\nKamera kapatıldı.")

    def kaydet(self):
        if self.detected_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "Resmi Kaydet", "sonuc.jpg", "Resim Dosyaları (*.jpg *.png)")
            if file_path:
                self.detected_image.save(file_path)
                QMessageBox.information(self, "Başarılı", "Resim başarıyla kaydedildi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek bir sonuç yok!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KiyafetTespitUygulamasi()
    window.show()
    sys.exit(app.exec_())