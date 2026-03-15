import numpy as np
from scipy.optimize import linprog

class EconomyEngine:
    """
    微生物代謝経済学（Microbial Metabolic Economics）共通エンジン
    
    役割: 
    1. ATP（通貨）の収支管理
    2. FBA（フラックスバランス解析）による資源配分の最適化
    3. ROI（投資対効果）に基づくアポトーシスの判定
    """

    def __init__(self, initial_atp=100.0, maintenance_cost=5.0):
        # 微生物のPL（損益計算書）管理変数
        self.atp_balance = initial_atp  # 現在のエネルギー残高
        self.maintenance_cost = maintenance_cost  # 生存維持コスト（固定費）
        self.is_alive = True
        
        # 統計データ
        self.history = {"atp": [], "roi": []}

    def calculate_fba_optimization(self, available_resources, transformation_efficiency):
        """
        簡易的なフラックスバランス解析（FBA）の実装
        
        目的関数: 利益（増殖速度）を最大化する資源配分を算出する
        制約条件: 利用可能な資源量とエネルギー保存則
        """
        # 目的関数: - (資源 * 変換効率) -> 最小化問題として最大化を解く
        c = [-1 * eff for eff in transformation_efficiency]
        
        # 制約条件: A_ub * x <= b_ub (資源の消費量は利用可能量を超えない)
        A = [[1 for _ in range(len(available_resources))]]
        b = [sum(available_resources)]
        
        # 境界条件: 各フラックスは0以上
        x_bounds = [(0, r) for r in available_resources]
        
        res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')
        
        if res.success:
            return res.x  # 最適化された資源配分フラックス
        else:
            return np.zeros(len(available_resources))

    def update_cycle(self, gained_energy):
        """
        1サイクル（1日/1ターン）の収支更新
        """
        if not self.is_alive:
            return 0.0

        # ROI = (獲得エネルギー - 維持コスト) / 維持コスト
        # 微生物にとってのROIは増殖効率に相当する [1]
        roi = (gained_energy - self.maintenance_cost) / self.maintenance_cost
        
        # ATP残高の更新
        self.atp_balance += (gained_energy - self.maintenance_cost)
        
        # 履歴の記録
        self.history["atp"].append(self.atp_balance)
        self.history["roi"].append(roi)

        # アポトーシスの判定
        self._check_apoptosis(roi)
        
        return self.atp_balance

    def _check_apoptosis(self, current_roi):
        """
        プログラムされた死（アポトーシス）の判定
        条件: 
        1. ATP残高が枯渇した
        2. ROIが閾値を下回り、集団全体の利益のために死ぬべきと判断された [2, 3]
        """
        # ROIが極端に低い、またはエネルギーがマイナスになった場合
        # 「自己生存による利得 < 自己犠牲による集団への利得」をモデル化 [2]
        if self.atp_balance <= 0 or current_roi < -0.8:
            self.is_alive = False
            self.atp_balance = 0
            # 死後、残ったATPは「資源」として開放される（集団への貢献）
            # print("DEBUG: Apoptosis triggered for resource recycling.")

    def get_status(self):
        """
        現在の経営状態をビジネス指標で返す
        """
        return {
            "status": "ALIVE" if self.is_alive else "DEAD (RECYCLED)",
            "balance_atp": self.atp_balance,
            "maintenance_fixed_cost": self.maintenance_cost,
            "last_roi": self.history["roi"][-1] if self.history["roi"] else 0
        }

# 使用例（他のゲームモジュールから呼び出される想定）
if __name__ == "__main__":
    # カフェ経営（Source [4, 5]）を模したテスト
    cafe_microbe = EconomyEngine(initial_atp=100.0, maintenance_cost=10.0)
    
    # 資源投入（客足）
    daily_customer_energy = 15.0
    
    new_balance = cafe_microbe.update_cycle(daily_customer_energy)
    print(f"Cycle 1 Status: {cafe_microbe.get_status()}")
  
