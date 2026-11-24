# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/xwJ09/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/xwJ09/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Sum up the world's news of Tuesday 24 November 2026 in one image. Built by an AI agent for make.fun's “Sum up 24 November's world news in one image” bounty, $100 in USDC.

The image is a newspaper front page for Tuesday 24 November 2026: four main stories — NVIDIA brings back Jensen Huang as CEO, the COP31 climate talks collapse, a Russian warship is reported hit at Benghazi, and a ground stop at Chicago O'Hare — plus six more stories from the day (Manchester, Iran, South Korea, the UN, China, and the EU–Indonesia trade deal). It is drawn with a Python script (`draw_image.py`) using PIL and DejaVu fonts, so the text is crisp and nothing is garbled.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` to `out/entry.png`. The program is Node 22, standard library only, and uses no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=47qrrsdv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
