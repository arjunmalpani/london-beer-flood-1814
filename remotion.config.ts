import { Config } from "@remotion/cli/config";

// In cloud/CI environments without physical GPUs (like GitHub Actions),
// use 'swangle' (SwiftShader on ANGLE) to emulate WebGL in software.
Config.setChromiumOpenGlRenderer("swangle");
