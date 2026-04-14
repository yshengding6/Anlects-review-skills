# -*- coding: utf-8 -*-
"""
文化比较核心模块 (Cultural Comparison Module)
cultural-comparator v2.0.0

功能：三层文化比较——诸子百家横向对话 + 东西方思想纵深对照 + 宗教传统交叉审视
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ========================================
# 诸子百家核心观点库（精简版）
# ========================================

ZHUZI_DB = {
    "孔子": {
        "core": {"仁": "爱人克己", "礼": "和为贵", "义": "喻于义", "忠恕": "己所不欲"},
        "人性": "性相近", "方法": "启发因材", "政治": "为政以德"
    },
    "孟子": {
        "core": {"性善": "水就下", "仁政": "民贵君轻", "四端": "恻隐羞恶", "王道": "以德王"},
        "人性": "性善论", "方法": "推己及人", "政治": "民本"
    },
    "荀子": {
        "core": {"性恶": "其善伪也", "礼法": "隆礼重法", "天人之分": "制天命用之"},
        "人性": "性恶论", "方法": "解蔽积伪", "政治": "礼法兼治"
    },
    "老子": {
        "core": {"道": "道法自然", "无为": "无不为", "柔弱": "胜刚强", "自然": "人法天地"},
        "人性": "自然素朴", "方法": "致虚守静", "政治": "无为而治"
    },
    "庄子": {
        "core": {"逍遥": "乘天地正", "齐物": "万物一马", "天籁": "吹万不同"},
        "人性": "天性完整", "方法": "寓言重言", "政治": "不刻意"
    },
    "墨子": {
        "core": {"兼爱": "爱无差等", "非攻": "兴天下利", "尚贤": "政之本", "节用": "民用则止"},
        "人性": "性可善", "方法": "三表法", "政治": "兼爱尚同"
    },
    "韩非子": {
        "core": {"法": "国之权衡", "术": "循名责实", "势": "胜者王", "耕战": "农战兴国"},
        "人性": "性恶自为", "方法": "参验功用", "政治": "法治集权"
    },
}

# 西方哲学核心观点库（精简版）
WESTERN_DB = {
    "苏格拉底": {
        "core": {"美德知识": "无人有意作恶", "产婆术": "问答引导", "认识自己": "未经省察的人生不值得过"},
        "方法": "反诘法", "政治": "德性治国"
    },
    "柏拉图": {
        "core": {"理念论": "现实是影子", "哲学王": "哲人王统治", "洞穴隐喻": "走出洞穴看阳光", "正义": "各安其位"},
        "方法": "辩证法", "政治": "理想国"
    },
    "亚里士多德": {
        "core": {"中道": "两极端之间", "目的论": "幸福是终极目的", "友爱": "生活的必需品", "实体": "个别事物"},
        "方法": "经验归纳", "政治": "混合政体"
    },
    "康德": {
        "core": {"绝对命令": "愿成为普遍法则", "人是目的": "不止视为手段", "物自体": "不可知", "理性": "有界限"},
        "方法": "先验演绎", "政治": "永久和平"
    },
    "尼采": {
        "core": {"权力意志": "生命追求超越", "超人": "大地之意义", "虚无主义": "上帝死了", "永恒轮回": "热爱命运"},
        "方法": "谱系学", "政治": "批判民主"
    },
    "萨特": {
        "core": {"存在先于本质": "人先存在后成什么", "自由": "命中注定", "责任": "选择即责任", "他人地狱": "他人是异化"},
        "方法": "现象学", "政治": "介入承担"
    },
    "边沁/密尔": {
        "core": {"功利": "最大幸福", "伤害原则": "不伤害他人", "自由": "个性发展", "质量": "高质量快乐"},
        "方法": "效益计算", "政治": "代议民主"
    },
    "斯多葛派": {
        "core": {"自然": "按自然生活", "自足": "内在自由", "区分": "可控与不可控"},
        "方法": "哲学实践", "政治": "世界公民"
    },
}

# 概念对应映射
CONCEPT_MAP = {
    "仁": {
        "zh": ["孔子仁", "孟子仁政"],
        "confucian": {"孔子": "克己复礼，忠恕爱人", "孟子": "恻隐之心，仁之端"},
        "western": {
            "亚里士多德": "phronesis(实践智慧)/agape(博爱)",
            "康德": "善意(good will)，人是目的",
            "边沁/密尔": "最大幸福原则",
        },
        "similar": "都关注人际道德，都强调利他",
        "diff": "儒家仁是情感发用，西方是理性原则；儒家重推恩，西方重契约"
    },
    "义": {
        "zh": ["孔子义", "孟子义", "荀子礼法"],
        "western": {
            "康德": "定言命令，道德律令",
            "柏拉图": "正义(dikaiosyne)",
            "亚里士多德": "justice，中道",
        },
        "similar": "都强调道德正当性，都反对唯利是图",
        "diff": "儒家义侧重内在情感外发，西方义侧重外在规范"
    },
    "礼": {
        "zh": ["周礼", "孔子礼", "荀子礼法"],
        "western": {
            "亚里士多德": "中道，仪式美德",
            "柏拉图": "秩序，和谐",
            "康德": "道德法则",
        },
        "similar": "都规范行为，都维护秩序",
        "diff": "儒家礼是情感化规范（礼乐教化），西方是理性规范"
    },
    "天命": {
        "zh": ["孔子天命", "孟子尽心知命"],
        "western": {
            "柏拉图": "理念，永恒真理",
            "康德": "物自体，绝对命令",
            "基督教": "上帝旨意",
        },
        "similar": "都承认超越性存在，都认为人应服从更高法则",
        "diff": "儒家天命内化为人性，西方超越外在"
    },
    "君子": {
        "zh": ["孔子君子", "孟子大人"],
        "western": {
            "亚里士多德": "有德之人",
            "柏拉图": "哲学家王",
            "康德": "道德行动者",
        },
        "similar": "都追求完美人格，都强调道德修养",
        "diff": "儒家君子重社会角色，西方哲人重理性卓越"
    },
    "无为": {
        "zh": ["老子无为", "庄子逍遥"],
        "western": {
            "斯多葛派": "顺其自然",
            "爱比克泰德": "区分可控/不可控",
            "第欧根尼": "按自然生活",
        },
        "similar": "都反对过度干预，都追求自然",
        "diff": "道家无为是退隐超越，斯多葛是理性接纳"
    },
    "性善": {
        "zh": ["孟子性善", "荀子性恶", "董仲舒性三品"],
        "western": {
            "柏拉图": "灵魂回忆",
            "卢梭": "高贵的野蛮人",
            "康德": "善意内在于理性",
        },
        "similar": "都认为人有向善可能",
        "diff": "孟子是情感四端，西方多是理性本质"
    },
}


# ========================================
# 宗教传统观点库（v2.0.0 新增）
# ========================================

# 东亚宗教
EASTERN_RELIGION_DB = {
    "儒教(礼制)": {
        "天": "天命靡常，唯德是辅",
        "人": "天地之性人为贵",
        "修行": "修身齐家治国平天下",
        "与儒关系": "本体",
        "超越性": "内在超越（天命→性→心）",
        "救赎": "成圣（尽心知性知天）",
        "仪式": "礼（祭祀、冠婚丧祭）",
    },
    "道教": {
        "天": "天道自然，天法道道法自然",
        "人": "性命双修",
        "修行": "内丹外丹，炼精化气",
        "与儒关系": "互补/竞争",
        "超越性": "自然超越（返璞归真）",
        "救赎": "得道成仙",
        "仪式": "斋醮、符箓、内丹修炼",
    },
    "中国佛教": {
        "天": "天是六道之一，仍在轮回",
        "人": "众生皆有佛性",
        "修行": "戒定慧三学",
        "与儒关系": "融合/批判",
        "超越性": "内在超越（佛性本具）",
        "救赎": "解脱涅槃",
        "仪式": "诵经、禅修、忏法",
    },
}

# 亚伯拉罕传统
ABRAHAMIC_RELIGION_DB = {
    "犹太教": {
        "神": "唯一神，与以色列立约",
        "人": "按神形象造，有自由意志",
        "救赎": "守律法（托拉）",
        "与儒对照": "天命 vs 神意：天命可内化，神意始终外在",
        "超越性": "完全外在超越",
        "核心差异": "契约关系 vs 天人合一",
    },
    "基督教": {
        "神": "三位一体，道成肉身",
        "人": "原罪堕落，需救赎",
        "救赎": "因信称义",
        "与儒对照": "性善 vs 原罪：人性可否自足向善？",
        "超越性": "外在超越（道成肉身 bridging）",
        "核心差异": "恩典 vs 修身：救赎来自外部还是自身？",
    },
    "伊斯兰教": {
        "神": "真主独一，至大至慈",
        "人": "代治者，有选择权",
        "救赎": "顺从真主（伊斯兰=顺从）",
        "与儒对照": "顺天 vs 顺主：超越性的方向不同",
        "超越性": "完全外在超越",
        "核心差异": "天命可敬而远之 vs 真主须完全顺从",
    },
}

# 南亚传统
SOUTH_ASIAN_RELIGION_DB = {
    "印度教": {
        "终极": "梵我合一（Atman = Brahman）",
        "人": "轮回主体（Atman）",
        "救赎": "解脱（moksha）——打破轮回",
        "与儒对照": "天人合一 vs 梵我合一：合一的路径截然不同",
        "超越性": "内在即超越",
        "核心差异": "儒家合一是道德性的，印度教合一是本体性的",
    },
    "上座部佛教": {
        "终极": "涅槃（无我、寂灭）",
        "人": "五蕴和合，无恒常自我",
        "救赎": "涅槃——彻底止息苦",
        "与儒对照": "无我 vs 性善：如果无我，谁来修身？",
        "超越性": "否定超越（无我即超越）",
        "核心差异": "儒家预设道德主体，佛教解构主体",
    },
    "大乘佛教": {
        "终极": "真如佛性，空性中道",
        "人": "众生皆有佛性",
        "救赎": "菩萨道（自利利他）",
        "与儒对照": "人皆可为尧舜 vs 众生皆有佛性：表面相似但路径不同",
        "超越性": "内在超越（佛性本具）",
        "核心差异": "尧舜是道德理想，佛性是存在论基础",
    },
}

# 宗教维度概念映射
RELIGION_CONCEPT_MAP = {
    "天命": {
        "东亚": {"儒教": "天命靡常", "道教": "天道自然", "佛教": "天为六道"},
        "亚伯拉罕": {"犹太教": "神意立约", "基督教": "神意/天意", "伊斯兰教": "真主前定"},
        "南亚": {"印度教": "因果业力", "佛教": "缘起法"},
        "不可通约点": "天命兼具内在性（可内化为性）和超越性，亚伯拉罕的神意完全外在，南亚的因果无意志",
    },
    "性": {
        "东亚": {"儒教": "天地之性人为贵", "道教": "自然素朴", "佛教": "佛性/无我"},
        "亚伯拉罕": {"犹太教": "按神形象", "基督教": "原罪+神形象", "伊斯兰教": "fitrah(天性)"},
        "南亚": {"印度教": "Atman(我)", "佛教": "无我/佛性"},
        "不可通约点": "儒家性是道德向善的可能性，基督教人性是堕落后的残余，佛教性是存在论基础（但'无我'否定性本身）",
    },
    "礼": {
        "东亚": {"儒教": "礼乐教化，祭祀制度", "道教": "自然无为反礼", "佛教": "戒律"},
        "亚伯拉罕": {"犹太教": "律法(托拉)", "基督教": "圣事/礼仪", "伊斯兰教": "沙里亚(教法)"},
        "南亚": {"印度教": "达摩(法)", "佛教": "戒律(vinaya)"},
        "不可通约点": "儒家礼是情感化规范（礼乐），亚伯拉罕律法是神命，佛教戒律是自觉——礼的本质是'人情+秩序'而非'服从'",
    },
    "德": {
        "东亚": {"儒教": "得于道者，内得于己", "道教": "上德不德", "佛教": "功德/波罗蜜"},
        "亚伯拉罕": {"犹太教": "义(tzedek)", "基督教": "恩典(grace)/美德", "伊斯兰教": "taqwa(敬畏)"},
        "南亚": {"印度教": "达摩/dharma", "佛教": "波罗蜜(paramita)"},
        "不可通约点": "儒家德是'得道'（道德自觉），基督教美德是'恩典'（外来赋予），核心分歧在于德是内生还是外予",
    },
}


# ========================================
# 数据类（v2.0.0 扩展）
# ========================================

@dataclass
class ComparisonResult:
    chapter_id: str
    source_text: str
    confucian: Dict[str, Any]
    western: Dict[str, Any]
    eastern_religion: Dict[str, Any] = None
    abrahamic_religion: Dict[str, Any] = None
    south_asian_religion: Dict[str, Any] = None
    similarities: List[str] = None
    differences: List[str] = None
    incommensurables: List[str] = None  # v2.0.0: 不可通约点
    cold_knowledge: str = ""
    timestamp: str = ""


# ========================================
# 文化比较器
# ========================================

class CulturalComparator:
    """文化比较器 v2.0.0 — 三层架构"""

    def __init__(self):
        self.zhuzi = ZHUZI_DB
        self.western = WESTERN_DB
        self.concepts = CONCEPT_MAP
        self.eastern_religion = EASTERN_RELIGION_DB
        self.abrahamic_religion = ABRAHAMIC_RELIGION_DB
        self.south_asian_religion = SOUTH_ASIAN_RELIGION_DB
        self.religion_concepts = RELIGION_CONCEPT_MAP

    def extract_concepts(self, text: str) -> List[str]:
        """提取文本中的核心概念"""
        found = []
        for concept in self.concepts:
            if concept in text:
                found.append(concept)
        if not found:
            for k in ["仁", "义", "礼", "智", "信", "忠", "孝"]:
                if k in text:
                    found.append(k)
        return found

    def analyze_confucian(self, text: str, chapter: str = "") -> Dict[str, Any]:
        """分析儒家内部分歧"""
        concepts = self.extract_concepts(text)
        results = {
            "intra_confucian": [],
            "zhuzi_vs_dao": [],
            "zhuzi_vs_mo": [],
            "zhuzi_vs_fa": []
        }

        for concept in concepts:
            if concept in self.concepts:
                mapping = self.concepts[concept]
                for philosopher, view in mapping.get("confucian", {}).items():
                    results["intra_confucian"].append({
                        "concept": concept,
                        "philosopher": philosopher,
                        "view": view
                    })

        daoists = ["老子", "庄子"]
        mo = ["墨子"]
        legalists = ["韩非子"]

        for p, data in self.zhuzi.items():
            if p in daoists:
                results["zhuzi_vs_dao"].append({
                    "philosopher": p,
                    "view": f"人性:{data['人性']}, 政治:{data['政治']}"
                })
            if p in mo:
                results["zhuzi_vs_mo"].append({
                    "philosopher": p,
                    "view": f"核心:{list(data['core'].keys())}, 政治:{data['政治']}"
                })
            if p in legalists:
                results["zhuzi_vs_fa"].append({
                    "philosopher": p,
                    "view": f"核心:{list(data['core'].keys())}, 政治:{data['政治']}"
                })

        return results

    def analyze_western(self, text: str, chapter: str = "") -> Dict[str, Any]:
        """分析中西概念对应"""
        concepts = self.extract_concepts(text)
        results = {
            "concept_mapping": [],
            "traditions": [],
            "method_diff": [],
            "values_diff": []
        }

        for concept in concepts:
            if concept in self.concepts:
                mapping = self.concepts[concept]
                for trad, equiv in mapping.get("western", {}).items():
                    results["concept_mapping"].append({
                        "chinese_concept": concept,
                        "western_tradition": trad,
                        "equivalent": equiv
                    })
                    if trad not in results["traditions"]:
                        results["traditions"].append(trad)

                results["method_diff"].append({
                    "concept": concept,
                    "similar": mapping.get("similar", ""),
                    "diff": mapping.get("diff", "")
                })

        results["traditions"] = list(set(results["traditions"]))
        return results

    def compare(self, text: str, chapter_id: str = "") -> ComparisonResult:
        """执行完整文化比较（三层架构）"""
        concepts = self.extract_concepts(text)
        confucian = self.analyze_confucian(text, chapter_id)
        western = self.analyze_western(text, chapter_id)

        similarities = []
        differences = []
        incommensurables = []

        for concept in concepts:
            if concept in self.concepts:
                mapping = self.concepts[concept]
                if mapping.get("similar"):
                    similarities.append(f"{concept}：{mapping['similar']}")
                if mapping.get("diff"):
                    differences.append(f"{concept}：{mapping['diff']}")

        # 第三层：宗教传统数据
        eastern_religion = None
        abrahamic_religion = None
        south_asian_religion = None

        for concept in concepts:
            if concept in self.religion_concepts:
                rmap = self.religion_concepts[concept]
                eastern_religion = rmap.get("东亚", None) if eastern_religion is None else eastern_religion
                abrahamic_religion = rmap.get("亚伯拉罕", None) if abrahamic_religion is None else abrahamic_religion
                south_asian_religion = rmap.get("南亚", None) if south_asian_religion is None else south_asian_religion
                inc = rmap.get("不可通约点", "")
                if inc and inc not in incommensurables:
                    incommensurables.append(inc)

        cold_knowledge = self._generate_cold_knowledge(text, concepts, confucian, western)

        return ComparisonResult(
            chapter_id=chapter_id,
            source_text=text,
            confucian=confucian,
            western=western,
            eastern_religion=eastern_religion,
            abrahamic_religion=abrahamic_religion,
            south_asian_religion=south_asian_religion,
            similarities=similarities,
            differences=differences,
            incommensurables=incommensurables if incommensurables else None,
            cold_knowledge=cold_knowledge,
            timestamp=datetime.now().isoformat()
        )

    def _generate_cold_knowledge(self, text: str, concepts: List[str],
                                 confucian: Dict, western: Dict) -> str:
        """生成冷知识命题"""
        if not concepts:
            return '【冷知识】儒家"仁"与斯多葛派"顺应自然"看似相近，实则前者是情感发用，后者是理性接纳，方向相反。'

        c = concepts[0]
        if c in self.concepts:
            diff = self.concepts[c].get("diff", "")
            if "情感" in diff and "理性" in diff:
                return f"【冷知识】{c}的中西理解：表面都强调利他，但儒家是情感推恩，西方是理性原则，本质不同。"

        return "【冷知识】诸子百家与西方哲学的最大差异不在于答案，而在于问题意识：儒家问如何成圣，西方问如何获得真理。"

    def generate_report(self, result: ComparisonResult) -> str:
        """生成文化比较报告（Markdown格式）"""
        lines = [
            f"# 文化比较分析报告",
            f"",
            f"**章节**: {result.chapter_id}",
            f"**生成时间**: {result.timestamp}",
            f"",
            f"---",
            f"",
            f"## 原始章句",
            f"",
            f"{result.source_text}",
            f"",
            f"---",
            f"",
            f"## 一、儒家内部分析",
            f"",
        ]

        if result.confucian.get("intra_confucian"):
            lines.append("### 1.1 孔孟荀观点差异")
            for item in result.confucian["intra_confucian"][:6]:
                lines.append(f"- **{item['philosopher']}** 论{item['concept']}：{item['view']}")

        if result.confucian.get("zhuzi_vs_dao"):
            lines.append("\n### 1.2 儒道分歧")
            for item in result.confucian["zhuzi_vs_dao"][:2]:
                lines.append(f"- {item['philosopher']}：{item['view']}")

        if result.confucian.get("zhuzi_vs_mo"):
            lines.append("\n### 1.3 儒墨分歧")
            for item in result.confucian["zhuzi_vs_mo"][:2]:
                lines.append(f"- {item['philosopher']}：{item['view']}")

        if result.confucian.get("zhuzi_vs_fa"):
            lines.append("\n### 1.4 儒法分歧")
            for item in result.confucian["zhuzi_vs_fa"][:2]:
                lines.append(f"- {item['philosopher']}：{item['view']}")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 二、中西哲学比较",
            f"",
        ])

        if result.western.get("concept_mapping"):
            lines.append("### 2.1 概念对应")
            for item in result.western["concept_mapping"][:6]:
                lines.append(
                    f"- **{item['chinese_concept']}** → **{item['western_tradition']}**：{item['equivalent']}"
                )

        if result.western.get("traditions"):
            lines.append(f"\n### 2.2 涉及西方传统")
            lines.append(f"{'、'.join(result.western['traditions'])}")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 四、宗教传统交叉审视",
            f"",
        ])

        # 4.1 东亚宗教
        if result.eastern_religion:
            lines.append("### 4.1 东亚宗教视角")
            for tradition, views in result.eastern_religion.items():
                if isinstance(views, dict):
                    key_points = [f"{k}：{v}" for k, v in list(views.items())[:3]]
                    lines.append(f"- **{tradition}**：{'；'.join(key_points)}")
            lines.append("")

        # 4.2 亚伯拉罕传统
        if result.abrahamic_religion:
            lines.append("### 4.2 亚伯拉罕传统视角")
            for tradition, views in result.abrahamic_religion.items():
                if isinstance(views, dict):
                    contrast = views.get("与儒对照", views.get("核心差异", ""))
                    if contrast:
                        lines.append(f"- **{tradition}**：{contrast}")
                    else:
                        key_points = [f"{k}：{v}" for k, v in list(views.items())[:2]]
                        lines.append(f"- **{tradition}**：{'；'.join(key_points)}")
            lines.append("")

        # 4.3 南亚传统
        if result.south_asian_religion:
            lines.append("### 4.3 南亚传统视角")
            for tradition, views in result.south_asian_religion.items():
                if isinstance(views, dict):
                    contrast = views.get("与儒对照", views.get("核心差异", ""))
                    if contrast:
                        lines.append(f"- **{tradition}**：{contrast}")
                    else:
                        key_points = [f"{k}：{v}" for k, v in list(views.items())[:2]]
                        lines.append(f"- **{tradition}**：{'；'.join(key_points)}")
            lines.append("")

        # 4.4 不可通约点
        if result.incommensurables:
            lines.append("### 4.4 不可通约点")
            for inc in result.incommensurables[:5]:
                lines.append(f"- {inc}")
            lines.append("")

        lines.extend([
            f"---",
            f"",
            f"## 五、异同总结",
            f"",
            f"### 5.1 相同点",
        ])
        for s in result.similarities[:5]:
            lines.append(f"- {s}")

        lines.extend([
            f"",
            f"### 5.2 根本差异",
        ])
        for d in result.differences[:5]:
            lines.append(f"- {d}")

        lines.extend([
            f"",
            f"---",
            f"",
            f"## 六、冷知识命题",
            f"",
            f"{result.cold_knowledge}",
            f"",
            f"---",
            f"",
            f"*本报告由 cultural-comparator v2.0.0 自动生成*",
        ])

        return "\n".join(lines)


# ========================================
# 入口函数（供外部调用）
# ========================================

def run_cultural_comparison(text: str, chapter_id: str = "") -> ComparisonResult:
    """执行文化比较分析"""
    comparator = CulturalComparator()
    return comparator.compare(text, chapter_id)


def generate_comparison_report(result: ComparisonResult) -> str:
    """生成文化比较报告"""
    comparator = CulturalComparator()
    return comparator.generate_report(result)


if __name__ == "__main__":
    # 测试
    test_text = "子曰：仁者爱人，克己复礼为仁。"
    result = run_cultural_comparison(test_text, "论语·颜渊12.1")
    report = generate_comparison_report(result)
    print(report)
