#!/usr/bin/env python3
"""카드 대신 일러스트를 세우는 장의 그림을 판형에 맞게 다듬는다.

힉스필드에서 받은 원본은 배경색이 미세하게 다르고 오브제 크기와 위치도 제각각이다.
배경을 순백으로 맞추고, 한 장 안의 그림끼리 크기가 같아 보이게 고른 뒤, 같은 캔버스에 바닥 기준으로 앉힌다.
슬라이드에서는 mix-blend-mode:multiply로 얹어 카드 그라데이션 위에 자연스럽게 놓이게 한다.

사용법: python3 prep_illus.py
입력: assets/illus/src/<묶음>_<번호>.png
출력: assets/illus/<묶음>_<번호>.png
"""
import pathlib

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "assets" / "illus"
SRC = OUT / "src"

# 한 장에 나란히 서는 그림끼리만 크기를 맞춘다. 장이 다르면 칸 폭도 달라서다.
GROUPS = {
    "sowhat": 3,   # 53장 So What
    "debt": 3,     # 24장 세 가지 부채
    "force": 5,    # 44장 다섯 가지 힘
}

OUT_W, OUT_H = 1080, 720   # 3:2 판형
MAX_W, MAX_H = 0.94, 0.86  # 캔버스 대비 오브제가 넘지 않을 한계
BOTTOM = 0.05              # 바닥 여백 비율
THRESH = 9                 # 배경과 다르다고 볼 최소 차이


WHITE_FULL = 249   # 이 값보다 밝으면 순백으로 본다
WHITE_KEEP = 244   # 이 값보다 어두우면 원본을 그대로 둔다


def normalize_bg(img):
    """네 모서리에서 배경색을 읽어 순백으로 끌어올린다.

    원본 배경에는 옅은 명암 차가 남아 있다. multiply로 얹으면 그만큼 카드가 어두워져
    그림 자리에 네모가 비친다. 거의 흰 화소만 완전한 흰색으로 밀어 그 자국을 없앤다.
    그림자는 이 구간보다 어두워서 그대로 남는다.
    """
    a = np.asarray(img).astype(np.float32)
    h, w, _ = a.shape
    k = max(8, min(h, w) // 40)
    corners = np.concatenate([
        a[:k, :k].reshape(-1, 3), a[:k, -k:].reshape(-1, 3),
        a[-k:, :k].reshape(-1, 3), a[-k:, -k:].reshape(-1, 3),
    ])
    bg = np.median(corners, axis=0)
    a = np.clip(a * (255.0 / bg), 0, 255)

    keep = np.clip((WHITE_FULL - a.min(axis=2)) / (WHITE_FULL - WHITE_KEEP), 0, 1)[..., None]
    a = a * keep + 255.0 * (1 - keep)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), bg


MINOR = 0.06   # 가장 큰 덩어리의 이 비율에 못 미치면 자국으로 보고 버린다


def main_run(counts, span):
    """줄별 화소 수에서 본체가 놓인 구간을 골라 낸다.

    원본에 오브제와 떨어진 옅은 자국이 남는 일이 있다. 그대로 두면 잘라내기 상자가 커져
    정작 그림이 작아진다. 빈 줄로 갈라진 덩어리를 나눈 뒤, 화소가 눈에 띄게 적은 덩어리만 버린다.
    떠 있는 종이처럼 구도에 필요한 조각은 화소가 많아 그대로 남는다.
    """
    floor = max(3, span // 500)          # 이만큼도 안 되면 빈 줄로 본다
    gap = max(6, len(counts) // 200)     # 이만큼 이어서 비면 덩어리를 나눈다
    runs, start, empty = [], None, 0
    for i, c in enumerate(counts):
        if c > floor:
            if start is None:
                start = i
            empty = 0
        elif start is not None:
            empty += 1
            if empty >= gap:
                runs.append((start, i - empty + 1))
                start, empty = None, 0
    if start is not None:
        runs.append((start, len(counts)))
    if not runs:
        return 0, len(counts)
    mass = [counts[a:b].sum() for a, b in runs]
    kept = [r for r, m in zip(runs, mass) if m >= max(mass) * MINOR]
    return kept[0][0], kept[-1][1]


def content_box(img):
    """배경과 다른 화소를 감싸는 사각형을 찾는다. 그림자도 포함한다."""
    a = np.asarray(img).astype(np.int16)
    mask = np.abs(255 - a).max(axis=2) > THRESH
    y0, y1 = main_run(mask.sum(axis=1), mask.shape[1])
    x0, x1 = main_run(mask[y0:y1].sum(axis=0), mask.shape[0])
    return x0, y0, x1, y1


def prepare(name):
    src = Image.open(SRC / name).convert("RGB")
    img, bg = normalize_bg(src)
    crop = img.crop(content_box(img))
    return crop, bg


def common_size(crops):
    """가로로 퍼진 그림과 세로로 선 그림이 같은 크기로 보이게, 넓이를 기준으로 배율을 맞춘다.

    높이만 맞추면 가로로 긴 그림이 훨씬 커 보이고, 폭만 맞추면 반대가 된다.
    한 묶음의 넓이 제곱근을 같은 값으로 두고, 그 값은 캔버스 한계에 걸리지 않는 최대치로 잡는다.
    """
    limits = []
    for c in crops:
        ratio = c.width / c.height                       # 가로 대 세로
        side = (c.width * c.height) ** 0.5               # 넓이 제곱근
        limits.append(min(OUT_W * MAX_W / (side * ratio ** 0.5),
                          OUT_H * MAX_H / (side / ratio ** 0.5)) * side)
    return min(limits)


def place(crop, side, out_name):
    scale = side / (crop.width * crop.height) ** 0.5
    new = crop.resize((max(1, round(crop.width * scale)),
                       max(1, round(crop.height * scale))), Image.LANCZOS)
    canvas = Image.new("RGB", (OUT_W, OUT_H), (255, 255, 255))
    canvas.paste(new, ((OUT_W - new.width) // 2,
                       max(0, OUT_H - int(OUT_H * BOTTOM) - new.height)))
    canvas.save(OUT / out_name, optimize=True)
    return new.size


if __name__ == "__main__":
    for group, count in GROUPS.items():
        names = [f"{group}_{i}.png" for i in range(1, count + 1)]
        missing = [n for n in names if not (SRC / n).exists()]
        if missing:
            print(f"{group}: 원본이 없어 건너뜁니다 ({', '.join(missing)})")
            continue
        prepared = [prepare(n) for n in names]
        side = common_size([c for c, _ in prepared])
        for name, (crop, bg) in zip(names, prepared):
            size = place(crop, side, name)
            print(f"{name}: 배경 {bg.round(1).tolist()} → 잘라낸 크기 {crop.size} → 앉힌 크기 {size}")


# ── 어두운 카드에 얹는 가로 배너 ──────────────────────────────────
# 08장의 커뮤니티 글 카드는 짙은 남색이라 multiply로는 그림이 묻힌다. 배경을 카드색으로
# 옮겨 이음새를 없애고, 인물이 있는 띠만 남기고 위아래를 잘라 배너로 만든다.
BANNERS = {"adrift_a": "adrift"}
CARD_BG = (22, 26, 36)   # #161A24. 카드 배경과 같은 값
BANNER_W = 1600
BANNER_PAD = 80          # 내용 위아래로 남기는 여백(원본 픽셀)


def prep_banner(name, out_name):
    src = SRC / f"{name}.png"
    if not src.exists():
        return
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    bg = a[:40].reshape(-1, 3).mean(0)
    a = np.clip(a + (np.array(CARD_BG) - bg), 0, 255).astype(np.uint8)

    ink = np.abs(a.astype(int) - CARD_BG).sum(2) > 40
    rows = np.flatnonzero(ink.sum(1) > 30)
    cols = np.flatnonzero(ink.sum(0) > 20)
    top = max(0, int(rows[0]) - BANNER_PAD)
    bottom = min(a.shape[0], int(rows[-1]) + BANNER_PAD)
    left = max(0, int(cols[0]) - BANNER_PAD)
    right = min(a.shape[1], int(cols[-1]) + BANNER_PAD)

    out = Image.fromarray(a[top:bottom, left:right])
    out = out.resize((BANNER_W, round(out.height * BANNER_W / out.width)), Image.LANCZOS)
    out.save(OUT / f"{out_name}.png", optimize=True)
    print(f"  {out_name}.png  {out.width}x{out.height}")


# 판을 통째로 채우는 그림. 자르지 않고 폭만 줄인다.
SHOTS = {"s08_new": "s08"}
SHOT_W = 1000   # 화면에 660쯤으로 놓이므로 두 배면 넉넉하다


def prep_shot(name, out_name):
    src = SRC / f"{name}.png"
    if not src.exists():
        return
    im = Image.open(src).convert("RGB")
    im = im.resize((SHOT_W, round(im.height * SHOT_W / im.width)), Image.LANCZOS)
    im.save(OUT / f"{out_name}.png", optimize=True)
    print(f"  {out_name}.png  {im.width}x{im.height}")


def main_shots():
    print("판을 채우는 그림")
    for name, out_name in SHOTS.items():
        prep_shot(name, out_name)


def main_banners():
    print("어두운 배너")
    for name, out_name in BANNERS.items():
        prep_banner(name, out_name)


if __name__ == "__main__":
    main_banners()
    main_shots()
