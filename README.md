# OSOMA 발표 자료 틀

`merryyear-ai-showcase`의 덱 빌더와 시연물 빌더를 가져와 새로 시작하는 저장소입니다. 완성본 HTML과 PDF,
GA4 원자료, 각종 작업 기록은 가져오지 않았습니다.

## 지금 상태

빌더 코드 안에 열매나눔재단 덱의 문장과 구성이 그대로 들어 있습니다. 새 자료로 바꾸는 일이 첫 작업입니다.
`python3 build_ax.py`를 한 번 돌리면 코드 안의 글이 `본문_AX60.md`로 뽑혀 나옵니다. 이 파일이 화면에 보이는
글 전부이고, 장별로 한 줄에 한 덩이입니다.

첫 빌드는 교정 게이트에서 멈춥니다. 353문장이 승인 기록 없이 새로 들어왔기 때문입니다. 문장을 검수한 뒤
`python3 build_ax.py --approve`로 승인하면 덱이 만들어집니다.

## 덱 만들기

```bash
python3 build_ax.py            # 본문_AX60.md 를 읽어 덱을 만듭니다
python3 build_ax.py --approve  # 대기 문장을 검수하고 고친 뒤 승인합니다
python3 build_ax.py --export   # 코드 쪽 글로 본문_AX60.md 를 다시 뽑습니다. 파일의 수정이 지워집니다
python3 build_ax.py --v2       # 레이아웃 개정본
python3 build_ax.py --all      # 장마다 후보 셋을 놓은 비교 화면
python3 export_pdf.py          # 한 장 한 쪽으로 PDF를 찍습니다. 구글 크롬과 pypdf가 필요합니다
```

글만 고칠 때는 `본문_AX60.md`를 고치고 다시 빌드합니다. 줄을 더하거나 지우면 구조가 어긋나 빌드가 멈추고,
코드 기준 새 추출본을 `본문_AX60.새로추출.md`에 써 줍니다. 장을 더하거나 빼는 일은 빌더에서 합니다.

덱 오른쪽 위 도구 모음에는 발표자 보기, 번호 이동, PDF 내려받기, 전체보기, 편집이 있습니다. 화면에서 고친 글은
브라우저에만 남으므로, 편집 바의 내보내기를 눌러 받은 `편집본_AX60.json`을 `python3 apply_edits.py`로
본문 파일에 되박아야 다음 빌드에 남습니다.

## 파일 구성

```
build_ax.py                덱 빌더. 장 구성과 조립 순서
build_ax_deep.py           본 흐름과 심화 장, 카드 아이콘
build_ax_add.py            조직의 단계, 기록 모으기, 검증 기준, 변화관리 장
build_ax_v2.py             레이아웃 개정본 패치
build_slides.py            공통 CSS, 로고, 금지 기호 검사기, 교정 게이트
build_v2_all.py            장별 후보 비교 화면
build_v2_variants.py       후보 판과 비교 화면의 CSS
v2_layouts.py              후보 판 묶음. 축, 계단, 마주 놓기, 막대, 표
v2_parts.py                원본 장에서 글을 뽑는 추출기와 그림 구획
v2_pick.py                 비교 화면에서 안을 고르고 기록을 남기는 층
v2_sketch.py               손그림 SVG 묶음
sync_text.py               본문_AX60.md 와 덱을 맞추는 모듈
sync_script.py             시연물_대본.md 와 시연물 네 편을 맞춥니다
toolbar.py                 오른쪽 위 도구 모음
apply_edits.py             화면에서 고친 글을 본문 파일로 되박습니다
export_pdf.py              덱을 한 장 한 쪽으로 PDF로 찍습니다
prep_illus.py              삽화 배경을 순백으로 맞춥니다
assets/                    로고, 갈무리, 삽화

시연물/
  extract.py               GA4 조회 9종. 결과는 data/*.json
  campaigns.py             캠페인 이름 정리 규칙
  build_race.py            30일 롤링 계산 후 race_template.html 에 자료를 박습니다
  build_graph.py           부채꼴 배치 계산 후 graph_template.html 에 자료를 박습니다
  build_analog.py          표와 대시보드와 질의 화면
  build_orchestra.py       원격 지휘 연출 화면
  *_template.html          손볼 곳은 이 템플릿입니다
  shot.sh                  헤드리스 크롬 갈무리
```

## 시연물

시연물 빌더와 템플릿은 가져왔지만 `시연물/data/`의 GA4 원자료는 가져오지 않았습니다. 그래서 네 편의 완성본
HTML은 아직 없고, 덱의 임베드 자리는 비어 있습니다. 새 자료를 `시연물/data/`에 채운 뒤 각 빌더를 돌립니다.

```bash
python3 -m venv .venv && ./.venv/bin/pip install -r 시연물/requirements.txt

cd 시연물
../.venv/bin/python3 build_race.py --write
../.venv/bin/python3 build_graph.py
python3 build_analog.py
python3 build_orchestra.py
```

`build_analog.py`와 `build_orchestra.py`는 numpy 없이 돕니다. 덱도 numpy가 필요하지 않습니다.

## 자산

`assets/`는 원본 저장소에서 그대로 가져왔습니다. 열매나눔재단 로고(`merryyear.png`)와 재단 화면 갈무리가
들어 있으니, 새 자료로 갈아 끼우기 전까지는 덱에 재단 것이 보입니다. `build_slides.py`가 불러오기 시점에
로고와 몇몇 이미지를 base64로 박으므로, 파일 이름을 바꾸려면 그 줄도 함께 고칩니다.
