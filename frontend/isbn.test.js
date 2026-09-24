import { describe, expect, it } from 'vitest';
import { normalizeIsbn } from './isbn.js';

describe('ISBN-13 validation', () => {
  it('accepts a valid ISBN with spaces or hyphens', () => {
    expect(normalizeIsbn('978-89-5469-904-4')).toEqual({ valid: true, isbn: '9788954699044' });
  });
  it('rejects an EAN-13 product barcode outside ISBN prefixes', () => {
    expect(normalizeIsbn('1923055034006').valid).toBe(false);
  });
  it('rejects the reserved ISMN prefix', () => {
    expect(normalizeIsbn('9790123456785').valid).toBe(false);
  });
  it('rejects an incorrect check digit', () => {
    expect(normalizeIsbn('9788954699045').valid).toBe(false);
  });
  it('rejects a non-13 digit value', () => {
    expect(normalizeIsbn('97889624752').valid).toBe(false);
  });
});
