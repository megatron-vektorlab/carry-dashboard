/** @type {import('next').NextConfig} */
const nextConfig = {
  outputFileTracingIncludes: {
    "/api/paper": ["./data/**"],
  },
};

export default nextConfig;
