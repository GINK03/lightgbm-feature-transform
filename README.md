
# Gradient Dicision Boosting Tree Machineで特徴量を非線形化

## この着想から、実践まで2ヶ月ほどかかりました
Facebook社のGradient Boosting Machineで特徴量を非線形化して、CTRを予想するという問題の論文から一年近く経ちましたが、その論文のユニークさは私の中では色あせることなく
しばらく残っています。  

原理的には、単純でGrandient Boosting Machineの特徴量で複数の特徴量を選択して決定木で非線形な状態にして、数値にすることでより高精度でリニアレグレッションなどシンプル伊豆ベストなもので予想できるようになります  

では、どのような時に有益でしょうか。  

CTR予想はアドテクの重要な基幹技術の一つですが、リアルタイムで計算して、ユーザにマッチした結果を返す必要がある訳ですが、何も考えずに自然言語やユーザ属性を追加していくと、特徴量の数が50万から100万を超えるほどになり、さらに増えると1000万を超えることがあります  

GBM系のアルゴリズムの一種であるLightGBMを用いることで、LightGBMで特徴量を500個非線形化して、これ単独でやるより各々の木の出力値をLinear Regression
にかけるだけで性能が同等になるか、向上していることを示します　　　


## 図示
<div align="center">
  <img width="600px" src="https://user-images.githubusercontent.com/4949982/32413605-21c77ea8-c258-11e7-9e1d-421ff8053192.png">
</div>
<div align="center"> 図1. 全体の流れ </div>

## 仕組みの説明
1. Yahoo!Japna社のAPIで商品のレビュー情報を取得します  
2. レビューの星の数と、形態素解析してベクトル化したテキストのペア情報を作ります
3. これをそのままLightGBMで学習させます  
4. LightGBMで作成したモデル情報を解析し、木構造の粒度に分解します
5. 2のベクトル情報を作成した木構造で非線形化します
6. ScikitLearnで非線形化した特徴でLinear Regressionを行い、星の数を予想します　

## データセット

## LightGBM(L1)単独での精度

## LightGBM + Linear Regressionでの精度

## まとめ
