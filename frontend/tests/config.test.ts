import { expect, test } from 'vitest';
import config from '../vite.config';

test('development and preview forward relative API requests to Parallax on its own port', () => {
  for (const server of [config.server, config.preview]) {
    expect(server?.proxy?.['/api']).toBe('http://127.0.0.1:8001');
    expect(server?.strictPort).toBe(true);
  }
  expect(config.server?.port).toBe(5174);
  expect(config.preview?.port).toBe(4174);
});
