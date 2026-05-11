"""
ブラックジャックゲームロジック
Sub.javaをそのままPythonに移植
"""
import random
from typing import List


class BlackjackGame:
    """ブラックジャックゲームのロジック（Sub.java完全移植版）"""
    
    # カードの種類（Sub.javaと同じ）
    CARDS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
    
    def __init__(self):
        """ゲームの初期化"""
        self.player_hand: List[str] = []
        self.dealer_hand: List[str] = []
        self.game_over = False
        self.result_message = ""
        self.last_action = ""
    
    def deal_initial_cards(self):
        """初期カードを2枚ずつ配布"""
        self.player_hand = [self._draw_card(), self._draw_card()]
        self.dealer_hand = [self._draw_card(), self._draw_card()]
        self.game_over = False
        self.result_message = ""
        self.last_action = ""
    
    def _draw_card(self) -> str:
        """ランダムにカードを1枚引く"""
        return random.choice(self.CARDS)
    
    def player_hit(self):
        """
        プレイヤーがカードを引く（Sub.java仕様）
        changeCard() および playerHitCard() の動作を再現
        """
        if self.game_over:
            return
        
        # プレイヤーがカードを引く
        new_card = self._draw_card()
        self.player_hand.append(new_card)
        self.last_action = f"🎴 {new_card} を引きました"
        
        # スコア計算
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        # プレイヤーのスコアが21以上ならゲーム終了
        if player_score >= 21:
            self.game_over = True
            self.result_message = self._result()
            return
        
        # ディーラーのスコアが17以下なら自動ヒット（Sub.javaのchangeCard()と同じ）
        if dealer_score <= 17:
            dealer_card = self._draw_card()
            self.dealer_hand.append(dealer_card)
            self.last_action += f"\n🤖 ディーラーがカードを引きました"
            
            # ディーラーのスコアを再計算
            dealer_score = self.calculate_score(self.dealer_hand)
            
            # ディーラーがバーストしたかチェック
            if dealer_score > 21:
                self.game_over = True
                self.result_message = self._result()
        else:
            self.last_action += f"\n✋ ディーラーは引きませんでした"
    
    def player_stand(self):
        """
        プレイヤーがスタンド（Sub.javaのchangeCard()でnを選択した場合）
        ディーラーがスコア17以下の間カードを引き続ける
        """
        if self.game_over:
            return
        
        # ディーラーがスコア17以下の間ヒット
        while self.calculate_score(self.dealer_hand) <= 17:
            dealer_card = self._draw_card()
            self.dealer_hand.append(dealer_card)
        
        # 勝敗判定
        self.game_over = True
        self.result_message = self._result()
    
    def _result(self) -> str:
        """
        勝敗判定（より自然な日本語メッセージ）
        """
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        res = ""
        
        # 勝敗判定
        if player_score > 21:
            res = "🔥 プレイヤーがバーストしました！\nディーラーの勝利です"
        elif dealer_score > 21:
            res = "💥 ディーラーがバーストしました！\nプレイヤーの勝利です"
        elif dealer_score == player_score:
            res = "🤝 引き分けです！"
            if dealer_score == 21:
                res += "\n✨ 両者ブラックジャック"
        elif dealer_score > player_score:
            res = "😢 ディーラーの勝利です"
            if dealer_score == 21:
                res += "\n✨ ディーラーがブラックジャック"
        else:
            res = "🎉 プレイヤーの勝利です！"
            if player_score == 21:
                res += "\n✨ ブラックジャック"
        
        return res
    
    @staticmethod
    def calculate_score(hand: List[str]) -> int:
        """
        手札のスコアを計算（Sub.javaのtotal()メソッドを移植）
        A=1, K/Q/J/10=10, 数字=そのまま
        """
        score = 0
        for card in hand:
            if card == "A":
                score += 1
            elif card in ["K", "Q", "J", "10"]:
                score += 10
            else:
                try:
                    score += int(card)
                except ValueError:
                    pass  # 無効なカードはスキップ
        return score
    
    def get_player_score(self) -> int:
        """プレイヤーのスコアを取得"""
        return self.calculate_score(self.player_hand)
    
    def get_dealer_score(self) -> int:
        """ディーラーのスコアを取得"""
        return self.calculate_score(self.dealer_hand)
    
    def format_hand(self, hand: List[str], hide_second: bool = False) -> str:
        """手札を整形して表示"""
        if hide_second and len(hand) >= 2:
            return f"{hand[0]}, ?"
        return ", ".join(hand)
    
    def get_game_status(self, show_dealer_full: bool = False, show_result: bool = True) -> str:
        """ゲームの状態を文字列で取得（ゲームっぽく整形）"""
        player_score = self.get_player_score()
        dealer_score = self.get_dealer_score()
        
        # ゲーム状態をボックスで整形
        status = "```\n"
        status += "╔════════════════════════════════╗\n"
        status += "║      🎰 BLACKJACK GAME 🎰      ║\n"
        status += "╚════════════════════════════════╝\n"
        status += "```\n"
        
        # ディーラーの手札
        status += "🤵 **ディーラーの手札**\n"
        if show_dealer_full or self.game_over:
            status += f"┗━ 🃏 {self.format_hand(self.dealer_hand)} ┃ **{dealer_score}点**\n"
        else:
            visible_score = self.calculate_score([self.dealer_hand[0]])
            status += f"┗━ 🃏 {self.format_hand(self.dealer_hand, hide_second=True)} ┃ 見えている札: **{visible_score}点**\n"
        
        status += "\n"
        
        # プレイヤーの手札
        status += "👤 **あなたの手札**\n"
        status += f"┗━ 🎴 {self.format_hand(self.player_hand)} ┃ **{player_score}点**\n"
        
        # アクション履歴を表示
        if self.last_action:
            status += f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            status += f"📢 {self.last_action}\n"
        
        # 勝敗メッセージ（ゲーム終了時のみ、かつshow_resultがTrueの場合）
        if self.game_over and self.result_message and show_result:
            status += "\n```\n"
            status += "╔════════════════════════════════╗\n"
            status += "║         ⚡ 結果発表 ⚡          ║\n"
            status += "╚════════════════════════════════╝\n"
            status += "```\n"
            # 勝敗メッセージ（既に絵文字入り）
            status += f"{self.result_message}\n\n"
            # 最終スコアの詳細
            status += "```\n"
            status += "━━━━━━ 最終結果 ━━━━━━\n"
            status += f"👤 プレイヤー\n"
            status += f"   手札: {', '.join(self.player_hand)}\n"
            status += f"   得点: {player_score}点\n"
            status += f"\n"
            status += f"🤵 ディーラー\n"
            status += f"   手札: {', '.join(self.dealer_hand)}\n"
            status += f"   得点: {dealer_score}点\n"
            status += "━━━━━━━━━━━━━━━━━━━\n"
            status += "```"
        
        return status
