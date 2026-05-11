//元のソースコード、使用しない

//package blackjack.date;

import java.util.Random;
import java.util.Scanner;

public class Sub {
    // scanの受け取り
    // 0が素、1がX置き換え後
    String[] player;
    String[] dealer;
    // ディーラー手札のrandom用
    String[] cards = { "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1" };;
    // 配列管理用
    String[][] Hands;
    // 合計スコア
    // 合計スコア管理用
    int[] Score;
    // 入力値受け取り
    Scanner sc = new Scanner(System.in);
    Random rand = new Random();

    // インスタンス
    public Sub() {
        Hands = new String[2][];
        Score = new int[2];
        player = new String[2];
        dealer = new String[2];
    }

    // テスト
    public String test() {
        return "aaaa";
    }

    public void playerCards() {
        // カードの枚数
        int cardCount = 2;
        player[0] = "";

        for (int i = 0; i < cardCount; i++) {
            player[0] += cards[rand.nextInt(13)];
            player[1] = player[0];
        }
    }

    // ディーラーの手札（CPU）
    public void dealerCards() {
        // カードの枚数
        int cardCount = 2;
        dealer[0] = "";

        for (int i = 0; i < cardCount; i++) {
            dealer[0] += cards[rand.nextInt(13)];
            dealer[1] = dealer[0];
        }
    }

    public void changeCard() {
        System.out.println("あなたの手札は" + player[0] + "です");
        processHand();
        System.out.println("あなたの手札の合計は" + Score[1] + "です");

        if (Score[1] >= 21) {
            gameResult();
            return;
        } else {
            System.out.println("新しいカードを引きますか？　y/n");
            String answer = sc.next();
            if ("y".equals(answer)) {
                playerHitCard();
                if (Score[0] <= 17) {
                    dealerHitCard();
                } else {
                    System.out.println("ディーラーは引きませんでした");
                }
                if (Score[0] > 21) {
                    gameResult();
                    return;
                }
                changeCard();
                return;
            } else {
                while (Score[0] <= 17) {
                    dealerHitCard();
                }
                gameResult();
                return;
            }
        }
    }

    public void playerHitCard() {
        String newCard = cards[rand.nextInt(13)];
        System.out.println(newCard + " を引きました");

        player[0] += newCard;
        player[1] = player[0];
    }

    public void dealerHitCard() {
        String newCard = cards[rand.nextInt(13)];
        System.out.println("ディーラーがカードを引きました");

        dealer[0] += newCard;
        dealer[1] = dealer[0];

        processHand();
    }

    // 10をXに置き換え
    public void tenReplace() {
        if (dealer[1].contains("10")) {
            dealer[1] = dealer[1].replace("10", "X");
        }
        if (player[1].contains("10")) {
            player[1] = player[1].replace("10", "X");
        }
    }

    // 入力値を配列に分割
    public void typeConversion() {
        // 長さを可変にするためsplitで生成
        Hands[0] = dealer[1].split("");
        Hands[1] = player[1].split("");
    }

    // 手札の合計をカウント
    // 数字はそのまま足す、アルファベットはtryで弾いてswitch
    public void total() {
        // れスタート時用のリセット
        Score[0] = 0;
        Score[1] = 0;
        // ディーラーとプレイヤーを切り替え
        for (int i = 0; i < Hands.length; i++) {
            // 一文字ずつ判別
            for (int j = 0; j < Hands[i].length; j++) {
                try {
                    // 0がディーラー、1がプレイヤー1
                    Score[i] += Integer.parseInt(Hands[i][j]);
                } catch (Exception e) {
                    switch (Hands[i][j]) {
                        case "A":
                            Score[i] += 1;
                            break;
                        case "K":
                        case "Q":
                        case "J":
                        case "X":
                            Score[i] += 10;
                            break;

                        default:
                            break;
                    }
                }

            }
        }
    }

    // 結果の判定
    public String result() {
        String res;

        if (Score[1] > 21) {
            res = "!!!!プレイヤーがバーストしました！\nディーラーの勝利です";
        } else if (Score[0] > 21) {
            res = "!!!!ディーラーがバーストしました！\nプレイヤーの勝利です";
        } else if (Score[0] == Score[1]) {
            res = "引き分けです！";
            if (Score[0] == 21) {
                res += "\nどちらもブラックジャックです";
            }
        } else if (Score[0] > Score[1]) {
            res = "ディーラーの勝利です！";
            if (Score[0] == 21) {
                res += "\nディーラーはブラックジャックです";
            }
        } else {
            res = "プレイヤーの勝利です！";
            if (Score[1] == 21) {
                res += "\nプレイヤーはブラックジャックです";
            }
        }

        return res;
    }

    // まとめる
    public void startGame() {
        playerCards();
        dealerCards();

        changeCard();

        // processHand();

        // gameResult();

        reStartGame();
    }

    public void processHand() {
        tenReplace();
        typeConversion();
        total();
    }

    public void reStartGame() {
        System.out.println("もう一度遊びますか？ y/n");
        String answer = sc.next();
        if ("y".equals(answer)) {
            startGame();
        } else {
            System.out.println("終了します");
        }

    }

    public void gameResult() {
        String res = result();
        System.out.println(res);
        System.out.println("プレイヤーのスコア" + Score[1] + "点");
        System.out.println("ディーラーの手札" + dealer[0]);
        System.out.println("ディーラーのスコア" + Score[0] + "点");
    }

}

// scanもメソッド、mainはgamestartだけ
// 相手はランダム関数でCPU化

// 10を置き換え判定10をreplace,返りに文字列
// 入力値をintに分割（文字列を引数、tryはここ、返りに配列
// 手札の合計カウント（配列を引数、forで足す，返りは合計
// 合計比較（合計,合計）を引数,返り値に結果をstr、バースト含む
// 表示