import js from '@eslint/js';
import globals from 'globals';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import { defineConfig, globalIgnores } from 'eslint/config';

export default defineConfig([
  globalIgnores(['dist', 'node_modules', 'coverage']),
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 'latest',
      globals: {
        ...globals.browser,
        ...globals.es2021,
      },
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      // 1. Base Recommendations
      ...js.configs.recommended.rules,
      ...react.configs.flat.recommended.rules,
      ...react.configs.flat['jsx-runtime'].rules,
      ...reactHooks.configs.flat.recommended.rules,

      // 2. Google JavaScript Style Guide & Coding Standards
      'no-var': 'error',
      'prefer-const': 'error',
      'eqeqeq': ['error', 'always', { 'null': 'ignore' }],
      'no-unused-vars': ['error', { 
        'vars': 'all', 
        'args': 'after-used', 
        'ignoreRestSiblings': true,
        'varsIgnorePattern': '^[A-Z_]' 
      }],

      // Strict Formatting & Code Aesthetics (Google Style Guide)
      'semi': ['error', 'always'],
      'no-multiple-empty-lines': ['error', { 'max': 1, 'maxEOF': 0 }],
      'object-curly-spacing': ['error', 'always'],
      'array-bracket-spacing': ['error', 'never'],
      'space-infix-ops': 'error',
      'arrow-spacing': ['error', { 'before': true, 'after': true }],

      // 3. React & Developer Experience Controls
      'react/prop-types': 'off', // Handled by standard modern React/prop checking preference
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
]);
