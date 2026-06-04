# Pi Coding Agent Skills

根据 [Pi 官方文档](https://pi.dev/docs/latest) 创建的 skills 集合。

## 包含的 Skills

| Skill | 说明 |
|-------|------|
| `pi-coding-agent` | Pi 配置与使用完全指南 — 安装、认证、交互模式、会话管理、设置、CLI 参考等 |
| `pi-skill-creator` | Pi Skills 开发指南 — SKILL.md 格式、frontmatter 规范、加载位置、验证规则 |
| `pi-extension-creator` | Pi Extensions 开发指南 — TypeScript 扩展、事件系统、工具注册、自定义 UI、包发布 |

## 使用方法

将本仓库的 skills 链接到你的 Pi 配置：

```json
// ~/.pi/agent/settings.json
{
  "skills": ["/path/to/this/repo/pi"]
}
```

然后在 Pi 中通过 `/skill:name` 使用，或让 agent 自动检测加载。

## 参考文档

所有内容均来自 [Pi 官方文档](https://pi.dev/docs/latest)，覆盖：
- [Skills](https://pi.dev/docs/latest/skills)
- [Extensions](https://pi.dev/docs/latest/extensions)
- [Usage](https://pi.dev/docs/latest/usage)
- [Settings](https://pi.dev/docs/latest/settings)
- [Quickstart](https://pi.dev/docs/latest/quickstart)
- [Packages](https://pi.dev/docs/latest/packages)
- [Prompt Templates](https://pi.dev/docs/latest/prompt-templates)