// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "FamilyTVCore", products: [.library(name: "FamilyTVCore", targets: ["FamilyTVCore"])], targets: [.target(name: "FamilyTVCore", path: "Core"), .testTarget(name: "FamilyTVCoreTests", dependencies: ["FamilyTVCore"], path: "Tests")])
