"""Write and search memories in an existing AgentCore MemoryStore."""

import asyncio

from agentcore import AsyncAgentCore
from agentcore.memory import MemoryScope, MemoryTaskStatus


async def main():
    async with AsyncAgentCore.auto() as core:
        store = core.memory_store("test-memory")
        await store.add_memories(
            scope=MemoryScope(user_id="example-user", session_id="session-1"),
            text="用户喜欢简短的中文回答。",
        )

        submission = await store.add_memories(
            scope=MemoryScope(user_id="example-user", session_id="session-2"),
            text="昨天完成了项目评审。",
            reference_time="2026-09-18T10:00:00+08:00",
            sync=False,
        )
        while True:
            task = await store.get_memory_task(submission.task_id)
            if task.status not in {MemoryTaskStatus.PENDING, MemoryTaskStatus.RUNNING}:
                break
            await asyncio.sleep(1)
        if task.status is MemoryTaskStatus.UNKNOWN:
            print("异步写入结果未知，不自动重新提交 Add。")

        # Newly added memories may take time to become searchable.
        result = await store.search_memories(
            "用户有哪些回答偏好？",
            scope=MemoryScope(user_id="example-user"),
            top_k=5,
        )
        for hit in result.memories:
            print(hit.memory.content.text)


if __name__ == "__main__":
    asyncio.run(main())
