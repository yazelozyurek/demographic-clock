// MP4 kontrolü (24 Ekim): süre, kare hızı, boyut, kodek/profil, renk etiketleri, kare sayısı ve kare süreleri;
// istenen anlardan tam o kareyi PNG olarak çıkarır (AVAssetImageGenerator, tolerans sıfır).
//
// Kullanım (proje klasöründen):
//   swift pilot/mp4_kontrol.swift <video.mp4> <kare_klasörü> [saniye ...]     ("son" = son kare)
// Örnek:
//   swift pilot/mp4_kontrol.swift outputs/final_0_cover_video.mp4 /tmp/kontrol 0.2 3 5 7.5 son
//
// Her an için iki dosya yazılır:
//   kare_<sn>.png       : çözülen piksel değerleri, renk dönüşümü YOK (kaynak PNG'yle sayıca karşılaştırmak için)
//   kare_<sn>_srgb.png  : macOS'un renk yönetimiyle sRGB'ye çevrilmiş hali (Apple uygulamalarındaki görünüşe yakın)
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func dur(_ mesaj: String) -> Never {
    FileHandle.standardError.write((mesaj + "\n").data(using: .utf8)!)
    exit(1)
}
let a = Array(CommandLine.arguments.dropFirst())
guard a.count >= 2 else { dur("Kullanım: swift pilot/mp4_kontrol.swift <video.mp4> <kare_klasörü> [saniye ...]") }
let video = URL(fileURLWithPath: a[0])
let klasor = URL(fileURLWithPath: a[1])
let anlar = a.count > 2 ? Array(a[2...]) : ["0.2", "3", "5", "7.5", "son"]
try FileManager.default.createDirectory(at: klasor, withIntermediateDirectories: true)

let varlik = AVURLAsset(url: video)
let sure = try await varlik.load(.duration)
guard let iz = try await varlik.loadTracks(withMediaType: .video).first else { dur("Video izi yok") }
let (kareHizi, boyut, bicimler, enKisa) = try await iz.load(.nominalFrameRate, .naturalSize, .formatDescriptions, .minFrameDuration)
print(String(format: "süre %.4f sn · nominal kare hızı %.3f fps · iz boyutu %.0fx%.0f · en kısa kare %.4f sn",
             sure.seconds, kareHizi, boyut.width, boyut.height, enKisa.seconds))
for fd in bicimler {
    let kodek = CMFormatDescriptionGetMediaSubType(fd)
    let dort = String(bytes: [24, 16, 8, 0].map { UInt8((kodek >> $0) & 0xFF) }, encoding: .ascii) ?? "?"
    let uz = CMFormatDescriptionGetExtensions(fd) as? [String: Any] ?? [:]
    var profil = "?"
    if let atomlar = uz[kCMFormatDescriptionExtension_SampleDescriptionExtensionAtoms as String] as? [String: Any],
       let avcC = atomlar["avcC"] as? Data, avcC.count > 3 {
        let p = Int(avcC[1]), l = Int(avcC[3])
        profil = "\([66: "Baseline", 77: "Main", 100: "High"][p] ?? "profile \(p)") level \(Double(l) / 10)"
    }
    let primer = uz[kCMFormatDescriptionExtension_ColorPrimaries as String] ?? "-"
    let aktarim = uz[kCMFormatDescriptionExtension_TransferFunction as String] ?? "-"
    let matris = uz[kCMFormatDescriptionExtension_YCbCrMatrix as String] ?? "-"
    let tamAralik = uz[kCMFormatDescriptionExtension_FullRangeVideo as String] ?? "-"
    print("kodek \(dort) · \(profil) · renk: primerler \(primer), aktarım \(aktarim), matris \(matris), tam aralık \(tamAralik)")
}

// kare sayısı ve kare süreleri (sıkıştırılmış örnekler, sunum zamanına göre sıralı)
let okuyucu = try AVAssetReader(asset: varlik)
let cikis = AVAssetReaderTrackOutput(track: iz, outputSettings: nil)
okuyucu.add(cikis)
okuyucu.startReading()
var zamanlar: [Double] = []
var anahtar = 0
while let sb = cikis.copyNextSampleBuffer() {
    if CMSampleBufferGetNumSamples(sb) == 0 { continue }
    zamanlar.append(CMSampleBufferGetPresentationTimeStamp(sb).seconds)
    let ekler = CMSampleBufferGetSampleAttachmentsArray(sb, createIfNecessary: false) as? [[CFString: Any]]
    if !(ekler?.first?[kCMSampleAttachmentKey_NotSync] as? Bool ?? false) { anahtar += 1 }
}
zamanlar.sort()
var sureler: [Double] = []
for i in 0..<zamanlar.count { sureler.append((i + 1 < zamanlar.count ? zamanlar[i + 1] : sure.seconds) - zamanlar[i]) }
var dagilim: [String: Int] = [:]
for s in sureler { dagilim[String(format: "%.4f", s), default: 0] += 1 }
print("kare sayısı \(zamanlar.count) · anahtar kare \(anahtar) · ilk kare zamanı \(String(format: "%.4f", zamanlar.first ?? -1)) sn · "
      + "kare süreleri (sn: adet) " + dagilim.sorted { $0.key < $1.key }.map { "\($0.key): \($0.value)" }.joined(separator: ", "))

// istenen anlardaki kareler
let uretici = AVAssetImageGenerator(asset: varlik)
uretici.requestedTimeToleranceBefore = .zero
uretici.requestedTimeToleranceAfter = .zero
uretici.appliesPreferredTrackTransform = true
let sRGB = CGColorSpace(name: CGColorSpace.sRGB)!
func pngYaz(_ resim: CGImage, _ url: URL) {
    guard let hedef = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil) else { dur("PNG yazılamadı") }
    CGImageDestinationAddImage(hedef, resim, nil)
    if !CGImageDestinationFinalize(hedef) { dur("PNG yazılamadı: \(url.path)") }
}
let yarimKare = kareHizi > 0 ? 0.5 / Double(kareHizi) : 0.01
for an in anlar {
    let t = an == "son" ? sure.seconds - yarimKare : (Double(an) ?? 0)
    let (resim, gercek) = try await uretici.image(at: CMTime(seconds: t, preferredTimescale: 60000))
    let ad = an == "son" ? "son" : String(format: "%06.2f", t)
    pngYaz(resim, klasor.appendingPathComponent("kare_\(ad).png"))
    // macOS renk yönetimiyle sRGB'ye çevrilmiş kopya
    let ctx = CGContext(data: nil, width: resim.width, height: resim.height, bitsPerComponent: 8, bytesPerRow: 0, space: sRGB,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.draw(resim, in: CGRect(x: 0, y: 0, width: resim.width, height: resim.height))
    pngYaz(ctx.makeImage()!, klasor.appendingPathComponent("kare_\(ad)_srgb.png"))
    print(String(format: "kare %@: istenen %.4f sn → gelen %.4f sn · %dx%d · renk uzayı %@", ad, t, gercek.seconds,
                 resim.width, resim.height, (resim.colorSpace?.name as String?) ?? "yok"))
}
