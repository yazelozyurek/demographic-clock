// Video kurgusunun görüntü kısmı (29 Ekim): kurgu planındaki bölümleri ekran kayıtlarından sırayla alır, kayit_kes.swift'teki
// gibi siyah bantları ve sunum çubuğunu kesip 1920x1080'e ölçekler, kurgu_ses.py'nin yazdığı sesi koyar, H.264 MP4 yazar.
//
// Kullanım (proje klasöründen):
//   python pilot/kurgu_ses.py sunum/video/kurgu_plani_30ekim.json <ses.wav>
//   swift pilot/kurgu_video.swift sunum/video/kurgu_plani_30ekim.json <ses.wav> <cikti.mp4>
// Bir bölümde video_bas > bas ise aradaki süre video_bas'taki kare dondurularak, video_son < son ise son kare dondurularak doldurulur
// (ses ile görüntü süresi her bölümde aynı kalır).
// İsteğe bağlı 4. argüman (30 Ekim): gösterge listesi (JSON: bas, son, x, y, w, h; çıktı videosunun saniyeleri ve 1920x1080 pikseli,
// sol üst köşe başlangıç). Her gösterge o aralıkta kartın çevresinde sarı, hafif parlayan bir çerçeve olarak belirip kaybolur.
import AVFoundation
import Foundation
import ImageIO
import QuartzCore

// sessiz: n saniyelik sessiz bölüm, görüntüsü goruntu_bas'tan; goruntu_bas (sessiz olmadan): ses bas–son, görüntü goruntu_bas'tan aynı süre.
struct Bolum: Decodable { let bas: Double?; let son: Double?; let sessiz: Double?; let goruntu_bas: Double?; let video_bas: Double?; let video_son: Double? }
struct Parca: Decodable { let ad: String; let kaynak: String; let bolumler: [Bolum] }
struct Kesim: Decodable { let x: Double; let y: Double; let genislik: Double; let yukseklik: Double }
struct Boyut: Decodable { let genislik: Double; let yukseklik: Double }
struct Plan: Decodable { let kesim: Kesim; let cikti: Boyut?; let parcalar: [Parca] }

// Gösterge ve animasyon dikdörtgenleri 1920x1080'lik çıktı piksellerinde (sol üst başlangıç); çıktı daha büyükse ölçeklenir.
// kalin/yaricap/gecis (30 Ekim akşam, kart içi odak): çizgi kalınlığı, köşe yarıçapı, beliriş süresi; verilmezse kart çerçevesi (5, 14, 0,3).
struct Gosterge: Decodable { let bas: Double; let son: Double; let x: Double; let y: Double; let w: Double; let h: Double
                             let kalin: Double?; let yaricap: Double?; let gecis: Double? }
struct Dikdortgen: Decodable { let x: Double; let y: Double; let w: Double; let h: Double }
// Animasyon (30 Ekim): kayıttaki takılan GIF'in yerine asıl GIF kendi hızında oynar (gorunur aralığında, kucuk dikdörtgende);
// bekleme aralığında slayt kararır, GIF kucuk'ten buyuk'e büyür ve sonunda geri küçülür. gif_bekleme_basi: beklemenin başında GIF'in saniyesi.
// video verilirse (30 Ekim): animasyon klibi ikinci görüntü izi olarak döngüyle konur; büyüme dönüşüm rampasıyla, kararma ana izin
// opaklık rampasıyla yapılır (görüntü yeniden örneklenmez, net kalır). gif verilirse eski yol: CALayer içeriği olarak.
// dondur (30 Ekim akşam): klip dönmez; beklemeden önce ilk karesi (takvim görünümü) durur, beklemede bir kez oynar, sonra son sahnesinde
// (Nijerya/Türkiye/Japonya etiketleri) kalır; böylece "In 2023, Nigeria…" derken etiketler görünür ve parlatılabilir.
struct Animasyon: Decodable { let gif: String?; let video: String?; let kucuk: Dikdortgen; let buyuk: Dikdortgen; let gorunur: [Double]; let bekleme: [Double]; let gif_bekleme_basi: Double; let dondur: Bool? }
// isik: spot ışığının sırayla geçtiği dikdörtgenler (kart, kart içi parça); verilmezse gostergeler kullanılır.
struct GostergeDosyasi: Decodable { let gostergeler: [Gosterge]; let isik: [Gosterge]?; let animasyon: Animasyon? }

let a = CommandLine.arguments
guard a.count == 4 || a.count == 5 else { print("kullanım: swift pilot/kurgu_video.swift <plan.json> <ses.wav> <cikti.mp4> [gostergeler.json]"); exit(1) }
let plan = try JSONDecoder().decode(Plan.self, from: Data(contentsOf: URL(fileURLWithPath: a[1])))
var gostergeler: [Gosterge] = [], isikListesi: [Gosterge] = [], animasyon: Animasyon? = nil
if a.count == 5 {
    let veri = try Data(contentsOf: URL(fileURLWithPath: a[4]))
    if let d = try? JSONDecoder().decode(GostergeDosyasi.self, from: veri) { gostergeler = d.gostergeler; isikListesi = d.isik ?? d.gostergeler; animasyon = d.animasyon }
    else { gostergeler = try JSONDecoder().decode([Gosterge].self, from: veri); isikListesi = gostergeler }
}
let W = plan.cikti?.genislik ?? 1920, H = plan.cikti?.yukseklik ?? 1080, f = W / 1920
func dikdortgen(_ x: Double, _ y: Double, _ w: Double, _ h: Double) -> CGRect {   // sol üst → katman ekseni (alttan), çıktı ölçeğinde
    CGRect(x: x * f, y: H - (y + h) * f, width: w * f, height: h * f)
}
let sesURL = URL(fileURLWithPath: a[2]), cikti = URL(fileURLWithPath: a[3])
func zaman(_ s: Double) -> CMTime { CMTime(seconds: s, preferredTimescale: 48000) }
let kare = 1.0 / 30
let bitti = DispatchSemaphore(value: 0)

Task {
    do {
        let kompozisyon = AVMutableComposition()
        guard let vIz = kompozisyon.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid),
              let sIz = kompozisyon.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)
        else { print("iz açılamadı"); exit(1) }
        var imlec = 0.0
        func dondur(_ kaynak: AVAssetTrack, _ t: Double, _ sure: Double) throws {   // t anındaki kareyi sure kadar göster
            guard sure > 0.001 else { return }
            try vIz.insertTimeRange(CMTimeRange(start: zaman(t), duration: zaman(kare)), of: kaynak, at: zaman(imlec))
            vIz.scaleTimeRange(CMTimeRange(start: zaman(imlec), duration: zaman(kare)), toDuration: zaman(sure))
            imlec += sure
        }
        for p in plan.parcalar {
            let varlik = AVURLAsset(url: URL(fileURLWithPath: (p.kaynak as NSString).expandingTildeInPath))
            guard let iz = try await varlik.loadTracks(withMediaType: .video).first else { print("\(p.ad): görüntü yok"); exit(1) }
            let boyut = try await iz.load(.naturalSize)
            guard boyut.width == 2880 && boyut.height == 1800 else { print("\(p.ad): kayıt \(boyut), plan 2880x1800 için"); exit(1) }
            let izSonu = try await iz.load(.timeRange).end.seconds
            for b in p.bolumler {
                if b.sessiz != nil || b.goruntu_bas != nil {
                    let sure = b.sessiz ?? (b.son! - b.bas!), g = b.goruntu_bas ?? b.bas!
                    guard g + sure <= izSonu + 0.001 else { print("\(p.ad): görüntü kaydın dışında (\(g) + \(sure))"); exit(1) }
                    try vIz.insertTimeRange(CMTimeRange(start: zaman(g), duration: zaman(sure)), of: iz, at: zaman(imlec))
                    imlec += sure
                    continue
                }
                let bas = b.bas!, son = b.son!
                let vb = max(bas, b.video_bas ?? bas)
                let ve = min(son, b.video_son ?? son, izSonu)
                try dondur(iz, vb, vb - bas)
                try vIz.insertTimeRange(CMTimeRange(start: zaman(vb), end: zaman(ve)), of: iz, at: zaman(imlec))
                imlec += ve - vb
                try dondur(iz, ve - kare, son - ve)
            }
            print(String(format: "%@: görüntü %.2f sn'ye kadar", p.ad, imlec))
        }
        let ses = AVURLAsset(url: sesURL)
        guard let sesIz = try await ses.loadTracks(withMediaType: .audio).first else { print("ses dosyasında ses yok"); exit(1) }
        let sesSure = try await ses.load(.duration)
        print(String(format: "ses %.2f sn · görüntü %.2f sn (fark %.3f)", sesSure.seconds, imlec, sesSure.seconds - imlec))
        if abs(sesSure.seconds - imlec) > 0.05 { print("UYARI: ses ve görüntü süresi farklı") }
        try sIz.insertTimeRange(CMTimeRange(start: .zero, duration: sesSure), of: sesIz, at: .zero)

        var animIz: AVMutableCompositionTrack? = nil, animBoyut = CGSize(width: 1920, height: 1080)
        if let an = animasyon, let yol = an.video {
            let av = AVURLAsset(url: URL(fileURLWithPath: yol))
            guard let aiz = try await av.loadTracks(withMediaType: .video).first,
                  let t2 = kompozisyon.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid) else { print("animasyon klibi açılamadı"); exit(1) }
            animBoyut = try await aiz.load(.naturalSize)
            let tur = try await aiz.load(.timeRange).duration.seconds
            let ilk = an.bekleme[0] - an.gif_bekleme_basi
            let dongu = ilk - tur * ceil((ilk - an.gorunur[0]) / tur)   // gorunur'dan önce başlayan döngü; beklemenin başında klip başta
            if an.dondur == true {
                func tut(_ kt: Double, _ bas: Double, _ son: Double) throws {   // klibin kt anındaki karesi bas–son arası durur
                    try t2.insertTimeRange(CMTimeRange(start: zaman(kt), duration: zaman(kare)), of: aiz, at: zaman(bas))
                    t2.scaleTimeRange(CMTimeRange(start: zaman(bas), duration: zaman(kare)), toDuration: zaman(son - bas))
                }
                let g0 = an.gif_bekleme_basi, oyna = an.bekleme[1] - an.bekleme[0]
                guard g0 + oyna <= tur else { print("animasyon klibi beklemeden kısa"); exit(1) }
                try tut(g0, an.gorunur[0], an.bekleme[0])
                try t2.insertTimeRange(CMTimeRange(start: zaman(g0), duration: zaman(oyna)), of: aiz, at: zaman(an.bekleme[0]))
                try tut(g0 + oyna - kare, an.bekleme[1], an.gorunur[1])
            } else {
                var t = an.gorunur[0]
                while t < an.gorunur[1] - 0.001 {
                    let faz = (t - dongu).truncatingRemainder(dividingBy: tur), parca = min(tur - faz, an.gorunur[1] - t)
                    try t2.insertTimeRange(CMTimeRange(start: zaman(faz), duration: zaman(parca)), of: aiz, at: zaman(t))
                    t += parca
                }
            }
            animIz = t2
            print(String(format: "animasyon klibi: tur %.2f sn, %.1f–%.1f sn arası", tur, an.gorunur[0], an.gorunur[1]))
        }
        let k = plan.kesim, olcek = W / k.genislik
        let katman = AVMutableVideoCompositionLayerInstruction(assetTrack: vIz)
        katman.setTransform(CGAffineTransform(translationX: -k.x, y: -k.y).concatenating(CGAffineTransform(scaleX: olcek, y: olcek)), at: .zero)
        let talimat = AVMutableVideoCompositionInstruction()
        talimat.timeRange = CMTimeRange(start: .zero, duration: kompozisyon.duration)
        var katmanlar: [AVVideoCompositionLayerInstruction] = []
        if let an = animasyon, let t2 = animIz {
            let li = AVMutableVideoCompositionLayerInstruction(assetTrack: t2)
            func yer(_ d: Dikdortgen) -> CGAffineTransform {   // video bileşiminde eksen sol üstten başlar
                let s = d.w * f / animBoyut.width
                return CGAffineTransform(scaleX: s, y: s).concatenating(CGAffineTransform(translationX: d.x * f, y: d.y * f))
            }
            let kucukT = yer(an.kucuk), buyukT = yer(an.buyuk), b0 = an.bekleme[0], b1 = an.bekleme[1], r = 0.5
            li.setTransform(kucukT, at: .zero)
            li.setOpacity(0, at: zaman(an.gorunur[1]))   // iz bitince son karesini tutmasın (4. sayfada görünüyordu)
            li.setTransformRamp(fromStart: kucukT, toEnd: buyukT, timeRange: CMTimeRange(start: zaman(b0), duration: zaman(r)))
            li.setTransformRamp(fromStart: buyukT, toEnd: kucukT, timeRange: CMTimeRange(start: zaman(b1 - r), duration: zaman(r)))
            katmanlar.append(li)
            katman.setOpacityRamp(fromStartOpacity: 1, toEndOpacity: 0.22, timeRange: CMTimeRange(start: zaman(b0), duration: zaman(r)))
            katman.setOpacityRamp(fromStartOpacity: 0.22, toEndOpacity: 1, timeRange: CMTimeRange(start: zaman(b1 - r), duration: zaman(r)))
        }
        katmanlar.append(katman)
        talimat.layerInstructions = katmanlar
        let vk = AVMutableVideoComposition()
        vk.renderSize = CGSize(width: W, height: H)
        vk.frameDuration = CMTime(value: 1, timescale: 30)
        vk.instructions = [talimat]
        if !gostergeler.isEmpty || animasyon != nil {
            let alan = CGRect(x: 0, y: 0, width: W, height: H)
            let ana = CALayer(), videoKatman = CALayer()
            ana.frame = alan
            videoKatman.frame = alan
            ana.addSublayer(videoKatman)
            func goster(_ l: CALayer, _ bas: Double, _ son: Double, gecis: Double = 0) {   // katman yalnız bas–son arasında görünür
                l.opacity = 0
                let an = CAKeyframeAnimation(keyPath: "opacity"), sure = son - bas, g = min(gecis, sure / 3)
                an.values = g > 0 ? [0, 1, 1, 0] : [1, 1]
                an.keyTimes = g > 0 ? [0, NSNumber(value: g / sure), NSNumber(value: 1 - g / sure), 1] : [0, 1]
                an.beginTime = max(bas, AVCoreAnimationBeginTimeAtZero)
                an.duration = sure
                l.add(an, forKey: "gorun")
            }
            var gifIcerik: CAKeyframeAnimation? = nil
            if let an = animasyon, an.video == nil, let gifYol = an.gif {   // asıl GIF'in kareleri ve süreleri
                guard let kaynak = CGImageSourceCreateWithURL(URL(fileURLWithPath: gifYol) as CFURL, nil) else { print("GIF açılamadı"); exit(1) }
                var kareler: [CGImage] = [], sureler: [Double] = []
                for i in 0..<CGImageSourceGetCount(kaynak) {
                    kareler.append(CGImageSourceCreateImageAtIndex(kaynak, i, nil)!)
                    let o = CGImageSourceCopyPropertiesAtIndex(kaynak, i, nil) as? [CFString: Any]
                    let gif = o?[kCGImagePropertyGIFDictionary] as? [CFString: Any]
                    sureler.append((gif?[kCGImagePropertyGIFUnclampedDelayTime] as? Double) ?? (gif?[kCGImagePropertyGIFDelayTime] as? Double) ?? 0.06)
                }
                let tur = sureler.reduce(0, +)
                var anlar: [NSNumber] = [0], t = 0.0
                for s in sureler { t += s; anlar.append(NSNumber(value: t / tur)) }
                let c = CAKeyframeAnimation(keyPath: "contents")
                c.values = kareler
                c.keyTimes = anlar
                c.calculationMode = .discrete
                c.duration = tur
                let ilk = an.bekleme[0] - an.gif_bekleme_basi
                c.beginTime = ilk - tur * ceil((ilk - an.gorunur[0]) / tur)   // beklemenin başında GIF tam takvim görünümünde
                c.repeatCount = Float(ceil((an.gorunur[1] - c.beginTime) / tur) + 1)
                gifIcerik = c
                print(String(format: "animasyon: %d kare, tur %.2f sn", kareler.count, tur))
            }
            if let an = animasyon, let c = gifIcerik {   // küçük GIF: kayıttaki takılan animasyonun üstünü kapatır
                let kucuk = CALayer()
                kucuk.frame = dikdortgen(an.kucuk.x, an.kucuk.y, an.kucuk.w, an.kucuk.h)
                kucuk.contentsGravity = .resize
                kucuk.add(c, forKey: "gif")
                goster(kucuk, an.gorunur[0], an.gorunur[1])
                ana.addSublayer(kucuk)
            }
            // spot ışığı (30 Ekim): konuşulan kart dışındaki her yer hafifçe kararır; art arda göstergelerde ışık bir karttan ötekine kayar
            var zincirler: [[Gosterge]] = []
            for g in isikListesi.sorted(by: { $0.bas < $1.bas }) {
                if let son = zincirler.last?.last, g.bas - son.son < 0.05 { zincirler[zincirler.count - 1].append(g) } else { zincirler.append([g]) }
            }
            func delikli(_ g: Gosterge) -> CGPath {
                let yol = CGMutablePath()
                yol.addRect(alan)
                let r = ((g.yaricap ?? 14) * f).rounded()
                yol.addPath(CGPath(roundedRect: dikdortgen(g.x, g.y, g.w, g.h).integral, cornerWidth: r, cornerHeight: r, transform: nil))
                return yol
            }
            for z in zincirler {
                let bas = z.first!.bas, son = z.last!.son, sure = son - bas
                let isik = CAShapeLayer()
                isik.frame = alan
                isik.fillRule = .evenOdd
                isik.fillColor = CGColor(red: 0.01, green: 0.03, blue: 0.06, alpha: 0.28)   // öteki kartlar okunur kalır (kullanıcı: "görünmez olmasın")
                isik.path = delikli(z[0])
                if z.count > 1 {
                    var degerler: [CGPath] = [delikli(z[0])], anlar: [NSNumber] = [0]
                    for i in 1..<z.count {
                        let t0 = (z[i].bas - bas) / sure, t1 = min(1, (z[i].bas + 0.35 - bas) / sure)
                        degerler += [delikli(z[i - 1]), delikli(z[i])]
                        anlar += [NSNumber(value: t0), NSNumber(value: t1)]
                    }
                    degerler.append(delikli(z.last!)); anlar.append(1)
                    let ya = CAKeyframeAnimation(keyPath: "path")
                    ya.values = degerler
                    ya.keyTimes = anlar
                    // yumuşatma her geçişe ayrı (timingFunction tüm zincire uygulanınca ışık uzun zincirlerde zamandan önce/sonra kayıyordu)
                    ya.timingFunctions = Array(repeating: CAMediaTimingFunction(name: .easeInEaseOut), count: degerler.count - 1)
                    ya.beginTime = max(bas, AVCoreAnimationBeginTimeAtZero)
                    ya.duration = sure
                    isik.add(ya, forKey: "kay")
                }
                goster(isik, bas, son, gecis: 0.35)
                ana.addSublayer(isik)
            }
            let sari = CGColor(red: 1, green: 0.82, blue: 0.4, alpha: 1)   // "What it means" bandının sarısı (#FFD166)
            // Çerçeveler (30 Ekim akşam): CAShapeLayer çizgisi bazı konumlarda hiç çizilmiyordu (çizici hatası; hangi kutuda olacağı
            // önceden bilinmiyor: Q1, "Separate curves", Türkiye etiketi, sağlık ekseni…). Artık her çerçeve Core Graphics ile önceden
            // resim olarak çizilir (sarı çizgi + parıltı) ve katmanın içeriği olur; katman sadece o kutu kadar, bas–son arası görünür.
            let srgb = CGColorSpace(name: CGColorSpace.sRGB)!
            func cerceveResmi(_ w: Int, _ h: Int, _ r: CGFloat, _ kalin: CGFloat, _ pay: Int) -> CGImage {
                let ctx = CGContext(data: nil, width: w + 2 * pay, height: h + 2 * pay, bitsPerComponent: 8, bytesPerRow: 0, space: srgb,
                                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
                let yol = CGPath(roundedRect: CGRect(x: pay, y: pay, width: w, height: h), cornerWidth: r, cornerHeight: r, transform: nil)
                ctx.setLineWidth(kalin)
                ctx.setStrokeColor(sari)
                ctx.setShadow(offset: .zero, blur: 3 * kalin, color: sari.copy(alpha: 0.9))   // parıltı (eski shadowRadius 2·kalın'a yakın)
                for _ in 0..<2 { ctx.addPath(yol); ctx.strokePath() }                            // iki kez: parıltı daha dolgun
                ctx.setShadow(offset: .zero, blur: 0, color: nil)
                ctx.addPath(yol); ctx.strokePath()
                return ctx.makeImage()!
            }
            for g in gostergeler {
                let kalin = ((g.kalin ?? 5) * f).rounded(), r = ((g.yaricap ?? 14) * f).rounded()
                let kutu = dikdortgen(g.x, g.y, g.w, g.h).integral, pay = Int(5 * kalin)
                let k = CALayer()
                k.frame = kutu.insetBy(dx: -CGFloat(pay), dy: -CGFloat(pay))
                k.contents = cerceveResmi(Int(kutu.width), Int(kutu.height), r, kalin, pay)
                k.contentsGravity = .resize
                goster(k, g.bas, g.son, gecis: g.gecis ?? 0.3)
                ana.addSublayer(k)
            }
            if let an = animasyon, let c = gifIcerik {   // bekleme: slayt kararır, GIF büyür, sonra yerine döner
                let b0 = an.bekleme[0], b1 = an.bekleme[1], sure = b1 - b0, g = 0.5 / sure
                let karart = CALayer()
                karart.frame = alan
                karart.backgroundColor = CGColor(red: 0.03, green: 0.06, blue: 0.09, alpha: 1)
                karart.opacity = 0
                let ko = CAKeyframeAnimation(keyPath: "opacity")
                ko.values = [0, 0.78, 0.78, 0]
                ko.keyTimes = [0, NSNumber(value: g), NSNumber(value: 1 - g), 1]
                ko.beginTime = b0
                ko.duration = sure
                karart.add(ko, forKey: "karart")
                ana.addSublayer(karart)
                let buyuk = CALayer()
                let kb = dikdortgen(an.buyuk.x, an.buyuk.y, an.buyuk.w, an.buyuk.h), kk = dikdortgen(an.kucuk.x, an.kucuk.y, an.kucuk.w, an.kucuk.h)
                buyuk.frame = kb
                buyuk.contentsGravity = .resize
                buyuk.shadowColor = CGColor(red: 0, green: 0, blue: 0, alpha: 1)
                buyuk.shadowOpacity = 0.7
                buyuk.shadowRadius = 30 * f
                buyuk.shadowOffset = .zero
                buyuk.add(c, forKey: "gif")
                goster(buyuk, b0, b1)
                let s = kk.width / kb.width
                let kucukHali = CATransform3DScale(CATransform3DMakeTranslation(kk.midX - kb.midX, kk.midY - kb.midY, 0), s, s, 1)
                let tr = CAKeyframeAnimation(keyPath: "transform")
                tr.values = [kucukHali, CATransform3DIdentity, CATransform3DIdentity, kucukHali].map { NSValue(caTransform3D: $0) }
                tr.keyTimes = [0, NSNumber(value: g), NSNumber(value: 1 - g), 1]
                tr.timingFunctions = [CAMediaTimingFunction(name: .easeInEaseOut), CAMediaTimingFunction(name: .linear), CAMediaTimingFunction(name: .easeInEaseOut)]
                tr.beginTime = b0
                tr.duration = sure
                buyuk.add(tr, forKey: "buyu")
                ana.addSublayer(buyuk)
            }
            vk.animationTool = AVVideoCompositionCoreAnimationTool(postProcessingAsVideoLayer: videoKatman, in: ana)
            print("gösterge: \(gostergeler.count)")
        }
        let prores = cikti.pathExtension.lowercased() == "mov"   // .mov: ProRes 422 ara dosya (pilot/yuksek_kalite.swift ile H.264'e çevrilir)
        guard let disari = AVAssetExportSession(asset: kompozisyon, presetName: prores ? AVAssetExportPresetAppleProRes422LPCM : AVAssetExportPresetHighestQuality) else { print("dışa aktarma açılamadı"); exit(1) }
        disari.videoComposition = vk
        disari.shouldOptimizeForNetworkUse = !prores
        try? FileManager.default.removeItem(at: cikti)
        try await disari.export(to: cikti, as: prores ? .mov : .mp4)
        let mb = Double((try FileManager.default.attributesOfItem(atPath: cikti.path)[.size] as? Int) ?? 0) / 1e6
        let s = kompozisyon.duration.seconds
        print(String(format: "yazıldı: %@ · %d:%04.1f · %.0fx%.0f · %.0f MB", cikti.lastPathComponent, Int(s) / 60, s.truncatingRemainder(dividingBy: 60), W, H, mb))
        if s > 300 { print("UYARI: süre 5 dakikayı geçiyor") }
    } catch { print("hata:", error); exit(1) }
    bitti.signal()
}
bitti.wait()
