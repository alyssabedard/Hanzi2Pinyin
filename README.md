<div align="center">
<h1 style="font-family: monospace;">Hanzi2Pinyin</h1>
<!-- Anki Rate --><a href="https://ankiweb.net/shared/info/77106192"><img src="https://img.shields.io/badge/AnkiWeb-Rate-6cb5e7?style=for-the-badge&labelColor=grey&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cGF0aCBkPSJNNjYuNTk3IDMxLjgwOGMtLjY0Ljc2My00LjQ1OC0xLjMzNi01LjQyNC0xLjA5NC0uOTY2LjI0Mi0zLjM0MyAzLjg5My00LjI2NyAzLjUyMS0uOTI0LS4zNzItLjEwOC00LjY1Mi0uNjM2LTUuNDk2LS41MjktLjg0NC00LjczNi0xLjk3Ny00LjY2OC0yLjk3LjA2OS0uOTk0IDQuMzkxLTEuNTQgNS4wMy0yLjMwNC42NC0uNzYzLjQxNy01LjExNSAxLjM4NC01LjM1Ny45NjYtLjI0MiAyLjgyIDMuNyAzLjc0NSA0LjA3My45MjMuMzcyIDQuOTkzLTEuMTg0IDUuNTIyLS4zNC41MjkuODQ0LTIuNjQ4IDMuODI2LTIuNzE2IDQuODItLjA2OC45OTMgMi42NyA0LjM4MyAyLjAzIDUuMTQ3eiIgc3R5bGU9ImZpbGw6IzAwODRkZDtzdHJva2U6I2ZmZmZmZjtzdHJva2Utd2lkdGg6MiIvPjxwYXRoIGQ9Ik01OS43MTIgODIuMzU2Yy0yLjMzNSAyLjc4OS0xNi4yOC00Ljg3Ny0xOS44MDgtMy45OTMtMy41MjguODgzLTEyLjIxMiAxNC4yMTgtMTUuNTg2IDEyLjg2LTMuMzc0LTEuMzYtLjM5My0xNi45OS0yLjMyMy0yMC4wNzMtMS45MzEtMy4wODItMTcuMjk3LTcuMjItMTcuMDQ3LTEwLjg1LjI1LTMuNjI4IDE2LjAzNy01LjYyMyAxOC4zNzItOC40MTIgMi4zMzUtMi43ODggMS41MjMtMTguNjggNS4wNS0xOS41NjQgMy41MjktLjg4NCAxMC4zMDUgMTMuNTE0IDEzLjY3OCAxNC44NzMgMy4zNzQgMS4zNTkgMTguMjM4LTQuMzI1IDIwLjE2OC0xLjI0MyAxLjkzMSAzLjA4My05LjY2OSAxMy45NzYtOS45MTggMTcuNjA1LS4yNSAzLjYyOCA5Ljc0OCAxNi4wMDggNy40MTQgMTguNzk3eiIgc3R5bGU9ImZpbGw6IzAwODRkZDtzdHJva2U6I2ZmZmZmZjtzdHJva2Utd2lkdGg6MiIvPjwvc3ZnPg==" /></a>
<!-- GitHub Release --><a href="https://github.com/alyssabedard/Hanzi2Pinyin/releases"><img src="https://img.shields.io/github/v/release/alyssabedard/Hanzi2Pinyin?style=for-the-badge&labelColor=%231C1C1C&color=%23A692E3&logo=github" /></a>
</div>

<div align="center"><br>
    <img src="docs/screenshots/demo-liuqi.gif" width="600" alt="Demo of Hanzi2Pinyin"/>
</div>
<br>
<div align="center">
💜 For the <span style="color:#CBC3E3;">Quick Start Guide</span> click <a style="color:#9c87db;" href="https://github.com/alyssabedard/Hanzi2Pinyin/blob/master/docs/quick_start_guide.md">here</a>💜
</div>
<div align="center">
To download the companion Anki note type click <a style="color:#9c87db;" href="https://github.com/alyssabedard/Hanzi2Pinyin-notetype">here</a>
</div>


## Description
This [Anki](https://apps.ankiweb.net/) add-on lets you add **Pinyin** and **Zhuyin** readings above Chinese characters 
(Hanzi) in **any field**.

It works by converting your Chinese text into [ruby](https://en.wikipedia.org/wiki/Ruby_character) annotations, where 
the Pinyin appears as small text 
above the original characters, making it easier to read and study Chinese text.

_[Why Hanzi2Pinyin when there are other great add-ons?](#why-Hanzi2Pinyin-when-there-are-other-great-add-ons)_

> ⚠️ For the [ruby](https://en.wikipedia.org/wiki/Ruby_character) annotation to work
> use this [Anki note type](https://github.com/alyssabedard/Hanzi2Pinyin-notetype) made specifically for this add-on.
> 
> Read the [Anki documentation on Ruby characters](https://docs.ankiweb.net/templates/fields.html?highlight=furigana#ruby-characters).
 


_Looking for the Quick Start Guide? Need help? Want to raise an issue? Looking for documentation? See [Contributing & Support](#contributing--support)_

<div align="center">
<b>Example</b>
</div>



| Type          | Pinyin                                                                        | Zhuyin                                                                         |
|---------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Hanzi         | 你好                                                                            | 你好                                                                             |
| Hanzi to Ruby | `你[nǐ]好[hǎo]`                                                                 | `你[ㄋㄧˇ]好[ㄏㄠˇ]`                                                                 |
| HTML Code     | `<ruby>你<rt>nǐ</rt></ruby><ruby>好<rt>hǎo</rt></ruby>`                         | `<ruby>你<rt>ㄋㄧˇ</rt></ruby><ruby>好<rt>ㄏㄠˇ</rt></ruby>`                         |
| HTML Output   | <div align="center"><ruby>你<rt>nǐ</rt></ruby><ruby>好<rt>hǎo</rt></ruby></div> | <div align="center"><ruby>你<rt>ㄋㄧˇ</rt></ruby><ruby>好<rt>ㄏㄠˇ</rt></ruby></div> |



## Demo

<div align="center"><br>
    <img src="docs/screenshots/demo-pinyin.gif" width="800" alt="Demo of Hanzi2Pinyin"/>
   <img src="docs/screenshots/demo-sentencepinyin.gif" width="500" alt="Demo"/>
    <div>⬇️</div>
   <img src="docs/screenshots/demo-sentencepinyin-html.gif" width="400" alt="Demo"/>
</div>

<details>
    <summary>Demo with Zhuyin</summary>
    <div align="center"><br>
        <img src="docs/screenshots/demo-zhuyin.gif" width="800" alt="Demo of Hanzi2Pinyin"/>
    </div>
</details>

<details>
    <summary>Demo Tools settings (macOS)</summary>
    <div align="center"><br>
        <img src="docs/screenshots/demo-settings.gif" width="800" alt="Demo of Hanzi2Pinyin"/>
    </div>
</details>

## Features
- [x] Pinyin support - _Browse_ editor dialog
- [x] Pinyin support - _Add_ editor dialog
- [x] Zhuyin (Bopomofo) support 
- [x] Note Type that supports ruby text for Chinese

Key benefits:
- Works with any field name of your choosing (No restrictions)
- Simple and reliable functionality
- Support both Simplified and Traditional Chinese Characters 

### Planned Features

| Status | Feature                | Details                                                              |
|--------|------------------------|----------------------------------------------------------------------|
| 🔄     | Bulk add/remove        | Available in tools menu                                              |
| 🔄     | Jyutping and Cantonese | Support for Cantonese pronunciation                                  |
| 🔄     | Xiao'erjing            | Support for Arabic-Persian script (also known as Xiaor jin/Xiaojing) |
| 🔄     | Sandhi                 | Support for phonological changes between adjacent tones _(Note 1)_   |

> Note 1: Sandhi refers to how tones change when certain tones/words are next to each other in 
> speech. For example, in Mandarin, when a hanzi with the third 
> tone is followed by another hanzi with the third tone, 
> the first hanzi changes to second tone instead.

I plan on making additional Chinese language tools that will be 
released as separate add-ons to maintain simplicity as 
I prefer single-purpose add-ons.


## Why Hanzi2Pinyin when there are other great add-ons?
This add-on focuses on simplicity and flexibility. While many add-ons offer extensive features, 
they often come with drawbacks:
- Break when Anki or Qt versions are updated
- Restrict you to specific field names
- Bundle multiple features you might not need


## Contributing & Support

| Type                                                                     | Description                     |
|--------------------------------------------------------------------------|---------------------------------|
| [Issues & Requests](https://github.com/alyssabedard/Hanzi2Pinyin/issues) | Bug reports or feature requests | 
| [Contributing](.github/CONTRIBUTING.md)                                  | Fork the repo and submit a PR   |
| [Discussions](https://github.com/alyssabedard/Hanzi2Pinyin/discussions)  | Getting help and questions      |
| [Support](.github/SUPPORT.md)                                            | Support                         |
| [Quick Start Guide](docs/quick_start_guide.md)                           | Quick Start Guide               |
| [Technical documentation](docs/development.md)                           | Technical documentation         |

**OS**  
This script has been primarily tested on macOS and Windows.  I currently don't have access 
to a Linux machine for thorough testing.


## Acknowledgements

### Libraries
| Library | Links |
|---------|-------|
| jieba | [PyPi](https://pypi.org/project/jieba/), [GitHub](https://github.com/fxsjy/jieba) |
| pypinyin | [PyPi](https://pypi.org/project/pypinyin/), [GitHub](https://github.com/mozillazg/python-pinyin) |

### Other
| Description   | Source                                 |
|---------------|----------------------------------------|
| Anki SVG logo | [Glutanimate](https://glutanimate.com) |


<div align="center"><br>
    <p>加油</p>
    <img src="docs/screenshots/liuqi-jiayou.gif" width="200" alt="Demo of Hanzi2Pinyin"/>
</div>