# Get document content


## Request

Replace URL with api/documents/1/kaz to get kazakh version of this document (if available).

```bash
curl 'https://zan.gov.kz/api/documents/1/rus?withHtml=false&page=1&r=1770904118631' \
  -H 'Accept: */*' \
  -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Connection: keep-alive' \
  -b '_ym_uid=1770901695846484687; _ym_d=1770901695; _ga=GA1.3.1603482758.1770901695; _gid=GA1.3.1658480949.1770901695; _ym_isad=2; _gat=1; _ga_MKJWXJLFKK=GS2.3.s1770904113$o2$g0$t1770904113$j60$l0$h0' \
  -H 'Referer: https://zan.gov.kz/client/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"'
```


## Response JSON

```json
{
    "id": "1",
    "code": "1",
    "ngr": "K950001000_",
    "version": {
        "id": "1_782057",
        "language": "rus",
        "versionDate": "2023-01-01",
        "metadata": {
            "title": {
                "kaz": "Қазақстан Республикасының Конституциясы",
                "rus": "Конституция Республики Казахстан"
            },
            "requisites": {
                "kaz": "Конституция 1995 жылы 30 тамызда республикалық референдумда қабылданды",
                "rus": "Конституция принята на республиканском референдуме 30 августа 1995 года"
            },
            "stateAgencyDocNumber": "0",
            "stateAgencyApprovalDate": "1995-08-30",
            "approvalPlace": "100055000000",
            "judicialAuthority": "",
            "developingStateAgency": "",
            "approvingStateAgencies": [
                "102000000000"
            ],
            "status": "new",
            "classified": "НЕТ",
            "registryNumber": "1",
            "publication": [],
            "legalValidity": "0100",
            "region": [
                "100000000000"
            ],
            "legislationAreas": [
                "001001000000"
            ],
            "actTypes": [
                "КОНС"
            ]
        },
        "references": [],
        "changes": [
            "157266||840085",
            "209737||1498411",
            "213528||1537802",
            "210059||1598045"
        ],
        "cause": {
            "document": "160390",
            "title": {
                "kaz": "Қазақстан Республикасының Конституциясына өзгерістер мен толықтырулар енгізу туралы",
                "rus": "О внесении изменений и дополнений в Конституцию Республики Казахстан"
            },
            "requisites": {
                "kaz": "Қазақстан Республикасының 2022 жылғы 8 маусымдағы Заңы (2022 жылғы 5 маусымда республикалық референдумда қабылданды (республикалық референдумның қорытындылары туралы ресми хабарлама «Егемен Қазақстан» газетінде 08.06.2022 ж., № 107 (30336), «Казахстанская правда» 08.06.2022 ж. № 107 (29734) жарияланды)",
                "rus": "Закон Республики Казахстан от 8 июня 2022 года (принят на республиканском референдуме 5 июня 2022 года (официальное сообщение об итогах республиканского референдума опубликовано в газете «Егемен Қазақстан» от 08.06.2022 г., № 107 (30336), «Казахстанская правда» от 08.06.2022 г., № 107 (29734)"
            },
            "code": "168832"
        },
        "signature": {
            "container": "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",
            "userComment": "",
            "properties": [
                {
                    "key": "NotBefore",
                    "value": "Mon May 12 20:17:06 ALMT 2025"
                },
                {
                    "key": "SigningTime",
                    "value": "Wed Oct 29 16:12:50 ALMT 2025"
                },
                {
                    "key": "Subject",
                    "value": "CN=ИМАНБЕКОВА ГУЛНУР,SURNAME=ИМАНБЕКОВА,SERIALNUMBER=IIN890503401409,C=KZ,O=Республиканское государственное предприятие на праве хозяйственного ведения \\\"Институт законодательства и правовой информации Республики Казахстан\\\" Министерства юстиции Республики Казахстан,OU=BIN990540004034,G=ЖОМАРТОВНА"
                },
                {
                    "key": "TSP",
                    "value": "n/a"
                },
                {
                    "key": "NotAfter",
                    "value": "Tue May 12 20:17:06 ALMT 2026"
                },
                {
                    "key": "OCSP presents and valid",
                    "value": "false"
                },
                {
                    "key": "Issuer",
                    "value": "CN=ҰЛТТЫҚ КУӘЛАНДЫРУШЫ ОРТАЛЫҚ (GOST) 2022,C=KZ"
                },
                {
                    "key": "SignatureComments",
                    "value": ""
                }
            ]
        }
    },
    "language": "rus",
    "metadata": {
        "title": {
            "kaz": "Қазақстан Республикасының Конституциясы",
            "rus": "Конституция Республики Казахстан"
        },
        "requisites": {
            "kaz": "Конституция 1995 жылы 30 тамызда республикалық референдумда қабылданды",
            "rus": "Конституция принята на республиканском референдуме 30 августа 1995 года"
        },
        "stateAgencyDocNumber": "0",
        "stateAgencyApprovalDate": "1995-08-30",
        "approvalPlace": "100055000000",
        "judicialAuthority": "",
        "developingStateAgency": "",
        "approvingStateAgencies": [
            "102000000000"
        ],
        "status": "new",
        "classified": "НЕТ",
        "registryNumber": "1",
        "publication": [],
        "legalValidity": "0100",
        "region": [
            "100000000000"
        ],
        "legislationAreas": [
            "001001000000"
        ],
        "actTypes": [
            "КОНС"
        ]
    },
    "actualVersion": true,
    "versionsCount": 9,
    "versionDate": "2023-01-01",
    "hasSignature": true,
    "imported": false,
    "content": [
        {
            "id": "645147994",
            "type": "doc",
            "level": 1,
            "properties": []
        },
        {
            "id": "645147995",
            "type": "title",
            "level": 2,
            "text": "Конституция Республики Казахстан",
            "properties": []
        },
        {
            "id": "645147996",
            "type": "sideNoteGroup",
            "level": 2,
            "properties": []
        },
        {
            "id": "645147997",
            "type": "sideNote",
            "level": 3,
            "properties": []
        },
        {
            "id": "645147998",
            "type": "text",
            "level": 4,
            "text": "Мы, народ Казахстана,",
            "properties": [
                {
                    "key": "linkId",
                    "value": "63"
                }
            ]
        },
        {
            "id": "645147999",
            "type": "text",
            "level": 4,
            "text": "объединенный общей исторической судьбой,",
            "properties": []
        },
        {
            "id": "645148000",
            "type": "text",
            "level": 4,
            "text": "созидая государственность на исконной",
            "properties": []
        },
        {
            "id": "645148001",
            "type": "text",
            "level": 4,
            "text": "казахской земле,",
            "properties": []
        },
        {
            "id": "645148002",
            "type": "text",
            "level": 4,
            "text": "сознавая себя миролюбивым гражданским",
            "properties": []
        },
        {
            "id": "645148003",
            "type": "text",
            "level": 4,
            "text": "обществом,",
            "properties": []
        },
        {
            "id": "645148004",
            "type": "text",
            "level": 4,
            "text": "приверженным идеалам свободы, равенства",
            "properties": []
        },
        {
            "id": "645148005",
            "type": "text",
            "level": 4,
            "text": "и согласия,",
            "properties": []
        },
        {
            "id": "645148006",
            "type": "text",
            "level": 4,
            "text": "желая занять достойное место в мировом",
            "properties": []
        },
        {
            "id": "645148007",
            "type": "text",
            "level": 4,
            "text": "сообществе,",
            "properties": []
        },
        {
            "id": "645148008",
            "type": "text",
            "level": 4,
            "text": "осознавая свою высокую ответственность перед",
            "properties": []
        },
        {
            "id": "645148009",
            "type": "text",
            "level": 4,
            "text": "нынешним и будущими поколениями,",
            "properties": []
        },
        {
            "id": "645148010",
            "type": "text",
            "level": 4,
            "text": "исходя из своего суверенного права,",
            "properties": []
        },
        {
            "id": "645148011",
            "type": "text",
            "level": 4,
            "text": "принимаем настоящую Конституцию.",
            "properties": []
        },
        {
            "id": "645148012",
            "type": "section",
            "level": 2,
            "index": "1",
            "properties": []
        },
        {
            "id": "645148013",
            "type": "heading",
            "level": 3,
            "text": "Раздел I.",
            "properties": []
        },
        {
            "id": "645148014",
            "type": "heading",
            "level": 3,
            "text": "Общие положения",
            "properties": []
        },
        {
            "id": "645148015",
            "type": "article",
            "level": 3,
            "index": "1",
            "properties": []
        },
        {
            "id": "645148016",
            "type": "heading",
            "level": 4,
            "text": "Статья 1",
            "properties": []
        },
        {
            "id": "645148017",
            "type": "point",
            "level": 4,
            "index": "1",
            "properties": []
        },
        {
            "id": "1282165651",
            "type": "text",
            "level": 5,
            "text": "Примечание. См. нормативные постановления Конституционного Суда РК  от 08.04.2023 № 8-НП; от 18.05.2023 № 14-НП;  от 11.07.2023 № 20-НП; от 06.12.2023 № 37-НП; от 10.01.2024 № 40-НП; от 27.12.2024 № 59-НП; от 18.07.2025 № 73-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативные постановления Конституционного Суда РК </i> <i>от 08.04.2023 № 8-НП;</i> <i>от 18.05.2023 № 14-НП; </i> <i>от 11.07.2023 № 20-НП</i>; <i>от 06.12.2023 № 37-НП; </i><i>от 10.01.2024 № 40-НП;</i> <i>от 27.12.2024 № 59-НП; от 18.07.2025 № 73-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165652",
            "type": "text",
            "level": 5,
            "text": "1. Республика Казахстан утверждает себя демократическим, светским, правовым и социальным государством, высшими ценностями которого являются человек, его жизнь, права и свободы.",
            "properties": []
        },
        {
            "id": "645148019",
            "type": "point",
            "level": 4,
            "index": "2",
            "properties": []
        },
        {
            "id": "645148020",
            "type": "text",
            "level": 5,
            "text": "2. Основополагающими принципами деятельности Республики являются: общественное согласие и политическая стабильность, экономическое развитие на благо всего народа, казахстанский патриотизм, решение наиболее важных вопросов государственной жизни демократическими методами, включая голосование на республиканском референдуме или в Парламенте.",
            "properties": []
        },
        {
            "id": "645148021",
            "type": "article",
            "level": 3,
            "index": "2",
            "properties": []
        },
        {
            "id": "645148022",
            "type": "heading",
            "level": 4,
            "text": "Статья 2",
            "properties": []
        },
        {
            "id": "645148023",
            "type": "point",
            "level": 4,
            "index": "1",
            "properties": []
        },
        {
            "id": "645148024",
            "type": "text",
            "level": 5,
            "text": "1. Республика Казахстан является унитарным государством с президентской формой правления.",
            "properties": []
        },
        {
            "id": "645148025",
            "type": "point",
            "level": 4,
            "index": "2",
            "properties": []
        },
        {
            "id": "645148026",
            "type": "text",
            "level": 5,
            "text": "2. Суверенитет Республики распространяется на всю ее территорию. Государство обеспечивает целостность, неприкосновенность и неотчуждаемость своей территории.",
            "properties": []
        },
        {
            "id": "970963453",
            "type": "point",
            "level": 4,
            "index": "3",
            "properties": []
        },
        {
            "id": "997671339",
            "type": "text",
            "level": 5,
            "text": "3. Административно-территориальное устройство Республики, статус ее столицы определяются законом. Столицей Казахстана является город Астана.",
            "properties": []
        },
        {
            "id": "645148029",
            "type": "point",
            "level": 4,
            "index": "3-1",
            "properties": []
        },
        {
            "id": "997671340",
            "type": "text",
            "level": 5,
            "text": "3-1. В пределах города Астаны может быть установлен особый правовой режим в финансовой сфере в соответствии с конституционным законом.",
            "properties": []
        },
        {
            "id": "645148031",
            "type": "point",
            "level": 4,
            "index": "4",
            "properties": []
        },
        {
            "id": "645148032",
            "type": "text",
            "level": 5,
            "text": "4. Наименования Республика Казахстан и Казахстан равнозначны.",
            "properties": []
        },
        {
            "id": "997671341",
            "type": "note",
            "level": 3,
            "text": "Сноска. Статья 2 с изменениями, внесенными законами РК от 21.05.2007 № 254-III (вводится в действие со дня его официального опубликования); от 10.03.2017 № 51-VI (вводится в действие со дня его первого официального опубликования); от 23.03.2019 № 238-VІ (вводится в действие со дня его первого официального опубликования); от 17.09.2022 № 142-VII (вводится в действие со дня его первого официального опубликования).",
            "properties": []
        },
        {
            "id": "645148034",
            "type": "article",
            "level": 3,
            "index": "3",
            "properties": []
        },
        {
            "id": "645148035",
            "type": "heading",
            "level": 4,
            "text": "Статья 3",
            "properties": []
        },
        {
            "id": "645148036",
            "type": "point",
            "level": 4,
            "index": "1",
            "properties": []
        },
        {
            "id": "645148037",
            "type": "text",
            "level": 5,
            "text": "1. Единственным источником государственной власти является народ.",
            "properties": []
        },
        {
            "id": "645148038",
            "type": "point",
            "level": 4,
            "index": "2",
            "properties": []
        },
        {
            "id": "645148039",
            "type": "text",
            "level": 5,
            "text": "2. Народ осуществляет власть непосредственно через республиканский референдум и свободные выборы, а также делегирует осуществление своей власти государственным органам.",
            "properties": []
        },
        {
            "id": "645148040",
            "type": "point",
            "level": 4,
            "index": "3",
            "properties": []
        },
        {
            "id": "645148041",
            "type": "text",
            "level": 5,
            "text": "3. Никто не может присваивать власть в Республике Казахстан. Присвоение власти преследуется по закону. Право выступать от имени народа и государства принадлежит Президенту, а также Парламенту Республики в пределах его конституционных полномочий. Правительство Республики и иные государственные органы выступают от имени государства в пределах делегированных им полномочий.",
            "properties": []
        },
        {
            "id": "645148042",
            "type": "point",
            "level": 4,
            "index": "4",
            "properties": []
        },
        {
            "id": "1282165653",
            "type": "text",
            "level": 5,
            "text": "Примечание. См. нормативные постановления Конституционного Суда РК \nот 16.11.2023 № 35-НП;  от 24.12.2024 № 58-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативные постановления Конституционного Суда РК </i>\n<i>от 16.11.2023 № 35-НП;</i>  <i>от 24.12.2024 № 58-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165654",
            "type": "text",
            "level": 5,
            "text": "4. Государственная власть в Республике едина, осуществляется на основе Конституции и законов в соответствии с принципом ее разделения на законодательную, исполнительную и судебную ветви и взаимодействия между собой с использованием системы сдержек и противовесов.",
            "properties": []
        },
        {
            "id": "645148044",
            "type": "article",
            "level": 3,
            "index": "4",
            "properties": []
        },
        {
            "id": "1282165655",
            "type": "text",
            "level": 4,
            "text": "Примечание. См. нормативное постановление Конституционного Суда РК от 22.05.2023 № 17-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативное постановление Конституционного Суда РК от 22.05.2023 № 17-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165656",
            "type": "heading",
            "level": 4,
            "text": "Статья 4",
            "properties": []
        },
        {
            "id": "645148046",
            "type": "point",
            "level": 4,
            "index": "1",
            "properties": []
        },
        {
            "id": "1282165657",
            "type": "text",
            "level": 5,
            "text": "Примечание. См. нормативные постановления Конституционного Суда РК от 11.07.2023 № 20-НП; от 29.05.2024 № 45-НП; от 26.02.2025 № 67-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативные постановления Конституционного Суда РК о</i><i>т 11.07.2023 № 20-НП; от 29.05.2024 № 45-НП; от 26.02.2025 № 67-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165658",
            "type": "text",
            "level": 5,
            "text": "1. Действующим правом в Республике Казахстан являются нормы Конституции, соответствующих ей законов, иных нормативных правовых актов, международных договорных и иных обязательств Республики, а также нормативных постановлений Конституционного Суда и Верховного Суда Республики.",
            "properties": []
        },
        {
            "id": "979613099",
            "type": "note",
            "level": 5,
            "text": "Примечание. В соответствии с Законом Республики Казахстан\nот 08.06.2022 г. нормативные постановления Конституционного Совета\nприменяются в части, не противоречащей Конституции, до их пересмотра\nКонституционным Судом.      ",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. В соответствии с Законом Республики Казахстан\nот 08.06.2022 г. нормативные постановления Конституционного Совета\nприменяются в части, не противоречащей Конституции, до их пересмотра\nКонституционным Судом.      </i>"
                }
            ]
        },
        {
            "id": "645148048",
            "type": "point",
            "level": 4,
            "index": "2",
            "properties": []
        },
        {
            "id": "1282165659",
            "type": "text",
            "level": 5,
            "text": "Примечание. См. нормативные постановления Конституционного Суда РК \nот 08.04.2023 № 7-НП;   от 21.04.2023 № 11-НП; от 27.02.2025 № 68-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативные постановления Конституционного Суда РК </i>\n<i>от 08.04.2023 № 7-НП; </i>  <i>от 21.04.2023 № 11-НП; от 27.02.2025 № 68-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165660",
            "type": "text",
            "level": 5,
            "text": "2. Конституция имеет высшую юридическую силу и прямое действие на всей территории Республики.",
            "properties": []
        },
        {
            "id": "645148050",
            "type": "point",
            "level": 4,
            "index": "3",
            "properties": []
        },
        {
            "id": "1282165661",
            "type": "text",
            "level": 5,
            "text": "Примечание. См. нормативные постановления Конституционного Суда РК от 20.01.2025 № 61-НП; от 26.02.2025 № 67-НП; от 18.07.2025 № 73-НП.",
            "properties": [
                {
                    "key": "html",
                    "value": "<i>Примечание. См. нормативные постановления Конституционного Суда РК </i><i>от 20.01.2025 № 61-НП; </i><i>от 26.02.2025 № 67-НП; от 18.07.2025 № 73-НП.</i>"
                }
            ]
        },
        {
            "id": "1282165662",
            "type": "text",
            "level": 5,
            "text": "3. Международные договоры, ратифицированные Республикой, имеют приоритет перед ее законами. Порядок и условия действия на территории Республики Казахстан международных договоров, участником которых является Казахстан, определяются законодательством Республики.",
            "properties": []
        },
        {
            "id": "645148052",
            "type": "point",
            "level": 4,
            "index": "4",
            "properties": []
        }, {...}
    ],
    "index": [
        {
            "title": "Раздел I.",
            "level": 2,
            "type": "section",
            "index": "1",
            "docIndex": 18
        },
        {
            "title": "Статья 1",
            "level": 3,
            "type": "article",
            "index": "1",
            "docIndex": 21
        },
        {
            "title": "Статья 2",
            "level": 3,
            "type": "article",
            "index": "2",
            "docIndex": 28
        },
        {
            "title": "Статья 3",
            "level": 3,
            "type": "article",
            "index": "3",
            "docIndex": 41
        }, {...}
    ],
    "pagesCount": 1
}
```

