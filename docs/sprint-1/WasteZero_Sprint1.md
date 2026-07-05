# WasteZero AI — Sprint 1 Çıktıları

**Takım:** The Parsimonia
**Proje:** WasteZero AI — Restoranlar İçin Akıllı Menü, Talep ve İsraf Karar Destek Sistemi
**Sprint No:** 1 / 3
**Sprint Süresi:** 2 hafta
**Sprint Hedefi:** Agent bazlı sisteme uygun gerçek veri setlerini bulmak ve keşifsel veri analizine (EDA) başlamak. EDA sürecinin kalan kısmı Sprint 2'de tamamlanacaktır.

## Takım ve Roller

| Üye | Scrum Rolü | Sprint 1'deki Odak |
|---|---|---|
| Beyza ATA | Product Owner | Backlog yönetimi, veri kaynağı gereksinimleri, veri seti araştırma, veri hazırlama |
| Pelin ATAMAN | Scrum Master | İletişim, Scrum event yönetimi, veri seti araştırma, veri temizleme |
| Furkan BİTİK | Developer | Veri seti araştırma, keşifsel veri analizi (EDA) |

---

## 1. Backlog Dağıtma Mantığı

İlk sprintin hedefi bilinçli olarak dar tutuldu: sisteme uygun gerçek veri setlerini bulmak ve EDA'ya başlamak. Modelleme, agent eğitimi, dashboard ve karar katmanı gibi bileşenler sonraki sprintlere bırakıldı; çünkü sağlam bir veri temeli ve keşifsel analiz olmadan bunların anlamlı kurulması mümkün değildir.

Görevler üç ilkeye göre dağıtıldı:

- **Bağımlılık sırası:** EDA veriye bağımlı olduğu için önce veri araştırma ve temizleme görevleri planlandı; EDA görevi bu çıktının üzerine kuruldu.
- **Yetkinlik ve ilgi alanı:** Görevler, üyelerin güçlü olduğu veya geliştirmek istediği alana göre dağıtıldı.
- **İş yükü dengesi:** Üç kişilik takımda herkesin dengeli bir yük almasına dikkat edildi; Product Owner ve Scrum Master da aktif olarak geliştirmeye katıldı.

| ID | İş (User Story) | Atanan | Öncelik |
|---|---|---|---|
| US-01 | Agent bazlı sistem için uygun gerçek veri setlerinin araştırılması (talep, fire/israf, kâr/fiyat) | Beyza, Pelin, Furkan | Yüksek |
| US-02 | Seçilen veri setlerinin temizlenmesi ve ön işlenmesi (eksik değer, tip dönüşümü, tarih alanları) | Pelin, Beyza, Furkan  | Yüksek |
| US-03 | GitHub repo yapısı, klasör düzeni, README ve veri dokümantasyonu | Pelin | Orta |
| US-04 | Keşifsel veri analizinin başlatılması (temel keşif ve ilk görselleştirmeler) | Furkan | Orta |

---

## 2. Daily Scrum Notları

Ekip üyelerinin eğitim ve iş sorumlulukları nedeniyle Daily Scrum, sprint boyunca haftada bir gün, akşam saatlerinde online yapıldı (2 haftalık sprintte toplam 2 toplantı). Her üye üç soruyu yanıtladı: Geçen haftadan bu yana ne yaptım? Önümüzdeki hafta ne yapacağım? Önümde engel var mı?

### 1. Hafta — Akşam Toplantısı
- **Beyza ATA:** Bu hafta: Backlog'u oluşturdum, veri kaynağı gereksinimlerini netleştirdim ve repo yapısını kurmaya başladım. Bu hafta: Uygun veri setlerinin araştırmasına katıldım. Gelecek hafta: README ve veri dokümantasyonunu tamamlayacağım. Engel: Yok.
- **Pelin ATAMAN:** Bu hafta: Toplantı düzenini ve iletişim kanallarını kurdum; veri seti araştırmasına katıldım. Gelecek hafta: Seçilen veri setlerini temizlemeye başlayacağım. Engel: Veri setleri kesinleşmeli.
- **Furkan BİTİK:** Bu hafta: Talep, fire ve kâr için uygun gerçek veri setlerini araştırdım. Gelecek hafta: Temizlenen veri üzerinde EDA'ya başlayacağım. Engel: Temiz veriyi bekliyorum.

### 2. Hafta — Akşam Toplantısı
- **Beyza ATA:** Bu hafta: README ve veri dokümantasyonunu (kaynak, değişkenler, kullanım) tamamladım. Gelecek hafta: Sprint Review dokümanını derleyeceğim. Engel: Yok.
- **Pelin ATAMAN:** Bu hafta: Seçilen veri setlerini temizledim; eksik değerler ve tarih alanları işlendi. Gelecek hafta: Review ve Retrospective'i yöneteceğim. Engel: Yok.
- **Furkan BİTİK:** Bu hafta: Temizlenen veri üzerinde EDA'ya başladım; ilk keşif ve temel görselleştirmeler çıkarıldı. Gelecek hafta: EDA'yı Sprint 2'de derinleştireceğim. Engel: Yok.

---

## 3. Sprint Board Updates

Görevler To Do → In Progress → Done sütunlarında takip edildi. Aşağıda sprint başı, ortası ve sonu durumu gösterilmiştir. Kullanılan panonun başlangıç ve bitiş ekran görüntüleri repoda `docs/sprint-1/screenshots/` klasöründe yer almaktadır.

**Sprint Başı (1. Hafta):**

| To Do | In Progress | Done |
|---|---|---|
| US-01, US-02, US-03, US-04 | — | — |

**Sprint Ortası (1.–2. Hafta geçişi):**

| To Do | In Progress | Done |
|---|---|---|
| US-04 | US-02, US-03 | US-01 |

**Sprint Sonu (2. Hafta):**

| To Do | In Progress | Done |
|---|---|---|
| — | US-04 (devam ediyor) | US-01, US-02, US-03 |

**Board hareket özeti:** Veri araştırma (US-01), temizleme (US-02) ve dokümantasyon (US-03) görevleri tamamlandı. EDA (US-04) planlandığı gibi bu sprintte başlatıldı ve Sprint 2'de tamamlanmak üzere devam etmektedir.

---

## 4. Ürün Durumu

Sprint 1 sonunda WasteZero AI'nın veri temeli hazır ve keşifsel analiz başlatıldı. Şu an repoda bulunan çıktılar:

- **Seçilmiş gerçek veri setleri:** Agent bazlı sisteme uygun, talep, fire/israf ve kâr/fiyat konularını kapsayan gerçek veri setleri araştırıldı ve seçildi.
- **Temizlenmiş veri:** Seçilen setler temizlenip ön işlendi; eksik değerler, tip dönüşümleri ve tarih alanları düzenlendi.
- **Veri dokümantasyonu:** Verilerin kaynağı ve değişken açıklamaları belgelendi.
- **Repo altyapısı:** Public GitHub reposu, klasör yapısı, README ve gerekli dokümanlar kuruldu.
- **Keşifsel veri analizi (başlangıç):** Temel keşif ve ilk görselleştirmeler üretildi. Analizin kalan kısmı Sprint 2'de sürdürülecektir.

**Henüz yapılmadı (sonraki sprintlere):** EDA'nın tamamlanması, agent'ların kendi verileriyle eğitilmesi, agent'lar arası orkestrasyon, karar katmanı ve arayüz. Bunlar Sprint 2 ve 3 kapsamındadır.

**Genel durum:** Veri temeli kuruldu ve keşifsel analiz başladı. Bir sonraki sprintte EDA tamamlanıp agent geliştirmeye geçilmeye hazır.

---

## 5. Sprint Review

Sprint Review, tamamlanan işlere ve çalışan çıktılara odaklandı.

**Sprint hedefi neydi?** Agent bazlı sisteme uygun gerçek veri setlerini bulmak ve EDA'ya başlamak.

**Ne kadarına ulaşıldı?** Veri araştırma, temizleme ve dokümantasyon tamamlandı. EDA planlandığı gibi başlatıldı ve kalan kısmı Sprint 2'ye devredildi. Sprint hedefi karşılandı.

**Tamamlanan işler:**
- Uygun gerçek veri setleri araştırıldı ve seçildi (US-01)
- Veri setleri temizlendi ve ön işlendi (US-02)
- Repo, README ve veri dokümantasyonu kuruldu (US-03)
- EDA başlatıldı; temel keşif ve ilk görselleştirmeler üretildi (US-04)

**Devam eden işler:** EDA'nın derinleştirilmesi ve tamamlanması Sprint 2'ye planlandı.

**Demo:** Seçilen veri setleri, temizlik adımları ve ilk keşifsel analiz grafikleri gösterildi.

**Sonraki sprint'e taşınanlar:** EDA'nın tamamlanması ve ardından agent'ların kendi verileriyle eğitilmesine geçilmesi Sprint 2'nin hedefi olarak belirlendi.

---

## 6. Sprint Retrospective

Retrospective, takımın çalışma şekline odaklandı.

**Neler iyi gitti?**
- Sprint kapsamını dar ve gerçekçi tutmak (veri bulma + EDA başlangıcı) doğru karardı; hedefe ulaşıldı.
- Haftalık akşam Daily Scrum'ları, üyelerin yoğunluğuna uygundu ve düzenli yapıldı.
- Üç üyenin de veri araştırmasına katılması, uygun veri setlerinin hızlı seçilmesini sağladı.
- Veri görevlerini öne almak, EDA'nın beklemeden başlamasını sağladı.

**Neler zorladı?**
- İki kişi eksik başlanıldığı için zamansal olarak geri kaldık.
- Haftada tek toplantı olduğu için hafta içi çıkan küçük soruların çözümü zaman zaman yavaş kaldı.
- Farklı kaynaklardan gelen veri setlerini ortak bir yapıya oturtmak beklenenden fazla tartışma gerektirdi.

**Sonraki sprint'te neyi farklı yapacağız?**
- Aktif üye sayısına göre Backlog dağıtımı sürekli güncellenecek.
- Haftalık toplantıya ek olarak, hafta içi engeller için kısa yazılı güncelleme akışı kurulacak.
- Veri setlerinin ortak yapısı (kategori eşlemesi) Sprint 2'nin başında netleştirilecek.

---

*The Parsimonia — WasteZero AI — Sprint 1 Çıktıları · Yapay Zekâ ve Teknoloji Akademisi Bootcamp 2026*
