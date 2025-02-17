/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['firebasestorage.googleapis.com'],
        formats: ['image/avif', 'image/webp'], // Optional: for better optimization
        // dangerouslyAllowSVG: true,
      },
};

export default nextConfig;
