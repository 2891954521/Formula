# Formula 手写算式识别

#### 项目结构
```
Formula
├─ Core
│  ├─ Analyzer
│  │   └─ 算式解析器 解析收到的算式字符
│  └─ Recognizer
│      └─ 图片识别器 处理图片后将结果交给 Analyzer 处理
├─ GUI
│   └─ 图形界面 
└─ Server
│   └─ Web服务 将收到的图片交给 Recognizer 处理
└─ run.py
```

#### 使用
```bash
pip install requirements.txt
python run.py
```