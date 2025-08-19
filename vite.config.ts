import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
	plugins: [
		sveltekit(),
		viteStaticCopy({
			targets: [
				{
					src: 'node_modules/onnxruntime-web/dist/*.jsep.*',

					dest: 'wasm'
				}
			]
		})
	],
	define: {
		APP_VERSION: JSON.stringify(process.env.npm_package_version),
		APP_BUILD_HASH: JSON.stringify(process.env.APP_BUILD_HASH || 'dev-build')
	},
	build: {
		sourcemap: true
	},
	worker: {
		format: 'es'
	},
	server: {
		port: parseInt(process.env.VITE_PORT || '8357'),
		host: true,
		proxy: {
			'/api': {
				target: 'http://localhost:36950',
				changeOrigin: true
			},
			'/ollama': {
				target: 'http://localhost:11434',
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/ollama/, '')
			},
			'/socket.io': {
				target: 'http://localhost:36950',
				changeOrigin: true,
				ws: true
			}
		}
	},
	esbuild: {
		pure: process.env.ENV === 'dev' ? [] : ['console.log', 'console.debug']
	}
});
