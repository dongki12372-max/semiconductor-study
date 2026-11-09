/* 챕터 목록. 새 챕터를 추가할 때 여기에 한 줄 넣는다.
   file 이 null 이면 "준비 중" 카드로 표시된다.
   (fetch 없이 <script>로 읽으므로 file:// 에서도 동작) */
window.BOOK = {
  title: '반도체·식각 자습 교재',
  subtitle: '식각 엔지니어가 알아야 할 만큼, 물리 언어로',
  parts: [
    { id: 'p1', label: 'PART 1 · 반도체 기초' },
    { id: 'p2', label: 'PART 2 · 플라즈마 식각 원리' },
    { id: 'p3', label: 'PART 3 · 식각 장비' },
    { id: 'p4', label: 'PART 4 · 세메스 MICHELAN O5 스펙 해부' }
  ],
  chapters: [
    { id: 'ch1', part: 'p1', no: '1장', title: '반도체 재료와 트랜지스터', file: 'ch1.html',
      desc: '밴드갭, 실리콘과 열산화, 도핑·PN 접합, MOSFET, 스케일링, Planar → FinFET → GAA → CFET' },
    { id: 'ch2', part: 'p1', no: '2장', title: 'DRAM', file: null,
      desc: '1T1C 셀, 커패시터 HARC 식각, 매립 워드라인, 4F<sup>2</sup>, VCT, 3D DRAM' },
    { id: 'ch3', part: 'p1', no: '3장', title: '낸드·V-NAND', file: null },
    { id: 'ch4', part: 'p1', no: '4장', title: 'HBM', file: null },
    { id: 'ch5', part: 'p1', no: '5장', title: '공정 흐름', file: null },
    { id: 'ch6', part: 'p1', no: '6장', title: '식각 기술의 과거·현재·미래', file: null },
    { id: 'p2', part: 'p2', no: 'Part 2', title: '플라즈마 식각 원리', file: null },
    { id: 'p3', part: 'p3', no: 'Part 3', title: '식각 장비', file: null },
    { id: 'p4', part: 'p4', no: 'Part 4', title: '세메스 MICHELAN O5 스펙 해부', file: null }
  ]
};
