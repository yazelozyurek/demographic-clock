// Ekran kaydını videoya hazırlar (28 Ekim): siyah bantları ve sunumun alttaki kontrol çubuğunu ("< 1/6 >") kesip
// 1920x1080, 30 kare/sn, H.264 MP4 yapar. Ses aynen kalır.
//
// Kullanım (proje klasöründen):
//   swift pilot/kayit_kes.swift <kayit.mov> <cikti.mp4> [x y genislik yukseklik]
// Varsayılan kesim 2880x1800 ekran kaydı içindir (MacBook, "1440x900 gibi görünür" ayarı, Safari Present modu):
//   slayt 90..1709. satırlarda (2880x1620); kontrol çubuğu 1675. satırdan başlıyor, dipnot yazısı 1625'te bitiyor.
//   Kesim: x 31, y 90, 2818x1585 (16:9) → altta sadece boş kenar, yanlarda 31'er piksel boş kenar gider.
// Ölçüler 28 Ekim'deki iki deneme kaydından (Masaüstü/Ekran Kaydı 2026-10-28 21.38.45 ve 21.42.09) alındı.
import AVFoundation
import Foundation

let a = CommandLine.arguments
guard a.count == 3 || a.count == 7 else {
    print("kullanım: swift pilot/kayit_kes.swift <kayit.mov> <cikti.mp4> [x y genislik yukseklik]"); exit(1)
}
let girdi = URL(fileURLWithPath: a[1]), cikti = URL(fileURLWithPath: a[2])
let ozel = a.count == 7
let (x, y, gw, gh) = ozel ? (Double(a[3])!, Double(a[4])!, Double(a[5])!, Double(a[6])!) : (31.0, 90.0, 2818.0, 1585.0)
let asset = AVURLAsset(url: girdi)
let bitti = DispatchSemaphore(value: 0)

Task {
    do {
        guard let iz = try await asset.loadTracks(withMediaType: .video).first else { print("görüntü izi yok"); exit(1) }
        let boyut = try await iz.load(.naturalSize)
        if !ozel && (boyut.width != 2880 || boyut.height != 1800) {
            print("kayıt \(Int(boyut.width))x\(Int(boyut.height)); varsayılan kesim 2880x1800 için. Kesimi elle verin."); exit(1)
        }
        let sure = try await asset.load(.duration)
        let sesVar = !(try await asset.loadTracks(withMediaType: .audio)).isEmpty
        let olcek = 1920.0 / gw
        let katman = AVMutableVideoCompositionLayerInstruction(assetTrack: iz)
        katman.setTransform(CGAffineTransform(translationX: -x, y: -y).concatenating(CGAffineTransform(scaleX: olcek, y: olcek)), at: .zero)
        let talimat = AVMutableVideoCompositionInstruction()
        talimat.timeRange = CMTimeRange(start: .zero, duration: sure)
        talimat.layerInstructions = [katman]
        let kompozisyon = AVMutableVideoComposition()
        kompozisyon.renderSize = CGSize(width: 1920, height: 1080)
        kompozisyon.frameDuration = CMTime(value: 1, timescale: 30)
        kompozisyon.instructions = [talimat]
        guard let disari = AVAssetExportSession(asset: asset, presetName: AVAssetExportPresetHighestQuality) else { print("dışa aktarma açılamadı"); exit(1) }
        disari.videoComposition = kompozisyon
        try? FileManager.default.removeItem(at: cikti)
        try await disari.export(to: cikti, as: .mp4)
        let mb = Double((try FileManager.default.attributesOfItem(atPath: cikti.path)[.size] as? Int) ?? 0) / 1e6
        print(String(format: "yazıldı: %@ · %.1f sn · 1920x1080 · %.1f MB · ses %@", cikti.lastPathComponent, sure.seconds, mb, sesVar ? "var" : "YOK"))
        if sure.seconds > 300 { print(String(format: "UYARI: süre %.1f sn, 5 dakikayı (300 sn) geçiyor", sure.seconds)) }
    } catch { print("hata:", error); exit(1) }
    bitti.signal()
}
bitti.wait()
