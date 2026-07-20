# OpenCode Skills Collection

OpenCode 技能合集 - 扩展 AI 编程助手的能力

## Skills 列表

### wxvideos - 微信视频号视频分析

微信视频号视频下载与内容分析工具链。

**功能：**
- 从 weixin.qq.com/sph/ 链接解析视频信息
- 下载视频（支持直链下载）
- 使用 ffprobe 分析视频技术参数
- 使用 ffmpeg 提取关键帧
- 音频提取与 ASR 语音转录
- 综合视觉+音频内容分析
- 生成结构化分析报告

**触发词：** 视频号分析、下载视频号、分析视频内容、wxvideos、sph下载、微信视频下载、语音转文字

**依赖工具：**
- ffmpeg/ffprobe（视频处理）
- 浏览器工具（页面解析）
- ASR 服务（语音转文字）

---

### chinese-colors - 中国传统色配色工具

基于中国传统色彩体系的专业配色方案生成工具。

**功能：**
- 40+ 中国传统色查询（HEX/RGB/寓意）
- 10组经典双色搭配方案
- 5套国风五色主题方案
- 60-30-10 配色法则指导
- 按场景/季节快速查询配色
- 色彩心理学参考

**触发词：** 配色、中国传统色、色彩搭配、配色方案、国风配色、配色灵感

**包含色系：**
- 红色系（朱砂、海棠、胭脂、落霞等）
- 黄色系（栀子、鹅黄、姜黄、赤金等）
- 蓝色系（石青、靛蓝、景泰蓝、月白等）
- 绿色系（松柏、青葱、竹青、霜绿等）
- 紫色系（魏紫、丁香、藤紫、雪青等）
- 中性色（墨色、玄青、素色、藕色等）

---

## 安装

将对应目录下的 `SKILL.md` 文件复制到 OpenCode skills 目录：

```bash
# 默认路径
~/.config/opencode/skills/<skill-name>/SKILL.md
```

## 使用

在 OpenCode 中直接调用 skill 即可：

```bash
# 加载 wxvideos skill
skill("wxvideos")

# 加载 chinese-colors skill
skill("chinese-colors")
```

## 许可证

MIT License
