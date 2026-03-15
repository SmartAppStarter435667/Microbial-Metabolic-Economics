import matplotlib.pyplot as plt
import matplotlib.animation as animation
from games.physarum_solver.engine import PhysarumEngine

class PhysarumVisualizer:
    """
    粘菌ルート最適化エンジンの可視化モジュール
    
    役割:
    1. 菌糸（tube_map）の成長と淘汰をヒートマップで表示
    2. ATP残高とROI（投資対効果）の推移をリアルタイムグラフ化
    """

    def __init__(self, engine: PhysarumEngine):
        self.engine = engine
        self.fig, (self.ax_map, self.ax_stats) = plt.subplots(1, 2, figsize=(12, 5))
        
        # マップ表示の設定
        self.im = self.ax_map.imshow(self.engine.tube_map, cmap='viridis', interpolation='bilinear')
        self.ax_map.set_title("Physarum Network (Logic: Positive/Negative Feedback)")
        
        # エサ（住宅街）のプロット
        for food in self.engine.food_sources:
            fx, fy = food['pos']
            self.ax_map.plot(fy, fx, 'ro', markersize=5) # 座標系に合わせてxy反転
            
        # 統計グラフの設定
        self.ax_stats.set_title("Economic Status (ATP & ROI)")
        self.line_atp, = self.ax_stats.plot([], [], label='ATP Balance', color='blue')
        self.ax_stats_roi = self.ax_stats.twinx()
        self.line_roi, = self.ax_stats_roi.plot([], [], label='ROI', color='red', linestyle='--')
        self.ax_stats.legend(loc='upper left')
        self.ax_stats_roi.legend(loc='upper right')

    def update(self, frame):
        """アニメーションの更新関数"""
        # 1ステップ進行
        is_alive = self.engine.grow_step()
        
        # マップの更新
        self.im.set_array(self.engine.tube_map)
        
        # 統計データの更新
        history = self.engine.economy.history
        steps = range(len(history['atp']))
        
        if steps:
            self.line_atp.set_data(steps, history['atp'])
            self.line_roi.set_data(steps, history['roi'])
            
            # グラフ軸の自動調整
            self.ax_stats.set_xlim(0, max(10, len(steps)))
            self.ax_stats.set_ylim(0, max(600, max(history['atp']) * 1.1))
            self.ax_stats_roi.set_ylim(-1, 2)

        if not is_alive:
            self.ax_map.set_title("SYSTEM TERMINATED (Apoptosis/Bankrupt)")
            
        return self.im, self.line_atp, self.line_roi

    def run(self):
        """シミュレーションの開始"""
        ani = animation.FuncAnimation(self.fig, self.update, frames=200, interval=100, blit=False)
        plt.tight_layout()
        plt.show()

# 実行
if __name__ == "__main__":
    # エンジンの初期化（経済設定を含む）
    solver = PhysarumEngine(width=60, height=60)
    
    # テスト用：複数のエサ（住宅街）を配置し、インフラの冗長性とコストをテスト
    solver.add_food_source(10, 10, reward_value=30.0)
    solver.add_food_source(10, 50, reward_value=30.0)
    solver.add_food_source(50, 30, reward_value=50.0)
    
    # 可視化の実行
    visualizer = PhysarumVisualizer(solver)
    visualizer.run()
