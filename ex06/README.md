#　第6回
## ガンダムVSこうかとん(ex06/test.py)
### ゲーム概要
- ex06/test.pyを実行するとガンダム（自キャラ）が生成される。
-横向きシューティングゲームの要領でこうかとんが飛んでくるため、それを撃つ。
-こうかとんに当たるとscoreを表示してゲームを終了させる。
### 操作方法
- 矢印キーでガンダムを上下左右に移動する。
- スペースキーを押してビームを発射する。
### 追加機能
- 不規則に反射していた球を左方向のみに流れるように変更した。
- 球が１つだけであったものを時間に応じて再生成させるように変更した。
- killカウンタ―：こうかとんを倒した数に応じて増加するkillカウンターを表示させる。
- score機能:時間とkill数を重みづけした合計値を取得、表示する。
-
### Todo（実装しようと思ったけど時間が無かった）
- ゲーム終了画面をおしゃれにする。
- 他にも攻撃方法を増やす。