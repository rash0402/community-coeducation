# GEMINI.md - Project Context

This file provides context for the AI assistant about the current project directory.

## Directory Overview

This directory contains the planning and definition documents for a project named **"Regional Co-education Program" (地域共育プログラム)**, managed by the Faculty of Engineering, Part II. The project aims to create a "bulletin board" style system to connect night-school students with local small and medium-sized enterprises (SMEs) for part-time work that is relevant to their studies.

The project is currently in the planning and documentation phase. The files are all Markdown documents detailing the project's rules, processes, and communication materials.

## Key Files

*   **`20251129_定義書_地域共育プログラム.md`**: This is the core project definition document. It outlines the mission, operational scheme, rules, risk management (triage system), and stakeholder benefits. The core concept is to minimize university intervention and empower students and companies to connect directly, with the university providing a framework of trust and quality assurance (via student certification).

*   **`20251129_LPサイト要件定義.md`**: This document specifies the requirements for two separate landing pages (one for companies, one for students) to promote the platform. It defines the target audience, key messages (CTAs), and content structure for each page.

*   **Other Files**: The directory also contains various other documents supporting the project, such as:
    *   Trouble report forms (`トラブル報告フォーム.md`)
    *   Triage rules (`トリアージ規定.md`)
    *   Student training materials (`学生向け認定研修資料.md`)
    *   Corporate terms of service (`企業向け規約（案）.md`)
    *   Job registration form design (`求人登録フォーム設計書.md`)
    *   Operations manuals (`業務マニュアル.md`)

## Usage

This directory serves as the central repository for the project's foundational documents. The contents are used for planning, internal alignment, and creating the actual assets for the platform (like the landing pages and forms). It is a non-code project focused on project management and documentation.

## Metadata Specification

All documents MUST include the following YAML frontmatter:

```yaml
---
title: Document Title
category: 00_全体・要件定義 | 10_内部規定・マニュアル | 30_学生向け資料 | 40_企業向け資料
doc_type: 定義書 | 設計書 | 規約 | マニュアル | 研修資料 | 雛形 | 案内
audience:
  - 学生
  - 企業
  - 事務局
version: "1.0"
status: 🔴Draft | 🟡Review | 🟢Release
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: 工学部第二部長
review_cycle: 年1回 | 学期毎 | 随時
---
```

### Field Descriptions
| Field | Required | Description |
|-------|----------|-------------|
| `title` | ✅ | Document title |
| `category` | ✅ | Category corresponding to file prefix |
| `doc_type` | ✅ | Document type |
| `audience` | ✅ | Target readers (multiple allowed) |
| `version` | ✅ | Semantic version (as string) |
| `status` | ✅ | Approval status |
| `created` | ✅ | Creation date |
| `updated` | ✅ | Last update date (MUST update on edit) |
| `owner` | ✅ | Approval authority (always "工学部第二部長") |
| `review_cycle` | ✅ | Review frequency |

## IMPORTANT: Public Repository Rules

This repository is **publicly available on GitHub**. The following information **MUST NOT be included**:

1. **Personal Information**: Real names, email addresses, phone numbers, addresses
2. **Specific Company Names**: Any real company/organization names other than "Tokyo Denki University Faculty of Engineering Part II"
3. **Confidential Information**: Internal contacts, non-public operational details

### Acceptable Alternatives
- Placeholders: `〇〇株式会社`, `example@dendai.ac.jp`, `03-XXXX-XXXX`
- Anonymized personas: `Student A`, `Manager B`, `Staff C`, etc.
- Title-only references: `工学部第二部長` (without personal name)
