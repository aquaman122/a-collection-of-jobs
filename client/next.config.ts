import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    turbo: {
      rules: {
        "*.mdx": ["mdx-loader"]
      }
    }
  },
};

export default nextConfig;
