import Foundation
@preconcurrency import AVFoundation

struct FilmPlan: Decodable {
    struct Meta: Decodable {
        let title: String
        let slug: String
        let duration: Double
        let width: Int
        let height: Int
        let fps: Double
    }
    struct Credits: Decodable {
        let developed_by: String
        let company: String
    }
    struct Audio: Decodable {
        let music_file: String
        let voice_dir: String
        let music_base: Float
        let music_duck: Float
    }
    struct Render: Decodable {
        let silent_video: String
        let output_video: String
    }
    struct Narration: Decodable {
        let id: String
        let start: Double
        let duration: Double?
        let text: String
        let file: String?
    }
    let meta: Meta
    let credits: Credits
    let audio: Audio
    let render: Render
    let narration: [Narration]
}

let arguments = CommandLine.arguments
guard arguments.count == 2 else {
    fatalError("Usage: swift mix_video.swift /absolute/path/to/film-project")
}

let projectURL = URL(fileURLWithPath: arguments[1], isDirectory: true).standardizedFileURL
let planURL = projectURL.appendingPathComponent("film-plan.json")
let plan = try JSONDecoder().decode(FilmPlan.self, from: Data(contentsOf: planURL))
let timeScale: CMTimeScale = 48_000
let targetDuration = CMTime(seconds: plan.meta.duration, preferredTimescale: timeScale)
let crossfade = CMTime(seconds: 4, preferredTimescale: timeScale)

func projectFile(_ relative: String) -> URL {
    projectURL.appendingPathComponent(relative)
}

func removeIfPresent(_ url: URL) throws {
    if FileManager.default.fileExists(atPath: url.path) {
        try FileManager.default.removeItem(at: url)
    }
}

func waitForExport(_ exporter: AVAssetExportSession, label: String) {
    let semaphore = DispatchSemaphore(value: 0)
    exporter.exportAsynchronously { semaphore.signal() }
    semaphore.wait()
    guard exporter.status == .completed else {
        fatalError("\(label) failed: \(String(describing: exporter.error))")
    }
}

func clamp(_ value: Double, _ lower: Double = 0, _ upper: Double = 1) -> Double {
    min(upper, max(lower, value))
}

func makeMetadata() -> [AVMetadataItem] {
    let title = AVMutableMetadataItem()
    title.identifier = .commonIdentifierTitle
    title.value = plan.meta.title as NSString
    let artist = AVMutableMetadataItem()
    artist.identifier = .commonIdentifierArtist
    artist.value = [plan.credits.developed_by, plan.credits.company]
        .filter { !$0.isEmpty }
        .joined(separator: " — ") as NSString
    let description = AVMutableMetadataItem()
    description.identifier = .commonIdentifierDescription
    description.value = "Narrative film" as NSString
    return [title, artist, description]
}

let soundtrackURL = projectFile(plan.audio.music_file)
let silentVideoURL = projectFile(plan.render.silent_video)
let finalVideoURL = projectFile(plan.render.output_video)
let workDirectory = projectURL.appendingPathComponent("render/work", isDirectory: true)
try FileManager.default.createDirectory(at: workDirectory, withIntermediateDirectories: true)
let loopedMusicURL = workDirectory.appendingPathComponent("looped-music.m4a")
let mixedAudioURL = workDirectory.appendingPathComponent("mixed-audio.m4a")

try removeIfPresent(loopedMusicURL)
let musicAsset = AVURLAsset(url: soundtrackURL)
guard let musicSourceTrack = musicAsset.tracks(withMediaType: .audio).first else {
    fatalError("Soundtrack track not found: \(soundtrackURL.path)")
}
let musicDuration = musicAsset.duration
guard CMTimeGetSeconds(musicDuration) > 8 else {
    fatalError("Soundtrack must be longer than 8 seconds")
}

let loopComposition = AVMutableComposition()
guard
    let loopTrackA = loopComposition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid),
    let loopTrackB = loopComposition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)
else {
    fatalError("Cannot create soundtrack tracks")
}
let loopTracks = [loopTrackA, loopTrackB]
let loopParams = [
    AVMutableAudioMixInputParameters(track: loopTrackA),
    AVMutableAudioMixInputParameters(track: loopTrackB),
]

var insertionTime = CMTime.zero
var loopIndex = 0
while CMTimeCompare(insertionTime, targetDuration) < 0 {
    let remaining = CMTimeSubtract(targetDuration, insertionTime)
    let insertedDuration = CMTimeMinimum(musicDuration, remaining)
    let track = loopTracks[loopIndex % 2]
    let params = loopParams[loopIndex % 2]
    try track.insertTimeRange(
        CMTimeRange(start: .zero, duration: insertedDuration),
        of: musicSourceTrack,
        at: insertionTime
    )

    let fadeDuration = CMTimeMinimum(crossfade, insertedDuration)
    if loopIndex == 0 {
        params.setVolumeRamp(
            fromStartVolume: 0,
            toEndVolume: 1,
            timeRange: CMTimeRange(
                start: insertionTime,
                duration: CMTimeMinimum(CMTime(seconds: 2.0, preferredTimescale: timeScale), fadeDuration)
            )
        )
    } else {
        params.setVolumeRamp(
            fromStartVolume: 0,
            toEndVolume: 1,
            timeRange: CMTimeRange(start: insertionTime, duration: fadeDuration)
        )
    }

    let insertionEnd = CMTimeAdd(insertionTime, insertedDuration)
    if CMTimeCompare(insertionEnd, targetDuration) < 0 {
        let fadeStart = CMTimeSubtract(insertionEnd, fadeDuration)
        params.setVolumeRamp(
            fromStartVolume: 1,
            toEndVolume: 0,
            timeRange: CMTimeRange(start: fadeStart, duration: fadeDuration)
        )
    }

    insertionTime = CMTimeAdd(insertionTime, CMTimeSubtract(musicDuration, crossfade))
    loopIndex += 1
}

let loopMix = AVMutableAudioMix()
loopMix.inputParameters = loopParams
guard let loopExporter = AVAssetExportSession(asset: loopComposition, presetName: AVAssetExportPresetAppleM4A) else {
    fatalError("Cannot create soundtrack exporter")
}
loopExporter.outputURL = loopedMusicURL
loopExporter.outputFileType = .m4a
loopExporter.audioMix = loopMix
loopExporter.timeRange = CMTimeRange(start: .zero, duration: targetDuration)
waitForExport(loopExporter, label: "Soundtrack loop")
print("soundtrack=ready")

try removeIfPresent(mixedAudioURL)
let loopedMusicAsset = AVURLAsset(url: loopedMusicURL)
guard let loopedMusicTrack = loopedMusicAsset.tracks(withMediaType: .audio).first else {
    fatalError("Looped soundtrack track not found")
}

let audioComposition = AVMutableComposition()
guard
    let musicTrack = audioComposition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid),
    let narrationTrack = audioComposition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)
else {
    fatalError("Cannot create final audio tracks")
}
try musicTrack.insertTimeRange(
    CMTimeRange(start: .zero, duration: targetDuration),
    of: loopedMusicTrack,
    at: .zero
)

struct DuckWindow {
    var start: Double
    var end: Double
}

var windows: [DuckWindow] = []
for segment in plan.narration.sorted(by: { $0.start < $1.start }) {
    let voiceURL = projectFile(segment.file ?? "\(plan.audio.voice_dir)/\(segment.id).mp3")
    let voiceAsset = AVURLAsset(url: voiceURL)
    guard let voiceTrack = voiceAsset.tracks(withMediaType: .audio).first else {
        fatalError("Narration track not found: \(segment.id)")
    }
    let actualDuration = CMTimeGetSeconds(voiceAsset.duration)
    if let declared = segment.duration, abs(declared - actualDuration) > 0.15 {
        fatalError("Narration duration mismatch for \(segment.id)")
    }
    let start = CMTime(seconds: segment.start, preferredTimescale: timeScale)
    try narrationTrack.insertTimeRange(
        CMTimeRange(start: .zero, duration: voiceAsset.duration),
        of: voiceTrack,
        at: start
    )

    let duckStart = max(0, segment.start - 0.55)
    let releaseStart = min(plan.meta.duration, segment.start + actualDuration + 0.18)
    if let last = windows.last, duckStart <= last.end + 0.9 {
        windows[windows.count - 1].end = max(last.end, releaseStart)
    } else {
        windows.append(DuckWindow(start: duckStart, end: releaseStart))
    }
}

func musicVolume(at time: Double) -> Float {
    let intro = clamp(time / 1.2)
    let outro = clamp((plan.meta.duration - time) / 5.0)
    let baseEnvelope = min(intro, outro)
    let duckRatio = Double(plan.audio.music_duck / plan.audio.music_base)
    var factor = 1.0
    for window in windows {
        let duckEnd = window.start + 0.42
        let releaseEnd = window.end + 0.9
        if time >= window.start && time < duckEnd {
            let progress = clamp((time - window.start) / 0.42)
            factor = min(factor, 1 + (duckRatio - 1) * progress)
        } else if time >= duckEnd && time <= window.end {
            factor = min(factor, duckRatio)
        } else if time > window.end && time < releaseEnd {
            let progress = clamp((time - window.end) / 0.9)
            factor = min(factor, duckRatio + (1 - duckRatio) * progress)
        }
    }
    return Float(Double(plan.audio.music_base) * baseEnvelope * factor)
}

var automationTimes = [0.0, min(1.2, plan.meta.duration), max(0, plan.meta.duration - 5), plan.meta.duration]
for window in windows {
    automationTimes.append(window.start)
    automationTimes.append(min(plan.meta.duration, window.start + 0.42))
    automationTimes.append(window.end)
    automationTimes.append(min(plan.meta.duration, window.end + 0.9))
}
automationTimes = Array(Set(automationTimes.map { round($0 * 48_000) / 48_000 })).sorted()

let musicParams = AVMutableAudioMixInputParameters(track: musicTrack)
for index in 0..<(automationTimes.count - 1) {
    let startSeconds = automationTimes[index]
    let endSeconds = automationTimes[index + 1]
    guard endSeconds > startSeconds else { continue }
    musicParams.setVolumeRamp(
        fromStartVolume: musicVolume(at: startSeconds),
        toEndVolume: musicVolume(at: endSeconds),
        timeRange: CMTimeRange(
            start: CMTime(seconds: startSeconds, preferredTimescale: timeScale),
            duration: CMTime(seconds: endSeconds - startSeconds, preferredTimescale: timeScale)
        )
    )
}

let narrationParams = AVMutableAudioMixInputParameters(track: narrationTrack)
narrationParams.setVolume(1, at: .zero)
let finalAudioMix = AVMutableAudioMix()
finalAudioMix.inputParameters = [musicParams, narrationParams]

guard let audioExporter = AVAssetExportSession(asset: audioComposition, presetName: AVAssetExportPresetAppleM4A) else {
    fatalError("Cannot create mixed audio exporter")
}
audioExporter.outputURL = mixedAudioURL
audioExporter.outputFileType = .m4a
audioExporter.audioMix = finalAudioMix
audioExporter.timeRange = CMTimeRange(start: .zero, duration: targetDuration)
waitForExport(audioExporter, label: "Narration mix")
print("audio=ready")

try FileManager.default.createDirectory(at: finalVideoURL.deletingLastPathComponent(), withIntermediateDirectories: true)
try removeIfPresent(finalVideoURL)
let videoAsset = AVURLAsset(url: silentVideoURL)
let audioAsset = AVURLAsset(url: mixedAudioURL)
guard
    let sourceVideoTrack = videoAsset.tracks(withMediaType: .video).first,
    let sourceAudioTrack = audioAsset.tracks(withMediaType: .audio).first
else {
    fatalError("Final source tracks not found")
}

let finalComposition = AVMutableComposition()
guard
    let finalVideoTrack = finalComposition.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid),
    let finalAudioTrack = finalComposition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)
else {
    fatalError("Cannot create final composition")
}
try finalVideoTrack.insertTimeRange(
    CMTimeRange(start: .zero, duration: targetDuration),
    of: sourceVideoTrack,
    at: .zero
)
finalVideoTrack.preferredTransform = sourceVideoTrack.preferredTransform
try finalAudioTrack.insertTimeRange(
    CMTimeRange(start: .zero, duration: targetDuration),
    of: sourceAudioTrack,
    at: .zero
)

guard let finalExporter = AVAssetExportSession(asset: finalComposition, presetName: AVAssetExportPresetPassthrough) else {
    fatalError("Cannot create final video exporter")
}
finalExporter.outputURL = finalVideoURL
finalExporter.outputFileType = .mp4
finalExporter.shouldOptimizeForNetworkUse = true
finalExporter.timeRange = CMTimeRange(start: .zero, duration: targetDuration)
finalExporter.metadata = makeMetadata()
waitForExport(finalExporter, label: "Final mux")

let finalAsset = AVURLAsset(url: finalVideoURL)
guard
    let verifiedVideo = finalAsset.tracks(withMediaType: .video).first,
    finalAsset.tracks(withMediaType: .audio).first != nil
else {
    fatalError("Final video is missing a video or audio track")
}
let transformedSize = verifiedVideo.naturalSize.applying(verifiedVideo.preferredTransform)
let width = Int(abs(transformedSize.width.rounded()))
let height = Int(abs(transformedSize.height.rounded()))
let duration = CMTimeGetSeconds(finalAsset.duration)
guard width == plan.meta.width, height == plan.meta.height, abs(duration - plan.meta.duration) < 0.15 else {
    fatalError("Final media properties do not match film-plan.json")
}
print("final=\(finalVideoURL.path)")
print("duration=\(String(format: "%.3f", duration)) size=\(width)x\(height) fps=\(String(format: "%.3f", verifiedVideo.nominalFrameRate)) audio=yes")
