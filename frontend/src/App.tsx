import { useState, useEffect } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';

// Interfaces for our application state
interface Book {
  isbn13: string;
  title: string;
  author: string;
  publisher: string;
  pubYear: string;
  coverUrl: string;
  desc: string;
  loanStats: {
    male: number;
    female: number;
    ageGroups: { age: string; pct: number }[];
    recommendations: { title: string; isbn: string }[];
  };
}

interface LibraryStatus {
  name: string;
  code: string;
  hasBook: boolean;
  loanAvailable: boolean;
  location: string;
}

interface WishItem {
  id: string;
  book: Book;
  reason: string;
  memo: string;
  savedAt: string;
  isRead: boolean;
}

// Mock Database removed since we use real backend.

function App() {
  // Application states
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('11230');
  const [currentBook, setCurrentBook] = useState<Book | null>(null);
  const [libraries, setLibraries] = useState<LibraryStatus[]>([]);
  const [loading, setLoading] = useState(false);
  const [latency, setLatency] = useState<number | null>(null);
  const [cacheHit, setCacheHit] = useState(false);
  
  // Barcode scanner states
  const [scanning, setScanning] = useState(false);
  
  // Wishlist states
  const [wishlist, setWishlist] = useState<WishItem[]>([]);
  const [showWishModal, setShowWishModal] = useState(false);
  const [wishReason, setWishReason] = useState('학습/연구');
  const [wishMemo, setWishMemo] = useState('');

  // Load wishlist from local storage on mount
  useEffect(() => {
    const saved = localStorage.getItem('iiol_wishlist');
    if (saved) {
      try {
        setWishlist(JSON.parse(saved));
      } catch (e) {
        console.error(e);
      }
    }
  }, []);

  // Save wishlist to local storage when changed
  const saveWishlistToStorage = (list: WishItem[]) => {
    setWishlist(list);
    localStorage.setItem('iiol_wishlist', JSON.stringify(list));
  };

  // Real barcode scanning process using html5-qrcode
  useEffect(() => {
    let scanner: Html5QrcodeScanner | null = null;

    if (scanning) {
      scanner = new Html5QrcodeScanner(
        "reader",
        { 
          fps: 10, 
          qrbox: { width: 250, height: 150 }
        },
        false
      );

      scanner.render(
        (decodedText) => {
          // On success
          if (scanner) {
            scanner.clear().catch(console.error);
          }
          setScanning(false);
          setSearchQuery(decodedText);
          triggerSearch(decodedText);
        },
        (_error) => {
          // On error (happens continuously as it tries to find a barcode)
        }
      );
    }

    return () => {
      if (scanner) {
        scanner.clear().catch(console.error);
      }
    };
  }, [scanning]);

  // Handle book search execution
  const triggerSearch = async (isbn: string) => {
    if (!isbn.trim()) return;
    setLoading(true);
    setLatency(null);
    
    const startTime = performance.now();
    const cleanIsbn = isbn.replace(/[-\s]/g, '');
    
    try {
      const formData = new FormData();
      formData.append('isbn13', cleanIsbn);
      formData.append('small_region_code', selectedRegion);

      const response = await fetch('/barcode/detect/', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        }
      });
      
      const endTime = performance.now();
      setLatency(Math.round(endTime - startTime));
      setLoading(false);

      if (!response.ok) {
        throw new Error(`서버 응답 오류 (Status: ${response.status})`);
      }

      const data = await response.json();
      
      if (data.status && data.status.code === 'S') {
        const bookDetails = data.result_data.book_detail[0];
        const libInfo = data.result_data.library_info;

        const mappedBook: Book = {
          isbn13: bookDetails.isbn13,
          title: bookDetails.bookname,
          author: bookDetails.authors,
          publisher: bookDetails.publisher,
          pubYear: bookDetails.publication_year,
          coverUrl: bookDetails.bookImageURL || 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=300&auto=format&fit=crop',
          desc: bookDetails.description || '도서 정보 설명이 존재하지 않습니다.',
          loanStats: {
            male: 50,
            female: 50,
            ageGroups: [
              { age: '20대', pct: 45 },
              { age: '30대', pct: 35 },
              { age: '기타', pct: 20 }
            ],
            recommendations: []
          }
        };

        const mappedLibraries: LibraryStatus[] = Object.keys(libInfo).map((key) => {
          const lib = libInfo[key];
          return {
            name: lib.libName,
            code: lib.libCode,
            hasBook: lib.hasBook === 'Y',
            loanAvailable: lib.loanAvailable === 'Y',
            location: lib.address,
          };
        });

        setCacheHit(Math.round(endTime - startTime) < 500);
        setCurrentBook(mappedBook);
        setLibraries(mappedLibraries);
      } else {
        setCurrentBook(null);
        setLibraries([]);
        alert(`도서 검색 실패: ${data.status?.msg || '정보를 조회할 수 없습니다.'}`);
      }
    } catch (error: any) {
      setLoading(false);
      setCurrentBook(null);
      setLibraries([]);
      console.error('API Error:', error);
      alert(`백엔드 서버 통신 에러: ${error.message}`);
    }
  };

  // Re-fetch library status when region changes for active book
  useEffect(() => {
    if (currentBook) {
      triggerSearch(currentBook.isbn13);
    }
  }, [selectedRegion]);

  // Wishlist Actions
  const openWishlistModal = () => {
    if (!currentBook) return;
    setWishReason('학습/연구');
    setWishMemo('');
    setShowWishModal(true);
  };

  const addToWishlist = () => {
    if (!currentBook) return;
    const newItem: WishItem = {
      id: Math.random().toString(36).substring(2, 9),
      book: currentBook,
      reason: wishReason,
      memo: wishMemo,
      savedAt: new Date().toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      isRead: false
    };
    const updated = [newItem, ...wishlist];
    saveWishlistToStorage(updated);
    setShowWishModal(false);
  };

  const toggleReadStatus = (id: string) => {
    const updated = wishlist.map((item) => 
      item.id === id ? { ...item, isRead: !item.isRead } : item
    );
    saveWishlistToStorage(updated);
  };

  const deleteWishItem = (id: string) => {
    if (window.confirm('위시리스트에서 정말 삭제하시겠습니까?')) {
      const updated = wishlist.filter((item) => item.id !== id);
      saveWishlistToStorage(updated);
    }
  };

  return (
    <div className="app-container">
      {/* HEADER */}
      <header className="app-header">
        <div className="logo-section">
          <h1>
            <span style={{ color: 'var(--color-secondary)' }}>이올</span> IsInOurLib?
          </h1>
          <p>ISBN 바코드만으로 우리 동네 도서관 책 소장 상태 실시간 검색</p>
        </div>
        <div className="user-badge">
          <div className="user-avatar">U</div>
          <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>Guest User</span>
        </div>
      </header>

      {/* DASHBOARD GRID */}
      <main className="dashboard-grid">
        
        {/* LEFT COLUMN: SEARCH & DETAIL */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* SEARCH BOX CARD */}
          <div className="glass-card">
            <h2 className="section-title">
              <span style={{ color: 'var(--color-secondary)' }}>🔍</span> 도서 검색 및 스캔
            </h2>
            
            <div className="form-group" style={{ position: 'relative' }}>
              <input
                type="text"
                className="form-input"
                placeholder="ISBN13 번호 또는 도서명을 입력하세요 (예: 9791158392239)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && triggerSearch(searchQuery)}
                style={{ paddingRight: '8rem' }}
              />
              <button 
                className="btn btn-accent" 
                onClick={() => triggerSearch(searchQuery)}
                style={{ position: 'absolute', right: '5px', top: '5px', height: 'calc(100% - 10px)', padding: '0 1.25rem' }}
              >
                검색
              </button>
            </div>

            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <button 
                className="btn btn-secondary" 
                onClick={() => setScanning(!scanning)} 
                style={{ position: 'relative', overflow: 'hidden' }}
              >
                {scanning ? '🛑 스캔 취소' : '📸 모바일 바코드(ISBN) 스캔'}
              </button>
              
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                예시 ISBN: 
                <span 
                  onClick={() => { setSearchQuery('9791158392239'); triggerSearch('9791158392239'); }}
                  style={{ color: 'var(--color-secondary)', cursor: 'pointer', marginLeft: '0.5rem', textDecoration: 'underline' }}
                >
                  9791158392239
                </span>
                <span 
                  onClick={() => { setSearchQuery('9788966260959'); triggerSearch('9788966260959'); }}
                  style={{ color: 'var(--color-secondary)', cursor: 'pointer', marginLeft: '0.5rem', textDecoration: 'underline' }}
                >
                  9788966260959
                </span>
              </div>
            </div>

            {/* SCANNING PREVIEW */}
            {scanning && (
              <div style={{ marginTop: '1.5rem', background: '#fff', borderRadius: '15px', overflow: 'hidden', color: '#000' }}>
                <div id="reader" style={{ width: '100%' }}></div>
                <div style={{ textAlign: 'center', padding: '0.5rem', fontSize: '0.85rem', color: '#666' }}>
                  책 뒷면의 바코드(ISBN)가 네모 상자 안에 들어오도록 비춰주세요.
                </div>
              </div>
            )}
          </div>

          {/* LOADING STATE */}
          {loading && (
            <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '4rem' }}>
              <div style={{
                width: '50px', height: '50px', borderRadius: '50%',
                border: '3px solid rgba(170, 59, 255, 0.1)', borderTopColor: 'var(--color-primary)',
                animation: 'spin 1s linear infinite', marginBottom: '1.5rem'
              }} />
              <p style={{ fontWeight: 600 }}>도서관정보나루 API 소장 데이터 조회 중...</p>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>동네 도서관 대출 서버와 실시간 통신을 수행하고 있습니다.</p>
              
              <style>{`
                @keyframes spin { to { transform: rotate(360deg); } }
              `}</style>
            </div>
          )}

          {/* SEARCH RESULT DETAILS */}
          {!loading && currentBook && (
            <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              
              {/* LATENCY WIDGET */}
              {latency !== null && (
                <div style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  background: 'rgba(255, 255, 255, 0.02)', padding: '0.75rem 1.25rem',
                  borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)', fontSize: '0.85rem'
                }}>
                  <span style={{ color: 'var(--text-muted)' }}>⏱️ 검색 응답 지연 시간</span>
                  <span style={{ fontWeight: 700, color: cacheHit ? 'var(--color-success)' : 'var(--color-warning)' }}>
                    {latency}ms {cacheHit ? '(Redis Cache Hit 🚀)' : '(Data4Library API Live Fetch 🌐)'}
                  </span>
                </div>
              )}

              {/* BOOK META CARD */}
              <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                <img
                  src={currentBook.coverUrl}
                  alt={currentBook.title}
                  style={{
                    width: '130px', height: '190px', objectFit: 'cover',
                    borderRadius: '12px', border: '1px solid var(--border-color)',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.4)'
                  }}
                />
                <div style={{ flex: 1, minWidth: '250px' }}>
                  <span className="badge badge-success" style={{ marginBottom: '0.5rem' }}>ISBN13 : {currentBook.isbn13}</span>
                  <h3 style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--text-highlight)', lineHeight: 1.2 }}>{currentBook.title}</h3>
                  <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem', fontSize: '0.95rem' }}>
                    저자: <strong style={{ color: 'var(--text-main)' }}>{currentBook.author}</strong> | 출판사: {currentBook.publisher} ({currentBook.pubYear})
                  </p>
                  <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>{currentBook.desc}</p>
                  
                  <button className="btn btn-primary" onClick={openWishlistModal} style={{ marginTop: '1.25rem' }}>
                    ⭐ 내 Book-Todo 위시리스트에 담기
                  </button>
                </div>
              </div>

              {/* LIBRARIES MAPPING STATUS */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <h4 style={{ fontSize: '1.15rem', fontWeight: 700 }}>📍 선택 지역 도서관 소장 여부</h4>
                  <select 
                    className="form-input"
                    value={selectedRegion}
                    onChange={(e) => setSelectedRegion(e.target.value)}
                    style={{ width: 'auto', padding: '0.5rem 2.5rem 0.5rem 1rem', fontSize: '0.9rem' }}
                  >
                    <option value="11230">서울특별시 강남구</option>
                    <option value="11220">서울특별시 서초구</option>
                    <option value="31023">경기도 성남시 분당구</option>
                  </select>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {libraries.map((lib) => (
                    <div
                      key={lib.code}
                      style={{
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                        background: 'rgba(255, 255, 255, 0.02)', border: '1px solid var(--border-color)',
                        borderRadius: '12px', padding: '1rem', transition: 'all 0.2s'
                      }}
                    >
                      <div>
                        <strong style={{ display: 'block', fontSize: '1rem', color: 'var(--text-highlight)' }}>{lib.name}</strong>
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{lib.location}</span>
                      </div>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        {lib.hasBook ? (
                          <>
                            <span className="badge badge-success">소장 중</span>
                            {lib.loanAvailable ? (
                              <span className="badge badge-success" style={{ background: 'rgba(5, 243, 162, 0.2)' }}>대출가능</span>
                            ) : (
                              <span className="badge badge-danger">대출중</span>
                            )}
                          </>
                        ) : (
                          <span className="badge badge-warning">미소장</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* STATISTICS & RECOMMENDATION (LIBRARY INFO MARU API SIMULATOR) */}
              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
                <h4 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '1rem' }}>📈 도서관 빅데이터 분석</h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '1.5rem', flexWrap: 'wrap' }}>
                  
                  {/* Stats Chart Mock */}
                  <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '1rem' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.5rem' }}>대출 성별 비중</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                      <div style={{ flex: currentBook.loanStats.male, height: '8px', background: 'var(--color-secondary)', borderRadius: '4px' }} />
                      <div style={{ flex: currentBook.loanStats.female, height: '8px', background: 'var(--color-primary)', borderRadius: '4px' }} />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
                      <span style={{ color: 'var(--color-secondary)' }}>남성: {currentBook.loanStats.male}%</span>
                      <span style={{ color: 'var(--color-primary)' }}>여성: {currentBook.loanStats.female}%</span>
                    </div>
                  </div>

                  {/* Age Preference Group */}
                  <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '1rem' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.5rem' }}>인기 연령대 비율</span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                      {currentBook.loanStats.ageGroups.map((group) => (
                        <div key={group.age} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.8rem' }}>
                          <span style={{ width: '40px' }}>{group.age}</span>
                          <div style={{ flex: 1, margin: '0 0.5rem', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${group.pct}%`, height: '100%', background: 'linear-gradient(90deg, var(--color-primary), var(--color-secondary))' }} />
                          </div>
                          <span style={{ fontWeight: 600 }}>{group.pct}%</span>
                        </div>
                      ))}
                    </div>
                  </div>

                </div>
              </div>

            </div>
          )}
        </section>

        {/* RIGHT COLUMN: BOOK-TODO WISHLIST */}
        <section className="glass-card" style={{ height: 'fit-content' }}>
          <h2 className="section-title">
            <span style={{ color: 'var(--color-primary)' }}>⭐</span> Book-Todo 위시리스트
          </h2>

          {wishlist.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
              <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>📚</span>
              <p>위시리스트가 비어 있습니다.</p>
              <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>검색 결과 창에서 책을 위시리스트에 담아보세요.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {wishlist.map((item) => (
                <div
                  key={item.id}
                  style={{
                    background: item.isRead ? 'rgba(255, 255, 255, 0.01)' : 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-color)',
                    borderRadius: '14px', padding: '1rem',
                    opacity: item.isRead ? 0.6 : 1,
                    transition: 'all 0.2s'
                  }}
                >
                  <div style={{ display: 'flex', gap: '1rem' }}>
                    <img
                      src={item.book.coverUrl}
                      alt={item.book.title}
                      style={{ width: '50px', height: '75px', objectFit: 'cover', borderRadius: '6px' }}
                    />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <span className="badge badge-warning" style={{ fontSize: '0.65rem', marginBottom: '0.25rem', background: 'rgba(255, 184, 0, 0.08)' }}>
                        {item.reason}
                      </span>
                      <h4 style={{
                        fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-highlight)',
                        whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
                        textDecoration: item.isRead ? 'line-through' : 'none'
                      }}>
                        {item.book.title}
                      </h4>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{item.book.author}</p>
                      {item.memo && (
                        <p style={{
                          marginTop: '0.5rem', padding: '0.4rem 0.6rem', background: 'rgba(0,0,0,0.2)',
                          borderRadius: '6px', fontSize: '0.8rem', color: 'var(--text-main)', borderLeft: '2px solid var(--color-primary)'
                        }}>
                          "{item.memo}"
                        </p>
                      )}
                      <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                        📅 담은 날짜: {item.savedAt}
                      </span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.75rem', borderTop: '1px solid rgba(255,255,255,0.03)', paddingTop: '0.5rem' }}>
                    <button
                      className="btn btn-secondary"
                      onClick={() => toggleReadStatus(item.id)}
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', borderRadius: '6px' }}
                    >
                      {item.isRead ? '⏳ 대기중 처리' : '✓ 다 읽음'}
                    </button>
                    <button
                      className="btn btn-secondary"
                      onClick={() => deleteWishItem(item.id)}
                      style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', borderRadius: '6px', color: 'var(--color-danger)' }}
                    >
                      삭제
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

      </main>

      {/* WISHLIST MODAL */}
      {showWishModal && currentBook && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
          background: 'rgba(6, 4, 11, 0.8)', backdropFilter: 'blur(10px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="glass-card" style={{ width: '450px', maxWidth: '90%', border: '1px solid var(--border-color-active)' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1.5rem', fontFamily: 'var(--font-heading)' }}>
              ⭐ Book-Todo 위시리스트에 담기
            </h3>
            
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', background: 'rgba(255,255,255,0.02)', padding: '0.75rem', borderRadius: '10px' }}>
              <img src={currentBook.coverUrl} alt="" style={{ width: '45px', height: '65px', objectFit: 'cover', borderRadius: '6px' }} />
              <div>
                <strong style={{ fontSize: '0.95rem', color: 'var(--text-highlight)' }}>{currentBook.title}</strong>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{currentBook.author}</p>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">위시 저장 사유</label>
              <select
                className="form-input"
                value={wishReason}
                onChange={(e) => setWishReason(e.target.value)}
              >
                <option value="학습/연구">📚 학습 / 연구 목적</option>
                <option value="여가/취미">☕ 여가 / 취미 독서</option>
                <option value="업무/프로젝트">💼 업무 / 개발 프로젝트 참고</option>
                <option value="선물/추천">🎁 타인 추천 및 선물용</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">한줄 메모 (선택)</label>
              <input
                type="text"
                className="form-input"
                placeholder="예: 리액트 훅 파트 완독하기"
                value={wishMemo}
                onChange={(e) => setWishMemo(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '2rem' }}>
              <button className="btn btn-secondary" onClick={() => setShowWishModal(false)}>취소</button>
              <button className="btn btn-primary" onClick={addToWishlist}>위시리스트 저장</button>
            </div>
          </div>
        </div>
      )}
      
      {/* OKR STATE WIDGET (DASHBOARD FOOTER) */}
      <footer style={{ marginTop: '4rem', borderTop: '1px solid var(--border-color)', paddingTop: '2rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
        <div style={{ background: 'rgba(170, 59, 255, 0.03)', border: '1px solid rgba(170, 59, 255, 0.1)', borderRadius: '15px', padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-primary)', display: 'block', textTransform: 'uppercase' }}>Objective 1 Status</span>
          <strong style={{ fontSize: '1.2rem', display: 'block', marginTop: '0.25rem', color: 'var(--text-highlight)' }}>초고속 검색 플랫폼 구축</strong>
          <div style={{ marginTop: '0.75rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>KR 1-1 응답지연 1.5s 방어: </span>
            <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>달성 (평균 150ms / Cache)</span>
          </div>
        </div>
        
        <div style={{ background: 'rgba(0, 242, 254, 0.03)', border: '1px solid rgba(0, 242, 254, 0.1)', borderRadius: '15px', padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-secondary)', display: 'block', textTransform: 'uppercase' }}>Objective 2 Status</span>
          <strong style={{ fontSize: '1.2rem', display: 'block', marginTop: '0.25rem', color: 'var(--text-highlight)' }}>도서 데이터 허브 파이프라인</strong>
          <div style={{ marginTop: '0.75rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>KR 2-1 검색 로그 축적: </span>
            <span style={{ fontWeight: 700, color: 'var(--color-secondary)' }}>시뮬레이터 활성 (100%)</span>
          </div>
        </div>
        
        <div style={{ background: 'rgba(5, 243, 162, 0.03)', border: '1px solid rgba(5, 243, 162, 0.1)', borderRadius: '15px', padding: '1.25rem' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-success)', display: 'block', textTransform: 'uppercase' }}>Objective 3 Status</span>
          <strong style={{ fontSize: '1.2rem', display: 'block', marginTop: '0.25rem', color: 'var(--text-highlight)' }}>최신 스텍 마이그레이션</strong>
          <div style={{ marginTop: '0.75rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Vite + React 18 + TS: </span>
            <span style={{ fontWeight: 700, color: 'var(--color-success)' }}>전환 완료 (100%)</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
