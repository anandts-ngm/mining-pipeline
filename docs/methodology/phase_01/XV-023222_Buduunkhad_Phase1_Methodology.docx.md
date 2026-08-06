**БҮДҮҮНХАД ХАЙГУУЛЫН ТАЛБАЙ**

**XV-023222 / L23222**

**PHASE 1 — Өгөгдлийн аудит ба Master GIS бэлтгэл**

*Гүйцэтгэх дэлгэрэнгүй арга зүй ба ажлын дараалал*

**Стандарт CRS: WGS 84 / UTM Zone 47N — EPSG:32647**

Оролт: 78 raw input файл  •  Програм: QGIS

# **Агуулга**

# **1\. Phase 1-ийн зорилго ба үндсэн зарчим**

Phase 1 нь Бүдүүнхад талбайн хайгуулын дараагийн бүх шатны суурь болно. Энэ шатанд raw өгөгдлийг засварлахгүйгээр зөвхөн working copy дээр шалгалт, CRS тохируулга, бүртгэл, georeference хийж, бүх орон зайн өгөгдлийг нэг стандарт координатын системд (EPSG:32647) нэгтгэн Master GIS суурийг бий болгоно.

## **1.1. Эцсийн зорилго**

* Бүх 78 raw input файлыг GIS-д ашиглах боломжтой эсэхээр шалгах;

* License boundary болон бүх орон зайн өгөгдлийг EPSG:32647 стандарт CRS-д нэгтгэх;

* Scan map, JPG, PDF, GeoTIFF, KMZ/KML, DEM, Sentinel, KOMPSAT, металлогени/геологийн зурагт CRS / georeference / resolution / extent / metadata QA/QC хийх;

* Master GIS Database (.gpkg) болон Master QGIS Project (.qgz) үүсгэх;

* Өгөгдөл тус бүрийн итгэлцлийн зэрэглэл (data confidence ranking) гаргах;

* Phase 2 (Remote Sensing) болон Phase 3 (Geological Synthesis)-д ашиглахад бэлэн GIS суурь бүрдүүлэх.

## **1.2. Удирдах зарчим**

| Зарчим | Хэрэгжүүлэх дүрэм |
| :---- | :---- |
| Raw preservation | 00\_Raw\_Files\_Archive доторх эх файлыг read-only хадгална. Нэр солих шаардлагатай бол register-д бичнэ, эх файлыг overwrite хийхгүй. |
| Processing copy | Бүх боловсруулалтыг зөвхөн working copy дээр хийнэ. Эх raster, KMZ, PDF, scan-г шууд дарж хадгалахгүй. |
| CRS control | Эцсийн бүтээгдэхүүн EPSG:32647-д хадгалагдана. Native/source CRS-г metadata болон QA/QC log-д хадгална. |
| Sidecar integrity | .tfw, .jgw, .aux.xml, .ovr, .rpc, .eph, .txt зэрэг туслах файлуудыг үндсэн raster/image-ээс салгахгүй хамт хадгална. |
| Evidence hierarchy | Remote sensing / pXRF / drone \= support evidence. Lab assay \+ field geology \+ structural control \= decision evidence. |
| Decision gate | Phase 1 төгсгөлд QA/QC болон go/no-go шалгуурыг хангаж байж дараагийн шат руу шилжинэ. |

# **2\. Folder бүтэц**

Одоо байгаа 11 (эсвэл 12\) сэдэвчилсэн folder-ийг устгахгүй, нэрийг нь солихгүй. Үүнийг Raw / Input Evidence Library болгон ашиглаж, дээр нь тусдаа Phase 1 ажлын орчныг нэмнэ. Ингэснээр raw өгөгдөл ба боловсруулалт хоёр тусдаа байрлана.

## **2.1. Төслийн дээд түвшний бүтэц**

XV-023222\_Buduunkhad\_Project/  
│  
├── 00\_Raw\_Input\_Evidence\_Library/        (эх өгөгдөл — read-only)  
│     ├── 01\_Tectonic\_Terrane\_KMZ/  
│     ├── 02\_DEM\_ALOS\_ASTERGDEM/  
│     ├── 03\_KOMPSAT2\_MSC\_L1G/  
│     ├── 04\_HeavyMineral\_StreamSediment\_Field/  
│     ├── 05\_Geology\_Mineral\_Prospectivity/  
│     ├── 06\_Regional\_Metallogenic\_L47B/  
│     └── 07\_Basemap\_Sentinel2\_ASTER/  
│  
├── 01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup/   (энэ шатны ажлын орчин)  
├── 02\_Phase\_2\_Remote\_Sensing\_Preprocessing/  
├── 03\_Phase\_3\_Geological\_Metallogenic\_Synthesis/  
├── 04\_Phase\_4\_Preliminary\_Prospect\_Ranking/  
└── 99\_Final\_Deliverables/

## **2.2. Phase 1-ийн дотоод бүтэц**

01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup/  
│  
├── 00\_Admin\_and\_Method/  
│     ├── Phase1\_Methodology.docx  
│     ├── Phase1\_Action\_Log.xlsx  
│     └── Phase1\_QAQC\_Checklist.xlsx  
│  
├── 01\_Input\_Working\_Copy/         (raw-аас хуулсан ажлын хувь)  
│     ├── 01\_Tectonic\_Terrane\_KMZ/ ... 07\_Basemap\_Sentinel2\_ASTER/  
│  
├── 02\_Inventory\_and\_Metadata/  
│     ├── XV-023222\_Buduunkhad\_Phase1\_File\_Inventory.xlsx  
│     ├── XV-023222\_Buduunkhad\_Phase1\_Metadata\_Register.xlsx  
│     └── XV-023222\_Buduunkhad\_Sidecar\_File\_Check.xlsx  
│  
├── 03\_CRS\_Check/  
│     ├── Vector\_CRS\_Check/   Raster\_CRS\_Check/  
│     ├── Native\_CRS\_Notes/   Reprojected\_EPSG32647/  
│  
├── 04\_Georeference\_Check/  
│     ├── Scan\_Maps\_To\_Georeference/   GCP\_Tables/  
│     ├── Georeferenced\_Rasters/        Georeference\_Residual\_Reports/  
│     └── Low\_Confidence\_Georef/  
│  
├── 05\_Master\_GIS\_Database/  
│     ├── XV-023222\_Buduunkhad\_Master\_GIS\_Database.gpkg  
│     ├── XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz  
│     └── Styles\_QML/  
│  
├── 06\_QAQC\_and\_Confidence/  
│     ├── XV-023222\_Buduunkhad\_CRS\_Georeference\_QAQC\_Log.xlsx  
│     ├── XV-023222\_Buduunkhad\_Data\_Confidence\_Ranking.xlsx  
│     └── XV-023222\_Buduunkhad\_Data\_Gap\_Register.xlsx  
│  
└── 07\_Output/  
      ├── XV-023222\_Buduunkhad\_Phase1\_Desktop\_Study\_Summary.docx  
      ├── XV-023222\_Buduunkhad\_Phase1\_Master\_GIS\_Index\_Map.pdf  
      └── XV-023222\_Buduunkhad\_Phase1\_Deliverables\_Readme.txt

# **3\. Оролтын өгөгдөл (78 файл, 7 evidence group)**

Phase 1-д бүх 78 raw input файл хамрагдана. Эдгээрийг 7 evidence group-т ангилсан бөгөөд group тус бүрд хийх гол шалгалт доор үзүүлэв.

| № | Evidence group | Файл | Phase 1-д хийх гол шалгалт |
| :---- | :---- | :---- | :---- |
| 01 | Tectonic / Terrane KMZ | 8 | License boundary, террейн контекст, KMZ/KML координат шалгах; scan-уудыг georeference-д бэлтгэх. |
| 02 | DEM (ALOS / ASTER GDEM) | 14 | DEM-ийн CRS, resolution, extent, NoData, өндрийн нэгж шалгах; sidecar (tfw/aux/ovr) холбох. |
| 03 | KOMPSAT-2 MSC L1G | 24 | PAN/MS raster, RPC, metadata, band identity, georeference шалгах; bundle бүрэн эсэхийг шалгах. |
| 04 | Heavy Mineral / Stream Sediment / Field | 6 | Scan map, legend, хээрийн дэвтэр, координатын мэдээллийг бүртгэх. |
| 05 | Geology / Mineral Prospectivity | 16 | 1:50,000 ба 1:200,000 геологи/ашигт малтмалын зургийг georeference-д бэлтгэх; occurrence хүснэгт цэвэрлэх. |
| 06 | Regional Metallogenic L47B | 4 | 1:500,000 металлогений зураг, legend, тайлан scan бүртгэх; региональ контекстээр georeference. |
| 07 | Basemap / Sentinel-2 / ASTER | 6 | GeoTIFF, Sentinel derived raster, ASTER HDF, Google basemap-ийн CRS шалгах; reproject шаардлага тэмдэглэх. |

*Анхааруулга: Sidecar файлууд (.tfw, .jgw, .aux.xml, .ovr, .rpc, .eph, .txt) нь дангаараа орон зайн layer биш. Тэдгээрийг үндсэн raster/image-тэй хамт archive хийж, ганцаар нь GIS-д нээхгүй.*

# **4\. Ажлын дэлгэрэнгүй дараалал**

## **Алхам 1\. Raw archive хамгаалах ба working copy үүсгэх**

Эхний зарчим: 00\_Raw\_Input\_Evidence\_Library доторх эх файлыг огт өөрчлөхгүй. Phase 1-д ашиглах файлуудыг зөвхөн 01\_Input\_Working\_Copy руу хуулна.

| № | Ажил | Тайлбар |
| :---- | :---- | :---- |
| 1 | Raw folder-оос working copy үүсгэх | 7 evidence group-ийн бүтцийг хэвээр хадгална. |
| 2 | Файл бүрийн нэр, өргөтгөл, хэмжээ, эх сурвалж бүртгэх | Inventory Excel-д оруулна. |
| 3 | Sidecar бүрийг үндсэн файлтай холбох | .tfw, .jgw, .aux.xml, .ovr, .rpc, .eph, .txt бүрэн эсэхийг шалгах. |
| 4 | Дутуу sidecar байгаа эсэхийг шалгах | KOMPSAT bundle, GeoTIFF, scan map-д онцгой чухал. |
| 5 | SHA-256 / checksum бүртгэх | Raw ба working copy зөрсөн эсэхийг хянах. |

**Phase 1 Action Log-ийн баганууд:**

Date • Operator • File group • Action • Software • Input file • Output file • Issue • Status

## **Алхам 2\. Master inventory үүсгэх**

Файл бүрийг нэг мөрөөр бүртгэнэ. Inventory-ийн баганууд:

| Багана | Тайлбар / жишээ |
| :---- | :---- |
| File\_ID | BK-P1-001 гэх мэт давтагдашгүй дугаар |
| Evidence\_Group | 01\_Tectonic\_Terrane\_KMZ ... 07\_Basemap\_Sentinel2\_ASTER |
| Original\_Filename | Raw файлын нэр |
| Working\_Copy\_Path | Phase 1 working copy дахь зам |
| File\_Type | KMZ, KML, TIF, JPG, PDF, DOCX, XLSX, HDF гэх мэт |
| Spatial\_Type | Vector / Raster / Scan / Table / Text / Report |
| Has\_CRS / Native\_CRS | Yes / No / Unknown ба EPSG код эсвэл тайлбар |
| Target\_CRS | EPSG:32647 |
| Has\_Georeference | Yes / No / Approx / Unknown |
| Sidecar\_Files | TFW / RPC / AUX / OVR байгаа эсэх |
| Open\_Status | Opens / Error / Needs conversion |
| Main\_Use | Boundary, DEM, geology, occurrence, basemap гэх мэт |
| Confidence | High / Medium / Low / Needs verification |
| Note | Асуудал, тайлбар |

## **Алхам 3\. QGIS project тохируулах**

QGIS дээр шинэ project үүсгээд дараах үндсэн тохиргоог хийнэ:

| Тохиргоо | Утга |
| :---- | :---- |
| Project CRS | WGS 84 / UTM Zone 47N — EPSG:32647 |
| Distance unit | meters |
| Area unit | square kilometers / hectares |
| Ellipsoid | WGS84 |
| Project name | XV-023222\_Buduunkhad\_Master\_QGIS\_Project |
| Save format | .qgz |
| Main database | GeoPackage (.gpkg) |

*Анхаарах: Native/raw CRS-г устгахгүй. Эцсийн layer-уудыг EPSG:32647-д хадгалж, эх CRS болон source metadata-г attribute эсвэл QA/QC log-д хадгална.*

## **Алхам 4\. License boundary шалгах ба EPSG:32647 руу хөрвүүлэх**

MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz нь L23222 тусгай зөвшөөрлийн хил (WGS84 polygon). QGIS дээр хийх дараалал:

1. Layer → Add Layer → Add Vector Layer; KMZ/KML файлыг нээх.

2. Layer CRS-г шалгах (ихэвчлэн EPSG:4326 / WGS84).

3. Polygon зөв байрлалтай эсэхийг Google/Bing/OSM суурь зурагтай харьцуулах.

4. Right click → Export → Save Features As → Format: GeoPackage; CRS: EPSG:32647.

5. Layer name: license\_boundary\_L23222\_EPSG32647\_v01.

6. Үүссэн layer-ийг Master GeoPackage-д хадгалах.

**Нэмэх attribute талбарууд:**

| Field | Жишээ утга |
| :---- | :---- |
| license\_no | L23222 |
| project | Buduunkhad |
| code | XV-023222 |
| source\_file | MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz |
| source\_crs | EPSG:4326 |
| final\_crs | EPSG:32647 |
| confidence | High |
| note | Original WGS84 KMZ converted to UTM47N |

## **Алхам 5\. Buffer layer үүсгэх**

Phase 3-д CMCS болон региональ контекст шалгахад ашиглах buffer-уудыг Phase 1-д урьдчилан үүсгэнэ (Vector → Geoprocessing Tools → Buffer). Бүгд EPSG:32647-д хадгалагдана.

| Buffer | Ашиглах зорилго | Layer нэр |
| :---- | :---- | :---- |
| 500 м | Remote sensing clip хийхэд | license\_buffer\_500m\_EPSG32647\_v01 |
| 1 км | Sentinel, ASTER, KOMPSAT subset хийхэд | license\_buffer\_1km\_EPSG32647\_v01 |
| 5 км | Ойролцоох илрэл, хагарал, геологи шалгах | license\_buffer\_5km\_EPSG32647\_v01 |
| 10 км | Геохими, шлих, региональ структур шалгах | license\_buffer\_10km\_EPSG32647\_v01 |
| 20 км | CMCS, металлогений контекст шалгах | license\_buffer\_20km\_EPSG32647\_v01 |

## **Алхам 6\. Raster CRS / metadata QA/QC (DEM, KOMPSAT, Sentinel, ASTER, basemap)**

Raster файл бүрийн CRS, pixel size, band count, extent, NoData-г шалгаж бүртгэнэ. License boundary-тэй давхцаж байгаа эсэх, reproject шаардлагатай эсэхийг тэмдэглэнэ.

* DEM, hillshade, slope raster-уудын CRS, resolution, extent, NoData шалгах.

* KOMPSAT PAN/MS файлуудыг metadata (.txt), RPC (.rpc), ephemeris (.eph)-тэй тулгаж bundle бүрэн эсэхийг шалгах.

* Sentinel-2 (T46 tile — UTM46N байж болзошгүй), ASTER HDF, Google basemap-ийн CRS шалгах.

* EPSG:32647-аас өөр CRS-тэй raster-уудыг Reprojected\_EPSG32647 folder-т тэмдэглэх (хөрвүүлэлтийг Phase 2-д гүйцэтгэнэ).

* Scene extent index болон DEM extent index layer үүсгэх.

*Анхаар: ASTER HDF (№73) import алдаа гарч болзошгүй — compatibility шалгах. Sentinel болон зарим basemap UTM46N (EPSG:32646)-д ирсэн тул EPSG:32647 руу reproject хийх эсэхийг тэмдэглэнэ.*

## **Алхам 7\. Scan map georeference (тэргүүлэх дараалал)**

QGIS Georeferencer ашиглан scan зургуудыг координатад тааруулна. Тэргүүлэх дараалал:

| № | Зураг | Масштаб | Гаралт |
| :---- | :---- | :---- | :---- |
| 1 | Detailed geology map (Namalzakh L47-74-A) | 1:50,000 | detailed\_geology\_50k\_georef\_EPSG32647\_v01.tif |
| 2 | Mineral occurrence / source materials map | 1:50,000 | mineral\_occurrence\_50k\_georef\_EPSG32647\_v01.tif |
| 3 | Regional geology / stream sediment / heavy mineral | 1:200,000 | regional\_geology\_200k\_georef\_EPSG32647\_v01.tif |
| 4 | Regional metallogenic map (L47-B Talshand) | 1:500,000 | regional\_metallogenic\_500k\_georef\_EPSG32647\_v01.tif |

**Georeference дараалал:**

7. Зураг дээрх координатын grid эсвэл танигдах цэгүүдээс GCP (Ground Control Point) сонгох.

8. Transformation: эхлээд Polynomial 1, шаардлагатай бол Thin Plate Spline ашиглах.

9. Target CRS: EPSG:32647. Output GeoTIFF үүсгэх.

10. GCP хүснэгтийг GCP\_Tables-д, RMSE/residual тайланг Georeference\_Residual\_Reports-д хадгалах.

11. RMSE өндөр (масштабт тохирохгүй) бол Low\_Confidence\_Georef-т тэмдэглэж confidence-г бууруулах.

## **Алхам 8\. Master GIS Database (GeoPackage) угсрах**

Шалгагдсан, хөрвүүлэгдсэн бүх layer-ийг нэг GeoPackage-д нэгтгэнэ. Layer group-ийн логик нь Windows folder болон QGIS group-тэй нийцэх ёстой.

05\_Master\_GIS\_Database/  
├─ 01\_Rasters    (georeferenced scan, DEM, basemap extent index)  
├─ 02\_Vectors    (license boundary, buffers, occurrence points, anomaly polygons)  
├─ 03\_Metadata   (source file, CRS, projection date, data source)  
└─ 04\_QAQC       (CRS check log, overlay screenshots, alignment notes)

**Угсрах дараалал:**

12. Raster layer нэмэх (Layer → Add Raster Layer) — georeferenced scan, DEM деривативын extent.

13. Vector / point layer нэмэх (GPKG, CSV, XLSX) — alias, field name тохируулах, editable болгох.

14. Шаардлагатай attribute талбарт constraint тавих (Sample ID, Lithology, Mineralization).

15. CRS ба alignment шалгах: бүх layer EPSG:32647 эсэх, overlay-аар spatial alignment баталгаажуулах (license boundary \+ regional map \+ DEM).

16. Layer → Export → Save As → GeoPackage: XV-023222\_Buduunkhad\_Master\_GIS\_Database.gpkg.

17. Layer group-уудыг Raster / Vector (Points, Polygons, Lines) / QAQC болгон зохион байгуулах.

18. Style (.qml) файлуудыг Styles\_QML-д хадгалах.

19. QGIS project-ийг .qgz форматаар хадгалах; бүх subfolder-ийг backup .zip болгох.

## **Алхам 9\. QA/QC ба итгэлцлийн зэрэглэл (confidence ranking)**

Layer, raster, scan бүрд итгэлцлийн зэрэглэл өгч, data gap register гаргана.

| Зэрэглэл | Тайлбар |
| :---- | :---- |
| High | Native CRS тодорхой, georeference нарийвчлалтай (бага RMSE), metadata бүрэн. |
| Medium | CRS/metadata шалгагдсан боловч зарим тодруулга шаардлагатай. |
| Low | Georeference хийгдсэн ч RMSE өндөр, эсвэл source баталгаажаагүй scan. |
| Needs verification | Нээгдэхгүй, эсвэл CRS/source тодорхойгүй; нэмэлт шалгалт шаардлагатай. |

**QA/QC хийх зүйлс:**

* Бүх layer EPSG:32647 эсэхийг шалгах.

* License boundary, regional map, DEM-ийг overlay хийж spatial alignment баталгаажуулах.

* Overlay screenshot болон alignment note-ийг 04\_QAQC-д хадгалах.

* QGIS Print Layout ашиглан visual QA/QC report бэлдэх.

* Дутуу өгөгдөл, тулгарсан асуудлыг Data Gap Register-т бүртгэх.

# **5\. Ажлын бодит дараалал — эхний 5 өдөр**

| Өдөр | Хийх ажил | Гарах үр дүн |
| :---- | :---- | :---- |
| Өдөр 1 | Raw folder хамгаалах, working copy үүсгэх, file inventory эхлүүлэх (нэр, өргөтгөл, хэмжээ, type, sidecar, open status). | Phase1\_File\_Inventory.xlsx |
| Өдөр 2 | QGIS project (EPSG:32647); license boundary import ба GeoPackage руу хөрвүүлэх; 500м–20км buffer; Master GeoPackage \+ QGIS project үүсгэх. | Master\_GIS\_Database.gpkg; Master\_QGIS\_Project.qgz; boundary \+ 5 buffer layer |
| Өдөр 3 | DEM, hillshade, slope шалгах; KOMPSAT PAN/MS-ийг metadata/RPC/EPH-тэй тулгах; Sentinel/ASTER/basemap CRS; extent index үүсгэх. | Raster\_CRS\_QAQC\_Log.xlsx; scene & DEM extent index |
| Өдөр 4 | Scan map georeference (1:50k → 1:200k → 1:500k); GCP table, RMSE/residual report; confidence оноох. | Georeferenced .tif-үүд; Georeference\_QAQC\_Log.xlsx |
| Өдөр 5 | Бүх өгөгдөлд confidence; data gap register; Phase 2-д бэлэн dataset list; desktop study summary; Master GIS index map PDF. | Data\_Confidence\_Ranking.xlsx; Data\_Gap\_Register.xlsx; Index\_Map.pdf; Desktop\_Study\_Summary.docx |

# **6\. Нэршлийн стандарт**

Бүх output layer, raster, Excel, PDF-г нэг стандарт нэршлээр нэрлэнэ:

XV023222\_Buduunkhad\_\<Theme\>\_\<Description\>\_\<Scale\_or\_Resolution\>\_\<CRS\>\_v01

**Жишээ:**

XV023222\_Buduunkhad\_LicenseBoundary\_L23222\_EPSG32647\_v01  
XV023222\_Buduunkhad\_RegionalGeology\_200K\_Georef\_EPSG32647\_v01  
XV023222\_Buduunkhad\_DetailedGeology\_50K\_Georef\_EPSG32647\_v01  
XV023222\_Buduunkhad\_MineralOccurrences\_Points\_EPSG32647\_v01  
XV023222\_Buduunkhad\_StreamSediment\_AnomalyPolygons\_EPSG32647\_v01  
XV023222\_Buduunkhad\_ALOS\_DEM\_12p5m\_EPSG32647\_v01  
XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MetadataCheck\_v01

# **7\. Folder бүрийн “дууссан” шалгуур**

| Folder / сэдэв | Дууссан гэж үзэх нөхцөл |
| :---- | :---- |
| License boundary | Boundary EPSG:32647 болсон, 5 buffer үүссэн. |
| Regional geology 1:200K | Scan georeference хийгдсэн, confidence өгсөн. |
| Detailed geology 1:50K | Зураг georeference, lithology/fault/contact digitize эхэлсэн. |
| Mineral occurrences | Occurrence хүснэгт GIS point layer болсон. |
| Regional metallogeny 1:500K | Зураг context layer болсон. |
| Geochem / heavy mineral | Stream/heavy mineral map georeference, anomaly polygon эхэлсэн. |
| Metallogeny / prospectivity | Historical prospect polygon digitize болсон. |
| Field observation / routes | Observation point, route line GIS layer болсон. |
| Remote sensing imagery | Raster QA/QC, metadata, CRS status бүртгэгдсэн. |
| DEM / terrain | DEM/hillshade/slope CRS, extent, NoData шалгагдсан. |
| Tectonic / terrane | Terrane context layer, confidence flag бэлэн болсон. |

# **8\. Phase 1-ийн эцсийн бүтээгдэхүүн (deliverables)**

* XV-023222\_Buduunkhad\_Master\_GIS\_Database.gpkg — нэгдсэн GeoPackage.

* XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz — Master QGIS project.

* XV-023222\_Buduunkhad\_Phase1\_File\_Inventory.xlsx — бүх файлын бүртгэл.

* XV-023222\_Buduunkhad\_CRS\_Georeference\_QAQC\_Log.xlsx — CRS ба georeference QA/QC.

* XV-023222\_Buduunkhad\_Data\_Confidence\_Ranking.xlsx — итгэлцлийн зэрэглэл.

* XV-023222\_Buduunkhad\_Data\_Gap\_Register.xlsx — дутуу өгөгдлийн бүртгэл.

* XV-023222\_Buduunkhad\_Phase1\_Master\_GIS\_Index\_Map.pdf — индекс зураг.

* XV-023222\_Buduunkhad\_Phase1\_Desktop\_Study\_Summary.docx — desktop study дүгнэлт.

## **Phase 1-ийн логик урсгал**

Raw evidence folders  
      ↓  
Working copy  →  File inventory  →  CRS check  →  Georeference check  
      ↓  
Master GeoPackage  →  Master QGIS Project  →  Confidence ranking  
      ↓  
Phase 2 (Remote Sensing)  \+  Phase 3 (Geological Synthesis)

***Decision gate: Master GIS суурь EPSG:32647-д бүрэн нэгтгэгдэж, бүх өгөгдөл confidence-тэй бүртгэгдэж, QA/QC log бэлэн болсон тохиолдолд Phase 2 руу шилжинэ.***