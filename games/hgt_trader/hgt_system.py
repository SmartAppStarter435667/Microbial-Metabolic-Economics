import types
from core.economy import EconomyEngine

class MicrobialStrain:
    """
    菌株（個体）クラス
    
    特徴:
    - 自分のゲノムを軽量化し、他者のスキルを動的に取り込む（HGT）
    - 自社開発（垂直進化）よりもM&A（水平伝播）を優先する合理性
    """

    def __init__(self, name, economy_config=None):
        self.name = name
        self.skills = ["basic_metabolism"] # 初期スキル
        
        # 経済エンジンの統合
        config = economy_config if economy_config else {"initial_atp": 300.0, "maintenance_cost": 10.0}
        self.economy = EconomyEngine(**config)

    def basic_metabolism(self):
        """基本代謝（わずかなエネルギー獲得）"""
        return 5.0

    def install_skill(self, skill_name, skill_function):
        """
        水平伝播 (HGT) の実行
        外部の関数を自分のメソッドとして即座にインストールする
        """
        # Pythonの動的性質（setattr）を利用した即時プラグイン
        setattr(self, skill_name, types.MethodType(skill_function, self))
        if skill_name not in self.skills:
            self.skills.append(skill_name)
        
        # インストールには少量のエネルギー（M&A手数料）が必要
        self.economy.atp_balance -= 20.0 
        # print(f"HGT SUCCESS: Skill '{skill_name}' integrated into {self.name}!")

class HGTSystem:
    """
    水平伝播トレーダー（技術交換所）の管理
    """
    @staticmethod
    def transfer_gene(source_strain, target_strain, gene_name):
        """sourceからtargetへ遺伝子（関数）をコピーする"""
        if hasattr(source_strain, gene_name):
            func = getattr(source_strain, gene_name).__func__
            target_strain.install_skill(gene_name, func)
            return True
        return False

# --- 強強スキル（遺伝子）のライブラリ例 ---
def photosynthesis(self):
    """光合成：太陽光（環境資源）から大量エネルギー獲得"""
    return 50.0

def nitrogen_fixation(self):
    """窒素固定：特殊な資源を分解可能にする"""
    return 30.0

# --- 実行デモ ---
if __name__ == "__main__":
    # 自社（スタートアップ菌）
    my_startup = MicrobialStrain("Venture-Strain")
    
    # 他社（強強スキル保持菌）
    expert_strain = MicrobialStrain("Expert-Strain")
    setattr(expert_strain, "photosynthesis", types.MethodType(photosynthesis, expert_strain))

    print(f"Before HGT: {my_startup.skills}")
    
    # 水平伝播の実行：学習なしで「光合成」スキルを即時取得
    HGTSystem.transfer_gene(expert_strain, my_startup, "photosynthesis")
    
    # 取得したスキルを即実行
    gain = my_startup.photosynthesis()
    my_startup.economy.update_cycle(gain)
    
    print(f"After HGT: {my_startup.skills}")
    print(f"Status: {my_startup.get_status()}")
