# Vibe 코딩 환경 ToDo 리스트

## 문서 정보

- **문서번호**: d0004
- **작성일**: 2026-01-06
- **기반 문서**: d0001_prd.md
- **목적**: 일상 할 일 관리 및 디버깅 추적

## 문서이력관리

| 버전 | 날짜 | 변경내용 |
|------|------|----------|
| v02 | 2026-01-06 | oaisaddtodo → oaistodo 스킬명 변경 반영 |
| v01 | 2026-01-06 | 초기 작성 |

---

## 디버깅 (Debug)

> **디버깅 가이드**: v/guide/common_guide.md 섹션 2.8 참조

### 현재 이슈 (Active Issues)

| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
|----|--------|------|------|---------|------|
| A019 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A020 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A021 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A022 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A024 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A026 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A027 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-15 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A030 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A036 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A037 | 2026-01-15 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A038 | 2026-01-15 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A039 | 2026-01-15 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A040 | 2026-01-15 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A041 | 2026-01-15 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A042 | 2026-01-15 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A043 | 2026-01-15 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-15 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A045 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A046 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A048 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A049 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A050 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A051 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A054 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A056 | 2026-01-15 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A057 | 2026-01-15 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A058 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A060 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A061 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A063 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A064 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A065 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A067 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A068 | 2026-01-15 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A069 | 2026-01-15 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A070 | 2026-01-15 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-15 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-15 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A073 | 2026-01-15 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A074 | 2026-01-15 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A075 | 2026-01-15 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-15 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A077 | 2026-01-15 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A078 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A079 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A081 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A083 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A084 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A085 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A086 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A087 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A088 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A090 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A091 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A092 | 2026-01-15 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A020 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A021 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A022 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A024 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A026 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A027 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-13 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A030 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A036 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A037 | 2026-01-13 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A038 | 2026-01-13 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A039 | 2026-01-13 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A040 | 2026-01-13 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A041 | 2026-01-13 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A042 | 2026-01-13 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A043 | 2026-01-13 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-13 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A045 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A046 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A048 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A049 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A050 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A051 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A054 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A056 | 2026-01-13 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A057 | 2026-01-13 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A058 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A060 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A061 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A063 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A064 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A065 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A067 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A068 | 2026-01-13 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A069 | 2026-01-13 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A070 | 2026-01-13 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-13 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-13 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A073 | 2026-01-13 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A074 | 2026-01-13 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A075 | 2026-01-13 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-13 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A077 | 2026-01-13 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A078 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A079 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A081 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A083 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A084 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A085 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A086 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A087 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A088 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A090 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A091 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A092 | 2026-01-13 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 || A019 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:60 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A020 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:77 - "object" has no attribute "append"  [att... | 높음 | 대기 |
| A021 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:83 - "object" has no attribute "extend"  [att... | 높음 | 대기 |
| A022 | 2026-01-07 | BUGFIX | [TYPE] oais\book_summary.py:256 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A023 | 2026-01-07 | BUGFIX | [TYPE] oais\task_core.py:17 - Incompatible default for argument "defau... | 높음 | 대기 |
| A024 | 2026-01-07 | BUGFIX | [TYPE] oais\task_attachment.py:27 - No overload variant of "join" matches ar... | 높음 | 대기 |
| A025 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:284 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A026 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:288 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A027 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:294 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A028 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 0 has incompatible type "int";... | 높음 | 대기 |
| A029 | 2026-01-07 | BUGFIX | [TYPE] oais\community.py:497 - List item 1 has incompatible type "int";... | 높음 | 대기 |
| A030 | 2026-01-07 | BUGFIX | [TYPE] oais\columns.py:199 - Need type annotation for "result" (hint:... | 높음 | 대기 |
| A031 | 2026-01-07 | BUGFIX | [TYPE] oais\date_utils.py:44 - Module has no attribute "KR"  [attr-defi... | 높음 | 대기 |
| A032 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:55 - Need type annotation for "transactions" ... | 높음 | 대기 |
| A033 | 2026-01-07 | BUGFIX | [TYPE] oais\financial.py:153 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A034 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:36 - Argument 1 to "PdfReader" has incompatib... | 높음 | 대기 |
| A035 | 2026-01-07 | BUGFIX | [TYPE] oais\pdf_parser.py:68 - "object" has no attribute "read"  [attr-... | 높음 | 대기 |
| A036 | 2026-01-07 | BUGFIX | [TYPE] oais\file_upload.py:208 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A037 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Cannot assign to a type  [misc] | 높음 | 대기 |
| A038 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:55 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A039 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:135 - Unpacking a string is disallowed  [misc] | 높음 | 대기 |
| A040 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:165 - Argument 2 to "insert_page_by_file" has ... | 높음 | 대기 |
| A041 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:176 - Argument 2 to "work_img_gen_by_file" has... | 높음 | 대기 |
| A042 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:185 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A043 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:200 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A044 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:201 - Value of type "int" is not indexable  [i... | 높음 | 대기 |
| A045 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:240 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A046 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:258 - Argument 2 to "join" has incompatible ty... | 높음 | 대기 |
| A047 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:357 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A048 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:379 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A049 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:776 - Incompatible return value type (got "str... | 높음 | 대기 |
| A050 | 2026-01-07 | BUGFIX | [TYPE] oais\file_ops.py:812 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A051 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:59 - Incompatible return value type (got "str... | 높음 | 대기 |
| A052 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:193 - Incompatible return value type (got "str... | 높음 | 대기 |
| A053 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:562 - Incompatible return value type (got "str... | 높음 | 대기 |
| A054 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:598 - Incompatible return value type (got "str... | 높음 | 대기 |
| A055 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:629 - Incompatible return value type (got "str... | 높음 | 대기 |
| A056 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:708 - Incompatible return value type (got "str... | 높음 | 대기 |
| A057 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg_data.py:748 - Incompatible return value type (got "str... | 높음 | 대기 |
| A058 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:158 - Missing return statement  [return] | 높음 | 대기 |
| A059 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:202 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A060 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:733 - Incompatible default for argument "error... | 높음 | 대기 |
| A061 | 2026-01-07 | BUGFIX | [TYPE] oais\ui.py:808 - "None" object is not iterable  [misc] | 높음 | 대기 |
| A062 | 2026-01-07 | BUGFIX | [TYPE] oais\session.py:222 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A063 | 2026-01-07 | BUGFIX | [TYPE] oais\data_processing.py:122 - Need type annotation for "compare_normal... | 높음 | 대기 |
| A064 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:194 - Incompatible return value type (got "str... | 높음 | 대기 |
| A065 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:242 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A066 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:386 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A067 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:490 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A068 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1063 - Argument 1 to "get_all_info" has incompa... | 높음 | 대기 |
| A069 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1130 - Argument 5 to "join" has incompatible ty... | 높음 | 대기 |
| A070 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1406 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A071 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1462 - Incompatible return value type (got "str... | 높음 | 대기 |
| A072 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1786 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A073 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:1789 - Incompatible return value type (got "str... | 높음 | 대기 |
| A074 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2185 - "str" has no attribute "save"  [attr-def... | 높음 | 대기 |
| A075 | 2026-01-07 | BUGFIX | [TYPE] oais\bizreg.py:2245 - Incompatible return value type (got "tup... | 높음 | 대기 |
| A076 | 2026-01-07 | BUGFIX | [TYPE] oais\application.py:431 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A077 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 0 has incompatible type "str";... | 높음 | 대기 |
| A078 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 1 has incompatible type "str";... | 높음 | 대기 |
| A079 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:261 - List item 2 has incompatible type "str";... | 높음 | 대기 |
| A080 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:265 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A081 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:273 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A082 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:277 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A083 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:520 - Incompatible default for argument "check... | 높음 | 대기 |
| A084 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:704 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A085 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:744 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A086 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:747 - Unsupported operand types for + ("None" ... | 높음 | 대기 |
| A087 | 2026-01-07 | BUGFIX | [TYPE] oais\customer.py:754 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A088 | 2026-01-07 | BUGFIX | [TYPE] oais\company.py:841 - Need type annotation for "params" (hint:... | 높음 | 대기 |
| A089 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:521 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A090 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:527 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A091 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:765 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A092 | 2026-01-07 | BUGFIX | [TYPE] oais\sys_code.py:768 - Argument 1 to "append" of "list" has inc... | 높음 | 대기 |
| A093 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A094 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:285 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A095 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:288 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A096 | 2026-01-07 | BUGFIX | [TYPE] oais\services.py:296 - Value of type "Any | None" is not indexa... | 높음 | 대기 |
| A097 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:39 - Library stubs not installed for "request... | 높음 | 대기 |
| A098 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:108 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A099 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:136 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A100 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:148 - Need type annotation for "text_lst" (hin... | 높음 | 대기 |
| A101 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:224 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A102 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:248 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A103 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:340 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A104 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:344 - Unsupported target for indexed assignmen... | 높음 | 대기 |
| A105 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:348 - "str" has no attribute "pop"  [attr-defi... | 높음 | 대기 |
| A106 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:541 - Incompatible return value type (got "str... | 높음 | 대기 |
| A107 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:557 - Need type annotation for "naver_ocr_lst"... | 높음 | 대기 |
| A108 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:672 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A109 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:688 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A110 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:695 - Incompatible types in assignment (expres... | 높음 | 대기 |
| A111 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:760 - Incompatible return value type (got "str... | 높음 | 대기 |
| A112 | 2026-01-07 | BUGFIX | [TYPE] oais\ocr.py:825 - No return value expected  [return-value] | 높음 | 대기 |
| A113 | 2026-01-07 | BUGFIX | [TYPE] oais\hyphen_api.py:8 - Library stubs not installed for "request... | 높음 | 대기 |
| A114 | 2026-01-07 | BUGFIX | [TEST] tests/ - pytest 테스트 실패 | 높음 | 대기 |
#### 우선순위 분류

| 분류 | 설명 | 대응 시간 |
|------|------|----------|
| [CRITICAL] | 시스템 장애, 보안 취약점, 데이터 손실 | 즉시 |
| [ERROR] | 기능 오작동, 예외 미처리 | 24시간 내 |
| [WARNING] | 잠재적 문제, 성능 이슈 | 1주일 내 |
| [INFO] | 코드 스타일, 개선 권장 | 백로그 |

### 해결된 이슈 (Resolved Issues)

> 1~2주 모니터링 후 oaishistory run → d0010_history.md 아카이브

| ID | 발생일 | 분류 | 내용 | 해결일 | 해결방법 |
|----|--------|------|------|--------|---------|
| A018 | 2026-01-07 | BUGFIX | [LINT] oais\task_attachment.py:72 - [E0401] Unable... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A017 | 2026-01-07 | BUGFIX | [LINT] oais\task_attachment.py:24 - [E0401] Unable... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A016 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:543 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A015 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:235 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A014 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:223 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A013 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:220 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A012 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:220 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A011 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:219 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A010 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:219 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A009 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:216 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A008 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:216 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A007 | 2026-01-07 | BUGFIX | [LINT] oais\seal.py:148 - [E1101] Module 'cv2' has... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A006 | 2026-01-07 | BUGFIX | [LINT] oais\pdf_parser.py:17 - [E0401] Unable to i... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A005 | 2026-01-07 | BUGFIX | [LINT] oais\pdf_parser.py:16 - [E0401] Unable to i... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A004 | 2026-01-07 | BUGFIX | [LINT] oais\ocr.py:223 - [E1101] Module 'cv2' has ... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A003 | 2026-01-07 | BUGFIX | [LINT] oais\ocr.py:223 - [E1101] Module 'cv2' has ... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A002 | 2026-01-07 | BUGFIX | [LINT] oais\ocr.py:220 - [E1101] Module 'cv2' has ... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| A001 | 2026-01-07 | BUGFIX | [LINT] oais\date_utils.py:44 - [E1101] Module 'hol... | 2026-01-15 | False Positive - 동적 로딩/선택적 의존성 모듈 |
| - | - | - | (해결된 이슈 없음) | - | - |

---

## 할 일 (Todo)

### 진행 중

| ID | 등록일 | 내용 | 담당 | 상태 |
|----|--------|------|------|------|
| - | - | (진행 중인 작업 없음) | - | - |

### 대기 중

| ID | 등록일 | 내용 | 우선순위 | 비고 |
|----|--------|------|---------|------|
| - | - | (대기 중인 작업 없음) | - | - |

### 완료

| ID | 등록일 | 내용 | 완료일 | 비고 |
|----|--------|------|--------|------|
| T006 | 2026-01-07 | oaissync view 0013 | 2026-01-07 | 4개 차이 발견 |
| T005 | 2026-01-06 | oaissync diff 기능 다른 프로젝트 동기화 | 2026-01-06 | 5개 프로젝트 완료 |
| T004 | 2026-01-06 | oaistodo 스킬로 전환 | 2026-01-06 | v/oaistodo.md |
| T001 | 2026-01-06 | oaissync 스킬 생성 | 2026-01-06 | v/oaissync.md |
| T002 | 2026-01-06 | oaiscommand 명령어 표기법 통일 | 2026-01-06 | 스킬명 접두사 |
| T003 | 2026-01-06 | oaiscommand 스킬 문서 생성 | 2026-01-06 | v/oaiscommand.md |

---

## 참고 문서

- 공통 가이드: `v/guide/common_guide.md`
- 명령어 목록: `doc/d0007_command.md`
- 변경 이력: `doc/d0010_history.md`
