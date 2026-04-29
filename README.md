# HW2: Q-learning vs SARSA in Cliff Walking Environment

本專案為深度強化學習課程作業二，主要實作並比較兩種經典強化學習演算法——**Q-learning**（離策略方法，Off-policy）與 **SARSA**（同策略方法，On-policy），透過在相同的「懸崖漫步 (Cliff Walking)」環境中訓練，分析其學習行為、收斂特性與最終策略差異。

## 專案結構

* **`cliff_walking.py`**：實作 4x12 網格的 Cliff Walking 環境，包含狀態轉移與獎勵機制（掉入懸崖得 -100 並回到起點，其餘每步得 -1）。
* **`agents.py`**：實作基礎代理人與 $\epsilon$-greedy 策略，並分別包含 `QLearningAgent` 與 `SarsaAgent` 的演算法更新邏輯。
* **`main.py`**：主程式，負責初始化環境與代理人，進行訓練（預設 500 回合），並繪製累積獎勵曲線與最佳路徑視覺化圖。
* **`report.md`**：作業分析報告，包含對學習表現的比較、策略行為的分析及兩者演算法理論上的探討。
* **`requirements.txt`**：執行本專案所需的 Python 模組。

## 安裝與執行

1. **安裝依賴套件**
   請確保您的環境中已安裝必要的模組：
   ```bash
   pip install -r requirements.txt
   ```

2. **執行訓練與視覺化**
   直接執行 `main.py` 即可開始訓練：
   ```bash
   python main.py
   ```
   執行完畢後，程式會在目錄下自動生成：
   * `reward_curve.png`：Q-learning 與 SARSA 的累積獎勵曲線比較圖。
   * `path_visualization.png`：兩種演算法最終學習到的最佳路徑視覺化圖。

## 結果摘要

* **Q-learning** 傾向於學習理論上最佳的「最短路徑」（貼近懸崖邊緣），但在 $\epsilon$-greedy 的探索機制下，這條路徑非常危險，導致訓練期間的平均獎勵極低且震盪劇烈。
* **SARSA** 則因為是 On-policy，會將 $\epsilon$ 探索造成的風險納入評估，最終學習到遠離懸崖的「安全路徑」，在訓練期間的平均獎勵較高且收斂速度快、表現穩定。
