# Skills

Skills 集合仓库。每个子目录包含一个独立 skill。

## 目录

### pi

根据 [Pi 官方文档](https://pi.dev/docs/latest) 创建的 skills。

| Skill | 说明 |
|-------|------|
| [pi/pi-coding-agent](pi/pi-coding-agent.mdc) | Pi 配置与使用完全指南 — 安装、认证、交互模式、会话管理、设置、CLI 参考等 |
| [pi/pi-skill-creator](pi/pi-skill-creator.mdc) | Pi Skills 开发指南 — SKILL.md 格式、frontmatter 规范、加载位置、验证规则 |
| [pi/pi-extension-creator](pi/pi-extension-creator.mdc) | Pi Extensions 开发指南 — TypeScript 扩展、事件系统、工具注册、自定义 UI、包发布 |

### cloudflare

根据 [Cloudflare 官方文档](https://developers.cloudflare.com/) 创建的 skills。

| Skill | 说明 |
|-------|------|
| [cloudflare/cloudflare-agents](cloudflare/cloudflare-agents.mdc) | Cloudflare Agents SDK 完全指南 — Agent 类、Think 框架、状态管理、调度、工具、子代理 |
| [cloudflare/workers-ai](cloudflare/workers-ai.mdc) | Cloudflare Workers AI 完全指南 — 模型目录、Workers 绑定、Vercel AI SDK 集成、REST API、定价 |

### MiniMax (from [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills))

根据 MiniMax 官方技能仓库导入的 skills，覆盖移动端开发、前端、全栈、文档处理、创意工具等多个领域。

| Skill | 说明 |
|-------|------|
| [android-native-dev](android-native-dev/SKILL.md) | Android (Kotlin/Compose) 原生开发指南 — Material Design 3、Gradle 配置、测试策略 |
| [buddy-sings](buddy-sings/SKILL.md) | AI 伴侣唱歌技能 — 生成并播放带人声的歌曲 |
| [flutter-dev](flutter-dev/SKILL.md) | Flutter 跨平台开发指南 — Widget 模式、Riverpod/Bloc 状态管理、GoRouter 导航 |
| [frontend-dev](frontend-dev/SKILL.md) | 高级前端开发 — Bento 设计、Framer Motion/GSAP 动画、AI 媒体资产生成 |
| [fullstack-dev](fullstack-dev/SKILL.md) | 全栈后端架构 — 三层架构、错误处理、认证、实时通信、生产加固 |
| [gif-sticker-maker](gif-sticker-maker/SKILL.md) | 照片转 GIF 贴纸 — Funko Pop / Pop Mart 盲盒风格动画贴纸 |
| [ios-application-dev](ios-application-dev/SKILL.md) | iOS (UIKit/SwiftUI) 开发指南 — 44pt 触控目标、Dynamic Type、暗黑模式 |
| [minimax-docx](minimax-docx/SKILL.md) | DOCX 文档创建/编辑/格式化 — OpenXML SDK、13 种排版风格配方 |
| [minimax-multimodal-toolkit](minimax-multimodal-toolkit/SKILL.md) | MiniMax CLI 工具参考 — 文本/图像/视频/语音/音乐生成 |
| [minimax-music-gen](minimax-music-gen/SKILL.md) | 音乐生成 — 基础模式与高级控制模式，支持翻唱、多语言歌词 |
| [minimax-music-playlist](minimax-music-playlist/SKILL.md) | 个性化歌单生成 — 分析音乐品味，生成完整歌单与封面 |
| [minimax-pdf](minimax-pdf/SKILL.md) | PDF 创建/填写/重排版 — 15 种文档类型、Token 设计系统 |
| [minimax-xlsx](minimax-xlsx/SKILL.md) | Excel 文件创建/编辑/验证 — XML 模板、公式验证、金融配色标准 |
| [pptx-generator](pptx-generator/SKILL.md) | PowerPoint 创建/编辑 — 5 种幻灯片类型、PptxGenJS API |
| [react-native-dev](react-native-dev/SKILL.md) | React Native/Expo 开发指南 — FlashList、Reanimated 3、Expo Router |
| [shader-dev](shader-dev/SKILL.md) | GLSL 着色器效果 — 光线步进、SDF 建模、流体模拟、粒子系统 |
| [vision-analysis](vision-analysis/SKILL.md) | 图像分析 — 描述、OCR、UI 审查、图表数据提取、目标检测 |

### Superpowers (from [obra/superpowers](https://github.com/obra/superpowers))

从 obra/superpowers (v5.1.0) 导入的软件开发方法学 skills，覆盖从头脑风暴到分支完成的完整工作流。

| Skill | 说明 |
|-------|------|
| [using-superpowers](using-superpowers/SKILL.md) | 引导技能：如何发现和调用所有 skills，技能优先级表 |
| [brainstorming](brainstorming/SKILL.md) | 设计精炼：探索上下文、提问、提出方案、编写规格文档 |
| [writing-plans](writing-plans/SKILL.md) | 实现计划编写：将规格拆分为可执行的小任务（2-5 分钟） |
| [executing-plans](executing-plans/SKILL.md) | 计划执行：在独立会话中执行计划，含检查点机制 |
| [subagent-driven-development](subagent-driven-development/SKILL.md) | 子代理驱动开发：每任务分发子代理，两阶段审查（规格 + 质量） |
| [dispatching-parallel-agents](dispatching-parallel-agents/SKILL.md) | 并行代理分发：为独立任务同时分发多个子代理 |
| [test-driven-development](test-driven-development/SKILL.md) | TDD：RED-GREEN-REFACTOR 循环，铁律，反模式对照表 |
| [systematic-debugging](systematic-debugging/SKILL.md) | 系统化调试：4 阶段根因分析流程，含调用栈回溯、防御深度等配套技术 |
| [requesting-code-review](requesting-code-review/SKILL.md) | 代码审查请求：规范化的审查提交流程 |
| [receiving-code-review](receiving-code-review/SKILL.md) | 接收审查反馈：如何评估和回应代码评审意见 |
| [finishing-a-development-branch](finishing-a-development-branch/SKILL.md) | 分支完成：合并/PR/保留/丢弃决策工作流 |
| [using-git-worktrees](using-git-worktrees/SKILL.md) | Git Worktree 使用：通过原生工具或 git worktrees 创建隔离工作区 |
| [verification-before-completion](verification-before-completion/SKILL.md) | 完成前验证：先提供证据再声称完成的验证门禁 |
| [writing-skills](writing-skills/SKILL.md) | 元技能：如何编写新 skills — 将 TDD 应用于文档创作 |

## 使用

将所需 skill 目录链接到你的 agent 配置即可。详见各子目录的说明。

### 来源

| 来源 | 仓库地址 | Skills 数量 |
|------|---------|------------|
| 原生 | — | 2 (pi, cloudflare) |
| MiniMax | [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills) | 17 |
| Superpowers | [obra/superpowers](https://github.com/obra/superpowers) | 14 |