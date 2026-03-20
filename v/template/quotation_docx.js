/**
 * 견적서 마크다운 → 워드 변환기
 *
 * 사용법:
 *   node quotation_docx.js <input.md> <output.docx> [config.json]
 *
 * 예시:
 *   node quotation_docx.js doc/d0023_견적.md tmp/reports/견적서.docx
 */

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
        WidthType, ShadingType, VerticalAlign, PageNumber, ImageRun, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

// ============================================================================
// 설정 로드
// ============================================================================
function loadConfig(configPath) {
  const defaultConfig = {
    document: { defaultFont: "맑은 고딕", defaultSize: 22, margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 } },
    styles: {
      title: { size: 48, bold: true, color: "1F4E79", alignment: "center", spacingBefore: 200, spacingAfter: 300 },
      heading1: { size: 32, bold: true, color: "1F4E79", spacingBefore: 400, spacingAfter: 200 },
      heading2: { size: 28, bold: true, color: "2E75B6", spacingBefore: 300, spacingAfter: 150 },
      heading3: { size: 24, bold: true, color: "404040", spacingBefore: 200, spacingAfter: 100 },
      paragraph: { size: 20, spacingAfter: 100 },
      bullet: { size: 20, indent: 720 }
    },
    table: { headerBackground: "E8F4FD", subtotalBackground: "F0F0F0", totalBackground: "FFF3CD", borderColor: "CCCCCC", borderSize: 1, headerSize: 22, cellSize: 20 },
    header: { text: "", size: 18, color: "808080", alignment: "right" },
    footer: { showPageNumber: true, format: "- {current} -", size: 18, alignment: "center" },
    image: { defaultWidth: 100, defaultHeight: 180 },
    signature: { columns: ["작성", "검토", "승인"], rowHeight: 3 }
  };

  if (configPath && fs.existsSync(configPath)) {
    const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    return { ...defaultConfig, ...userConfig };
  }
  return defaultConfig;
}

// ============================================================================
// 마크다운 파서
// ============================================================================
class MarkdownParser {
  constructor(markdown, basePath = '.') {
    this.lines = markdown.split('\n');
    this.basePath = basePath;
    this.index = 0;
  }

  parse() {
    const elements = [];
    while (this.index < this.lines.length) {
      const line = this.lines[this.index];

      // 빈 줄
      if (line.trim() === '') {
        this.index++;
        continue;
      }

      // 구분선
      if (line.match(/^---+$/)) {
        this.index++;
        continue;
      }

      // 제목
      if (line.startsWith('#')) {
        elements.push(this.parseHeading(line));
        this.index++;
        continue;
      }

      // 표
      if (line.startsWith('|')) {
        elements.push(this.parseTable());
        continue;
      }

      // 목록
      if (line.match(/^[-*]\s/) || line.match(/^>\s*[-*]\s/)) {
        elements.push(this.parseBullet(line));
        this.index++;
        continue;
      }

      // 인용문 (설명문으로 처리)
      if (line.startsWith('>')) {
        elements.push(this.parseBlockquote(line));
        this.index++;
        continue;
      }

      // 이미지
      if (line.includes('![') && line.includes('](')) {
        elements.push(this.parseImage(line));
        this.index++;
        continue;
      }

      // 일반 문단
      elements.push(this.parseParagraph(line));
      this.index++;
    }

    return elements;
  }

  parseHeading(line) {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const text = match[2].replace(/\*\*/g, ''); // Bold 마커 제거
      return { type: 'heading', level, text };
    }
    return { type: 'paragraph', text: line };
  }

  parseTable() {
    const rows = [];
    while (this.index < this.lines.length && this.lines[this.index].startsWith('|')) {
      const line = this.lines[this.index];

      // 구분선 (|---|---|) 건너뛰기
      if (line.match(/^\|[\s-:|]+\|$/)) {
        this.index++;
        continue;
      }

      // 셀 파싱
      const cells = line.split('|')
        .slice(1, -1)  // 앞뒤 빈 요소 제거
        .map(cell => cell.trim().replace(/\*\*/g, ''));  // Bold 마커 제거

      rows.push(cells);
      this.index++;
    }

    return { type: 'table', rows };
  }

  parseBullet(line) {
    const text = line.replace(/^>\s*/, '').replace(/^[-*]\s+/, '').replace(/\*\*/g, '');
    return { type: 'bullet', text };
  }

  parseBlockquote(line) {
    const text = line.replace(/^>\s*/, '').replace(/\*\*/g, '');
    if (text.trim() === '') return { type: 'empty' };
    return { type: 'paragraph', text, style: 'blockquote' };
  }

  parseImage(line) {
    const match = line.match(/!\[([^\]]*)\]\(([^)]+)\)/);
    if (match) {
      let src = match[2];
      // 상대 경로를 절대 경로로 변환
      if (!path.isAbsolute(src)) {
        src = path.resolve(this.basePath, src);
      }
      return { type: 'image', alt: match[1], src };
    }
    return { type: 'paragraph', text: line };
  }

  parseParagraph(line) {
    const text = line.replace(/\*\*/g, '');
    return { type: 'paragraph', text };
  }
}

// ============================================================================
// 워드 문서 생성기
// ============================================================================
class WordGenerator {
  constructor(config) {
    this.config = config;
    this.tableBorder = { style: BorderStyle.SINGLE, size: config.table.borderSize, color: config.table.borderColor };
    this.cellBorders = { top: this.tableBorder, bottom: this.tableBorder, left: this.tableBorder, right: this.tableBorder };
  }

  // 헤더 셀 생성
  createHeaderCell(text, width) {
    const safeText = (text || '').toString();
    const safeWidth = width || 1840; // 기본 너비

    return new TableCell({
      borders: this.cellBorders,
      width: { size: safeWidth, type: WidthType.DXA },
      shading: { fill: this.config.table.headerBackground, type: ShadingType.CLEAR },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: safeText, bold: true, size: this.config.table.headerSize, font: this.config.document.defaultFont })]
      })]
    });
  }

  // 데이터 셀 생성
  createDataCell(text, width, align = AlignmentType.LEFT) {
    // 안전 처리
    const safeText = (text || '').toString();
    const safeWidth = width || 1840; // 기본 너비

    // 금액 셀 감지 (원 또는 숫자로 끝나는 경우)
    const isAmount = safeText.match(/[0-9,]+원$/) || safeText === '-' || safeText === '무료';
    const actualAlign = isAmount ? AlignmentType.RIGHT : align;

    // 소계/합계 셀 감지
    const isSubtotal = safeText.includes('소계');
    const isTotal = safeText.includes('합계');

    let shading = undefined;
    if (isSubtotal) {
      shading = { fill: this.config.table.subtotalBackground, type: ShadingType.CLEAR };
    } else if (isTotal) {
      shading = { fill: this.config.table.totalBackground, type: ShadingType.CLEAR };
    }

    return new TableCell({
      borders: this.cellBorders,
      width: { size: safeWidth, type: WidthType.DXA },
      shading,
      children: [new Paragraph({
        alignment: actualAlign,
        children: [new TextRun({
          text: safeText,
          bold: isSubtotal || isTotal,
          size: this.config.table.cellSize,
          font: this.config.document.defaultFont
        })]
      })]
    });
  }

  // 표 생성
  createTable(tableData) {
    if (!tableData.rows || tableData.rows.length === 0) return null;

    // 최대 열 수 계산 (모든 행 중 가장 많은 열)
    const colCount = Math.max(...tableData.rows.map(r => (r || []).length), 1);
    const totalWidth = 9200; // 전체 너비 (DXA)
    const colWidth = Math.floor(totalWidth / colCount);
    const columnWidths = Array(colCount).fill(colWidth);

    const rows = tableData.rows.map((rowData, rowIndex) => {
      const isHeader = rowIndex === 0;
      // 행의 열 수를 colCount에 맞춰 정규화
      const normalizedRow = [...(rowData || [])];
      while (normalizedRow.length < colCount) normalizedRow.push('');

      const cells = normalizedRow.slice(0, colCount).map((cellText, cellIndex) => {
        if (isHeader) {
          return this.createHeaderCell(cellText, columnWidths[cellIndex]);
        } else {
          // 첫 번째 열은 중앙 정렬 (구분, 페이지 등)
          const align = cellIndex === 0 ? AlignmentType.CENTER : AlignmentType.LEFT;
          return this.createDataCell(cellText, columnWidths[cellIndex], align);
        }
      });
      return new TableRow({ children: cells });
    });

    return new Table({ columnWidths, rows });
  }

  // 이미지 테이블 생성 (부록용)
  createImageTable(images) {
    const colCount = images.length;
    const colWidth = Math.floor(9200 / colCount);
    const columnWidths = Array(colCount).fill(colWidth);

    // 헤더 행
    const headerRow = new TableRow({
      children: images.map((img, i) => this.createHeaderCell(`시안 ${i + 1}`, colWidth))
    });

    // 이미지 행
    const imageRow = new TableRow({
      children: images.map(img => {
        if (fs.existsSync(img.src)) {
          return new TableCell({
            borders: this.cellBorders,
            width: { size: colWidth, type: WidthType.DXA },
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new ImageRun({
                type: "png",
                data: fs.readFileSync(img.src),
                transformation: { width: this.config.image.defaultWidth, height: this.config.image.defaultHeight },
                altText: { title: img.alt, description: img.alt, name: img.alt }
              })]
            })]
          });
        } else {
          return this.createDataCell(`[이미지 없음: ${img.alt}]`, colWidth, AlignmentType.CENTER);
        }
      })
    });

    return new Table({ columnWidths, rows: [headerRow, imageRow] });
  }

  // 서명 테이블 생성
  createSignatureTable() {
    const cols = this.config.signature.columns;
    const colWidth = Math.floor(9200 / cols.length);
    const columnWidths = Array(cols.length).fill(colWidth);

    const headerRow = new TableRow({
      children: cols.map(col => this.createHeaderCell(col, colWidth))
    });

    const emptyParagraphs = Array(this.config.signature.rowHeight).fill(null).map(() => new Paragraph({ children: [] }));
    const dataRow = new TableRow({
      children: cols.map(() => new TableCell({
        borders: this.cellBorders,
        width: { size: colWidth, type: WidthType.DXA },
        children: emptyParagraphs
      }))
    });

    return new Table({ columnWidths, rows: [headerRow, dataRow] });
  }

  // 파싱된 요소를 워드 요소로 변환
  convertElements(elements) {
    const docElements = [];
    const images = []; // 부록용 이미지 수집
    let title = '';

    for (const el of elements) {
      switch (el.type) {
        case 'heading':
          if (el.level === 1 && !title) {
            title = el.text;
            docElements.push(new Paragraph({
              heading: HeadingLevel.TITLE,
              children: [new TextRun(el.text)]
            }));
          } else if (el.level === 1) {
            docElements.push(new Paragraph({
              heading: HeadingLevel.HEADING_1,
              children: [new TextRun(el.text)]
            }));
          } else if (el.level === 2) {
            docElements.push(new Paragraph({
              heading: HeadingLevel.HEADING_2,
              children: [new TextRun(el.text)]
            }));
          } else if (el.level === 3 || el.level === 4) {
            docElements.push(new Paragraph({
              heading: HeadingLevel.HEADING_3,
              children: [new TextRun(el.text)]
            }));
          }
          break;

        case 'paragraph':
          if (el.text.trim()) {
            docElements.push(new Paragraph({
              spacing: { after: this.config.styles.paragraph.spacingAfter },
              children: [new TextRun({
                text: el.text,
                size: this.config.styles.paragraph.size,
                font: this.config.document.defaultFont
              })]
            }));
          }
          break;

        case 'bullet':
          docElements.push(new Paragraph({
            numbering: { reference: "bullet-list", level: 0 },
            children: [new TextRun({
              text: el.text,
              size: this.config.styles.bullet.size,
              font: this.config.document.defaultFont
            })]
          }));
          break;

        case 'table':
          const table = this.createTable(el);
          if (table) docElements.push(table);
          docElements.push(new Paragraph({ children: [] })); // 표 뒤 여백
          break;

        case 'image':
          images.push(el);
          break;

        case 'empty':
          break;
      }
    }

    // 부록: 이미지가 있으면 추가
    if (images.length > 0) {
      docElements.push(new Paragraph({ children: [new PageBreak()] }));
      docElements.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록: 앱 디자인 시안")]
      }));
      docElements.push(new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({
          text: "앱 화면 디자인의 시안입니다. 최종 디자인은 협의를 통해 결정됩니다.",
          size: this.config.styles.paragraph.size,
          font: this.config.document.defaultFont
        })]
      }));
      docElements.push(this.createImageTable(images));
    }

    // 서명 테이블
    docElements.push(new Paragraph({ children: [] }));
    docElements.push(new Paragraph({ children: [] }));
    docElements.push(this.createSignatureTable());

    return { docElements, title };
  }

  // 문서 생성
  generate(elements) {
    const { docElements, title } = this.convertElements(elements);

    // 헤더 텍스트 설정
    const headerText = this.config.header.text || title;

    const doc = new Document({
      styles: {
        default: { document: { run: { font: this.config.document.defaultFont, size: this.config.document.defaultSize } } },
        paragraphStyles: [
          { id: "Title", name: "Title", basedOn: "Normal",
            run: { size: this.config.styles.title.size, bold: this.config.styles.title.bold, color: this.config.styles.title.color, font: this.config.document.defaultFont },
            paragraph: { spacing: { before: this.config.styles.title.spacingBefore, after: this.config.styles.title.spacingAfter }, alignment: AlignmentType.CENTER } },
          { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
            run: { size: this.config.styles.heading1.size, bold: this.config.styles.heading1.bold, color: this.config.styles.heading1.color, font: this.config.document.defaultFont },
            paragraph: { spacing: { before: this.config.styles.heading1.spacingBefore, after: this.config.styles.heading1.spacingAfter }, outlineLevel: 0 } },
          { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
            run: { size: this.config.styles.heading2.size, bold: this.config.styles.heading2.bold, color: this.config.styles.heading2.color, font: this.config.document.defaultFont },
            paragraph: { spacing: { before: this.config.styles.heading2.spacingBefore, after: this.config.styles.heading2.spacingAfter }, outlineLevel: 1 } },
          { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
            run: { size: this.config.styles.heading3.size, bold: this.config.styles.heading3.bold, color: this.config.styles.heading3.color, font: this.config.document.defaultFont },
            paragraph: { spacing: { before: this.config.styles.heading3.spacingBefore, after: this.config.styles.heading3.spacingAfter }, outlineLevel: 2 } }
        ]
      },
      numbering: {
        config: [
          { reference: "bullet-list",
            levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: this.config.styles.bullet.indent, hanging: 360 } } } }] }
        ]
      },
      sections: [{
        properties: {
          page: { margin: this.config.document.margin }
        },
        headers: {
          default: new Header({ children: [new Paragraph({
            alignment: this.config.header.alignment === 'right' ? AlignmentType.RIGHT : AlignmentType.CENTER,
            children: [new TextRun({ text: headerText, size: this.config.header.size, color: this.config.header.color, font: this.config.document.defaultFont })]
          })] })
        },
        footers: {
          default: new Footer({ children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "- ", size: this.config.footer.size, font: this.config.document.defaultFont }),
              new TextRun({ children: [PageNumber.CURRENT], size: this.config.footer.size, font: this.config.document.defaultFont }),
              new TextRun({ text: " -", size: this.config.footer.size, font: this.config.document.defaultFont })
            ]
          })] })
        },
        children: docElements
      }]
    });

    return doc;
  }
}

// ============================================================================
// 메인 실행
// ============================================================================
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log('사용법: node quotation_docx.js <input.md> [output.docx] [config.json]');
    console.log('');
    console.log('  output.docx 미지정 시: 입력 파일과 같은 폴더에 같은 이름으로 생성');
    console.log('');
    console.log('예시:');
    console.log('  node quotation_docx.js doc/d0023_견적.md');
    console.log('    → doc/d0023_견적.docx 생성');
    console.log('  node quotation_docx.js doc/d0023_견적.md tmp/reports/견적서.docx');
    console.log('  node quotation_docx.js doc/d0023_견적.md tmp/reports/견적서.docx v/template/custom.json');
    process.exit(1);
  }

  const inputPath = args[0];
  // 출력 경로 미지정 시: 입력 파일과 같은 폴더에 같은 이름(.docx)으로 생성
  const outputPath = args[1] || inputPath.replace(/\.md$/i, '.docx');
  const configPath = args[2] || path.join(__dirname, 'quotation_docx.json');

  // 입력 파일 확인
  if (!fs.existsSync(inputPath)) {
    console.error(`오류: 입력 파일을 찾을 수 없습니다: ${inputPath}`);
    process.exit(1);
  }

  // 설정 로드
  const config = loadConfig(configPath);
  console.log(`설정 로드: ${configPath}`);

  // 마크다운 읽기 및 파싱
  const markdown = fs.readFileSync(inputPath, 'utf-8');
  const basePath = path.dirname(path.resolve(inputPath));
  const parser = new MarkdownParser(markdown, basePath);
  const elements = parser.parse();
  console.log(`마크다운 파싱 완료: ${elements.length}개 요소`);

  // 워드 문서 생성
  const generator = new WordGenerator(config);
  const doc = generator.generate(elements);

  // 출력 디렉토리 생성
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 파일 저장
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`워드 문서 생성 완료: ${outputPath}`);
}

// 모듈 내보내기 (다른 스크립트에서 사용 가능)
module.exports = { MarkdownParser, WordGenerator, loadConfig };

// 직접 실행 시
if (require.main === module) {
  main().catch(err => {
    console.error('오류:', err);
    process.exit(1);
  });
}
