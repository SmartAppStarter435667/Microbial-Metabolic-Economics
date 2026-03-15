import random

class VirusAttacker:
    """
    攻撃者（ウイルス）ロジック
    
    役割:
    1. 防御側の「抗体」を無効化するための継続的なパターン変異
    2. 赤の女王仮説における「追いかける側」の速度制御
    """

    def __init__(self, pattern_length=16, initial_mutation_rate=0.1):
        self.pattern_length = pattern_length
        self.mutation_rate = initial_mutation_rate
        # 初期の攻撃パターン（脆弱性）
        self.current_pattern = [random.randint(0, 1) for _ in range(pattern_length)]

    def mutate(self):
        """
        攻撃パターンの変異（進化）
        防御側の適応が追いついてきた際、ランダムにビットを反転させる
        """
        for i in range(self.pattern_length):
            if random.random() < self.mutation_rate:
                self.current_pattern[i] = 1 - self.current_pattern[i]
        return self.current_pattern

    def get_pattern_string(self):
        return "".join(map(str, self.current_pattern))

    def set_difficulty(self, new_rate):
        """変異速度を上げることで、赤の女王の『走る速度』を加速させる"""
        self.mutation_rate = new_rate
