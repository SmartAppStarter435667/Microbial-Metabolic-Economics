import matplotlib.pyplot as plt
import matplotlib.animation as animation
from games.quorum_consensus.signaling import QuorumSignaling

class QuorumVisualizer:
    """
    クオラム・合意形成の可視化と意思決定モニタリング
    
    役割:
    1. シグナル分子の濃度（熱量）をヒートマップで表示
    2. 集団発火（キャズム突破）の瞬間をエフェクトで表現
    """

    def __init__(self, engine: QuorumSignaling):
        self.engine = engine
        self.fig, (self.ax_map, self.ax_line) = plt.subplots(1, 2, figsize=(12, 5))
        
        # ヒートマップ表示
        self.im = self.ax_map.imshow(self.engine.signal_map, cmap='YlOrRd', origin='lower')
        self.ax_map.set_title("Signal Concentration (Marketing Heatmap)")
        
        # 統計グラフ
        self.ax_line.set_title("Active Ratio (Consensus Level)")
        self.line_active, = self.ax_line.plot([], [], color='green', label='Consensus Ratio')
        self.ax_line.axhline(y=0.5, color='gray', linestyle='--', label='Critical Mass (50%)')
        self.ax_line.set_ylim(0, 1.1)
        self.ax_line.legend()
        
        self.history_ratio = []

    def update(self, frame):
        # 1ステップ更新
        is_alive = self.engine.update_step()
        stats = self.engine.get_consensus_level()
        self.history_ratio.append(stats['active_ratio'])

        # ヒートマップ更新
        self.im.set_array(self.engine.signal_map)
        self.im.set_clim(0, max(1.0, stats['max_signal_density']))
        
        # グラフ更新
        self.line_active.set_data(range(len(self.history_ratio)), self.history_ratio)
        self.ax_line.set_xlim(0, max(50, len(self.history_ratio)))

        # キャズム突破時の視覚効果
        if stats['active_ratio'] > 0.5:
            self.ax_map.set_facecolor('black') # 背景を変えて「発火」を表現
        
        if not is_alive:
            self.ax_map.set_title("SYSTEM BANKRUPT")

        return self.im, self.line_active

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=100, interval=100, blit=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    engine = QuorumSignaling(grid_size=40, threshold=0.7)
    engine.add_agents(150)
    vis = QuorumVisualizer(engine)
    vis.run()
