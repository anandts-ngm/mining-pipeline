Доорхыг **03\. Phase 3 — Geological, Metallogenic and CMCS Synthesis** хэсэгт “илүү тодруулсан аргачлал” болгон шууд нэмж/орлуулж болно. Одоо байгаа баримтад Phase 3 нь №1-8, №53-72 input-ийг голчлон ашиглаж, 03A дэд workflow нь №47-78 болон №9-46 support output-уудыг deposit model-д туслах evidence болгон татах логиктой байна.

**03\. Phase 3 — Geological, Metallogenic and CMCS Synthesis: Дэлгэрүүлсэн аргачлал**

**03.1 Зорилго**

Phase 3-ийн зорилго нь Бүдүүн хад / XV-023222 / L23222 талбайн **геологийн суурь, структур, интрузив/contact, ашигт малтмалын илрэл, эрдэсжсэн цэг, хэтийн төлөвтэй хэсэг, металлогений бүс, CMCS/MRPAM орд-илрэлийн context**\-ийг нэг Master GIS орчинд нэгтгэж, дараагийн Phase 4 prospect ranking болон Phase 10 final target ranking-д ашиглах **geological evidence base** үүсгэх явдал юм.

Энэ шат нь **орд батлах шат биш**. Phase 3-аас гарах бүх output нь “historical/contextual/preliminary support evidence” бөгөөд хээрийн шалгалт, дээжлэлт, лабораторийн шинжилгээ, structural validation хийгдэх хүртэл decision-grade evidence гэж үзэхгүй.

**03.2 Ашиглах үндсэн input**

Phase 3-д дараах raw input-уудыг шууд ашиглана:

| Input № | Агуулга | Phase 3-д ашиглах зорилго |
| :---- | :---- | :---- |
| №1-7 | Tectonic / terrane context зураг, тайлбар | Lake island arc terrane, Ulaanshand Zone, Nuur Accretionary Megazone context тодорхойлох |
| №8 | License boundary KMZ | Overlay, clipping, buffer, CMCS/MRPAM search boundary |
| №53-56 | 1:200k болон 1:50k geological map \+ legend | Геологийн нэгж, lithology, contact, fault, intrusive, vein, alteration digitize хийх |
| №57-58 | Mineral resources map \+ legend | Региональ илрэл, anomaly, ore field context digitize хийх |
| №59-61 | Mineral distribution / metallogenic scheme | Ore district, ore node, metallogenic trend, ore formation context |
| №62-65 | Prospectivity assessment, source materials map \+ legend | Б-3 Толь хяр, Г-1 зэрэг prospectivity zone, route, observation, sample, trench/pit/source material digitize хийх |
| №66-68 | Gold occurrence description, mineralized point register/table | Илрэл, эрдэсжсэн цэгийн координат, агуулга, commodity, lithology, structure-г occurrence database болгох |
| №69-72 | Regional metallogenic map/report | 1:500k metallogenic belt, ore formation, commodity association, regional context |

Phase 3-ийн 03A deposit model дэд workflow-д Phase 2-оос гарсан Sentinel/ASTER/KOMPSAT/DEM derivative output-уудыг зөвхөн **support evidence** байдлаар ашиглана. Remote sensing, DEM, KOMPSAT, ASTER output нь хүдэржилтийн баталгаа биш.

---

**03.3 Ажиллах folder structure**

03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis/

├── 01\_Input\_Working\_Copy

├── 02\_Tectonic\_Terrane\_Context

├── 03\_Regional\_Metallogenic\_1M500K

├── 04\_Regional\_Geology\_Mineral\_1M200K

├── 05\_Local\_Geology\_Occurrence\_1M50K

├── 06\_Source\_Materials\_and\_Prospectivity

├── 07\_Occurrence\_Register\_and\_Coordinate\_QAQC

├── 08\_CMCS\_MRPAM\_Buffer\_Check\_5km\_10km\_20km

├── 09\_Geological\_Evidence\_Layers\_GPKG

├── 10\_Preliminary\_Deposit\_Model\_03A

├── 11\_Evidence\_Scoring\_and\_DataGap

└── 12\_Phase3\_QAQC\_and\_Handover

---

**03.4 Алхамчилсан аргачлал**

**Алхам 1 — Phase 1/2 output-уудыг шалгаж авах**

Phase 3 эхлэхээс өмнө дараах зүйлс бэлэн эсэхийг шалгана:

| Шалгах зүйл | Шаардлага |
| :---- | :---- |
| Master QGIS project | EPSG:32647 CRS-тэй, missing layer байхгүй |
| License boundary | №8-аас үүссэн EPSG:32647 GeoPackage layer |
| Georeference QA/QC log | Scan map бүрийн GCP, residual, scale, confidence бүртгэгдсэн |
| Phase 2 remote sensing output | Sentinel/ASTER/KOMPSAT/DEM support layer-үүд EPSG:32647-д бэлэн |
| Data confidence ranking | High / Medium / Low / Needs verification үнэлгээтэй |

Phase 1-д scan map бүрийн georeference residual, GCP count, map scale, reviewer/date/decision-г бүртгэх ёстой гэж баримтад заасан тул Phase 3 нь энэ QA/QC бүртгэл дээр тулгуурлана.

**Алхам 2 — Tectonic / terrane context нэгтгэх**

№1-7 input-ийг тус бүрээр шалгаж, дараах register үүсгэнэ:

**Output:**  
XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register\_v01.xlsx

Register-ийн баганууд:

| Field | Тайлбар |
| :---- | :---- |
| source\_raw\_input\_no | №1-7 |
| source\_raw\_filename | Exact filename |
| terrane\_zone\_name | Lake Terrane / Ulaanshand Zone / Nuur Accretionary Megazone гэх мэт |
| evidence\_type | map / explanatory text / regional tectonic interpretation |
| relevance\_to\_project | project boundary-тэй ямар context-ээр холбогдох |
| source\_scale | мэдэгдэж байвал |
| confidence | High / Medium / Low / Needs verification |
| limitation | scanned, non-native, georeference unknown гэх мэт |
| use\_in\_deposit\_model | ямар candidate model-д context болох |

Энэ шатанд terrane map-уудыг **local ore target boundary** мэт ашиглахгүй. Зөвхөн regional geological setting, tectonic affinity, deposit model screening context болгон ашиглана.

**Алхам 3 — 1:500,000 regional metallogenic context боловсруулах**

№69-72 input-ийг ашиглана.

Хийх ажил:

1. №69 legend scan-аас ore formation, commodity, symbol dictionary гаргана.

2. №70 metallogenic map-ийг georeference хийж, license boundary \+ 20 km buffer-тэй overlay хийнэ.

3. №71-72 report PDF-ээс project area-тэй холбоотой metallogenic belt, ore formation, commodity association, regional occurrence мэдээллийг evidence register-д оруулна.

4. 1:500k scale-ийн хязгаарлалтыг заавал тэмдэглэнэ.

**Output:**

XV023222\_Buduunkhad\_L47B\_RegionalMetallogenic\_Legend\_Dictionary\_v01.xlsx

XV023222\_Buduunkhad\_2020\_L47B\_Talshand\_RegionalMetallogenicMap\_1-500K\_Georeferenced\_EPSG32647\_v01.tif

metallogenic\_zones\_polygons\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_RegionalMetallogenic\_Context\_Map\_v01.pdf

XV023222\_Buduunkhad\_RegionalMetallogenic\_Evidence\_Register\_v01.xlsx

**Алхам 4 — 1:200,000 regional geology/mineral resources боловсруулах**

№53-54 болон №57-58 input-ийг ашиглана.

Хийх ажил:

1. №53 geological map-ийг georeference хийнэ.

2. №54 legend scan-аас lithology, age, intrusive, fault, contact, symbol dictionary гаргана.

3. Геологийн нэгжүүдийг polygon layer болгон digitize хийнэ.

4. Fault, structure, intrusive contact-уудыг line layer болгон digitize хийнэ.

5. №57 mineral resources map-ийг georeference хийж, ore field, occurrence, anomaly, mineralized zone-уудыг point/polygon layer болгоно.

6. №58 legend-аас commodity болон occurrence type lookup table үүсгэнэ.

**Output:**

XV023222\_Buduunkhad\_1987\_L47-XIX\_GeologicalMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif

geology\_units\_200k\_polygons\_EPSG32647\_v01.gpkg

structures\_faults\_200k\_lines\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_1987\_L47-XIX\_MineralResourcesMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif

regional\_mineral\_occurrences\_points\_EPSG32647\_v01.gpkg

regional\_mineralized\_zones\_polygons\_EPSG32647\_v01.gpkg

**Алхам 5 — 1:50,000 local geology, occurrence, prospectivity боловсруулах**

№55-68 input нь Phase 3-ийн хамгийн чухал local-scale evidence болно.

Хийх ажил:

| Input | Хийх ажил |
| :---- | :---- |
| №55 | 1:50k geology map georeference, lithology/contact/fault/vein/alteration digitize |
| №56 | Legend dictionary: stratigraphy, lithology, intrusive, alteration, vein type |
| №60 | Au-Cu, Cu, Mo, As, Zn occurrence points digitize |
| №63 | Б-3 Толь хяр, Г-1 зэрэг prospectivity polygons digitize |
| №64 | Route, observation, sample, trench/pit, section line digitize |
| №65 | Source material symbol/domain dictionary |
| №66 | Gold occurrence description-аас coordinate, grade, lithology, structure extract |
| №67 | Mineral occurrence/mineralized point PDF register extract |
| №68 | XLSX mineralized point table clean, coordinate validation, GIS point layer үүсгэх |

**Output:**

XV023222\_Buduunkhad\_2013\_L47-74-A\_GeologicalMap\_1-50K\_Georeferenced\_EPSG32647\_v01.tif

geology\_units\_50k\_polygons\_EPSG32647\_v01.gpkg

structures\_faults\_50k\_lines\_EPSG32647\_v01.gpkg

intrusive\_contacts\_lines\_EPSG32647\_v01.gpkg

dyke\_vein\_lines\_EPSG32647\_v01.gpkg

mineral\_occurrences\_points\_EPSG32647\_v01.gpkg

prospectivity\_target\_zones\_polygons\_EPSG32647\_v01.gpkg

source\_material\_observation\_points\_EPSG32647\_v01.gpkg

source\_material\_route\_lines\_EPSG32647\_v01.gpkg

source\_material\_trench\_pit\_points\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_Mineral\_Occurrences\_Register\_v01.xlsx

**Алхам 6 — Coordinate болон attribute QA/QC хийх**

№66, №67, №68-аас гарсан occurrence/mineralized point data-г хооронд нь тулгана.

Шалгах зүйл:

| QA/QC item | Тайлбар |
| :---- | :---- |
| Coordinate format | WGS84 lat/long, UTM, local grid эсэх |
| CRS conversion | EPSG:4326 → EPSG:32647 зөв хөрвүүлсэн эсэх |
| Duplicate point | Ижил нэр, ижил координат, ойролцоо давхцал |
| Commodity consistency | Au, Cu, Mo, As, Zn, Pb, W, Sn, Bi гэх мэт нэг мөр кодчилох |
| Map-register match | №60 map дээрх occurrence №68 table-тэй таарч байгаа эсэх |
| Confidence flag | map-derived / table-derived / text-derived / uncertain |
| Validation status | Historical only гэж тэмдэглэх |

**Output:**

XV023222\_Buduunkhad\_Occurrence\_CrossReference\_7255\_4186\_v01.xlsx

XV023222\_Buduunkhad\_Occurrence\_Coordinate\_QAQC\_Log\_v01.xlsx

XV023222\_Buduunkhad\_Validated\_Historical\_Occurrence\_Points\_EPSG32647\_v01.gpkg

**Алхам 7 — CMCS/MRPAM 5 km, 10 km, 20 km buffer check хийх**

№8 license boundary-аас 5 km, 10 km, 20 km buffer үүсгээд CMCS/MRPAM nearest deposit/occurrence мэдээллийг тусад нь register болгоно. Одоо байгаа баримтад CMCS evidence нь зөвхөн contextual support бөгөөд тухайн license дотор хүдэржилт байгааг батлахгүй гэж тэмдэглэх шаардлагатай.

**Хийх ажил:**

1. License boundary-аас 5 km, 10 km, 20 km buffer polygon үүсгэнэ.

2. CMCS/MRPAM-ээс deposit, occurrence, mineralized point, commodity, deposit type, distance, direction мэдээлэл авна.

3. Buffer доторх болон ойролцоох илрэлүүдийг distance/rank-аар ангилна.

4. “Context only — not proof of mineralization inside license” гэсэн limitation талбар оруулна.

**Output:**

XV023222\_Buduunkhad\_CMCS\_MRPAM\_Buffer\_5km\_10km\_20km\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_CMCS\_Nearest\_Deposit\_Register\_v01.xlsx

XV023222\_Buduunkhad\_CMCS\_Context\_Map\_v01.pdf

**Алхам 8 — Geological evidence layer-үүдийг нэг Master GPKG-д нэгтгэх**

Phase 3-ийн бүх vector output-ийг нэг GeoPackage-д нэгтгэнэ.

**Output file:**

XV023222\_Buduunkhad\_Geological\_Evidence\_Layers\_v01.gpkg

GeoPackage дотор байх layer-үүд:

license\_boundary

buffer\_5km\_10km\_20km

tectonic\_terrane\_context\_polygon

metallogenic\_zones\_polygon

ore\_district\_node\_context\_polygon

geology\_units\_200k\_polygon

geology\_units\_50k\_polygon

faults\_structures\_line

intrusive\_contacts\_line

dyke\_vein\_line

mineral\_occurrences\_point

mineralized\_points\_point

prospectivity\_target\_zones\_polygon

source\_material\_observation\_point

source\_material\_route\_line

source\_material\_trench\_pit\_point

cmcs\_nearest\_occurrences\_point

Layer бүрт дараах mandatory field байна:

| Field | Тайлбар |
| :---- | :---- |
| source\_raw\_input\_no | 1-78 дугаар |
| source\_raw\_filename | exact raw filename |
| source\_group | evidence group |
| processing\_phase | 03 эсвэл 03A |
| source\_scale | 1:50k / 1:200k / 1:500k |
| geometry\_type | point / line / polygon |
| evidence\_type | geology / structure / occurrence / metallogenic / prospectivity |
| validation\_status | Historical only / Field checked / Sampled / Lab confirmed |
| confidence | High / Medium / Low / Needs verification |
| limitation | scale, scan, georef, coordinate uncertainty |
| processing\_version | v01, v02 гэх мэт |
| reviewer | шалгасан хүн |
| review\_date | огноо |

**Алхам 9 — 03A Preliminary Deposit Model Preparation хийх**

03A нь Phase 3-ийн заавал хийх дэд workflow байна. Энэ шатанд Au-Cu hydrothermal vein, intrusion-related Cu-Au-Mo, skarn/contact metasomatic, polymetallic vein, VMS possibility, heavy mineral/placer indicator гэсэн candidate model бүрийг тусад нь үнэлнэ. Одоо байгаа баримтад эдгээр candidate model-ийг supporting evidence, missing evidence, validation work хүснэгтээр үнэлэхээр заасан байна.

**Deposit model evidence table:**

| Deposit model | Supporting evidence | Missing evidence | Validation work | Preliminary confidence |
| :---- | :---- | :---- | :---- | :---- |
| Au-Cu hydrothermal vein | quartz vein, Au-Cu occurrence, fault/shear, As-Bi support | vein continuity, width, lab Au grade | recon mapping, rock chip/channel, Au fire assay | High / Moderate / Low |
| Intrusion-related Cu-Au-Mo | intrusive contact, Cu-Mo-Bi-As, stockwork/alteration support | alteration zoning, sulphide confirmation | ASTER validation, soil grid, IP/magnetic | Moderate |
| Skarn/contact metasomatic | intrusive-carbonate contact, W-Bi-Cu, magnetite/skarn minerals | carbonate host, garnet/epidote confirmation | contact mapping, petrography, pXRF W/Bi/Cu | Moderate / Low |
| Polymetallic vein | Pb-Zn-Cu-Ag-As, vein/shear, gossan | grade and continuity | rock chip/channel, soil grid | Moderate / Low |
| VMS possibility | volcanic-sedimentary context, Cu-Zn-Pb-Ba-Fe-Mn | stratiform sulphide texture | stratigraphic mapping, IP, magnetic | Conceptual |
| Heavy mineral / placer | drainage/shlich anomaly, Au/W/Sn indicator | bedrock source | upstream sampling, panning, geomorphology | Contextual |

**Output:**

XV023222\_Buduunkhad\_Preliminary\_Deposit\_Model\_v01.docx

preliminary\_deposit\_model\_evidence\_table\_v01.xlsx

deposit\_model\_candidate\_score\_matrix\_v01.xlsx

**Алхам 10 — Evidence weight scoring хийх**

Deposit model бүрийг 100 оноогоор preliminary score өгнө.

| Шалгуур | Оноо |
| :---- | :---- |
| Favorable geology / host lithology | 20 |
| Intrusive/contact/structure control | 15 |
| Known mineral occurrence | 15 |
| Historical geochemistry / shlich / stream sediment | 15 |
| Metallogenic context | 10 |
| ASTER/Sentinel alteration support | 10 |
| Field mapping / pXRF support | 10 |
| Access / workability | 5 |
| **Нийт** | **100** |

**Confidence class:**

| Оноо | Ангилал |
| :---- | :---- |
| ≥70 | High priority model |
| 50-69 | Moderate priority model |
| 30-49 | Low / conceptual model |
| \<30 | Insufficient evidence |

**Алхам 11 — Phase 3 QA/QC хийх**

| QA/QC item | Acceptance criteria |
| :---- | :---- |
| Map scale limitation recorded | 1:50k, 1:200k, 1:500k ялгаж тэмдэглэсэн |
| Georeference confidence recorded | GCP count, residual, reviewer/date/decision бүртгэсэн |
| Occurrence coordinate validated | map/table/text source хооронд тулгасан |
| CMCS not used as proof | context only limitation бичсэн |
| Remote sensing not used as ore proof | support evidence гэж тэмдэглэсэн |
| Historical vector not mixed with confirmed data | validation\_status \= Historical only |
| Deposit model evidence/missing evidence table complete | model бүрээр бөглөсөн |
| Output source traceability complete | source\_raw\_input\_no, filename, phase, confidence бүрэн |

**Алхам 12 — Phase 4 ба Phase 10 руу handover хийх**

Phase 3-ийн output нь Phase 4-ийн prospect ranking-д шууд орно. Phase 4 дээр prospect polygon бүрт dominant\_deposit\_model, model\_confidence, missing\_model\_evidence, validation\_priority талбар нэмэх ёстой гэж баримтад заасан байна.

**Handover package:**

XV023222\_Buduunkhad\_Geological\_Evidence\_Layers\_v01.gpkg

XV023222\_Buduunkhad\_CMCS\_Nearest\_Deposit\_Register\_v01.xlsx

XV023222\_Buduunkhad\_Regional\_Metallogenic\_Context\_Map\_v01.pdf

XV023222\_Buduunkhad\_Preliminary\_Deposit\_Model\_v01.docx

deposit\_model\_candidate\_score\_matrix\_v01.xlsx

XV023222\_Buduunkhad\_Phase3\_QAQC\_Log\_v01.xlsx

XV023222\_Buduunkhad\_Phase3\_DataGap\_and\_Validation\_Priority\_v01.xlsx

**Decision gate**

Phase 3 дууссан гэж үзэх нөхцөл:

1. №1-8, №53-72 input-уудын геологи, структур, илрэл, prospectivity, metallogenic context Master GIS-д орсон байх.

2. Occurrence/mineralized point coordinate QA/QC хийгдсэн байх.

3. CMCS/MRPAM 5 km, 10 km, 20 km buffer register бэлэн байх.

4. Preliminary Deposit Model.docx болон score matrix бэлэн байх.

5. Бүх historical evidence validation\_status \= Historical only гэж тэмдэглэгдсэн байх.

6. Phase 4 рүү шилжүүлэх A/B/C prospect ranking-д хэрэглэх geological evidence package бэлэн байх.

