Доорх нь **02\. Phase 2 — Remote Sensing Preprocessing**\-ийг QGIS/SNAP/ILWIS/Global Mapper дээр бодитоор хийх **дэлгэрэнгүй ажлын заавар** юм. Энэ заавар нь таны оруулсан workflow document-д заасан Phase 2 input буюу **№9–22 DEM/ALOS/ASTERGDEM, №23–46 KOMPSAT-2, №73 ASTER HDF, №74–78 Sentinel/Google/basemap raster** дээр үндэслэв.

---

**02\. Phase 2 — Remote Sensing Preprocessing хийх дэлгэрэнгүй заавар**

**1\. Phase 2-ийн зорилго**

Phase 2-ийн зорилго нь Sentinel-2, ASTER, KOMPSAT-2, ALOS-PALSAR DEM, ASTER GDEM болон Google/basemap raster-уудыг **нэг CRS, нэг project standard, нэг QA/QC бүртгэлтэй** болгож, дараагийн Phase 3–4-д ашиглахад бэлэн **support evidence layer** гаргах явдал.

Анхаарах үндсэн зарчим:

Remote sensing output нь **хүдэржилтийн баталгаа биш**. Энэ нь зөвхөн alteration, lithology contrast, lineament, drainage, terrain, outcrop/access support evidence юм. Эцсийн баталгааг field mapping, rock chip/channel sampling, lab assay, structural validation, trench/geophysics/drilling өгнө.

---

**2\. Ажил эхлэхийн өмнөх шаардлага**

**2.1 Phase 1-ээс бэлэн байх ёстой зүйл**

Phase 2 эхлэхийн өмнө Phase 1 дээр дараах зүйлс бэлэн байна:

1. XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz

2. XV-023222\_Buduunkhad\_Master\_GIS\_Database.gpkg

3. LicenseBoundary\_EPSG32647.gpkg

4. XV023222\_Buduunkhad\_Project\_Buffer\_500m\_1km\_5km\_10km\_20km\_25km\_EPSG32647.gpkg

5. XV-023222\_Buduunkhad\_CRS\_Georeference\_QAQC\_Log.xlsx

6. XV-023222\_Buduunkhad\_Data\_Confidence\_Ranking.xlsx

Project CRS заавал:

**WGS 84 / UTM Zone 47N — EPSG:32647**

---

**3\. Phase 2 folder structure үүсгэх**

Windows Explorer дээр дараах folder бүтцийг яг ингэж үүсгэнэ:

02\_Phase\_2\_Remote\_Sensing\_Preprocessing/

├── 00\_Input\_Working\_Copy

├── 01\_Sentinel2\_SNAP13

│   ├── 01\_Input

│   ├── 02\_QAQC

│   ├── 03\_Masks

│   ├── 04\_Indices

│   ├── 05\_Composites

│   └── 06\_Export\_EPSG32647

├── 02\_ASTER\_Workflow\_v5

│   ├── 01\_Input\_HDF

│   ├── 02\_Band\_Extraction

│   ├── 03\_Project\_UTM47

│   ├── 04\_Index\_Calculation

│   ├── 05\_Score\_Class\_Binary

│   └── 06\_QAQC

├── 03\_KOMPSAT2\_ILWIS368\_QGIS

│   ├── 01\_Input\_Bundle

│   ├── 02\_Metadata\_RPC\_EPH\_Check

│   ├── 03\_Band\_Stack

│   ├── 04\_Orthorectification

│   ├── 05\_Pansharpen

│   ├── 06\_NDVI\_Lineament\_Outcrop

│   └── 07\_QAQC

├── 04\_ALOS\_ASTERGDEM\_GlobalMapper\_QGIS

│   ├── 01\_Input\_DEM

│   ├── 02\_DEM\_QAQC

│   ├── 03\_Reproject\_Clip

│   ├── 04\_Terrain\_Derivatives

│   ├── 05\_Drainage\_Watershed

│   └── 06\_Access\_Safety

├── 05\_Basemap\_Google\_HighRes

│   ├── 01\_Input

│   ├── 02\_Reproject\_Clip

│   └── 03\_QAQC

├── 06\_RemoteSensing\_QAQC

└── 07\_Final\_Export\_EPSG32647

00\_Input\_Working\_Copy дотор raw archive-оос зөвхөн **copy** хийж авна. Raw file дээр шууд ажиллахгүй.

---

**4\. Phase 2 input файлуудыг зөв байрлуулах**

**4.1 DEM / ALOS / ASTER GDEM input**

Дараах №9–22 файлуудыг:

04\_ALOS\_ASTERGDEM\_GlobalMapper\_QGIS/01\_Input\_DEM

дотор хуулна.

Үүнд:

№9  ASTER-GDEM-v3\_N45E096\_DEM\_1arcsec\_WGS84\_v01\_raw.tif

№10 ASTER-GDEM-v3\_N45E096\_NumObservations\_1arcsec\_WGS84\_v01\_raw.tif

№11 XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tfw

№12 XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif

№13 XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.aux.xml

№14 XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.ovr

№15–22 ALOS hillshade/slope sidecar болон derived raster files

Анхаарах зүйл: .tfw, .aux.xml, .ovr файлуудыг parent .tif файлаас салгаж болохгүй.

---

**4.2 KOMPSAT-2 input**

Дараах №23–46 файлуудыг:

03\_KOMPSAT2\_ILWIS368\_QGIS/01\_Input\_Bundle

дотор хуулна.

KOMPSAT bundle нь дараах бүтэцтэй байна:

PAN:

MSC\_111127030410\_28454\_08621344PN00\_1G.tif

MSC\_111127030410\_28454\_08621344PN00\_1G.txt

MSC\_111127030410\_28454\_08621344PN00\_1G.rpc

MSC\_111127030410\_28454\_08621344PN00\_1G.eph

Green:

MSC\_111127030410\_28454\_08621344M1N00G\_1G.tif

.txt / .rpc / .eph

Blue:

MSC\_111127030410\_28454\_08621344M2N00B\_1G.tif

.txt / .rpc / .eph

NIR:

MSC\_111127030410\_28454\_08621344M3N00N\_1G.tif

.txt / .rpc / .eph

Red:

MSC\_111127030410\_28454\_08621344M4N00R\_1G.tif

.txt / .rpc / .eph

Browse/thumbnail:

MSC\_111127030410\_28454\_08621344N00\_1G\_br.jpg

MSC\_111127030410\_28454\_08621344N00\_1G\_br.jgw

MSC\_111127030410\_28454\_08621344N00\_1G\_tn.jpg

.txt, .rpc, .eph нь metadata/geometry sidecar учраас устгаж, салгаж, rename хийж болохгүй.

---

**4.3 ASTER HDF input**

№73 файлыг:

02\_ASTER\_Workflow\_v5/01\_Input\_HDF

дотор хуулна.

2005-09-05\_MN\_ASTER-L1B\_MultispectralImagery\_00409052005043503\_v01\_raw.hdf

---

**4.4 Sentinel / Google / basemap input**

№74–78 файлуудыг:

01\_Sentinel2\_SNAP13/01\_Input

болон basemap бол:

05\_Basemap\_Google\_HighRes/01\_Input

дотор ангилж хуулна.

№74 2025-05-28\_MN\_T46TGS\_GeoreferencedSatelliteRaster\_v01\_raw.tif

№75 XV023222\_Buduunkhad\_GoogleMaps\_BasemapImagery\_RGB\_2p4m\_WGS84\_Raw\_v01.tif

№76 XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_EPSG3857\_0p15m\_Raw\_v01.tif

№77 XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_GeologicalInterpretation\_RGB\_B12-B08-B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif

№78 XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_B11B12\_B08B11\_B04B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif

№77, №78 нь нэрнээсээ харахад **UTM46N** байж болзошгүй тул заавал EPSG:32647 руу reproject хийнэ.

---

**5\. QGIS project тохируулах**

QGIS нээнэ.

Доорх тохиргоог хийнэ:

Project CRS: EPSG:32647

Project name: XV-023222\_Buduunkhad\_Phase2\_RemoteSensing.qgz

Дараах layer-үүдийг эхэлж оруулна:

1. License boundary EPSG:32647

2. 500 m buffer

3. 1 km buffer

4. 5 km / 10 km / 20 km / 25 km buffer

5. Phase 1 Master GIS base layers

Дараа нь бүх raster-уудыг нэг нэгээр нь QGIS-д оруулж CRS, extent, pixel size, band count, NoData шалгана.

---

**6\. DEM / ALOS-PALSAR / ASTER GDEM боловсруулах заавар**

**6.1 DEM metadata шалгах**

QGIS дээр DEM raster дээр right click:

Layer Properties → Information

Шалгах зүйл:

CRS

Extent

Pixel size

Band count

Data type

NoData value

Statistics

Resolution

QA/QC register-д дараах багануудыг бөглөнө:

source\_raw\_input\_no

source\_raw\_filename

raster\_type

native\_crs

pixel\_size

extent

nodata\_value

band\_count

sidecar\_available

processing\_action

qaqc\_status

reviewer

review\_date

comment

---

**6.2 DEM reproject хийх**

QGIS:

Raster → Projections → Warp (Reproject)

Тохиргоо:

Input layer: ALOS-PALSAR DEM эсвэл ASTER GDEM

Source CRS: native CRS

Target CRS: EPSG:32647

Resampling: Bilinear

Output resolution: эх raster-ийн resolution-д ойролцоо

NoData: эх NoData-г хадгална

Output нэр:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif

ASTER GDEM output:

XV023222\_Buduunkhad\_ASTERGDEM\_DEM\_EPSG32647\_v01.tif

---

**6.3 License \+ buffer-аар clip хийх**

QGIS:

Raster → Extraction → Clip Raster by Mask Layer

Тохиргоо:

Input raster: reprojected DEM

Mask layer: license\_boundary\_buffer\_1km эсвэл 5km

Crop to cutline: checked

Keep resolution of input raster: checked

Target CRS: EPSG:32647

Output:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_Clip1km\_EPSG32647\_v01.tif

---

**6.4 Hillshade гаргах**

QGIS:

Raster → Analysis → Hillshade

Тохиргоо:

Input: clipped DEM

Z factor: 1

Azimuth: 315

Vertical angle: 45

Output:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_Hillshade\_12p5m\_EPSG32647\_v01.tif

Нэмэлтээр lineament харахад өөр азимуттай hillshade гаргаж болно:

Azimuth 045

Azimuth 090

Azimuth 135

Azimuth 315

---

**6.5 Slope гаргах**

QGIS:

Raster → Analysis → Slope

Тохиргоо:

Input: clipped DEM

Slope expressed as: degrees

Output:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_SlopeDeg\_12p5m\_EPSG32647\_v01.tif

---

**6.6 Aspect гаргах**

QGIS:

Raster → Analysis → Aspect

Output:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_Aspect\_12p5m\_EPSG32647\_v01.tif

---

**6.7 Contour гаргах**

QGIS:

Raster → Extraction → Contour

Тохиргоо:

Input: DEM

Interval: 5 m эсвэл 10 m

Attribute name: elev

Output:

XV023222\_Buduunkhad\_Contour\_10m\_EPSG32647\_v01.gpkg

---

**6.8 Drainage / watershed гаргах**

QGIS Processing Toolbox ашиглана.

Дараалал:

Fill sinks

Flow direction

Flow accumulation

Channel network

Watershed / catchment

Output:

XV023222\_Buduunkhad\_Drainage\_Network\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_Watershed\_Catchments\_EPSG32647\_v01.gpkg

Үүнийг Phase 8 stream sediment / heavy mineral follow-up-д ашиглана.

---

**6.9 Terrain ruggedness / curvature гаргах**

QGIS эсвэл SAGA tools:

Terrain Ruggedness Index

Profile curvature

Plan curvature

Output:

XV023222\_Buduunkhad\_Terrain\_Ruggedness\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Curvature\_EPSG32647\_v01.tif

---

**6.10 DEM final package**

DEM хэсгийн final output:

XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_ASTERGDEM\_DEM\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_ALOS\_PALSAR\_Hillshade\_12p5m\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_ALOS\_PALSAR\_SlopeDeg\_12p5m\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_ALOS\_PALSAR\_Aspect\_12p5m\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Contour\_10m\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_Drainage\_Network\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_Watershed\_Catchments\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_DEM\_QAQC\_Log.xlsx

---

**7\. Sentinel-2 боловсруулах заавар**

**7.1 Sentinel raster status шалгах**

№74, №77, №78-г QGIS дээр нээнэ.

Шалгах зүйл:

CRS: UTM46N эсэх, EPSG:32647 эсэх

Pixel size: 10 m эсэх

Band count

Band order

Extent license boundary-тэй давхцаж байгаа эсэх

NoData

Хэрэв raster аль хэдийн derivative product бол дахин Sen2Cor хийхгүй. Зөвхөн metadata бүртгэж, EPSG:32647 руу reproject/clip хийнэ.

Хэрэв raw Sentinel-2 L1C SAFE folder байгаа бол SNAP 13.0.0 дээр Sen2Cor ашиглаж L2A болгоно.

---

**7.2 SNAP дээр L1C → L2A болгох**

SNAP 13.0.0 нээнэ.

File → Open Product

Sentinel SAFE product оруулна.

Дараа нь:

Optical → Thematic Land Processing → Sen2Cor

Output:

L2A product

L2A болсны дараа 10 m bands:

B02 Blue

B03 Green

B04 Red

B08 NIR

20 m bands:

B11 SWIR1

B12 SWIR2

Эдгээрийг 10 m grid рүү resample хийнэ.

---

**7.3 SNAP дээр resample хийх**

Raster → Geometric Operations → Resampling

Тохиргоо:

Reference band: B08 эсвэл B04 10 m

Resampling method: Bilinear

Output: 10 m aligned product

---

**7.4 QGIS дээр EPSG:32647 руу reproject хийх**

QGIS:

Raster → Projections → Warp (Reproject)

Тохиргоо:

Target CRS: EPSG:32647

Resampling: Bilinear

Output:

XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_Geology\_RGB\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_EPSG32647\_v01.tif

---

**7.5 Cloud / shadow / snow / water / vegetation mask**

Sentinel дээр дараах mask-ууд үүсгэнэ.

**NDVI**

NDVI \= (B08 \- B04) / (B08 \+ B04)

Vegetation mask:

NDVI \> 0.3

**NDWI**

NDWI \= (B03 \- B08) / (B03 \+ B08)

Water mask:

NDWI \> 0.2

**Shadow / dark pixel mask**

B02 эсвэл B04 маш бага reflectance-тэй pixel

Жишээ threshold:

B04 \< 0.05

Threshold-ийг тухайн raster-ийн DN/reflectance scale-аас хамаарч тохируулна.

Output:

XV023222\_Buduunkhad\_Sentinel2\_NDVI\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_NDWI\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_VegetationMask\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_WaterShadowMask\_EPSG32647\_v01.tif

---

**7.6 Sentinel composite гаргах**

QGIS дээр Build Virtual Raster эсвэл Raster Calculator / Merge ашиглаж composite үүсгэнэ.

**Natural RGB**

R \= B04

G \= B03

B \= B02

Output:

XV023222\_Buduunkhad\_Sentinel2\_NaturalRGB\_EPSG32647\_v01.tif

**Geological SWIR-NIR-Red composite**

R \= B12

G \= B08

B \= B03

Output:

XV023222\_Buduunkhad\_Sentinel2\_Geology\_RGB\_B12\_B08\_B03\_EPSG32647\_v01.tif

**False color vegetation / lithology support**

R \= B08

G \= B04

B \= B03

Output:

XV023222\_Buduunkhad\_Sentinel2\_FalseColor\_B08\_B04\_B03\_EPSG32647\_v01.tif

---

**7.7 Sentinel lithology / alteration index**

№78 файл дээр аль хэдийн lithology index байж болзошгүй тул эхлээд band composition-г шалгана. Таны workflow нэршлээс харахад:

B11/B12

B08/B11

B04/B03

гэсэн band ratio stack байх магадлалтай.

Үүнийг reproject/clip хийгээд support layer гэж тэмдэглэнэ.

Output:

XV023222\_Buduunkhad\_Sentinel2\_LithologyIndex\_B11B12\_B08B11\_B04B03\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_LithologyIndex\_QAQC\_Log.xlsx

---

**7.8 Sentinel final package**

XV023222\_Buduunkhad\_Sentinel2\_NaturalRGB\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_Geology\_RGB\_B12\_B08\_B03\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_LithologyIndex\_B11B12\_B08B11\_B04B03\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_NDVI\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_NDWI\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_VegetationMask\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_Sentinel2\_QAQC\_Log.xlsx

---

**8\. ASTER HDF workflow v5 хийх заавар**

**8.1 ASTER raw HDF-г хадгалах**

№73 raw HDF-г:

02\_ASTER\_Workflow\_v5/01\_Input\_HDF

дотор хадгална.

Raw HDF-г өөрчлөхгүй.

---

**8.2 ASTER band extraction**

ASTER HDF-г ILWIS 3.6.8, QGIS/GDAL, эсвэл SNAP ашиглан нээж боломжтой band-уудыг гаргана.

Гарах band-уудыг дараах байдлаар хадгална:

b1\_project.tif

b2\_project.tif

b3\_project.tif

b4\_project.tif

b5\_project.tif

b6\_project.tif

b7\_project.tif

b8\_project.tif

b9\_project.tif

Output folder:

02\_ASTER\_Workflow\_v5/02\_Band\_Extraction

---

**8.3 ASTER band-уудыг UTM47 / EPSG:32647 болгох**

QGIS:

Raster → Projections → Warp (Reproject)

Target CRS:

EPSG:32647

Output:

b1\_project\_EPSG32647.tif

b2\_project\_EPSG32647.tif

...

b9\_project\_EPSG32647.tif

---

**8.4 ASTER index тооцох**

ASTER workflow v5-ийн зарчим:

1. HDF import

2. Band extraction

3. UTM47 project grid

4. b\*\_project band-аас index тооцох

5. Haze/edge filter-ийг ratio calculation-д ашиглахгүй

6. Raw score, class, binary mask-г тусад нь хадгалах

**Үндсэн index/score layer-үүд**

Таны өмнөх workflow-т ашигласан logic-ийг баримталбал дараах score layer-үүдийг гаргана:

score\_sericite

score\_aloh

score\_clay

score\_argilic

score\_quartz

score\_silicification

score\_silica

score\_iron\_oxide

score\_ferric

score\_chlorite

score\_mgoh

score\_carbonate

score\_carbonate\_swir

score\_structure\_v1

score\_lithology

Эдгээр нь бүгд Float32 raw score raster хэлбэрээр хадгалагдана.

---

**8.5 Porphyry alteration score тооцох**

ASTER final alteration score-г дараах weighted score хэлбэрээр тооцно:

score\_porphyry\_alteration \=

0.12282 \* score\_sericite \+

0.08776 \* score\_aloh \+

0.07022 \* score\_clay \+

0.05265 \* score\_argilic \+

0.05765 \* score\_quartz \+

0.08020 \* score\_silicification \+

0.06013 \* score\_silica \+

0.08270 \* score\_iron\_oxide \+

0.06766 \* score\_ferric \+

0.06013 \* score\_chlorite \+

0.04511 \* score\_mgoh \+

0.03008 \* score\_carbonate \+

0.01503 \* score\_carbonate\_swir \+

0.03760 \* score\_structure\_v1 \+

0.10527 \* score\_lithology

Output:

XV023222\_Buduunkhad\_ASTER\_score\_porphyry\_alteration\_raw\_v01.tif

Data type:

Float32

---

**8.6 ASTER class map гаргах**

Raw score-г 3 ангилал болгоно.

Жишээ:

Class 1 \= Low

Class 2 \= Moderate

Class 3 \= High

Ангиллын threshold-г тухайн raster-ийн histogram/statistics дээр үндэслэнэ.

Жишээ арга:

Low: доод 0–60 percentile

Moderate: 60–85 percentile

High: 85–100 percentile

Output:

XV023222\_Buduunkhad\_ASTER\_porphyry\_potential\_class\_v01.tif

---

**8.7 ASTER binary mask гаргах**

High class буюу class 3-ыг 1, бусдыг 0 болгоно.

QGIS Raster Calculator:

("ASTER\_porphyry\_potential\_class@1" \= 3\) \* 1

Output:

XV023222\_Buduunkhad\_ASTER\_porphyry\_final\_target\_binary\_mask\_v01.tif

Binary mask утга:

0 \= not selected

1 \= ASTER high alteration support

---

**8.8 ASTER QA/QC**

ASTER QA/QC дээр дараахыг заавал шалгана:

HDF import амжилттай эсэх

Band extraction бүрэн эсэх

Band alignment зөв эсэх

Projection EPSG:32647 болсон эсэх

Raw score Float32 хэвээр хадгалагдсан эсэх

Class raster 1/2/3 тусдаа гарсан эсэх

Binary mask 0/1 тусдаа гарсан эсэх

Haze/edge filter ratio calculation-д ороогүй эсэх

Output нь ore proof биш support evidence гэж тэмдэглэгдсэн эсэх

Output:

XV023222\_Buduunkhad\_ASTER\_QAQC\_Log.xlsx

---

**9\. KOMPSAT-2 боловсруулах заавар**

**9.1 KOMPSAT bundle бүрэн эсэхийг шалгах**

KOMPSAT folder дотор PAN, Green, Blue, NIR, Red band тус бүрийн:

.tif

.txt

.rpc

.eph

байгаа эсэхийг шалгана.

QA/QC register-д:

PAN tif/txt/rpc/eph complete?

Green complete?

Blue complete?

NIR complete?

Red complete?

Browse image available?

Thumbnail available?

гэж бүртгэнэ.

---

**9.2 Band identity шалгах**

Файлын нэрээр band identity:

PN00 \= PAN

M1N00G \= Green

M2N00B \= Blue

M3N00N \= NIR

M4N00R \= Red

QA/QC-д band order-г ингэж бүртгэнэ:

Blue \= M2

Green \= M1

Red \= M4

NIR \= M3

PAN \= PN

---

**9.3 KOMPSAT orthorectification**

Хэрэв RPC ашиглан orthorectification хийх боломжтой бол Global Mapper, QGIS/GDAL, эсвэл photogrammetry-capable software ашиглана.

Оруулах input:

PAN tif \+ PAN rpc \+ PAN eph \+ DEM

MS band tif \+ rpc \+ eph \+ DEM

Target CRS:

EPSG:32647

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_Orthorectified\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_KOMPSAT2\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif

---

**9.4 KOMPSAT MS band stack**

QGIS:

Raster → Miscellaneous → Build Virtual Raster

эсвэл GDAL merge stack ашиглана.

Band order:

Band 1 \= Blue

Band 2 \= Green

Band 3 \= Red

Band 4 \= NIR

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_MS\_BandStack\_BGRNIR\_EPSG32647\_v01.tif

---

**9.5 KOMPSAT true color composite**

RGB display:

R \= Red

G \= Green

B \= Blue

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_TrueColor\_RGB\_EPSG32647\_v01.tif

---

**9.6 KOMPSAT false color composite**

False color:

R \= NIR

G \= Red

B \= Green

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_FalseColor\_NIR\_Red\_Green\_EPSG32647\_v01.tif

---

**9.7 KOMPSAT NDVI гаргах**

Formula:

NDVI \= (NIR \- Red) / (NIR \+ Red)

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_EPSG32647\_v01.tif

Use:

vegetation mask

outcrop visibility

drainage/access planning

---

**9.8 KOMPSAT pan-sharpen хийх**

Input:

PAN orthorectified

MS band stack orthorectified

Method:

Brovey / Gram-Schmidt / IHS

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif

Use:

lineament interpretation

outcrop mapping support

access road / track / disturbance mapping

field route planning

---

**9.9 KOMPSAT lineament / outcrop interpretation**

QGIS дээр pan-sharpened image \+ hillshade \+ slope overlay хийнэ.

Digitize layer үүсгэнэ:

lineament\_interpretation\_line

outcrop\_interpretation\_polygon

access\_track\_line

disturbance\_surface\_polygon

Layer fields:

feature\_id

feature\_type

interpretation\_basis

source\_raw\_input\_no

source\_raw\_filename

processing\_phase

confidence

validation\_status

limitation

reviewer

date

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg

---

**9.10 KOMPSAT QA/QC**

Шалгах зүйл:

PAN/MS alignment зөв эсэх

RPC/EPH/TXT хадгалагдсан эсэх

Orthorectified output EPSG:32647 болсон эсэх

Pansharpened image license boundary-тэй давхцаж байгаа эсэх

NDVI range \-1 to \+1 эсэх

Lineament interpretation нь support evidence гэж тэмдэглэгдсэн эсэх

Output:

XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx

---

**10\. Google / high-resolution basemap боловсруулах**

**10.1 №75 WGS84 basemap**

Input:

XV023222\_Buduunkhad\_GoogleMaps\_BasemapImagery\_RGB\_2p4m\_WGS84\_Raw\_v01.tif

QGIS дээр CRS шалгана.

Reproject:

Target CRS: EPSG:32647

Output:

XV023222\_Buduunkhad\_GoogleMaps\_Basemap\_RGB\_2p4m\_EPSG32647\_v01.tif

---

**10.2 №76 EPSG3857 high-resolution basemap**

Input:

XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_EPSG3857\_0p15m\_Raw\_v01.tif

Reproject:

Source CRS: EPSG:3857

Target CRS: EPSG:32647

Clip:

license \+ 500 m эсвэл 1 km buffer

Output:

XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_0p15m\_EPSG32647\_v01.tif

Use:

field access

outcrop visibility

old workings/disturbance

track/road mapping

---

**11\. Бүх output-уудыг EPSG:32647 final export хийх**

Дараах output-ууд бүгд:

07\_Final\_Export\_EPSG32647

folder дотор нэгтгэгдэнэ.

Final output package:

XV023222\_Buduunkhad\_Sentinel2\_Processed\_Products\_EPSG32647\_v01.tif/gpkg

XV023222\_Buduunkhad\_ASTER\_score\_porphyry\_alteration\_raw\_v01.tif

XV023222\_Buduunkhad\_ASTER\_porphyry\_potential\_class\_v01.tif

XV023222\_Buduunkhad\_ASTER\_porphyry\_final\_target\_binary\_mask\_v01.tif

XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_EPSG32647\_v01.tif

XV023222\_Buduunkhad\_KOMPSAT2\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_ALOS\_PALSAR\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg

XV023222\_Buduunkhad\_RemoteSensing\_QAQC\_Report\_v01.docx

---

**12\. Phase 2 QA/QC checklist**

QA/QC register-д дараах checklist-ийг заавал бөглөнө.

| QA/QC item | Acceptance criterion |
| :---- | :---- |
| Raw preservation | Raw file overwrite хийгдээгүй |
| Sidecar completeness | .tfw, .aux.xml, .ovr, .rpc, .eph, .txt parent file-тэй хамт хадгалагдсан |
| CRS control | Final spatial output бүгд EPSG:32647 |
| Sentinel mask | Cloud/shadow/water/vegetation mask үүсгэсэн буюу шаардлагагүй гэж тайлбарласан |
| Sentinel reproject | UTM46N input-ууд EPSG:32647 болсон |
| ASTER raw score | Float32 raw score тусдаа хадгалагдсан |
| ASTER class | 1/2/3 class map тусдаа хадгалагдсан |
| ASTER binary | 0/1 binary mask тусдаа хадгалагдсан |
| KOMPSAT metadata | PAN/MS .txt, .rpc, .eph бүртгэгдсэн |
| KOMPSAT alignment | PAN/MS alignment checked |
| DEM derivatives | Hillshade, slope, aspect, drainage, contour шалгагдсан |
| Support evidence flag | Remote sensing output-ыг ore proof гэж ашиглаагүй |
| Source traceability | Output бүрт source\_raw\_input\_no/source\_raw\_filename хадгалагдсан |

---

**13\. Output бүрт заавал байх metadata fields**

GeoPackage layer, raster index, QA/QC register, report бүрт дараах талбаруудыг хадгална:

source\_raw\_input\_no

source\_raw\_filename

source\_group

processing\_phase

processing\_software

processing\_action

native\_crs

output\_crs

pixel\_size

output\_filename

processing\_version

qaqc\_status

validation\_status

confidence

limitation

reviewer

review\_date

Remote sensing output дээр:

validation\_status \= Support evidence only

limitation \= Not ore proof; requires field/lab validation

---

**14\. Phase 2 completion criteria**

Phase 2 дууссан гэж үзэх нөхцөл:

1. №9–22 DEM/ALOS/ASTERGDEM input бүгд QA/QC хийгдсэн.

2. ALOS/ASTER DEM-ээс hillshade, slope, aspect, contour, drainage, watershed гарсан.

3. №23–46 KOMPSAT PAN/MS bundle бүрэн шалгагдсан.

4. KOMPSAT orthobasemap, NDVI, lineament/outcrop interpretation support гарсан.

5. №73 ASTER HDF-ээс raw score, class, binary mask гарсан.

6. №74–78 Sentinel/basemap raster EPSG:32647 руу reproject/clip хийгдсэн.

7. Sentinel geology composite, lithology index, NDVI/NDWI/masks бэлэн болсон.

8. Бүх final output 07\_Final\_Export\_EPSG32647 folder дотор нэгтгэгдсэн.

9. XV023222\_Buduunkhad\_RemoteSensing\_QAQC\_Report\_v01.docx бэлэн болсон.

10. Phase 3-д handover хийхэд бүх output support evidence гэж тэмдэглэгдсэн.

---

**15\. Phase 3 руу шилжүүлэх handover package**

Phase 2-оос Phase 3 руу дараах package өгнө:

01\_Sentinel2\_Processed\_Products/

02\_ASTER\_Alteration\_Products/

03\_KOMPSAT2\_Orthobasemap\_Lineament/

04\_Terrain\_Derivatives/

05\_Basemap\_Reference/

06\_RemoteSensing\_QAQC/

Phase 3 дээр эдгээрийг дараах байдлаар ашиглана:

| Phase 2 output | Phase 3 use |
| :---- | :---- |
| Sentinel geology RGB | lithology contrast support |
| Sentinel lithology index | alteration/lithology support |
| ASTER porphyry score | alteration support |
| ASTER binary mask | target support, not proof |
| KOMPSAT pansharpened image | outcrop/access/lineament support |
| KOMPSAT NDVI | vegetation/outcrop visibility mask |
| DEM hillshade/slope | structure, drainage, access |
| Drainage/watershed | stream sediment and heavy mineral follow-up |

---

**16\. Хамгийн чухал анхааруулга**

Phase 2-ийн хамгийн том алдаа нь remote sensing output-ыг шууд “орд байна” гэж тайлбарлах явдал. Тиймээс report, map, layer attribute бүр дээр:

Remote sensing derivative \= support evidence only.

Not mineralization proof.

Requires field validation and laboratory confirmation.

гэж заавал бичнэ.

Phase 2-ийн зөв гарц бол “эрдэсжилт батлах” биш, харин:

хаана шалгах вэ,

ямар structure харагдаж байна,

аль хэсэгт alteration support байна,

аль хэсэгт terrain/access тохиромжтой байна,

аль хэсгийг Phase 3–4 дээр илүү нягт overlay хийх вэ

гэсэн шийдвэрт ашиглах support layer бэлтгэх юм.

