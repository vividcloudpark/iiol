export function normalizeIsbn(value) {
  const isbn = String(value ?? '').replace(/[\s-]/g, '');
  if (!/^\d{13}$/.test(isbn)) return { valid: false, error: 'ISBN-13 숫자 13자리를 확인해 주세요.' };
  if (!isbn.startsWith('978') && !isbn.startsWith('979')) {
    return { valid: false, error: '책 ISBN 바코드가 아닙니다. ISBN-13 바코드를 스캔해 주세요.' };
  }
  if (isbn.startsWith('9790')) {
    return { valid: false, error: '9790으로 시작하는 악보용 번호는 ISBN이 아닙니다.' };
  }
  const checksum = [...isbn].reduce((sum, digit, index) => sum + Number(digit) * (index % 2 ? 3 : 1), 0);
  if (checksum % 10 !== 0) return { valid: false, error: 'ISBN 검사 숫자가 맞지 않습니다. 다시 확인해 주세요.' };
  return { valid: true, isbn };
}
