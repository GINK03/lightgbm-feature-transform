
# Gradient Dicision Boosting Tree Machineで特徴量を非線形化

## Practical Lessons from Predicting Clicks on Ads at Facebook
Facebook社のGradient Boosting Machineで特徴量を非線形化して、[CTRを予想するという問題の論文](http://quinonero.net/Publications/predicting-clicks-facebook.pdf)からだいぶ時間が、その論文のユニークさは私の中では色あせることなくしばらく残っています。  

原理的には、単純でGrandient Boosting Machineの特徴量で複数の特徴量を選択して決定木で非線形な状態にして、数値にすることでより高精度でリニアレグレッションなどシンプルイズベストなもので予想できるようになります  

では、どのような時に有益でしょうか。  

CTR予想はアドテクの重要な基幹技術の一つですが、リアルタイムで計算して、ユーザにマッチした結果を返す必要がある訳ですが、何も考えずに自然言語やユーザ属性を追加していくと、特徴量の数が50万から100万を超えるほどになり、さらに増えると1000万を超えることがあります  

GBM系のアルゴリズムの一種であるLightGBMを用いることで、LightGBMで特徴量を500個の非線形化した特徴量にして、これ単独でやるより各々の木の出力値をLinear Regressionにかけるだけで性能が同等になるか、向上していることを示します　　　


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
[ここでご紹介していただいている方法](https://qiita.com/nannoki/items/9473ac358872f891de0c)で、コーパスを作りました。  

[コーパスのダウンロードのみはこちら](https://www.dropbox.com/s/iw7zyfebmc4rnk2/yahoo.jsonp?dl=0)から行えます。  

## LightGBM(L1)単独での精度
LightGBM単体での精度はどうでしょうか。

このようなパラメータで学習を行いました。
```console
task = train
boosting_type = gbdt
objective = regression
metric_freq = 1
is_training_metric = true
max_bin = 255
data = misc/xgb_format
valid_data = misc/xgb_format
num_trees = 500
learning_rate = 0.30
num_leaves = 100
tree_learner = serial
feature_fraction = 0.9
bagging_fraction = 0.8
min_data_in_leaf = 100
min_sum_hessian_in_leaf = 5.0
is_enable_sparse = true
use_two_round_loading = false
output_model = misc/LightGBM_model.txt
convert_model=misc/gbdt_prediction.cpp
convert_model_language=cpp
```

これも50万次元程度のウルトラスパースマトリックスなので、コマンドを叩いて学習します  
```console
$ lightgbm config=config/train.lightgbm.conf  
...
[LightGBM] [Info] 47.847420 seconds elapsed, finished iteration 499
[LightGBM] [Info] Iteration:500, training l1 : 0.249542
```

## 出力したモデルを木で非線形化するPythonのコードに変換
```console
$ cd misc
$ python3 formatter.py > f.py
...(適宜取りこぼしたエラーをvimやEmacs等で修正してください)
```

## 特徴量を木で非線形化したデータセットに変換
```console
$ python3 test.py > ../shrinkaged/shrinkaged.jsonp
```

## LightGBM + Linear Regressionでの精度
```console
$ cd shrinkaged
$ python3 linear_reg.py --data_gen
$ python3 linear_reg.py --fit
train mse: 0.24
test mse: 0.21
```
testデータセットで0.21の平均絶対誤差と、LightGBM単体での性能に逼迫し、上回っているとわかりました  

## まとめ
できましたね、という感じでしたが、これに極めて特徴量が大きい問題に対して、決定木による非線形化と、非線形化した状態で保存することで、モデルの先方の評価が可能になり、いくつかの実質的に可能な計算時間がかなり伸びることが期待できます  
