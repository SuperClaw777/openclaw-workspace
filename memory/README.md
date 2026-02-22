# 如何使用 Kimi Claw 自我迭代系统

## 快速开始

### 1. 添加任务
编辑 `memory/tasks.json`：
```json
{
  "tasks": [
    {
      "id": "task-001",
      "title": "开发一个爬虫",
      "description": "抓取某网站数据",
      "priority": "high",
      "status": "pending",
      "createdAt": "2026-02-22T04:00:00+08:00",
      "deadline": "2026-02-23T18:00:00+08:00"
    }
  ]
}
```

### 2. 我会自动
- 每 30 分钟检查一次任务队列
- 自动分解复杂任务
- 派生子代理执行
- 汇报进度到 Telegram

### 3. 任务状态
- `pending` - 等待执行
- `in_progress` - 正在执行
- `completed` - 已完成
- `blocked` - 需要用户确认

## 紧急任务
如果需要我立即处理，直接发消息：
" urgent: 帮我写个脚本 xxx"

## 每日报告
每天 23:00 自动发送工作总结到 Telegram

## 文件位置
- 任务队列：`memory/tasks.json`
- 工作日志：`memory/worklog.md`
- 心跳配置：`HEARTBEAT.md`
