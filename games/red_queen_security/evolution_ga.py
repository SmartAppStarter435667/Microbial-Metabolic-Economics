import random
import numpy as np
from core.economy import EconomyEngine

class RedQueenDefense:
    """
    赤の女王・自動進化セキュリティ (Evolutionary Defense System)
    
    役割:
    1. 遺伝的アルゴリズム (GA) を用いた「抗体コード」の自動生成
    2. 攻撃パターンの変異に対する適応速度の計算
    3. 進化が止まった瞬間に生存率が低下する「赤の女王」効果の再現
    """

    def __init__(self, target_pattern="10101010", population_size=20, economy_config=None):
        self.population_size = population_size
        self.gene_length = len(target_pattern)
        # 現在の攻撃パターン（ターゲット）
        self.target_pattern = [int(b) for b in target_pattern]
        
        # 防御側の個体群（抗体の候補）
        self.population = [self._generate_random_gene() for _ in range(population_size)]
        
        # 経済エンジンの統合
        config = economy_config if economy_config else {"initial_atp": 500.0, "maintenance_cost": 10.0}
        self.economy = EconomyEngine(**config)

    def _generate_random_gene(self):
        return [random.randint(0, 1) for _ in range(self.gene_length)]

    def _calculate_fitness(self, gene):
        """適応度：攻撃パターンとの一致率（抗体としての性能）"""
        matches = sum(1 for g, t in zip(gene, self.target_pattern) if g == t)
        return matches / self.gene_length

    def evolve_step(self, mutation_rate=0.05):
        """
        1世代の進化ステップ（選択・交叉・突然変異）
        """
        if not self.economy.is_alive:
            return False

        # 1. 現世代の評価
        fitness_scores = [self._calculate_fitness(g) for g in self.population]
        max_fitness = max(fitness_scores)
        
        # 2. 経済的報酬（防御成功率に応じたATP獲得）
        # 防御に失敗（適応度が低い）すると損害が発生する
        gained_energy = max_fitness * 20.0
        damage = (1.0 - max_fitness) * 15.0
        self.economy.update_cycle(gained_energy - damage)

        # 3. 次世代の生成
        new_population = []
        for _ in range(self.population_size // 2):
            # エリート選択（簡易版）
            parent1 = self.population[np.argmax(fitness_scores)]
            parent2 = random.choice(self.population)
            
            # 交叉（一点交叉）
            cp = random.randint(1, self.gene_length - 1)
            child1 = parent1[:cp] + parent2[cp:]
            child2 = parent2[:cp] + parent1[cp:]
            
            # 突然変異
            child1 = [1-g if random.random() < mutation_rate else g for g in child1]
            child2 = [1-g if random.random() < mutation_rate else g for g in child2]
            
            new_population.extend([child1, child2])
            
        self.population = new_population
        return self.economy.is_alive

    def shift_attack_pattern(self):
        """
        攻撃者（ウイルス）の変異：ターゲットパターンをランダムに変更
        これが「赤の女王」の走る速度を決定する
        """
        idx = random.randint(0, self.gene_length - 1)
        self.target_pattern[idx] = 1 - self.target_pattern[idx]

    def get_defense_status(self):
        fitness_scores = [self._calculate_fitness(g) for g in self.population]
        return {
            "max_fitness": max(fitness_scores),
            "target": "".join(map(str, self.target_pattern)),
            "economy_status": self.economy.get_status()
        }

# 使用例
if __name__ == "__main__":
    defense_system = RedQueenDefense(target_pattern="1100110011001100")
    
    print("Starting Evolutionary Defense...")
    for generation in range(50):
        # 10世代ごとに攻撃者が変異する
        if generation % 10 == 0 and generation > 0:
            defense_system.shift_attack_pattern()
            print(f"\n[!] ATTACKER MUTATED: New Target = {defense_system.get_defense_status()['target']}")

        alive = defense_system.evolve_step()
        status = defense_system.get_defense_status()
        
        print(f"Gen {generation}: Fitness={status['max_fitness']:.2f}, ATP={status['economy_status']['balance_atp']:.1f}")
        
        if not alive:
            print("Defense System Crashed (Bankrupt/Apoptosis)")
            break
