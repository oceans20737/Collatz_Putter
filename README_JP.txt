# Base-3 Putter Shot: Friction Dynamics in the Shiftless Collatz Model  
*“Hunting the truth of the Collatz Conjecture on the base-3 Green”*

**Author:** Hiroshi Harada  
**License:** MIT License  
**Date:** March 29, 2026  

---

## 概要 (Overview)
このリポジトリは、**Shiftless（シフトなし）Collatz モデル**と **3進極座標（base-3 polar coordinates）** の視点からコラッツ予想の軌道を探索するための、Python ビジュアライザ（静止画版 & アニメーション版）のセットを提供する。

数学的な変換を **対数螺旋グリーン上のダイナミックな「パット（Putter Shot）」** として捉えることで、最下位ビット（LSB）が物理的な摩擦係数  
$$\mu_k = \frac{\mathrm{LSB}}{B_{k+1}}$$
としてどのように作用し、軌道を曲げ、最終的に純粋な 2 の冪乗（$2^M$）のカップへ沈ませるのかを視覚的に観察できる。

---

## 主な機能 (Key Features)
- **ビリヤード・スタイルのアニメーション：** 各ステップにおける「情報の衝突」を視覚的に表現する、重厚な動的レンダリング。

- **オーバーフロー装甲 (Overflow Armor)：** 天文学的な巨大整数でも `OverflowError` を回避して安全に対数計算を実行。  
  巨大なシードのハントを可能にする。

- **スケールの完全固定 (Scale Locking)：** 極座標軸の最大値を事前に固定することで、最終フラッグ展開時にも画面が一切ブレない安定性を実現。

- **デュアル・エクスポート：** `tqdm` のプログレスバー付きで、MP4（`ffmpeg` 必須）と GIF（Pillow）を標準サポート。

---

## 図の見方 (Visual Guide)
- **対数螺旋グリーン（背景）：** 3 進極座標系。  
  半径：整数の対数スケール（$r = \log_3 n$）  
  角度：3 進位相（$\theta = 2\pi\{\log_3 n\}$）

- **白い星の井戸（White Starry Wells）：** 純粋な 2 の冪乗（$2^N$）。  
  グリーン上に無数に散らばる「カップ」。

- **軌道（カラーの線）：** Shiftless Collatz 数列の離散ステップ。

- **摩擦ヒートマップ（$\mu_k$）：** 軌道の色と太さは LSB 摩擦係数  
  $$\mu_k = \frac{\mathrm{LSB}}{B_{k+1}}$$
  によって決まる。

  - **シアン / 細い線：** 低摩擦。歴史的慣性が支配的で、軌道はスムーズに進む。  
  - **マゼンタ / 太い線：** 高摩擦。強力な LSB の介入による鋭いターン。  
    「情報の衝突」を象徴する。

- **イエローフラッグと星：** 最終ジャックポット。  
  数列が純粋な 2 の冪乗（$2^M$）に到達し、カップインしてショットが終了したことを示す。

---

## 必要な環境 (Requirements)
以下の Python パッケージが必要：

```bash
pip install numpy matplotlib tqdm
```

※ 高品質 MP4 を出力する場合は、システムに **ffmpeg** が必要。

---

## 使い方 (Usage)
ターミナルまたは Jupyter Notebook でスクリプトを実行するだけ。

`seed` を変更すると、まったく異なる軌道のハントが始まる。

```python
# ハントしたいシード値に変更する
seed = 27
```

---
