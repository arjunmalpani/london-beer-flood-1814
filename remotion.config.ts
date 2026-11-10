import { Config } from "@remotion/cli/config";

// In cloud/CI environments without physical GPUs (like GitHub Actions),
// use 'swangle' (SwiftShader on ANGLE) to emulate WebGL in software.
Config.setChromiumOpenGlRenderer("swangle");

// Increase frame initialization and shader compilation timeout to 3 minutes
Config.setTimeoutInMilliseconds(180000);
