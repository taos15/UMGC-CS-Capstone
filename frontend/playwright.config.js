import {defineConfig} from '@playwright/test';
export default defineConfig({
  testDir: './e2e', workers: 1, retries: 0, timeout: 60000,
  reporter: [['list']],
  use: {baseURL: process.env.SKILLMATCH_E2E_BASE_URL, headless: true},
});
