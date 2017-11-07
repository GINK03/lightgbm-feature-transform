
# Gradient Dicision Boosting Tree Machineで特徴量を非線形化

## Practical Lessons from Predicting Clicks on Ads at Facebook
Facebook社のGradient Boosting Machineで特徴量を非線形化して、[CTRを予想するという問題の論文](http://quinonero.net/Publications/predicting-clicks-facebook.pdf)からだいぶ時間が、その論文のユニークさは私の中では色あせることなくしばらく残っています。  

原理的には、単純でGrandient Boosting Machineの特徴量で複数の特徴量を選択して決定木で非線形な状態にして、数値にすることでより高精度でリニアレグレッションなどシンプルイズベストなもので予想できるようになります  

では、どのような時に有益でしょうか。  

CTR予想はアドテクの重要な基幹技術の一つですが、リアルタイムで計算して、ユーザにマッチした結果を返す必要がある訳ですが、何も考えずに自然言語やユーザ属性を追加していくと、特徴量の数が50万から100万を超えるほどになり、さらに増えると1000万を超えることがあります  

GBM系のアルゴリズムの一種であるLightGBMを用いることで、LightGBMで特徴量を500個の非線形化した特徴量にして、これ単独でやるより各々の木の出力値をLinear Regressionにかけるだけで性能が同等になるか、向上していることを示します　　　


## 図示
<div align="center">
  <img width="600px" src="https://user-images.githubusercontent.com/4949982/32472819-d152591a-c3a7-11e7-8584-bdabd95730b7.png">
</div>
<div align="center"> 図1. FBの論文の引用 </div>
GBMで特徴量を非線形化して、その非線形になった特徴量の係数をLinear Regressionで計算します

## 仕組みの説明
1. 映画.comの映画のレビュー情報を取得します  
2. レビューの星の数と、形態素解析してベクトル化したテキストのペア情報を作ります
3. これをそのままLightGBMで学習させます  
4. LightGBMで作成したモデル情報を解析し、木構造の粒度に分解します
5. 2のベクトル情報を作成した木構造で非線形化します
6. ScikitLearnで非線形化した特徴でLinear Regressionを行い、星の数を予想します　

## データセット
[作成したコーパスはここからダウンロード](https://www.dropbox.com/s/t9jitxtdv1znkql/reviews.json?dl=0)ができます


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

## Linear Regressionとの比較
Linear Regressionより性能が高くなると期待できるので比較検討します  
今回の使用したデータセットは50万程度の特徴量ですので、単純にLinear Regressionで計算したものと比較します  
```console
$ ./train -s 11 ../xgb_format 
iter  1 act 7.950e+06 pre 7.837e+06 delta 1.671e+00 f 9.896e+06 |g| 2.196e+07 CG   2
cg reaches trust region boundary
iter  2 act 3.798e+05 pre 3.755e+05 delta 6.685e+00 f 1.946e+06 |g| 8.440e+05 CG   5
cg reaches trust region boundary
iter  3 act 2.320e+05 pre 2.300e+05 delta 2.674e+01 f 1.566e+06 |g| 1.298e+05 CG  12
cg reaches trust region boundary
iter  4 act 2.481e+05 pre 2.476e+05 delta 1.070e+02 f 1.334e+06 |g| 4.600e+04 CG  28
cg reaches trust region boundary
iter  5 act 3.378e+05 pre 3.489e+05 delta 4.278e+02 f 1.086e+06 |g| 4.329e+04 CG 104
iter  6 act 1.306e+05 pre 1.698e+05 delta 4.278e+02 f 7.481e+05 |g| 9.367e+04 CG 180
iter  7 act 4.090e+04 pre 1.129e+05 delta 1.117e+02 f 6.175e+05 |g| 2.774e+04 CG 419
```
学習が完了しました
```console
$ ./predict ../xgb_format xgb_format.model result
Mean squared error = 0.785621 (regression)
Squared correlation coefficient = 0.424459 (regression)
```
MSE(Mean Squared Error)は0.78という感じで、星半分以上間違えています

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
できましたね、という感じでしたが、これに極めて特徴量が大きい問題に対して、決定木による非線形化と、非線形化した状態で保存することで、モデルの先方の評価が可能になり、いくつかの実質的に可能な計算時間がかなり伸びることが期待できます(クリエイティブの特徴量とユーザ行動列の特徴量を別に保存するとか。。。)  

## 謝辞
SNSで理論をだらだら述べていた時に、先行して研究を行っていてそのノウハウや本質を伝えてくださった菜園さんに深く感謝しています。  
[より多角的な指標で検討されている](https://qiita.com/Quasi-quant2010/items/a30980bd650deff509b4)ので、ぜひ一読されると良いと思います。
