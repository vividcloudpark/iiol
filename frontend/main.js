import { BarcodeFormat, BrowserMultiFormatReader } from '@zxing/browser';
import { normalizeIsbn } from './isbn.js';

const form = document.querySelector('#search-form');
const provinceSelect = document.querySelector('#province-select');
const regionSelect = document.querySelector('#region-select');
const isbnInput = document.querySelector('#isbn-input');
const video = document.querySelector('#camera-video');
const cameraFrame = document.querySelector('#camera-frame');
const cameraStatus = document.querySelector('#camera-status');
const results = document.querySelector('#results');
const startButton = document.querySelector('#start-camera');
const stopButton = document.querySelector('#stop-camera');
const photoInput = document.querySelector('#barcode-photo');
const searchButton = document.querySelector('#search-button');

const regionDataElement = document.querySelector('#region-data');
const regions = regionDataElement ? JSON.parse(regionDataElement.textContent) : { big: {}, small: {} };
let stream = null;
let zxingControls = null;
let active = false;
let reader = null;
let nativeTimer = null;

function setStatus(message, kind = '') {
  cameraStatus.textContent = message;
  cameraStatus.dataset.kind = kind;
}

function populateProvinces() {
  Object.entries(regions.big).forEach(([code, name]) => {
    const option = new Option(name, code);
    provinceSelect.add(option);
  });
  provinceSelect.addEventListener('change', populateLocalRegions);
  regionSelect.addEventListener('change', () => {
    regionSelect.setCustomValidity(regionSelect.value ? '' : '검색할 시·군·구를 선택해 주세요.');
  });
  if (window.IIOL_PROFILE_REGION) {
    provinceSelect.value = window.IIOL_PROFILE_REGION.slice(0, 2);
  }
  populateLocalRegions();
  if (window.IIOL_PROFILE_REGION) regionSelect.value = window.IIOL_PROFILE_REGION;
}

function populateLocalRegions() {
  regionSelect.replaceChildren(new Option('시·군·구 선택', ''));
  const localRegions = regions.small[provinceSelect.value] || {};
  Object.entries(localRegions).forEach(([code, name]) => regionSelect.add(new Option(name, code)));
  regionSelect.value = '';
  regionSelect.setCustomValidity('검색할 시·군·구를 선택해 주세요.');
}

function stopCamera() {
  active = false;
  if (nativeTimer) window.clearTimeout(nativeTimer);
  nativeTimer = null;
  if (zxingControls) {
    zxingControls.stop();
    zxingControls = null;
  }
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }
  video.srcObject = null;
  cameraFrame.hidden = true;
  startButton.disabled = false;
}

function acceptIsbn(value) {
  const checked = normalizeIsbn(value);
  if (!checked.valid) {
    setStatus(checked.error, 'error');
    return false;
  }
  isbnInput.value = checked.isbn;
  setStatus(`ISBN ${checked.isbn}을 읽었습니다. 번호를 확인한 뒤 도서관 찾기를 눌러주세요.`, 'success');
  stopCamera();
  isbnInput.focus();
  return true;
}

function getReader() {
  if (!reader) {
    reader = new BrowserMultiFormatReader(undefined, { delayBetweenScanAttempts: 150 });
    reader.possibleFormats = [BarcodeFormat.EAN_13];
  }
  return reader;
}

async function useZxingCamera() {
  if (!active) return;
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
  }
  setStatus('ISBN 바코드를 찾고 있어요. 책 뒷면을 화면 안에 맞춰주세요.');
  try {
    zxingControls = await getReader().decodeFromVideoDevice(undefined, video, (_result, error) => {
      if (!active) return;
      if (_result) acceptIsbn(_result.getText());
      else if (error && error.name !== 'NotFoundException' && error.name !== 'ChecksumException' && error.name !== 'FormatException') {
        setStatus('바코드 인식이 중단되었습니다. 사진이나 직접 입력을 이용해 주세요.', 'error');
      }
    });
  } catch (error) {
    setStatus(error.name === 'NotAllowedError'
      ? '카메라 권한이 꺼져 있습니다. 사진 업로드나 ISBN 직접 입력을 이용해 주세요.'
      : '카메라를 열 수 없습니다. HTTPS 연결과 카메라 권한을 확인해 주세요.', 'error');
    stopCamera();
  }
}

async function scanWithNativeDetector(detector, startedAt) {
  if (!active) return;
  if (Date.now() - startedAt > 6500) {
    await useZxingCamera();
    return;
  }
  try {
    const found = await detector.detect(video);
    const valid = found.map((item) => normalizeIsbn(item.rawValue)).filter((item) => item.valid);
    if (valid.length === 1) {
      acceptIsbn(valid[0].isbn);
      return;
    }
    if (valid.length > 1) {
      setStatus('ISBN 바코드가 여러 개 보입니다. 하나만 화면에 맞춰주세요.');
    }
  } catch {
    await useZxingCamera();
    return;
  }
  nativeTimer = window.setTimeout(() => scanWithNativeDetector(detector, startedAt), 180);
}

async function startCamera() {
  if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
    setStatus('카메라 스캔은 HTTPS 연결이 필요합니다. 사진이나 직접 입력을 이용해 주세요.', 'error');
    return;
  }
  cameraFrame.hidden = false;
  startButton.disabled = true;
  active = true;
  setStatus('카메라 권한을 기다리고 있어요.');
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: { facingMode: { ideal: 'environment' }, width: { ideal: 1280 }, height: { ideal: 720 } },
    });
    video.srcObject = stream;
    await video.play();
    const Detector = window.BarcodeDetector;
    const supportedFormats = Detector && typeof Detector.getSupportedFormats === 'function'
      ? await Detector.getSupportedFormats().catch(() => [])
      : [];
    if (Detector && supportedFormats.includes('ean_13')) {
      const detector = new Detector({ formats: ['ean_13'] });
      setStatus('ISBN 바코드를 화면 안에 맞춰주세요.');
      scanWithNativeDetector(detector, Date.now());
    } else {
      await useZxingCamera();
    }
  } catch (error) {
    setStatus(error.name === 'NotAllowedError'
      ? '카메라 권한이 거부되었습니다. 사진 업로드나 ISBN 직접 입력을 이용해 주세요.'
      : '카메라를 사용할 수 없습니다. 사진 업로드나 ISBN 직접 입력을 이용해 주세요.', 'error');
    stopCamera();
  }
}

function appendText(parent, tag, text, className) {
  const element = document.createElement(tag);
  element.textContent = text;
  if (className) element.className = className;
  parent.append(element);
  return element;
}

function renderSearchResult(data) {
  results.replaceChildren();
  const card = document.createElement('article');
  card.className = 'result-card';
  appendText(card, 'p', `${data.region_name} 검색 결과`, 'result-region');
  const book = data.book || {};
  appendText(card, 'h3', book.bookname || '도서 정보를 찾았습니다.');
  appendText(card, 'p', [book.authors, book.publisher, book.publication_year].filter(Boolean).join(' · '), 'book-meta');
  appendText(card, 'p', `ISBN ${data.isbn13}`, 'isbn-result');

  const count = data.libraries.length;
  appendText(card, 'h4', count ? `소장 도서관 ${count}곳` : '소장 도서관을 찾지 못했습니다.');
  if (count) {
    const list = document.createElement('ul');
    list.className = 'library-list';
    data.libraries.forEach((library) => {
      const item = document.createElement('li');
      const details = document.createElement('div');
      appendText(details, 'strong', library.name);
      if (library.address) appendText(details, 'span', library.address, 'library-address');
      const status = library.loan_available === true ? '대출 가능' : library.loan_available === false ? '대출 중 또는 대출 불가' : '대출 상태 확인 불가';
      const label = library.has_book === false ? '소장 정보 없음' : status;
      appendText(item, 'span', label, `availability ${library.loan_available === true && library.has_book !== false ? 'available' : ''}`);
      item.prepend(details);
      list.append(item);
    });
    card.append(list);
    appendText(card, 'p', `대출 상태는 ${data.availability_as_of} 기준입니다. 참여 도서관 자료만 표시됩니다.`, 'data-note');
  } else {
    appendText(card, 'p', '정보나루 참여 도서관에서 확인한 결과입니다. 참여하지 않는 도서관의 소장 여부는 포함되지 않을 수 있어요.', 'data-note');
  }
  results.append(card);
}

async function submitSearch(event) {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const checked = normalizeIsbn(isbnInput.value);
  if (!checked.valid) {
    setStatus(checked.error, 'error');
    isbnInput.focus();
    return;
  }
  isbnInput.value = checked.isbn;
  results.replaceChildren();
  searchButton.disabled = true;
  searchButton.textContent = '찾는 중…';
  appendText(results, 'p', '지역 도서관을 검색하고 있어요.', 'loading-message');
  const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;
  try {
    const response = await fetch(form.dataset.searchUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
      body: JSON.stringify({ isbn13: checked.isbn, region_code: regionSelect.value }),
      credentials: 'same-origin',
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || '도서관 검색에 실패했습니다.');
    renderSearchResult(data);
  } catch (error) {
    results.replaceChildren();
    appendText(results, 'p', error.message, 'error-message');
  } finally {
    searchButton.disabled = false;
    searchButton.textContent = '도서관 찾기';
  }
}

async function readPhoto(file) {
  if (!file) return;
  setStatus('사진에서 ISBN 바코드를 찾고 있어요.');
  const url = URL.createObjectURL(file);
  const image = new Image();
  try {
    image.src = url;
    await image.decode();
    const result = await getReader().decodeFromImageElement(image);
    acceptIsbn(result.getText());
  } catch {
    setStatus('사진에서 ISBN을 읽지 못했습니다. 바코드를 크게 촬영하거나 직접 입력해 주세요.', 'error');
  } finally {
    URL.revokeObjectURL(url);
    photoInput.value = '';
  }
}

populateProvinces();
startButton.addEventListener('click', startCamera);
stopButton.addEventListener('click', () => {
  stopCamera();
  setStatus('카메라를 닫았습니다.');
});
photoInput.addEventListener('change', (event) => readPhoto(event.target.files?.[0]));
form.addEventListener('submit', submitSearch);
window.addEventListener('pagehide', stopCamera);
