// Subject cutout with Apple Vision (macOS 14+). Writes a transparent PNG.
//
//   swiftc -O cutout.swift -o /tmp/cutout
//   /tmp/cutout photo.jpg cutout.png
//
// Works best on a plain background. Check the edges afterwards on the page's
// brand color; crop to the subject with Pillow: im.crop(im.getbbox()).
import Foundation
import Vision
import CoreImage

let args = CommandLine.arguments
guard args.count == 3 else {
    print("usage: cutout <input-image> <output.png>")
    exit(1)
}
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
guard let image = CIImage(contentsOf: inURL, options: [.applyOrientationProperty: true]) else {
    print("could not read \(args[1])")
    exit(1)
}
let handler = VNImageRequestHandler(ciImage: image, options: [:])
let request = VNGenerateForegroundInstanceMaskRequest()
do {
    try handler.perform([request])
    guard let result = request.results?.first else {
        print("no subject found")
        exit(2)
    }
    let buffer = try result.generateMaskedImage(ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: false)
    let output = CIImage(cvPixelBuffer: buffer)
    try CIContext().writePNGRepresentation(of: output, to: outURL, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
    print("ok: \(result.allInstances.count) subject(s) -> \(args[2])")
} catch {
    print("error: \(error)")
    exit(3)
}
