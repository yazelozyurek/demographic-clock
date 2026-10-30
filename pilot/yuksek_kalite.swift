// Yüksek kaliteli son kodlama (30 Ekim): kurgu_video.swift'in yazdığı ProRes .mov ara dosyasını H.264 MP4'e çevirir.
// AVAssetExportSession'ın "en yüksek kalite" ayarı 2560x1440'ta ~5 Mbit/sn veriyordu; koyu zeminde bloklanma ve yazılarda
// yumuşama oluyordu. Burada bit hızı elle verilir (varsayılan 20 Mbit/sn), H.264 High, 2 sn'de bir anahtar kare,
// ses AAC 256 kbit/sn. ffmpeg gerekmez.
// Renk etiketi (30 Ekim, kullanıcı: "Safari'de daha canlı, videoda soluk"): BT.709 aktarım etiketiyle QuickTime/macOS koyu tonları
// açıyor (kart #15222E → ekranda ~#1A2D3B), görüntü soluk duruyordu. Varsayılan artık sRGB aktarım etiketi: piksel değerleri
// olduğu gibi gösterilir (mp4_yaz.swift'teki "srgb" seçeneğiyle aynı ölçüm). Renk değerleri değişmez, sadece etiket: kareler
// kodlayıcıya verilmeden önce sRGB diye yeniden etiketlenir; yoksa kodlayıcı 709 → sRGB dönüşümü yapıp değerleri açıyordu (ölçüldü).
//
// Kullanım (proje klasöründen):
//   swift pilot/yuksek_kalite.swift <ara.mov> <cikti.mp4> [Mbit/sn] [srgb|709]
import AVFoundation
import Foundation

let a = CommandLine.arguments
guard (3...5).contains(a.count) else { print("kullanım: swift pilot/yuksek_kalite.swift <ara.mov> <cikti.mp4> [Mbit/sn] [srgb|709]"); exit(1) }
let girdi = URL(fileURLWithPath: a[1]), cikti = URL(fileURLWithPath: a[2])
let mbps = a.count >= 4 ? Double(a[3])! : 20
let srgb = a.count == 5 ? a[4] != "709" : true
let bitti = DispatchSemaphore(value: 0)

Task {
    do {
        let varlik = AVURLAsset(url: girdi)
        guard let vIz = try await varlik.loadTracks(withMediaType: .video).first else { print("görüntü yok"); exit(1) }
        let sIz = try await varlik.loadTracks(withMediaType: .audio).first
        let boyut = try await vIz.load(.naturalSize), sure = try await varlik.load(.duration)
        let okuyucu = try AVAssetReader(asset: varlik)
        let vOku = AVAssetReaderTrackOutput(track: vIz, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA])
        okuyucu.add(vOku)
        var sOku: AVAssetReaderTrackOutput? = nil
        if let sIz {
            let o = AVAssetReaderTrackOutput(track: sIz, outputSettings: [AVFormatIDKey: kAudioFormatLinearPCM])
            okuyucu.add(o)
            sOku = o
        }
        try? FileManager.default.removeItem(at: cikti)
        let yazici = try AVAssetWriter(outputURL: cikti, fileType: .mp4)
        yazici.shouldOptimizeForNetworkUse = true
        let renk: [String: Any] = [AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
                                   AVVideoTransferFunctionKey: srgb ? AVVideoTransferFunction_IEC_sRGB : AVVideoTransferFunction_ITU_R_709_2,
                                   AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2]
        let vYaz = AVAssetWriterInput(mediaType: .video, outputSettings: [
            AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: boyut.width, AVVideoHeightKey: boyut.height,
            AVVideoColorPropertiesKey: renk,
            AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: Int(mbps * 1_000_000),
                                              AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
                                              AVVideoMaxKeyFrameIntervalKey: 60, AVVideoExpectedSourceFrameRateKey: 30,
                                              AVVideoAllowFrameReorderingKey: true, AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC]])
        vYaz.expectsMediaDataInRealTime = false
        yazici.add(vYaz)
        let uyarlayici = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vYaz, sourcePixelBufferAttributes: nil)
        var sYaz: AVAssetWriterInput? = nil
        if sOku != nil {
            let i = AVAssetWriterInput(mediaType: .audio, outputSettings: [AVFormatIDKey: kAudioFormatMPEG4AAC, AVSampleRateKey: 48000,
                                                                           AVNumberOfChannelsKey: 2, AVEncoderBitRateKey: 256_000])
            i.expectsMediaDataInRealTime = false
            yazici.add(i)
            sYaz = i
        }
        guard okuyucu.startReading(), yazici.startWriting() else { print("başlatılamadı:", okuyucu.error ?? yazici.error ?? "?"); exit(1) }
        yazici.startSession(atSourceTime: .zero)
        let grup = DispatchGroup()
        func aktar(_ giris: AVAssetWriterInput, _ cikis: AVAssetReaderTrackOutput, _ ad: String) {
            grup.enter()
            giris.requestMediaDataWhenReady(on: DispatchQueue(label: ad)) {
                while giris.isReadyForMoreMediaData {
                    if let ornek = cikis.copyNextSampleBuffer() { giris.append(ornek) }
                    else { giris.markAsFinished(); grup.leave(); return }
                }
            }
        }
        // görüntü: kareler yeniden etiketlenip (değer değişmeden) uyarlayıcıyla yazılır
        grup.enter()
        vYaz.requestMediaDataWhenReady(on: DispatchQueue(label: "goruntu")) {
            while vYaz.isReadyForMoreMediaData {
                guard let ornek = vOku.copyNextSampleBuffer() else { vYaz.markAsFinished(); grup.leave(); return }
                guard let kare = CMSampleBufferGetImageBuffer(ornek) else { continue }
                CVBufferSetAttachment(kare, kCVImageBufferColorPrimariesKey, kCVImageBufferColorPrimaries_ITU_R_709_2, .shouldPropagate)
                CVBufferSetAttachment(kare, kCVImageBufferYCbCrMatrixKey, kCVImageBufferYCbCrMatrix_ITU_R_709_2, .shouldPropagate)
                CVBufferSetAttachment(kare, kCVImageBufferTransferFunctionKey,
                                      srgb ? kCVImageBufferTransferFunction_sRGB : kCVImageBufferTransferFunction_ITU_R_709_2, .shouldPropagate)
                CVBufferRemoveAttachment(kare, kCVImageBufferGammaLevelKey)
                CVBufferRemoveAttachment(kare, kCVImageBufferICCProfileKey)
                if !uyarlayici.append(kare, withPresentationTime: CMSampleBufferGetPresentationTimeStamp(ornek)) {
                    print("kare yazılamadı:", yazici.error ?? "?"); exit(1)
                }
            }
        }
        if let sYaz, let sOku { aktar(sYaz, sOku, "ses") }
        grup.wait()
        await yazici.finishWriting()
        guard yazici.status == .completed else { print("yazılamadı:", yazici.error ?? "?"); exit(1) }
        let mb = Double((try FileManager.default.attributesOfItem(atPath: cikti.path)[.size] as? Int) ?? 0) / 1e6
        print(String(format: "yazıldı: %@ · %.1f sn · %.0fx%.0f · %.0f MB (ortalama %.1f Mbit/sn)", cikti.lastPathComponent, sure.seconds,
                     boyut.width, boyut.height, mb, mb * 8 / sure.seconds))
    } catch { print("hata:", error); exit(1) }
    bitti.signal()
}
bitti.wait()
