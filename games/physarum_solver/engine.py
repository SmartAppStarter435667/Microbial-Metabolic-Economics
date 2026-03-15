import numpy as np
import random
from core.economy import EconomyEngine

class PhysarumEngine:
    """
    粘菌ルート最適化エンジン (Physarum Solver)
    
    役割: 
    1. 空間上の「エサ（住宅街）」を探索するエージェントの制御
    2. 正のフィードバックによる通信路（管）の強化
    3. 負のフィードバック（アポトーシス）による無駄なルートの消去
    """

    def __init__(self, width=100, height=100, economy_config=None):
        self.width = width
        self.height = height
        # 通信路（管）の太さを保持するマップ（数値化されたインフラ）
        self.tube_map = np.zeros((width, height))
        # 住宅街（エサ）の座標リスト
        self.food_sources = []
        
        # 微生物代謝経済エンジンの統合
        config = economy_config if economy_config else {"initial_atp": 500.0, "maintenance_cost": 2.0}
        self.economy = EconomyEngine(**config)

    def add_food_source(self, x, y, reward_value=50.0):
        """住宅街（エサ）を配置 [1]"""
        self.food_sources.append({'pos': (x, y), 'reward': reward_value})

    def grow_step(self, exploration_rate=0.1):
        """
        1ステップの成長シミュレーション
        """
        if not self.economy.is_alive:
            return False

        new_tube_map = self.tube_map.copy()
        total_gained_energy = 0.0

        # 1. 探索と正のフィードバック: エサに向かってルートを太くする [2]
        for food in self.food_sources:
            fx, fy = food['pos']
            # 簡易的な勾配降下法によるルート探索（実際は多点エージェントが望ましいがコアロジックとして実装）
            # エサの周囲の既存の「管」を強化
            self._strengthen_route(fx, fy, food['reward'])
            
            # エサに到達している場合のエネルギー獲得（ROIの源泉） [1]
            if self.tube_map[fx, fy] > 0.5:
                total_gained_energy += food['reward'] * 0.1

        # 2. 経済エンジンの更新（ATP消費とアポトーシスの判定） [1, 3]
        # 維持コストは管の総面積（インフラ維持費）に比例させる
        active_tubes_count = np.count_nonzero(self.tube_map > 0.1)
        dynamic_cost = active_tubes_count * 0.01 
        self.economy.maintenance_cost = 2.0 + dynamic_cost
        
        self.economy.update_cycle(total_gained_energy)

        # 3. 負のフィードバック（アポトーシス）: 効率の悪いルートを細くし、消去する [1, 2]
        # ROIが低い場合、縮小速度を速める
        decay_rate = 0.95 if self.economy.is_alive else 0.5
        self.tube_map *= decay_rate
        
        # 閾値を下回った管は完全に消去（プログラムされた死） [2, 4]
        self.tube_map[self.tube_map < 0.05] = 0

        # 4. ゆらぎ（確率的変動）: 人間が思いつかない裏道の探索 [2]
        if random.random() < exploration_rate:
            rx, ry = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.tube_map[rx, ry] += 0.5

        return self.economy.is_alive

    def _strengthen_route(self, tx, ty, strength):
        """特定の座標周辺のルートを強化する内部メソッド"""
        # 周囲3x3に正のフィードバックを与える
        x_start = max(0, tx-1)
        x_end = min(self.width, tx+2)
        y_start = max(0, ty-1)
        y_end = min(self.height, ty+2)
        self.tube_map[x_start:x_end, y_start:y_end] += strength * 0.05
        # 最大太さ（容量）の制限
        self.tube_map = np.clip(self.tube_map, 0, 10.0)

    def get_network_stats(self):
        """現在のネットワークの冗長性とコストを返す [1]"""
        return {
            "total_infrastructure_cost": np.sum(self.tube_map),
            "active_routes": np.count_nonzero(self.tube_map > 0.5),
            "economy_status": self.economy.get_status()
        }

# 使用例
if __name__ == "__main__":
    solver = PhysarumEngine(width=50, height=50)
    solver.add_food_source(10, 10) # 住宅街A
    solver.add_food_source(40, 40) # 住宅街B
    
    for i in range(20):
        alive = solver.grow_step()
        if not alive: break
        stats = solver.get_network_stats()
        print(f"Step {i}: Routes={stats['active_routes']}, ATP={stats['economy_status']['balance_atp']:.1f}")
