// PNG kare klasörü → H.264 MP4 (macOS AVFoundation; ffmpeg gerekmez). 24 Ekim.
//
// Kullanım (proje klasöründen):
//   swift pilot/mp4_yaz.swift <kare_klasörü> <fps> <çıktı.mp4> [son_kare_bekleme_sn] [anahtar_kare_sn] [renk]
// Örnek:
//   swift pilot/mp4_yaz.swift /tmp/kareler 30 outputs/final_0_cover_video.mp4 12
//   swift pilot/mp4_yaz.swift /tmp/kareler 30 outputs/final_0_cover_clip.mp4 45 10 srgb    (sunumun içindeki klip, 25 Ekim)
// - anahtar_kare_sn (varsayılan 1): anahtar kareler arası en fazla süre. Kurgu için 1 sn; sadece oynatılacak klipte 10 sn
//   (uzun beklemede her anahtar kare yüzlerce KB tutuyor; sunum klipleri en fazla 20 MB olabiliyor).
// - renk (varsayılan 709): aktarım (transfer) etiketi. "srgb" = IEC 61966-2-1 (macOS 15+). 25 Ekim ölçümü (bu Mac, macOS 26):
//   macOS'un renk eşlemesinde (CoreVideo etiketten renk uzayı kurar) zemin #101C27 sRGB etiketle #101C27 kalıyor, çözülen
//   karede #101D27 (sıkıştırma payı); 709 etiketiyle #0E202C'ye kayıyor. Safari videoyu bu katmanla çiziyor; kendisi ayrıca denenmedi.
//
// - Kareler klasördeki .png dosyalarıdır, ada göre sıralanır (kare_00000.png, kare_00001.png, ...). Hepsi aynı boyutta olmalı.
// - Kare i'nin zamanı tam olarak i / fps (CMTime(value: i, timescale: fps)).
// - son_kare_bekleme_sn: son kare bu kadar saniye daha ekranda kalır. Son kare her kare aralığında yeniden eklenir
//   (sabit kare hızı; kurgu programları ve oynatıcılar için en uyumlu; aynı kareler H.264'te çok az yer tutar) ve
//   endSession(atSourceTime:) bitiş anına konur: video tam (kare sayısı / fps + bekleme) saniye sürer.
//   (Denendi, 24 Ekim: son kareyi sadece bitişte bir kez eklemek nominal kare hızını 10,2 fps gösterdi ve iz, edit list'le
//   kırpılan daha uzun bir medya yazdı → kullanılmadı.)
// - Kodlama: H.264 High profil, kalite 0,99, ortalama bit hızı en fazla 14 Mbit/sn, 1 sn'de bir anahtar kare,
//   B-kare yok, BT.709 renk etiketleri (aktarım istenirse sRGB), shouldOptimizeForNetworkUse (moov başta: dosya hemen oynamaya başlar).
//   Dosya geçici klasörde yazılıp yerine taşınır. Yazdıktan sonra profil okunur; High (100) değilse hata verir.
// - Renk: PNG pikselleri sRGB kabul edilir ve DEĞİŞTİRİLMEDEN BGRA tampona çizilir; tampon da çıktıyla aynı etiketlenir
//   (BT.709 ya da sRGB aktarımı), böylece kodlayıcı sadece RGB → YCbCr (BT.709 matrisi) dönüşümü yapar, ton/gama dönüşümü yapmaz.
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO

var geciciKlasor: URL? = nil                                    // hata olursa dur() bunu da siler
func dur(_ mesaj: String) -> Never {
    FileHandle.standardError.write((mesaj + "\n").data(using: .utf8)!)
    if let g = geciciKlasor { try? FileManager.default.removeItem(at: g) }
    exit(1)
}

let a = Array(CommandLine.arguments.dropFirst())
guard a.count >= 3, let fps = Int32(a[1]), fps > 0 else {
    dur("Kullanım: swift pilot/mp4_yaz.swift <kare_klasörü> <fps> <çıktı.mp4> [son_kare_bekleme_sn] [anahtar_kare_sn] [renk: 709|srgb]")
}
let klasor = URL(fileURLWithPath: a[0])
let cikti = URL(fileURLWithPath: a[2])
let bekleme = a.count >= 4 ? (Double(a[3]) ?? -1) : 0
if bekleme < 0 { dur("son_kare_bekleme_sn bir sayı olmalı (0 veya daha büyük)") }
let anahtarSn = a.count >= 5 ? (Double(a[4]) ?? -1) : 1
if anahtarSn <= 0 { dur("anahtar_kare_sn sıfırdan büyük bir sayı olmalı") }
let renk = a.count >= 6 ? a[5].lowercased() : "709"
if renk != "709" && renk != "srgb" { dur("renk 709 ya da srgb olmalı") }
let aktarim = renk == "srgb" ? AVVideoTransferFunction_IEC_sRGB : AVVideoTransferFunction_ITU_R_709_2
let aktarimCV = renk == "srgb" ? kCVImageBufferTransferFunction_sRGB : kCVImageBufferTransferFunction_ITU_R_709_2
if cikti.pathExtension.lowercased() != "mp4" { dur("Çıktı dosyasının uzantısı .mp4 olmalı") }
let ORTALAMA_BIT_HIZI = 14_000_000

// ---------- kareler ----------
let dosyalar: [URL]
do {
    dosyalar = try FileManager.default.contentsOfDirectory(at: klasor, includingPropertiesForKeys: nil)
        .filter { $0.pathExtension.lowercased() == "png" }
        .sorted { $0.lastPathComponent < $1.lastPathComponent }
} catch { dur("Kare klasörü okunamadı: \(klasor.path)") }
if dosyalar.isEmpty { dur("Klasörde PNG yok: \(klasor.path)") }

let sRGB = CGColorSpace(name: CGColorSpace.sRGB)!
func resimOku(_ url: URL) -> CGImage {
    guard let kaynak = CGImageSourceCreateWithURL(url as CFURL, nil),
          let resim = CGImageSourceCreateImageAtIndex(kaynak, 0, nil) else { dur("PNG okunamadı: \(url.path)") }
    // Piksel değerleri sRGB kabul edilir (etiket değiştirilir, değerler değişmez): matplotlib/Pillow PNG'leri etiketsizdir.
    return resim.copy(colorSpace: sRGB) ?? resim
}
let ilk = resimOku(dosyalar[0])
let W = ilk.width, H = ilk.height
if W % 2 != 0 || H % 2 != 0 { dur("Genişlik ve yükseklik çift sayı olmalı (\(W)x\(H))") }

// ---------- yazıcı ----------
// Dosya önce geçici bir klasöre yazılır, bitince yerine taşınır, geçici klasör silinir. Neden: moov'u başa alırken
// (shouldOptimizeForNetworkUse) AVFoundation bir ara dosya kullanıyor; 24 Ekim'de bu ara dosya çıktının yanında
// "<ad>.mp4.sb-…" olarak kaldı (sadece mdat içeriyordu). Ayrıca yazma yarıda kalırsa eski çıktı silinmemiş olur.
let gecici = FileManager.default.temporaryDirectory.appendingPathComponent("mp4_yaz_\(UUID().uuidString)", isDirectory: true)
do { try FileManager.default.createDirectory(at: gecici, withIntermediateDirectories: true) } catch { dur("Geçici klasör açılamadı: \(error)") }
geciciKlasor = gecici
let araCikti = gecici.appendingPathComponent(cikti.lastPathComponent)
let yazici: AVAssetWriter
do { yazici = try AVAssetWriter(outputURL: araCikti, fileType: .mp4) } catch { dur("AVAssetWriter açılamadı: \(error)") }
yazici.shouldOptimizeForNetworkUse = true
let ayarlar: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W,
    AVVideoHeightKey: H,
    AVVideoColorPropertiesKey: [
        AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
        AVVideoTransferFunctionKey: aktarim,
        AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2,
    ],
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: ORTALAMA_BIT_HIZI,
        // Kalite 0,99: sadece bit hızı verilince kodlayıcı ~3 Mbit/sn kullandı ve sabit yazıları her anahtar karede biraz
        // farklı kodladı; yazılar saniyede bir "titredi" (24 Ekim testi: 60 tona kadar). 0,99 ile en fazla 3 ton (görünmez),
        // parlaklık (luma) PSNR ~54 dB. Kalan küçük fark 4:2:0 renk örneklemesinden (her H.264 dosyasında var).
        // 1,0 KULLANMA: kodlayıcı kayıpsız kipe geçip "High 4:4:4 Predictive" profil (244) yazdı; çoğu tarayıcı ve
        // kurgu programı bunu oynatamaz. Aşağıda yazılan dosyanın profili kontrol ediliyor.
        AVVideoQualityKey: 0.99,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC,
        AVVideoMaxKeyFrameIntervalKey: max(1, Int((Double(fps) * anahtarSn).rounded())),   // varsayılan 1 sn: kurguda hızlı atlama
        AVVideoExpectedSourceFrameRateKey: Int(fps),
        // B-kare yok: kod çözme sırası = gösterim sırası. B-karelerle AVAssetWriter bir "edit list" (zaman kaydırma) yazıyor;
        // seyrek beklemede bu kayma 2 sn'ye çıktı (24 Ekim testi). Bazı oynatıcı/kurgu programları edit list'i yok sayar.
        AVVideoAllowFrameReorderingKey: false,
    ] as [String: Any],
]
let giris = AVAssetWriterInput(mediaType: .video, outputSettings: ayarlar)
giris.expectsMediaDataInRealTime = false
let uyarlayici = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: giris, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferWidthKey as String: W,
    kCVPixelBufferHeightKey as String: H,
    kCVPixelBufferCGImageCompatibilityKey as String: true,
    kCVPixelBufferCGBitmapContextCompatibilityKey as String: true,
])
guard yazici.canAdd(giris) else { dur("Video girişi eklenemedi") }
yazici.add(giris)
guard yazici.startWriting() else { dur("Yazma başlamadı: \(String(describing: yazici.error))") }
yazici.startSession(atSourceTime: .zero)

func tampon(_ resim: CGImage) -> CVPixelBuffer {
    guard let havuz = uyarlayici.pixelBufferPool else { dur("Piksel tamponu havuzu yok: \(String(describing: yazici.error))") }
    var pb: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, havuz, &pb)
    guard let b = pb else { dur("Piksel tamponu oluşturulamadı") }
    CVPixelBufferLockBaseAddress(b, [])
    guard let ctx = CGContext(data: CVPixelBufferGetBaseAddress(b), width: W, height: H, bitsPerComponent: 8,
                              bytesPerRow: CVPixelBufferGetBytesPerRow(b), space: sRGB,
                              bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)
    else { dur("Çizim bağlamı oluşturulamadı") }
    ctx.setFillColor(CGColor(srgbRed: 0, green: 0, blue: 0, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    ctx.interpolationQuality = .none
    ctx.draw(resim, in: CGRect(x: 0, y: 0, width: W, height: H))  // aynı boyut, aynı renk uzayı: pikseller aynen kopyalanır
    CVPixelBufferUnlockBaseAddress(b, [])
    // Tampon BT.709 olarak etiketlenir (çıktıyla aynı): kodlayıcı ton/gama dönüşümü yapmaz.
    CVBufferSetAttachment(b, kCVImageBufferColorPrimariesKey, kCVImageBufferColorPrimaries_ITU_R_709_2, .shouldPropagate)
    CVBufferSetAttachment(b, kCVImageBufferTransferFunctionKey, aktarimCV, .shouldPropagate)
    CVBufferSetAttachment(b, kCVImageBufferYCbCrMatrixKey, kCVImageBufferYCbCrMatrix_ITU_R_709_2, .shouldPropagate)
    return b
}

func ekle(_ b: CVPixelBuffer, _ kareNo: Int64) {
    while !giris.isReadyForMoreMediaData {
        if yazici.status == .failed { dur("Kodlama hatası: \(String(describing: yazici.error))") }
        Thread.sleep(forTimeInterval: 0.002)
    }
    if !uyarlayici.append(b, withPresentationTime: CMTime(value: kareNo, timescale: fps)) {
        dur("Kare \(kareNo) eklenemedi: \(String(describing: yazici.error))")
    }
}

let n = dosyalar.count
var son: CVPixelBuffer? = nil
for (i, url) in dosyalar.enumerated() {
    autoreleasepool {
        let resim = i == 0 ? ilk : resimOku(url)
        if resim.width != W || resim.height != H { dur("Boyut farklı: \(url.lastPathComponent) \(resim.width)x\(resim.height)") }
        let b = tampon(resim)
        ekle(b, Int64(i))
        if i == n - 1 { son = b }
    }
}
let bekleKare = Int64((bekleme * Double(fps)).rounded())
if bekleKare > 0, let s = son {
    for j in 0..<bekleKare { ekle(s, Int64(n) + j) }            // sabit kare hızı: son kare her aralıkta tekrar
}
let bitis = CMTime(value: Int64(n) + bekleKare, timescale: fps)
giris.markAsFinished()
yazici.endSession(atSourceTime: bitis)
let isaret = DispatchSemaphore(value: 0)
yazici.finishWriting { isaret.signal() }
isaret.wait()
guard yazici.status == .completed else { dur("Yazma tamamlanmadı: \(String(describing: yazici.error))") }
do {                                                            // bitmiş dosyayı yerine taşı (varsa eskisinin yerine)
    if FileManager.default.fileExists(atPath: cikti.path) { try FileManager.default.removeItem(at: cikti) }
    try FileManager.default.moveItem(at: araCikti, to: cikti)
} catch { dur("Çıktı yerine taşınamadı: \(error)") }
try? FileManager.default.removeItem(at: gecici)                 // geçici klasör (ara dosyalarla birlikte)
let boyut = ((try? FileManager.default.attributesOfItem(atPath: cikti.path)[.size]) as? NSNumber)?.doubleValue ?? 0

// profil kontrolü: dosyanın başındaki avcC kutusu (moov başta) → AVCProfileIndication, AVCLevelIndication
var profil = -1, seviye = -1
if let fh = try? FileHandle(forReadingFrom: cikti), let bas = try? fh.read(upToCount: 1 << 20),
   let r = bas.range(of: Data("avcC".utf8)), r.upperBound + 3 < bas.count {
    profil = Int(bas[r.upperBound + 1]); seviye = Int(bas[r.upperBound + 3])
}
print(String(format: "Yazıldı: %@ · %d kare + %lld bekleme karesi · %.3f sn · %d fps · %dx%d · %.2f MB · H.264 profil %d seviye %.1f · anahtar kare %g sn · renk %@",
             cikti.lastPathComponent, n, bekleKare, bitis.seconds, fps, W, H, boyut / 1e6, profil, Double(seviye) / 10, anahtarSn, renk))
if profil != 100 { dur("UYARI: profil High (100) değil (\(profil)); bu dosya bazı oynatıcılarda açılmayabilir") }
