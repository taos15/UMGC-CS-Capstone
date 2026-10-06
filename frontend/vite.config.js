import {defineConfig, loadEnv} from 'vite';

export default defineConfig(({mode}) => {
  const env = loadEnv(mode, process.cwd(), 'SKILLMATCH_');
  return {
    server: {proxy: {'/api': env.SKILLMATCH_API_PROXY_TARGET || 'http://127.0.0.1:8000'}},
    test: {include: ['src/**/*.test.{js,jsx}'], environment: 'jsdom', setupFiles: './src/test-setup.js', clearMocks: true},
  };
});
