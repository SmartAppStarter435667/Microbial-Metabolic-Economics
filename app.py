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
