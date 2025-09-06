import { defineConfig, devices } from '@playwright/test';
import * as path from 'path';

export default defineConfig({
  // Test directory
  testDir: './tests',
  
  // Global timeout
  globalTimeout: 60 * 60 * 1000, // 1 hour
  timeout: 60 * 1000, // 1 minute per test
  
  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,
  
  // Retry on CI only
  retries: process.env.CI ? 2 : 1,
  
  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,
  
  // Global setup and teardown
  globalSetup: require.resolve('./utils/global-setup'),
  globalTeardown: require.resolve('./utils/global-teardown'),
  
  // Reporter configuration with HTML, JSON, and custom reporting
  reporter: [
    ['html', { 
      outputFolder: 'playwright-report',
      open: 'never'
    }],
    ['json', { 
      outputFile: 'reports/test-results.json' 
    }],
    ['junit', { 
      outputFile: 'reports/test-results.xml' 
    }],
    ['./utils/custom-reporter.ts'],
    // Include line reporter for console output
    ['line']
  ],
  
  // Configure projects for major browsers
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    
    // Desktop browsers
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Enable video recording
        video: 'retain-on-failure',
        // Enable screenshots
        screenshot: 'only-on-failure',
        // Custom viewport for consistency
        viewport: { width: 1920, height: 1080 },
        // Slower actions for better debugging
        actionTimeout: 10000,
        navigationTimeout: 30000,
        // Context options
        ignoreHTTPSErrors: true,
        // Custom user agent
        userAgent: 'HackathonPlatform-E2E-Tests/1.0'
      },
      dependencies: ['setup'],
    },
    
    {
      name: 'firefox',
      use: { 
        ...devices['Desktop Firefox'],
        video: 'retain-on-failure',
        screenshot: 'only-on-failure',
        viewport: { width: 1920, height: 1080 },
        actionTimeout: 10000,
        navigationTimeout: 30000,
        ignoreHTTPSErrors: true,
        userAgent: 'HackathonPlatform-E2E-Tests-Firefox/1.0'
      },
      dependencies: ['setup'],
    },
    
    {
      name: 'webkit',
      use: { 
        ...devices['Desktop Safari'],
        video: 'retain-on-failure',
        screenshot: 'only-on-failure',
        viewport: { width: 1920, height: 1080 },
        actionTimeout: 10000,
        navigationTimeout: 30000,
        ignoreHTTPSErrors: true,
        userAgent: 'HackathonPlatform-E2E-Tests-Safari/1.0'
      },
      dependencies: ['setup'],
    },
    
    // Mobile browsers
    {
      name: 'mobile-chrome',
      use: { 
        ...devices['Pixel 5'],
        video: 'retain-on-failure',
        screenshot: 'only-on-failure',
        actionTimeout: 15000, // Mobile might be slower
        navigationTimeout: 45000,
        ignoreHTTPSErrors: true
      },
      dependencies: ['setup'],
    },
    
    {
      name: 'mobile-safari',
      use: { 
        ...devices['iPhone 12'],
        video: 'retain-on-failure',
        screenshot: 'only-on-failure',
        actionTimeout: 15000,
        navigationTimeout: 45000,
        ignoreHTTPSErrors: true
      },
      dependencies: ['setup'],
    },
  ],
  
  // Shared settings for all projects
  use: {
    // Base URL for the application
    baseURL: process.env.BASE_URL || 'http://localhost:3001',
    
    // Global navigation timeout
    navigationTimeout: 30 * 1000,
    
    // Global action timeout
    actionTimeout: 10 * 1000,
    
    // Capture trace for debugging
    trace: 'retain-on-failure',
    
    // Capture screenshots
    screenshot: 'only-on-failure',
    
    // Record video
    video: 'retain-on-failure',
    
    // Locale and timezone
    locale: 'en-US',
    timezoneId: 'America/New_York',
    
    // Ignore HTTPS errors for local testing
    ignoreHTTPSErrors: true,
    
    // Accept downloads
    acceptDownloads: true,
    
    // Storage state for authentication
    storageState: {
      cookies: [],
      origins: []
    }
  },
  
  // Expect configuration
  expect: {
    // Global assertion timeout
    timeout: 10 * 1000,
    
    // Screenshot comparison threshold
    threshold: 0.2,
    
    // Animation handling
    toHaveScreenshot: { 
      threshold: 0.2,
      animation: 'disabled',
      mode: 'rgb'
    },
    
    toMatchSnapshot: { 
      threshold: 0.2,
      animation: 'disabled'
    }
  },
  
  // Web server configuration for local testing
  webServer: process.env.CI ? undefined : {
    command: 'cd .. && npm run dev',
    port: 3001,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000, // 2 minutes to start server
    env: {
      NODE_ENV: 'test'
    }
  },
  
  // Output directory for test artifacts
  outputDir: 'test-results/',
  
  // Metadata for test runs
  metadata: {
    'Test Environment': process.env.NODE_ENV || 'test',
    'Base URL': process.env.BASE_URL || 'http://localhost:3001',
    'Playwright Version': require('@playwright/test/package.json').version,
    'Node Version': process.version,
    'OS': process.platform,
    'Test Run ID': new Date().toISOString()
  }
});
