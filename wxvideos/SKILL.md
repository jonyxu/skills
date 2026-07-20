---
name: wxvideos
description: 微信视频号视频下载与内容分析工具链。支持从 weixin.qq.com/sph/ 链接解析、下载视频、提取关键帧、提取音频并转录、分析视频内容的完整流程。触发词：视频号分析、下载视频号、分析视频内容、wxvideos、sph下载、微信视频下载、语音转文字。
---

# 微信视频号视频分析（wxvideos）

完整工作流：从视频号分享链接 → 解析 → 下载 → 提取帧 → 提取音频 → ASR转录 → 综合分析内容。

## 环境配置

### ffmpeg 路径（按实际安装路径修改）
```powershell
$ffmpegPath = "D:\ffmpeg-7.0.2-full_build\bin"
$ffprobe = "$ffmpegPath\ffprobe.exe"
$ffmpeg = "$ffmpegPath\ffmpeg.exe"
```

### 工作目录
```powershell
$workDir = "$env:USERPROFILE\Downloads"
$videoFile = "$workDir\video.mp4"
$framesDir = "$workDir\vf"
$audioDir = "$workDir\audio"
```

---

## Phase 1: 获取视频信息

### 步骤 1.1: 打开视频号页面获取元数据

用浏览器访问视频号链接，获取页面基本信息（标题、作者、互动数据等）：

```bash
chrome-devtools_new_page(url="https://weixin.qq.com/sph/XXX")
chrome-devtools_take_snapshot()  # 获取页面文本信息
```

从 snapshot 中提取：
- **发布者**（author name）
- **视频标题**（title/description）
- **互动数据**（点赞、评论、转发、收藏）
- **发布时间**
- **标签（hashtags）**

### 步骤 1.2: 使用在线解析工具获取视频下载地址

推荐工具：**ltaoo/wx_channels_download** 在线解析服务

```
https://sph.litao.workers.dev/
```

操作步骤：
1. 打开 `https://sph.litao.workers.dev/`
2. 在输入框中粘贴视频号分享链接（如 `https://weixin.qq.com/sph/Avu1QzJAdR`）
3. 点击"查询"按钮
4. 等待解析结果
5. 从结果中获取：
   - 视频预览播放器
   - "下载视频"按钮（标准画质）
   - "下载原始视频"按钮（原始画质）
   - 原始视频直链 URL（`finder.video.qq.com` 域名）
   - 视频标题、作者、互动数据

**备选方案（如在线解析不可用）：**

可使用以下 GitHub 项目作为替代：
- `ltaoo/wx_channels_download`（7.3k stars）— 支持代理注入+在线解析
- `qiye45/wechatVideoDownload`（5.5k stars）— GUI 工具，支持批量下载
- `nobiyou/wx_channel`（2.3k stars）— Web 控制台，支持批量下载
- `putyy/res-downloader`（18.7k stars）— 通用资源嗅探下载器

---

## Phase 2: 下载视频

### 步骤 2.1: 通过直链下载视频

从 Phase 1 获取到的 `finder.video.qq.com` 直链，使用 PowerShell 下载：

```powershell
$url = "https://finder.video.qq.com/251/...&token=...&sign=..."
Invoke-WebRequest -Uri $url -OutFile "$workDir\video.mp4" -UserAgent "Mozilla/5.0"
```

验证下载：
```powershell
Test-Path "$videoFile"
Get-ChildItem "$videoFile" | Select-Object Name, Length
```

### 步骤 2.2: 备选方案 — 通过浏览器触发下载

如果直链下载失败，可使用浏览器点击下载按钮：
```bash
chrome-devtools_click(uid="下载视频按钮的uid")
```

---

## Phase 3: 视频技术分析

### 步骤 3.1: 使用 ffprobe 获取视频元数据

获取完整视频信息：
```powershell
& $ffprobe -v quiet -print_format json -show_format -show_streams "$videoFile"
```

提取关键参数：
- **容器格式**：mov/mp4
- **视频编码**：h264 (High Profile)
- **分辨率**：width × height
- **帧率**：frame_rate
- **视频码率**：bit_rate
- **总时长**：duration
- **总帧数**：nb_frames
- **音频编码**：aac (HE-AACv2)
- **音频采样率**：sample_rate
- **音频码率**：bit_rate
- **编码工具**：encoder（如 `Wxmm_9020230808` 表示微信视频号编码器）

### 步骤 3.2: 识别视频类型

根据元数据判断：
- **竖屏视频**：width < height（如 720×1560）→ 手机全屏视频
- **横屏视频**：width > height → 桌面/电影格式
- **方形视频**：width ≈ height → 社交媒体常见格式
- **编码工具**：`Wxmm_*` → 微信视频号原生编码

### 步骤 3.3: 判断是否有音频轨道

```powershell
# 检查是否有音频流
$probeResult = & $ffprobe -v quiet -print_format json -show_streams "$videoFile" | ConvertFrom-Json
$hasAudio = $probeResult.streams | Where-Object { $_.codec_type -eq "audio" }
if ($hasAudio) { Write-Output "有音频轨道，可进行语音转录" } else { Write-Output "无音频轨道" }
```

---

## Phase 4: 提取关键帧

### 步骤 4.1: 按固定间隔提取帧

```powershell
New-Item -ItemType Directory -Path "$framesDir" -Force | Out-Null

# 每秒提取2帧（fps=2），6秒视频约12帧
& $ffmpeg -y -i "$videoFile" -vf "fps=2" "$framesDir\frame_%04d.png"
```

### 步骤 4.2: 按时间点提取特定帧

```powershell
# 提取第2秒的帧
& $ffmpeg -y -i "$videoFile" -ss 2 -frames:v 1 "$workDir\frame_at_2s.png"

# 提取第4.5秒的帧
& $ffmpeg -y -i "$videoFile" -ss 4.5 -frames:v 1 "$workDir\frame_at_4.5s.png"
```

### 步骤 4.3: 仅提取关键帧（I-frames）

```powershell
& $ffmpeg -y -i "$videoFile" -vf "select=eq(pict_type\,I)" -vsync vfr "$framesDir\keyframe_%04d.png"
```

### 帧率选择建议

| 视频时长 | 建议 fps | 预计帧数 |
|---------|---------|---------|
| < 5秒 | 2-3 | 10-15 |
| 5-15秒 | 1-2 | 15-30 |
| 15-60秒 | 0.5-1 | 15-60 |
| > 60秒 | 0.2-0.5 | 20-30 |

---

## Phase 5: 音频提取与语音转录

### 步骤 5.1: 从视频中提取音频

```powershell
New-Item -ItemType Directory -Path "$audioDir" -Force | Out-Null

# 提取为 WAV 格式（ASR 最佳兼容格式，16kHz 单声道）
& $ffmpeg -y -i "$videoFile" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$audioDir\audio.wav"

# 同时提取为 MP3 格式（备用，文件更小）
& $ffmpeg -y -i "$videoFile" -vn -acodec libmp3lame -ar 16000 -ac 1 "$audioDir\audio.mp3"
```

**音频参数说明：**
- `-vn`：不包含视频流
- `-acodec pcm_s16le`：16位 PCM 编码（WAV 格式）
- `-ar 16000`：16kHz 采样率（ASR 标准采样率）
- `-ac 1`：单声道（ASR 标准声道数）

### 步骤 5.2: 验证音频提取

```powershell
# 检查音频文件
Get-ChildItem "$audioDir" | Select-Object Name, Length, LastWriteTime

# 使用 ffprobe 验证音频信息
& $ffprobe -v quiet -print_format json -show_streams "$audioDir\audio.wav"
```

### 步骤 5.3: ASR 语音转录（推荐方案）

#### 方案 A：FreeASR（推荐 — 无需注册，CLI 工具）

**安装：**
```powershell
pip install freeasr
```

**使用方式：**
```powershell
# 方式 1：CLI 直接转录
freeasr transcribe "$audioDir\audio.wav"

# 方式 2：指定语言为中文
freeasr transcribe "$audioDir\audio.wav" --language zh

# 方式 3：输出为 JSON 格式
freeasr transcribe "$audioDir\audio.wav" --output json
```

**HTTP API 方式（启动本地服务器后）：**
```powershell
# 启动 FreeASR 服务器
freeasr serve --port 8080

# 使用 curl 调用
curl -X POST http://localhost:8080/v1/audio/transcriptions -F file=@"$audioDir\audio.wav"

# 使用 Python OpenAI SDK 调用
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8080/v1', api_key='freeasr')
result = client.audio.transcriptions.create(model='freeasr-1', file=open('$audioDir/audio.wav', 'rb'))
print(result.text)
"
```

#### 方案 B：OpenAI Whisper 本地运行（离线方案）

**安装：**
```powershell
pip install openai-whisper
```

**使用方式：**
```powershell
# 方式 1：命令行
whisper "$audioDir\audio.wav" --language Chinese --output_format txt --output_dir "$audioDir"

# 方式 2：指定模型大小
# tiny: 最快，准确度最低
# base: 平衡速度和准确度（推荐短视频）
# small: 更准确，速度较慢
# medium: 高准确度，需要更多内存
# large: 最高准确度，需要 GPU
whisper "$audioDir\audio.wav" --language Chinese --model base --output_format txt --output_dir "$audioDir"

# 方式 3：输出带时间戳的字幕
whisper "$audioDir\audio.wav" --language Chinese --model base --output_format srt --output_dir "$audioDir"
```

**Python 脚本方式：**
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("$audioDir/audio.wav", language="zh")

# 输出完整文本
print(result["text"])

# 输出带时间戳的段落
for segment in result["segments"]:
    print(f"[{segment['start']:.1f}s - {segment['end']:.1f}s] {segment['text']}")
```

#### 方案 C：在线网页工具（备用方案）

如果 CLI 工具不可用，可使用以下在线工具（需手动操作）：

| 工具 | 网址 | 支持格式 | 限制 |
|------|------|---------|------|
| Any2Text | https://www.any2text.online | MP3/WAV/M4A/MP4 | 无公开限制 |
| FineVoice | https://finevoice.ai/zh/ai-speech-to-text | MP3/AAC/AMR/M4A/WAV | 30分钟/300MB |
| Whisper Web | https://whisperweb.dev/whisper-transcription | 音频URL | 浏览器内运行 |

**操作步骤：**
1. 打开在线工具网址
2. 上传 `$audioDir\audio.wav` 文件
3. 选择语言为"中文"
4. 点击"转录"按钮
5. 等待处理完成
6. 复制转录结果

### 步骤 5.4: 转录结果后处理

```powershell
# 如果使用 Whisper，会生成 .txt 和 .srt 文件
Get-ChildItem "$audioDir\*.txt" | Select-Object Name
Get-ChildItem "$audioDir\*.srt" | Select-Object Name

# 读取转录文本
$transcription = Get-Content "$audioDir\audio.txt" -Raw -Encoding UTF8
Write-Output $transcription
```

---

## Phase 6: 综合内容分析

### 步骤 6.1: 逐帧查看截图

使用 read 工具查看提取的每一帧截图：

```bash
read(filePath="C:\Users\XUJF\Downloads\vf\frame_0001.png")
read(filePath="C:\Users\XUJF\Downloads\vf\frame_0002.png")
# ... 依次查看所有帧
```

### 步骤 6.2: 内容分析维度

**视觉内容分析（逐帧）：**
- 画面主体（人物/产品/界面/文字/图表）
- 色彩方案（主色调、配色风格）
- 布局结构（全屏/分屏/画中画）
- 文字内容（标题/字幕/标签/UI文字）

**音频内容分析（转录文本）：**
- 旁白/解说内容
- 关键信息点（产品名、数据、链接）
- 语气/风格（教程/推广/访谈/新闻）
- 语速/节奏（快节奏/舒缓/停顿）

**内容类型判断：**
- 录屏演示（screencast）+ 旁白解说
- 实拍视频（live action）+ 对话/独白
- 动画/动效（motion graphics）+ 配音
- 图文混排（mixed media）+ 背景音乐
- 直播回放（live replay）+ 实时互动

### 步骤 6.3: 视觉-音频交叉验证

将视觉内容与音频转录进行交叉验证：
1. **时间对齐**：转录文本的时间戳与帧截图的时间点对应
2. **内容一致性**：旁白提到的内容是否在画面中展示
3. **信息补充**：画面中无法识别的小字/细节是否在旁白中提到
4. **遗漏发现**：画面展示但旁白未提及的内容（可能为补充信息）

---

## 生成分析报告

### 报告模板

```markdown
# 视频内容分析报告

## 基本信息
| 项目 | 详情 |
|------|------|
| 来源链接 | ... |
| 发布者 | ... |
| 发布时间 | ... |
| 视频时长 | ... |
| 分辨率 | ... |
| 文件大小 | ... |
| 有无音频 | 有/无 |

## 技术参数
| 项目 | 详情 |
|------|------|
| 编码格式 | ... |
| 帧率 | ... |
| 视频码率 | ... |
| 音频编码 | ... |
| 音频采样率 | ... |
| 音频码率 | ... |

## 内容摘要
（视频的核心内容，1-3句话概括）

## 语音转录文本
（ASR 识别的完整旁白/解说文本）

### 关键信息提取
- 产品/项目名称：...
- 核心卖点：...
- 数据指标：...
- 操作步骤：...

## 逐帧分析
### 帧 1（0-0.5秒）
- 内容描述：...
- 文字信息：...
- 视觉元素：...
- 对应旁白：...

### 帧 2（0.5-1秒）
...

## 视觉-音频交叉分析
- 一致性：旁白与画面是否匹配
- 信息密度：视觉/音频各自承载的信息量
- 互补性：哪些信息需要结合视觉+音频才能完整理解

## 内容分类
- 类型：（教程/推广/演示/娱乐/资讯...）
- 主题：（前端开发/AI工具/设计系统/...）
- 目标受众：（开发者/设计师/产品经理/...）

## 关键发现
1. ...
2. ...
3. ...

## 相关资源
- 项目地址：...
- 工具链接：...
- 参考文档：...
```

---

## 完整工作流示例

```powershell
# === 环境配置 ===
$ffmpegPath = "D:\ffmpeg-7.0.2-full_build\bin"
$ffprobe = "$ffmpegPath\ffprobe.exe"
$ffmpeg = "$ffmpegPath\ffmpeg.exe"
$workDir = "$env:USERPROFILE\Downloads"
$videoFile = "$workDir\video.mp4"
$framesDir = "$workDir\vf"
$audioDir = "$workDir\audio"

# === Phase 1: 获取视频信息 ===
chrome-devtools_new_page(url="https://weixin.qq.com/sph/Avu1QzJAdR")
chrome-devtools_take_snapshot()

# 使用在线解析工具
chrome-devtools_navigate_page(type="url", url="https://sph.litao.workers.dev/")
chrome-devtools_fill(uid="输入框uid", value="https://weixin.qq.com/sph/Avu1QzJAdR")
chrome-devtools_click(uid="查询按钮uid")
chrome-devtools_wait_for(text=["下载", "失败"])

# === Phase 2: 下载视频 ===
Invoke-WebRequest -Uri "$videoUrl" -OutFile "$videoFile" -UserAgent "Mozilla/5.0"

# === Phase 3: 视频技术分析 ===
& $ffprobe -v quiet -print_format json -show_format -show_streams "$videoFile"

# === Phase 4: 提取关键帧 ===
New-Item -ItemType Directory -Path "$framesDir" -Force | Out-Null
& $ffmpeg -y -i "$videoFile" -vf "fps=2" "$framesDir\frame_%04d.png"

# === Phase 5: 音频提取与转录 ===
New-Item -ItemType Directory -Path "$audioDir" -Force | Out-Null
& $ffmpeg -y -i "$videoFile" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$audioDir\audio.wav"

# ASR 转录（选择一种方案）
# 方案 A: FreeASR
freeasr transcribe "$audioDir\audio.wav" --language zh

# 方案 B: Whisper
# whisper "$audioDir\audio.wav" --language Chinese --model base --output_format txt --output_dir "$audioDir"

# === Phase 6: 综合分析 ===
# 逐帧查看
read(filePath="$framesDir\frame_0001.png")
read(filePath="$framesDir\frame_0002.png")
# ... 查看所有帧

# 读取转录文本
$transcription = Get-Content "$audioDir\audio.txt" -Raw -Encoding UTF8

# === 生成报告 ===
# 结合视觉分析 + 音频转录，生成完整分析报告
```

---

## 注意事项

### 下载相关
1. **视频号反爬**：微信视频号直链有时效性（token/sign 参数），需尽快使用
2. **画质选择**：在线解析工具默认提供标准画质，原始画质需额外下载
3. **编码兼容**：微信视频号使用 `Wxmm_*` 编码器，部分旧版 ffmpeg 可能不兼容

### 帧提取相关
4. **帧率策略**：对于快速切换的画面，建议 fps≥2 以捕获所有关键画面
5. **文字识别**：如截图中文字较小，可使用 OCR 工具（如 Tesseract）辅助识别

### 音频转录相关
6. **音频格式**：ASR 最佳输入格式为 16kHz 单声道 WAV
7. **噪音影响**：背景音乐过大会影响语音识别准确度
8. **方言/口音**：Whisper 对标准普通话识别效果最好，方言可能需要 larger 模型
9. **长视频分段**：超过 30 分钟的视频建议分段提取和转录
10. **FreeASR 限制**：依赖豆包输入法 ASR 服务，可能存在速率限制，服务可用性可能变化
11. **Whisper 硬件**：本地运行 Whisper 需要较大内存，GPU 加速可显著提升速度

### 综合分析相关
12. **交叉验证**：视觉内容与音频转录应相互验证，发现不一致时需进一步确认
13. **时间对齐**：将转录文本的时间戳与帧截图对应，便于理解内容上下文
