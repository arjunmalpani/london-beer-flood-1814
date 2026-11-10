import { Config } from "@remotion/cli/config";

// On GitHub Actions (CPU-only), use 'swangle' software backend.
// On Colab or local GPU systems, allow hardware-accelerated OpenGL (e.g. 'angle-egl').
if (process.env.GITHUB_ACTIONS) {
  Config.setChromiumOpenGlRenderer("swangle");
}

Config.setTimeoutInMilliseconds(180000);
