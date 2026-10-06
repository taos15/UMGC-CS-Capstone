import js from '@eslint/js';
import globals from 'globals';
import react from 'eslint-plugin-react';

export default [
  {ignores: ['dist/**', 'node_modules/**', 'test-results/**', 'playwright-report/**', 'coverage/**']},
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {ecmaVersion: 'latest', sourceType: 'module',
      parserOptions: {ecmaFeatures: {jsx: true}}, globals: {...globals.browser, ...globals.node}},
    plugins: {react},
    rules: {...js.configs.recommended.rules,
      'react/jsx-uses-react': 'error', 'react/jsx-uses-vars': 'error', 'react/jsx-key': 'error',
      'no-unused-vars': ['error', {argsIgnorePattern: '^_', caughtErrors: 'none', ignoreRestSiblings: true}],
      'no-empty': ['error', {allowEmptyCatch: true}]},
  },
];
