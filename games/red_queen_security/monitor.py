import matplotlib.pyplot as plt
import matplotlib.animation as animation
from games.red_queen_security.evolution_ga import RedQueenDefense
from games.red_queen_security.virus_attacker import VirusAttacker

class RedQueenMonitor:
    """
    赤の女王セキュリティ・監視ダッシュボード
    
    可視化内容:
    - 防御適応度（抗体の有効性）
    - ATP残高（経済的生存性）
    - 攻撃パターンの変異タイミング
    """

    def __init__(self, defense: RedQueenDefense, attacker: VirusAttacker):
        self.defense = defense
        self.attacker = attacker
        self.fig, (self.ax_fitness, self.ax_atp) = plt.subplots(2, 1, figsize=(10, 8))
        
        self.history_fitness = []
        self.history_atp = []
        
        self.ax_fitness.set_title("Defense Adaptation (Fitness)")
        self.ax_fitness.set_ylim(0, 1.1)
        self.line_fit, = self.ax_fitness.plot([], [], color='blue', label='Adaptation Rate')
        
        self.ax_atp.set_title("Economic Survival (ATP Balance)")
        self.line_atp, = self.ax_atp.plot([], [], color='green', label='ATP')
        
    def update(self, frame):
        # 1. 攻撃者の変異（5ステップごと）
        if frame % 5 == 0:
            new_pattern = self.attacker.mutate()
            self.defense.target_pattern = new_pattern # 防御側のターゲットを更新
            
        # 2. 防御側の進化ステップ
        is_alive = self.defense.evolve_step()
        status = self.defense.get_defense_status()
        
        self.history_fitness.append(status['max_fitness'])
        self.history_atp.append(status['economy_status']['balance_atp'])
        
        # グラフ更新
        steps = range(len(self.history_fitness))
        self.line_fit.set_data(steps, self.history_fitness)
        self.line_atp.set_data(steps, self.history_atp)
        
        self.ax_fitness.set_xlim(0, max(50, len(steps)))
        self.ax_atp.set_xlim(0, max(50, len(steps)))
        self.ax_atp.set_ylim(0, max(1000, max(self.history_atp) * 1.2))
        
        if not is_alive:
            self.ax_fitness.set_facecolor('mistyrose')
            self.ax_atp.set_title("SYSTEM TERMINATED - Adaptive Failure")

        return self.line_fit, self.line_atp

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update, frames=200, interval=150, blit=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    v = VirusAttacker(pattern_length=16, initial_mutation_rate=0.05)
    d = RedQueenDefense(target_pattern=v.get_pattern_string(), population_size=30)
    monitor = RedQueenMonitor(d, v)
    monitor.run()
