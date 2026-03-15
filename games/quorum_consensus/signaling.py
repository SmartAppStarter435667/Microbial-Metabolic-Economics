import numpy as np
from core.economy import EconomyEngine

class QuorumSignaling:
    """
    クオラム・合意形成エンジン (Quorum Consensus)
    
    役割:
    1. 各個体によるシグナル分子（オートインデューサー）の放出と拡散
    2. 空間内のシグナル濃度（熱量）の計算
    3. 閾値（キャズム）突破による集団行動スイッチの制御
    """

    def __init__(self, grid_size=50, threshold=0.6, economy_config=None):
        self.grid_size = grid_size
        self.threshold = threshold  # 合意形成のための臨界濃度
        
        # 空間内のシグナル濃度マップ
        self.signal_map = np.zeros((grid_size, grid_size))
        # 各個体の位置と状態 (x, y, is_active)
        self.agents = []
        
        # 経済エンジンの統合
        config = economy_config if economy_config else {"initial_atp": 1000.0, "maintenance_cost": 5.0}
        self.economy = EconomyEngine(**config)

    def add_agents(self, count=100):
        """ランダムな位置に個体を追加"""
        for _ in range(count):
            self.agents.append({
                'pos': (np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size)),
                'active': False
            })

    def update_step(self, emission_rate=0.1, diffusion_rate=0.1):
        """
        1ステップのシグナル拡散と判定
        """
        if not self.economy.is_alive:
            return False

        # 1. シグナルの放出（各個体が周囲に分子を撒く）
        for agent in self.agents:
            x, y = agent['pos']
            self.signal_map[x, y] += emission_rate

        # 2. シグナルの拡散（簡易的な近傍平均によるボヤけ）
        # 実際の微生物の化学拡散をシミュレート
        from scipy.ndimage import gaussian_filter
        self.signal_map = gaussian_filter(self.signal_map, sigma=1.0) * (1 - diffusion_rate)

        # 3. 閾値判定と集団行動の発動
        active_count = 0
        for agent in self.agents:
            x, y = agent['pos']
            # 周囲のシグナル濃度が閾値を超えているか
            if self.signal_map[x, y] >= self.threshold:
                agent['active'] = True
                active_count += 1
            else:
                agent['active'] = False

        # 4. 経済的影響（集団行動には大量のエネルギーが必要）
        # 行動している個体数に応じてATPを消費
        action_cost = active_count * 0.5
        gained_energy = active_count * 0.8 if active_count > len(self.agents) * 0.5 else 0
        
        self.economy.update_cycle(gained_energy - action_cost)
        
        # 極端な資源枯渇によるアポトーシス判定はEconomyEngineが担当
        return self.economy.is_alive

    def get_consensus_level(self):
        """現在の合意形成率（発火率）を返す"""
        active_agents = sum(1 for a in self.agents if a['active'])
        return {
            "active_ratio": active_agents / len(self.agents) if self.agents else 0,
            "max_signal_density": np.max(self.signal_map),
            "economy_status": self.economy.get_status()
        }

# 使用例
if __name__ == "__main__":
    consensus = QuorumSignaling(threshold=0.5)
    consensus.add_agents(200)
    
    for i in range(50):
        alive = consensus.update_step()
        stats = consensus.get_consensus_level()
        print(f"Step {i}: Active={stats['active_ratio']:.2%}, MaxSignal={stats['max_signal_density']:.2f}")
        if not alive: break
