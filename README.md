👕 BLG-407 Makine Öğrenmesi - YOLOv8 ile Kıyafet Tespiti Projesi
Bu proje, BLG-407 Makine Öğrenmesi dersi kapsamında Özge Zara Özçelik (2212721014) tarafından geliştirilmiştir. Projenin temel amacı, görüntü işleme ve derin öğrenme tekniklerini kullanarak, görsellerdeki kıyafetleri "Üst Giyim" ve "Alt Giyim" olmak üzere iki ana kategoride tespit etmektir.

Proje, Ultralytics YOLOv8 (Nano) mimarisi kullanılarak eğitilmiş ve son kullanıcıların modeli kolayca test edebilmesi için PyQt5 ile modern bir masaüstü arayüzü (GUI) geliştirilmiştir.

📌 Proje İçeriği ve Özellikleri
Model Mimarisi: YOLOv8n (Nano) - Transfer Learning (Transfer Öğrenme) yöntemiyle.

Sınıflar (Classes):

ust_giyim (Tişört, Gömlek, Kazak vb.)

alt_giyim (Pantolon, Etek, Şort vb.)

Veri Seti: Roboflow üzerinden etiketlenen özgün veri seti.

Arayüz (GUI): Python PyQt5 kütüphanesi ile geliştirilmiş kullanıcı dostu arayüz.

Başarı Metrikleri: Confusion Matrix, F1-Score ve mAP değerleri ile model performansı analiz edilmiştir.

📂 Dosya Yapısı
Repo içerisinde bulunan temel dosyalar ve görevleri şöyledir:

PROJE2/proje2_yolo_training.ipynb: Google Colab üzerinde modelin eğitimi, veri setinin indirilmesi ve test işlemlerinin yapıldığı Jupyter Notebook dosyası.

gui_app.py: Eğitilen modeli kullanarak bilgisayarınızda test yapmanızı sağlayan Masaüstü Arayüz uygulaması.

best.pt: Eğitim sonucunda elde edilen en başarılı model ağırlık dosyası.

requirements.txt: Projenin çalışması için gerekli kütüphanelerin listesi.

⚙️ Kurulum (Installation)
Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla takip edin.

1. Repoyu Klonlayın
Bash

git clone https://github.com/ozgezaraozcelik/makine_ogrenmesi_proje2.git
cd makine_ogrenmesi_proje2
2. Sanal Ortam Oluşturun (Önerilen)
Python kütüphanelerinin çakışmasını önlemek için sanal ortam (venv) kullanmanız önerilir.

Bash

# Windows için:
python -m venv sanal_ortam
sanal_ortam\Scripts\activate

# Mac/Linux için:
python3 -m venv sanal_ortam
source sanal_ortam/bin/activate
3. Gerekli Kütüphaneleri Yükleyin
Projenin çalışması için gerekli olan ultralytics, PyQt5, torch, opencv-python gibi kütüphaneleri yükleyin.

Bash

pip install -r requirements.txt
⚠️ Önemli Not (Windows Kullanıcıları İçin): gui_app.py dosyası içerisinde, Windows işletim sistemlerinde sıkça karşılaşılan WinError 1114 ve libiomp5md.dll hatalarını önlemek için özel ayarlar yapılmıştır. Kodun en başında os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" satırı ve import sıralaması (YOLO önce, OpenCV sonra) bu hataları engellemek içindir. Lütfen bu sıralamayı değiştirmeyin.

🚀 Model Eğitimi (Training)
Eğer modeli sıfırdan kendiniz eğitmek isterseniz PROJE2 klasörü altındaki .ipynb dosyasını kullanabilirsiniz.

Google Colab'i açın ve proje2_yolo_training.ipynb dosyasını yükleyin.

Çalışma zamanı türünü GPU (T4) olarak seçin.

Roboflow üzerinden kendi veri setinizi veya mevcut veri setini çekmek için API anahtarınızı girin.

Aşağıdaki komut notebook içerisinde otomatik çalıştırılarak eğitim başlatılır:

Python

model = YOLO('yolov8n.pt') # Nano model yüklenir
results = model.train(
    data='data.yaml',
    epochs=50,         # 50 Epoch eğitim
    imgsz=640,         # 640x640 görüntü boyutu
    name='kiyafet_modelim'
)
Eğitim bittiğinde runs/detect/kiyafet_modelim/weights/best.pt dosyası oluşacaktır. Bu dosyayı indirip gui_app.py ile kullanabilirsiniz.

🖥️ Arayüzün Kullanımı (GUI)
Eğitilen modeli test etmek için arayüzü çalıştırın:

Bash

python gui_app.py
Uygulama Adımları:

Modeli Yükle: Uygulama açıldığında best.pt dosyası otomatik olarak yüklenir.

Resim Seç: "Resim Yükle" butonuna basarak test etmek istediğiniz bir kıyafet fotoğrafını seçin.

Tespit Et: Model görüntüyü analiz eder ve kıyafetleri çerçeve içine alarak (Bounding Box) "Alt Giyim" veya "Üst Giyim" olarak etiketler.

Sonuçlar: Tespit edilen nesne sayısı ve güven oranları (Confidence Score) ekranın sağ tarafında listelenir.

📊 Sonuçlar ve Performans
Model 50 epoch boyunca eğitilmiş ve aşağıdaki başarımlar elde edilmiştir:

Confusion Matrix: Modelin sınıfları (alt/üst) birbirine karıştırma oranı oldukça düşüktür.

mAP50 (Mean Average Precision): Modelin nesneleri doğru konumlandırma ve sınıflandırma başarısı tatmin edici seviyededir.

Test Sonuçları: Farklı ışık ve açılardan çekilen fotoğraflarda yüksek doğrulukla tespit yapabilmektedir.

(Detaylı grafikler ve eğitim çıktıları runs/ klasörü altında incelenebilir.)

📞 İletişim
Geliştirici: Özge Zara Özçelik

Ders: BLG-407 Makine Öğrenmesi

Email: zaraozcelik1@gmail.com

GitHub: https://github.com/ozgezaraozcelik
