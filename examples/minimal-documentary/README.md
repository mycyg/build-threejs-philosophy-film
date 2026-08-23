# Sample：河流留下的名字

这是一个虚构的 24 秒微型纪录片预制作工程。它停在分镜已经确认、声音与素材尚未生产的阶段，因此可以通过 `plan` 校验，但不会通过 `assets`、`audio` 或 `rendered` 校验。

```bash
python3 ../../scripts/validate_project.py --project . --stage plan
python3 ../../scripts/build_asset_queue.py --project . --replace
```

Sample 的重点是展示数据关系：原文进入证据账本，证据进入镜头，镜头声明素材需求，确认记录固定分镜修订号，素材队列再把每项需求展开为多张候选图。
