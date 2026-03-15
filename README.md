```
microbial-metabolic-economy/
├── README.md              # プロジェクト全体の概要、セットアップ方法、無料スタックの解説
├── LICENSE                # MIT License（OSSとしての公開用）
├── requirements.txt       # 依存ライブラリ（numpy, matplotlib, pandas, streamlit等）
├── .github/
│   └── workflows/         # GitHub Actions（無料の自動デプロイ設定用）
│       └── deploy.yml
│
├── core/                  # 全ゲーム共通の経済計算ロジック
│   ├── __init__.py
│   ├── economy_engine.py  # ATP（通貨）収支、ROI計算、PL管理の基盤クラス [1, 2]
│   └── fba_optimizer.py   # フラックスバランス解析（FBA）による資源配分最適化 [3]
│
├── games/                 # 各学習プログラム（ゲーム）のメインディレクトリ
│   ├── physarum_solver/   # 1. 粘菌ルート最適化エンジン [4, 5]
│   │   ├── main.py        # 実行用スクリプト（Matplotlibアニメーション）
│   │   ├── logic.py       # 正のフィードバック・アポトーシスの実装 [5]
│   │   └── data/          # 住宅街（エサ）の座標データ（JSON）
│   │
│   ├── quorum_consensus/  # 2. クオラム・合意形成エンジン [4, 6]
│   │   ├── app.py         # Streamlit等での可視化画面
│   │   ├── sensing.py     # シグナル濃度勾配と発火閾値の計算 [7]
│   │   └── config.yaml    # 閾値（キャズム）のパラメータ設定
│   │
│   ├── hgt_trader/        # 3. 水平伝播・技術交換所 [6, 8]
│   │   ├── hgt_system.py  # 動的メソッド追加（setattr）によるスキルコピー実装 [9]
│   │   ├── player.py      # 自機（菌株）のクラス定義
│   │   └── library/       # 奪取可能なスキル（遺伝子）のテンプレート
│   │
│   └── red_queen/         # 4. 赤の女王・自動進化セキュリティ [8, 10]
│       ├── security_ga.py # 遺伝的アルゴリズムによる自己修復防御 [11]
│       ├── virus_evo.py   # 攻撃側（ウイルス）の自動変異ロジック
│       └── monitor.py     # 生存率と進化速度のリアルタイム可視化
│
├── notebooks/             # Google Colab用（無料実行環境）
│   ├── tutorial_fba.ipynb # 微生物代謝経済学の基礎学習ノート
│   └── game_demo.ipynb    # 各ゲームをブラウザで即座に試すためのノート
│
└── docs/                  # 設計ドキュメント・学習資料
    ├── design_doc.md      # システム設計詳細
    ├── metabolic_econ.md  # 微生物代謝経済学の理論解説 [1]
    └── assets/            # UI設計図やデモ画像

```

### 1. プロジェクト全体をまとめる「README.md」

このドキュメントは、本プロジェクトが「微生物代謝経済学」という高度に最適化されたアルゴリズムを、いかにビジネスやシステム設計に応用しているかを解説するものです [1, 2]。

```markdown
# Microbial Metabolic Economics (MME) Game Suite

## 概要
本プロジェクトは、微生物の「自我がないゆえの究極の合理性」をアルゴリズム化し、ビジネス戦略やシステム設計を学ぶための4つのシミュレーション・プログラムを提供します [1, 3]。

### コア・コンセプト：微生物代謝経済学
微生物の生存戦略をビジネス用語で再定義しています [1, 4]。
- **ATP（通貨）**: 細胞内のエネルギー。常にPL（損益計算書）として管理されます [4, 5]。
- **アポトーシス（プログラムされた死）**: ROI（投資対効果）が低下した際、集団全体の資源を最大化するために自己を消去する合理的判断 [6, 7]。
- **水平伝播（HGT）**: 学習ではなく、他者の設計図（コード）を直接取り込む爆速の技術取得 [6, 8]。

## 収録プログラム
1. **Physarum Solver (粘菌ルート最適化)**: 最小コストで冗長性の高いインフラを設計する [9, 10]。
2. **Quorum Consensus (合意形成エンジン)**: 多数決に頼らず、シグナル濃度で市場のキャズムを突破する [9, 11]。
3. **HGT Trader (技術交換所)**: M&Aや技術提携を微生物の「コピー＆ペースト」でシミュレートする [12, 13]。
4. **Red Queen Security (自動進化セキュリティ)**: 攻撃者の変異に合わせて防御壁を自動生成し続ける動的防御 [12, 14]。

## セットアップと実行
すべて無料のツール（Python, Google Colab）で動作するように設計されています。

```bash
pip install -r requirements.txt
python app.py
```
```

---

### 2. UIデザインの現状と完成度について

**現状の完成度:** 
これまでのコード出力により、**ロジック（計算部分）と基本的な視覚化（Matplotlib）は100%完成**しています。現在のUIは「シミュレーター（研究ツール）」としての性質が強く、データの推移をグラフで追うには最適です [4]。

**今後のUI発展性:** 
「ゲーム」としての体験を向上させるためには、ブラウザ上でスライダーを用いて、**「シグナル濃度」や「ATP消費率」をリアルタイムで操作できるUI**が必要です [15]。そのため、最後にこれらすべてのモジュールをWeb UIとして統合するコードを作成します。

---

### 3. 次のファイルのコード出力：`app.py` (統合UIランチャー)

このファイルは、これまで作成した4つのプログラムを一つの画面で切り替えて操作・観測できるようにする、Streamlitベースのダッシュボードです。

```python
import streamlit as st
import numpy as np
from games.physarum_solver.engine import PhysarumEngine
from games.quorum_consensus.signaling import QuorumSignaling
from games.hgt_trader.hgt_system import MicrobialStrain, HGTSystem
from games.red_queen_security.evolution_ga import RedQueenDefense

st.set_page_config(page_title="Microbial Economy Suite", layout="wide")

st.title("🧫 微生物代謝経済学 シミュレーター")
st.sidebar.header("プログラム選択")
app_mode = st.sidebar.selectbox("実行するプログラムを選んでください",
    ["Physarum (ルート最適化)", "Quorum (合意形成)", "HGT (技術交換)", "Red Queen (セキュリティ)"])

if app_mode == "Physarum (ルート最適化)":
    st.header("🍄 Physarum Solver")
    st.write("住宅街（エサ）を効率よく結び、無駄なルートをアポトーシスで消去します。")
    # Streamlit用のパラメータ調整
    cost = st.sidebar.slider("インフラ維持コスト", 1.0, 10.0, 2.0)
    if st.button("シミュレーション実行"):
        solver = PhysarumEngine(economy_config={"maintenance_cost": cost})
        solver.add_food_source(10, 10)
        solver.add_food_source(40, 40)
        # ここでvis_matplotlibのロジックをStreamlitのst.pyplotで表示する処理を記述
        st.success("ロジック起動準備完了。詳細は vis_matplotlib.py を実行してください。")

elif app_mode == "Quorum (合意形成)":
    st.header("波及効果の測定: Quorum Consensus")
    threshold = st.sidebar.slider("合意形成の閾値（キャズム）", 0.1, 1.0, 0.6)
    st.info(f"現在の閾値: {threshold}。シグナル濃度がこれを超えると集団行動が発火します。")
    # signaling.pyのロジックを呼び出し、グラフを表示

elif app_mode == "HGT (技術交換)":
    st.header("🧬 Horizontal Gene Trader")
    st.write("他社のスキルを即座にプラグイン（M&A）し、ゲノムを軽量化します。")
    # hgt_system.py を用いた動的スキルの実行ボタンなどを配置

elif app_mode == "Red Queen (セキュリティ)":
    st.header("🏃 赤の女王セキュリティ")
    st.write("攻撃者の進化に追いつかなければ、今の場所にとどまることすらできません。")
    # evolution_ga.py の世代更新をリアルタイムチャートで表示

