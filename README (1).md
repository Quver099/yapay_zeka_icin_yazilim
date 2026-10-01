**GitHub:** https://github.com/Quver099/yapay_zeka_icin_yazilim/  
**Web sürümü:** https://quver099.github.io/yapay_zeka_icin_yazilim/

# Karar Deposu: Oylamalı Karar Forumu

**Amaç.** Forum bir sohbet yeri değil, karar alma mekanizması. Her konu bir depo gibi tutulur; konunun altındaki metin o konudaki güncel karardır. Metni değiştirmek, konuyu gizlemek veya kapatmak için öneri açılır ve oylanır. Her değişiklik oylamayla yapılır, hiçbir kayıt silinmez, yalnızca gizlenir.

## Yaptıklarımız

- **Kullanıcı ve konular:** Kayıtta ad, soyad, doğum tarihi, adres, takma ad ve şifre alınır (şifre özetlenerek saklanır). Konu açılır, düzenleme/silme/kapatma önerilir, alt konu açılır, yorum yazılır. Yeni konu 2 destekçi bulana kadar taslaktır.
- **Oy hakkı ilgiye bağlı:** Oylamaya yalnızca konunun alanıyla ilgilenenler katılır. Etki alanı büyüdükçe (sınıf, üniversite, herkes) yeter sayı artar (%30, %50, %60). Örneğin üniversiteye uçak indirmek sınıfı değil tüm üniversiteyi ilgilendirir.
- **Delegasyon grafı:** Herkes oyunu alan bazında bilgili birine ya da yapay zekâya devredebilir ve istediği an geri alabilir. Bir kişi en fazla 10 devir toplar. Devirler grafta görünür.
- **Gerçek yapay zekâ (Claude):** Python (FastAPI) sunucusu üzerinden iki iş yapar: önerilere gerekçeli oy verir (gerekçe azınlık raporuna yazılır) ve yeni içeriğin yönetmeliğe uygun olup olmadığını denetler. Sunucu kapalıysa kural tabanlı yedek devreye girer.
- **Dağıtık defter:** Her olay hash zinciriyle deftere yazılır, zincir doğrulanabilir.
- **Değişmez kurallar ve yönetmelik:** Oy hakkını kaldıran, defteri silen veya kimlik ifşa eden öneriler reddedilir. Temel haklara dokunan öneriler 2/3 çoğunluk ister.

## Sorulara cevabımız

**1. Çoğunluk azınlığı nasıl tüketemez?** Üç katman: (a) anayasal konularda 2/3 eşiği, (b) *karesel oylama*: herkese haftada 100 karar puanı verilir, n oy vermek n²−1 puan tutar; tutkulu bir azınlık puanını tek konuda toplayıp ilgisiz çoğunluğa karşı ağırlık kazanabilir, yeter sayı ise şiddetten etkilenmez, (c) her kararla birlikte kaybeden tarafın gerekçelerini içeren azınlık raporu saklanır ve karar 90 gün sonra yeniden oylanır.

**2. Kalabalık nasıl çözülür?** Kullanıcı yalnızca ilgi alanındaki konularda oy kullanır, benzer başlık uyarısı çift konuyu engeller, 2 destekçi şartı gürültüyü eler, konular alt konulara bölünür ve oy devri sayesinde herkes her konuda oy vermek zorunda kalmaz.

## Teknoloji

Tek dosyalı web arayüzü (HTML/JS), Python FastAPI sunucusu (`backend/server.py`), Claude API, Android uygulaması (Kotlin, WebView; `app/`), GitHub Pages.

## Neler yaşadık, nasıl çözdük

- **Sahte yapay zekâ:** İlk kodda Claude'un oyu basit bir `if-else`ti. Gerçek model için bir sunucu yazdık; API anahtarı tarayıcıya konamayacağı için ortam değişkeninde tutuldu.
- **Regex yerine denetim:** Yönetmelik kontrolü yalnızca regex'le yapılıyordu. Yapay zekâ denetimini ekledik, regex'i ucuz ön filtre ve sunucu çökerse yedek olarak bıraktık.
- **Android kurulumu:** Doğru şablonu (Empty Views Activity), `assets` klasörünü, internet iznini ve `usesCleartextTraffic` ayarını öğrendik. Emülatörde sunucuya `localhost` değil `10.0.2.2` ile ulaşılıyor. Emülatör ilk denemede "5 dakika içinde bağlanamadı" hatası verdi; Device Manager'daki üç nokta menüsünden **Cold Boot Now** seçeneğiyle sıfırdan başlatınca sorun çözüldü.
- **GitHub:** Commit uyarılarını (8 uyarı) aştık, projeyi push ettik, Pages'i `master` / `root` olarak ayarlayıp web sürümünü yayınladık.

## Sınırlamalar

- Veriler `localStorage`'da tutulduğu için her cihaz kendi forumunu görür. Ortak forum için verinin sunucuya taşınması gerekir.
- Yayındaki web sitesinde sunucu olmadığı için yapay zekâ yedek modda çalışır.
- Karesel oylama sahte hesaplara açıktır. Kayıtta kimlik bilgisi istememiz bunu kısmen azaltır ama çözmez.
- Şifre özetleme demo düzeyindedir, gerçek güvenlik için sunucu tarafı doğrulama gerekir.
- Planlanan: tartışmayı yapay zekâyla özetleme butonu, ortak veri tabanı, iOS uygulaması.
