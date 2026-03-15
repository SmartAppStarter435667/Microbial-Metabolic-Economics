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


