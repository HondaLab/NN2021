# Keyboard RC
RasPiロボット(SSRX)で，ラジコンで操縦するプログラムです．
コントローラーは用いず，簡便にキーボードだけで，
前進，後退，右折，左折などを行います．

## 必要なもの (Requirement)
### pigpiod
```
sudo apt-get install pigpiod
sudo pigpiod
```

### OpenCV
```
sudo apt-get install python3-opencv
```

## rcXX.pyを実行してください．
```
python3 rcXY.py
```

## キーボードで操縦します (Control by keyboard)

  - q: 終了
  - s: stop
  - f: 前進増速
  - d: 後退増速
  - j: 左折増速
  - k: 右折増速
  - h: 左折
  - l: 右折


