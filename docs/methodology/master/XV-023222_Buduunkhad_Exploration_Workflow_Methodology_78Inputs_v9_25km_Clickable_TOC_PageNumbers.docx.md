XV-023222 / L23222 Buduunkhad Exploration Workflow Methodology v8 Phase 3 25 km Buffer and TOC

**78 raw input files \+ QGIS \+ SNAP 13.0.0 \+ ASTER workflow \+ KOMPSAT-2 \+ ALOS-PALSAR \+ DJI Matrice 400 \+ Zenmuse L2/L3/P1 \+ Olympus Vanta M \+ Bruker Titan S1 \+ pXRF \+ target ranking workflow**

| Талбар | Утга |
| :---- | :---- |
| Project area | Buduunkhad / XV-023222 / L23222 |
| Standard CRS | WGS 84 / UTM Zone 47N, EPSG:32647 |
| Document type | Methodology / workflow guide. Бодит боловсруулалтын үр дүн, нөөцийн тооцоо, final target баталгаа биш. |
| Source basis | XV-023222\_Buduunkhad\_Exploration\_Workflow\_Methodology\_78Inputs\_v1.docx дахь 78 raw input file register, CRS, project identity, equipment/software logic. |
| Style reference | BuduunKhad\_Namalzakh\_29RawInputs\_SNAP\_ASTER\_Drone\_XRF\_Methodology.docx-ийн phase format, folder tree, QA/QC, input/output template-ийн бичлэгийн хэв маяг. 29 input file list-ийг хуулж оруулаагүй. |
| Main principle | Raw data-г өөрчлөхгүй хадгалж, зөвхөн processing copy дээр ажиллана; sidecar metadata файлуудыг parent raster/image-тэй хамт хадгална. |
| v3 нэмэлт | Historical Scanned Maps QGIS Vectorization Workflow v02 Detailed аргачлалыг Phase 1-ийн дэд аргачлал / Appendix E хэлбэрээр нэмэв. |
| v4 нэмэлт | Preliminary Deposit Model Preparation Methodology-г Appendix биш, үндсэн workflow-ийн 03\_Phase\_3 дотор 03A дэд workflow болгон нэгтгэв; Phase 4 preliminary prospect ranking болон Phase 10 final target ranking руу handover холбоос нэмэв. |
| v5 нэмэлт | Phase бүрийн Input files хэсгийг ерөнхий evidence group-ээр биш, яг ашиглах raw input file № болон filename-аар заасан. Мөн 1A Explicit Input File Assignment Matrix нэмэж, raw input \-\> primary phase \-\> methodology action холбоосыг бүрэн тодорхойлов. |

**Анхааруулга:** Satellite, ASTER, KOMPSAT-2, DEM, Drone/LiDAR болон pXRF output нь хүдэржилтийн баталгаа биш. Эдгээр нь target generation, field validation, sampling prioritization-д ашиглах support evidence юм. Эцсийн confidence нь хээрийн шалгалт, лабораторийн шинжилгээ, structural/geological evidence, шаардлагатай бол trench/geophysics/scout drilling-аар баталгаажна.

# **Table of Contents / Гарчгийн жагсаалт**

*Click a section title to jump directly to that section. Page numbers are based on the rendered document layout.*

**Section / Гарчиг**	**Page / Хуудас**

[0\. Methodology scope and governing principles](#bookmark=id.wcxrij336ktm)	7  
[1\. Enhanced 78 raw input file register](#bookmark=id.muxup4gr7bkn)	7  
[1A. Explicit raw input assignment by workflow phase](#bookmark=id.qoig3fpq7lrc)	13  
[1A.1 Phase-level input control summary](#bookmark=id.306n2uzgk37j)	13  
[1A.2 File-by-file input assignment matrix](#bookmark=id.sirn6loo6al9)	14  
[1A.3 Mandatory rule for every phase](#bookmark=id.j4rukgtn4sbi)	17  
[1B. Phase-wise exact raw input file processing and output matrix — v6 update](#bookmark=id.2o2wmtb2jeot)	18  
[1B.1 Phase тус бүрийн raw input file assignment summary](#bookmark=id.2x4fk5wm44ui)	18  
[1B.2 Detailed 78 raw input file → software → processing → output matrix](#bookmark=id.dptbs5wld91u)	18  
[Phase 1 inputs: boundary, full metadata audit and Master GIS setup](#bookmark=id.sbfk4hyfctfa)	18  
[Phase 2 inputs: DEM, ALOS-PALSAR, KOMPSAT-2, ASTER, Sentinel and basemap processing](#bookmark=id.4k0i21nwg5yu)	19  
[Phase 3 / 03A inputs: tectonic, geology, mineral occurrence, prospectivity and metallogenic synthesis](#bookmark=id.dusk2kb3i3hd)	25  
[Phase 6 and Phase 8 field/historical geochemistry inputs](#bookmark=id.cw9co5951h55)	28  
[1B.3 Required source-traceability fields for every output](#bookmark=id.mqeufafzk1c7)	29  
[v6 implementation note](#bookmark=id.lfc0n82ws16y)	30  
[2\. Integrated 00-99 phase workflow](#bookmark=id.lhbhtmah54la)	32  
[00\. Raw Files Archive](#bookmark=id.b3qet34s5i0q)	32  
[Processing folder structure](#bookmark=id.vmwhe8892rqe)	32  
[Step-by-step methodology](#bookmark=id.hulsdvmpepbu)	33  
[QA/QC check](#bookmark=id.u117qgvwyk19)	33  
[Expected outputs](#bookmark=id.sbgt4laqqswm)	33  
[Decision gate / next phase condition](#bookmark=id.81x9mf1dgmnp)	33  
[01\. Phase 1 — Data Audit and Master GIS Setup](#bookmark=id.zbn05geucq66)	33  
[Processing folder structure](#bookmark=id.qzedaor2zt1e)	33  
[Step-by-step methodology](#bookmark=id.g970c5yicdb3)	33  
[QA/QC check](#bookmark=id.9uusjg6ujm1)	33  
[Expected outputs](#bookmark=id.ms81mbc5k4lu)	33  
[Decision gate / next phase condition](#bookmark=id.59uw2x2behjc)	33  
[02\. Phase 2 — Remote Sensing Preprocessing](#bookmark=id.nzncxam0i4dw)	35  
[Processing folder structure](#bookmark=id.kh1dmou7j421)	35  
[Step-by-step methodology](#bookmark=id.7c1irxp6id7y)	35  
[QA/QC check](#bookmark=id.pwazzmpg1web)	35  
[Expected outputs](#bookmark=id.mof8yhbrq3yt)	35  
[Decision gate / next phase condition](#bookmark=id.6aclkssia55t)	36  
[03\. Phase 3 — Geological, Metallogenic and CMCS Synthesis](#bookmark=id.hmntwovtrzus)	36  
[Purpose and scope](#bookmark=id.so2cdv6cll2m)	36  
[03.1 Phase 3 input control](#bookmark=id.vk3xva64z6ew)	36  
[03.2 Working folder structure](#bookmark=id.veg7yr3rcxjc)	37  
[03.3 Pre-start readiness check](#bookmark=id.xngneethavuy)	38  
[03.4 Step-by-step methodology](#bookmark=id.v2csbkr0bh07)	38  
[Step 7 — CMCS/MRPAM 5 km / 10 km / 20 km / 25 km contextual check](#bookmark=id.oave95bdxnqk)	39  
[Step 7A — 25 km near-occurrence coverage buffer for all nearby mineral occurrences](#bookmark=id.6ph9a2r82vpb)	40  
[QGIS method for 25 km buffer creation](#bookmark=id.wdoo7ppocg3q)	40  
[Recommended buffer interpretation hierarchy](#bookmark=id.efq98em6duv)	40  
[Additional expected outputs from Step 7A](#bookmark=id.r1r5oxlka3vg)	40  
[Step 8 — Integrate all Phase 3 evidence into one GeoPackage](#bookmark=id.4s6t6zdx9uwf)	40  
[03.5 Expected output package](#bookmark=id.u5mqi9285rlb)	41  
[03.6 Mandatory GeoPackage layer schema](#bookmark=id.d8j1pm6geoek)	42  
[03.7 QA/QC checklist](#bookmark=id.bhtpmoxqmu8p)	42  
[03.8 Decision gate and handover to Phase 4 / Phase 10](#bookmark=id.5adtipbm2037)	43  
[03.9 Phase 3 completion criteria](#bookmark=id.vfoi8li6q6ny)	43  
[03A. Preliminary Deposit Model Preparation — Phase 3 доторх дэд workflow](#bookmark=id.8fk9otmy0n7d)	44  
[03A.1 Зорилго ба гарах баримт бичиг](#bookmark=id.c4qe4c5roded)	44  
[03A.2 Ашиглах input evidence](#bookmark=id.y840etixt72v)	44  
[03A.3 Ажлын үндсэн дараалал](#bookmark=id.fks25munda5u)	45  
[Алхам 1 — Evidence layer-үүдийг Master GIS дээр нэгтгэх](#bookmark=id.gg3p0xcc7fm9)	45  
[Алхам 2 — Historical map-уудаас ордын төрлийн evidence ялгах](#bookmark=id.hpy7t1l2kq08)	45  
[Алхам 3 — Deposit model candidate-уудыг тодорхойлох](#bookmark=id.9mk0ba9jptq8)	45  
[Алхам 4 — Supporting evidence / missing evidence / validation work хүснэгт гаргах](#bookmark=id.v6kn5ctafj8z)	45  
[Алхам 5 — Evidence weight ашиглаж preliminary ranking хийх](#bookmark=id.s28rfhd2evh0)	45  
[03A.4 Deposit model candidate screening](#bookmark=id.cufp0fym1ui)	45  
[03A.5 Evidence weight ба preliminary ranking](#bookmark=id.8wmqblgpmpz)	46  
[03A.6 XV-023222\_Buduunkhad\_Preliminary\_Deposit\_Model.docx санал болгох бүтэц](#bookmark=id.enrk68ylm78f)	47  
[03A.7 Богино ажлын checklist](#bookmark=id.st7utkvt7dan)	47  
[03A.8 Phase 3 QA/QC notes for deposit model preparation](#bookmark=id.lhq6u6g0dtsn)	47  
[03A.9 Handover from Phase 3 to Phase 4 and Phase 10](#bookmark=id.ei36kqs2nx16)	47  
[04\. Phase 4 — Preliminary Prospect Delineation and Ranking](#bookmark=id.o1lxxz6eq3ed)	48  
[Processing folder structure](#bookmark=id.lnvu08csfqgd)	48  
[Step-by-step methodology](#bookmark=id.dj4i89r8ypw)	48  
[QA/QC check](#bookmark=id.8gcqucz9958f)	48  
[Expected outputs](#bookmark=id.palz7shzt2rc)	49  
[Decision gate / next phase condition](#bookmark=id.h5spkppthbgw)	49  
[05\. Phase 5 — DJI Matrice 400 Drone LiDAR Photogrammetry Survey](#bookmark=id.5ihnrhr7kl7t)	49  
[Processing folder structure](#bookmark=id.t74wfvmp1d3y)	49  
[Step-by-step methodology](#bookmark=id.avqfnbygeu2j)	49  
[QA/QC check](#bookmark=id.lhj0p853zlo)	50  
[Expected outputs](#bookmark=id.lb9bmcmfizhw)	50  
[Decision gate / next phase condition](#bookmark=id.s7302v8rdyso)	50  
[06\. Phase 6 — Recon Mapping and Portable XRF Field Screening](#bookmark=id.vu5dwpofnxn0)	50  
[Processing folder structure](#bookmark=id.17uh65f54fz)	50  
[Step-by-step methodology](#bookmark=id.d6kqzzzf9t1n)	51  
[QA/QC check](#bookmark=id.ohn0ggsxk1m5)	51  
[Expected outputs](#bookmark=id.hfma6981e1c1)	51  
[Decision gate / next phase condition](#bookmark=id.6o31klypkh91)	51  
[07\. Phase 7 — Rock Chip, Channel and Verification Sampling](#bookmark=id.u9w5bxw7tcpk)	51  
[Processing folder structure](#bookmark=id.s14xazguf30q)	51  
[Step-by-step methodology](#bookmark=id.bcz2th76dbyl)	51  
[QA/QC check](#bookmark=id.7hnf214w9foq)	51  
[Expected outputs](#bookmark=id.74iq4l9kazar)	51  
[Decision gate / next phase condition](#bookmark=id.u5xhur2ru02n)	51  
[08\. Phase 8 — Orientation Soil, Stream Sediment and Heavy Mineral Check](#bookmark=id.60y10uy0dtv2)	52  
[Processing folder structure](#bookmark=id.3nyzgz3hjdst)	53  
[Step-by-step methodology](#bookmark=id.9n3tqfmixv2q)	53  
[QA/QC check](#bookmark=id.lz5r3chqn9v5)	53  
[Expected outputs](#bookmark=id.lm1vo1gw8mlh)	53  
[Decision gate / next phase condition](#bookmark=id.r6sy5of9nzh8)	53  
[09\. Phase 9 — Systematic Soil Grid and Laboratory QA/QC](#bookmark=id.97t4l8so3wk2)	53  
[Processing folder structure](#bookmark=id.a5dpp38ep5vh)	53  
[Step-by-step methodology](#bookmark=id.jx8dkvtfn4n5)	53  
[QA/QC check](#bookmark=id.ueaxu4x1388e)	53  
[Expected outputs](#bookmark=id.4qubftlavafs)	53  
[Decision gate / next phase condition](#bookmark=id.8sxta15ulor9)	53  
[10\. Phase 10 — Integrated Interpretation and Final Target Ranking](#bookmark=id.xaqm80eziw2r)	55  
[Processing folder structure](#bookmark=id.vfwwpqio1w0n)	55  
[Step-by-step methodology](#bookmark=id.744khtf8xwl4)	55  
[QA/QC check](#bookmark=id.u85in4yqgtln)	55  
[Expected outputs](#bookmark=id.9ul39qrpg5am)	55  
[Decision gate / next phase condition](#bookmark=id.t8vwfzgze9r8)	56  
[11\. Phase 11 — Follow-up Trench, Geophysics and Scout Drill Planning](#bookmark=id.ddvnvyuhdtn0)	56  
[Processing folder structure](#bookmark=id.z7wldtfcoca3)	56  
[Step-by-step methodology](#bookmark=id.ln95j84nhyt3)	56  
[QA/QC check](#bookmark=id.q1oyqxveys1c)	56  
[Expected outputs](#bookmark=id.7xiq9dyqooh)	57  
[Decision gate / next phase condition](#bookmark=id.ps7neykkij78)	57  
[99\. Final Deliverables](#bookmark=id.z87jdtffjgnw)	57  
[Processing folder structure](#bookmark=id.79g2amx4hcqh)	57  
[Step-by-step methodology](#bookmark=id.ahrx4oki2mgr)	57  
[QA/QC check](#bookmark=id.a0r8fuklkqta)	57  
[Expected outputs](#bookmark=id.fdvqqdo18t0n)	57  
[Decision gate / next phase condition](#bookmark=id.lgi2hrcf2hse)	57  
[3\. Remote sensing special subworkflows](#bookmark=id.p8ux1zzhz2zq)	58  
[4\. Deposit model candidate screening table](#bookmark=id.47o34afplp0s)	58  
[5\. Preliminary and final target ranking matrix](#bookmark=id.5im8q76i6za2)	59  
[6\. Portable XRF QA/QC and register schema](#bookmark=id.etbl4v68d65s)	59  
[7\. Sampling methodology and QA/QC insertion](#bookmark=id.wbe02pol5qsk)	60  
[8\. Final target description sheet schema](#bookmark=id.wt60roi7m1d9)	60  
[Appendix E — Historical Scanned Maps QGIS Vectorization Workflow v02 Detailed](#bookmark=id.ecin9ytyu7x8)	61  
[Агуулгын товч жагсаалт](#bookmark=id.6sq0hwt1co60)	61  
[1\. Зорилго ба хамрах хүрээ](#bookmark=id.1kgi7gptgaol)	61  
[2\. Reference document-тэй нийцүүлэх зарчим](#bookmark=id.ox5tjt8sd9sc)	61  
[3\. Ажил гүйцэтгэх ерөнхий sequence](#bookmark=id.9cy8sn26wdsz)	61  
[4\. Input scanned map inventory](#bookmark=id.ulye8fi7pn3f)	61  
[4.1 Inventory-д заавал нэмэх metadata баганууд](#bookmark=id.i8976bw9zkdb)	67  
[5\. Map-to-legend linkage ба symbol dictionary](#bookmark=id.bzdybj68iisi)	67  
[5.1 Symbol dictionary үүсгэх алхам](#bookmark=id.6j66rmwffhvo)	68  
[6\. Folder structure ба file governance](#bookmark=id.god6nimb82po)	68  
[7\. QGIS project setup](#bookmark=id.hvzdfeir9ghb)	69  
[8\. Georeferencing workflow](#bookmark=id.a844i9vg9950)	70  
[8.1 GCP сонгох эх сурвалжийн эрэмбэ](#bookmark=id.697c2riuq6ys)	70  
[8.2 QGIS Georeferencer дээр хийх алхам](#bookmark=id.jfd7v5k9ts55)	71  
[8.3 DMS coordinate-г decimal degree болгох дүрэм](#bookmark=id.vpju7ai97csh)	71  
[9\. Raster QA/QC ба confidence](#bookmark=id.ad9gnk3nrxz6)	72  
[9.1 Georeferenced raster output naming](#bookmark=id.vdl75890y142)	72  
[10\. Vectorization strategy by map type](#bookmark=id.ogq9ycwjfi2v)	73  
[11\. Master GeoPackage design](#bookmark=id.chtvmt3muh3x)	74  
[11.1 GeoPackage үүсгэх QGIS алхам](#bookmark=id.8nlrv9z7g2vk)	74  
[12\. Field schema ба domain/lookup](#bookmark=id.z0g1k26pslm9)	75  
[12.1 Common source traceability fields](#bookmark=id.2r3r78i9ab9z)	75  
[12.2 Standard domain values](#bookmark=id.pukgphp2kiph)	75  
[13\. Layer-specific schema](#bookmark=id.m7dbkktgdafx)	76  
[13.x Layer: geology\_units\_polygons](#bookmark=id.mutng4pcc10t)	76  
[13.x Layer: structures\_faults\_lines](#bookmark=id.ywy9yeku56ia)	76  
[13.x Layer: mineral\_occurrences\_points](#bookmark=id.1dpvcv3b1qkq)	76  
[13.x Layer: heavy\_mineral\_anomaly\_polygons](#bookmark=id.50niu4weh0rf)	77  
[13.x Layer: stream\_sediment\_anomaly\_polygons](#bookmark=id.xbuommed8enu)	77  
[13.x Layer: prospectivity\_target\_zones\_polygons](#bookmark=id.i0puw1kf3d15)	77  
[13.x Layer: source\_material\_observation\_points](#bookmark=id.njc6lqjerpal)	78  
[13.x Layer: source\_material\_route\_lines](#bookmark=id.g2cco3x4hl7x)	78  
[13.x Layer: metallogenic\_zones\_polygons](#bookmark=id.iexxygo4i9ai)	78  
[14\. QGIS digitizing SOP](#bookmark=id.38mfcgig2r5l)	78  
[15\. Layer бүрийн нарийвчилсан SOP](#bookmark=id.jliiycbvd2my)	79  
[15.1 Geological unit polygons](#bookmark=id.5aceq4ro7gj2)	79  
[15.2 Structures/faults/lineaments](#bookmark=id.w3i1wr7rw0r5)	79  
[15.3 Mineral occurrence points](#bookmark=id.jpls5gczrd9h)	79  
[15.4 Heavy mineral layers](#bookmark=id.jrjoavubnl1r)	79  
[15.5 Stream sediment polyelement layers](#bookmark=id.cvrs6b34bytw)	80  
[15.6 Source materials layers](#bookmark=id.5og92x9vlv63)	80  
[15.7 Prospectivity target zones](#bookmark=id.okeht6pwppam)	80  
[15.8 Metallogenic context](#bookmark=id.6pc0toik7rh9)	80  
[16\. Excel register workbook](#bookmark=id.nexl66r62swk)	80  
[16.1 GCP table sheet schema](#bookmark=id.vv38q5h0uunt)	81  
[17\. QA/QC checklist](#bookmark=id.o7xqfs6jp1qg)	81  
[18\. Confidence ranking logic](#bookmark=id.eh552im664tf)	82  
[19\. Data gap register](#bookmark=id.3qm2vfefqfdx)	82  
[20\. Cross-map integration](#bookmark=id.sg6gblatffo2)	84  
[21\. Handover package ба acceptance criteria](#bookmark=id.u7osc071u53s)	84  
[22\. Final workflow diagram](#bookmark=id.97rb272hp0rj)	85  
[23\. Appendices](#bookmark=id.nbrqramdv63s)	85  
[Appendix A \- Feature ID naming standard](#bookmark=id.5eiwk7kekccx)	85  
[Appendix B \- QGIS Field Calculator expressions](#bookmark=id.j06cf7rfr30d)	86  
[Appendix C \- QField package preparation note](#bookmark=id.g553pd4i1m2s)	86  
[Appendix D \- Чанарын хяналтын анхааруулга](#bookmark=id.9aui6onfnzf1)	86  
[Critical QA/QC Notes](#bookmark=id.1i068qvosj1t)	86  
[Methodology Limitation](#bookmark=id.2y6nqgf0o0by)	87

# **0\. Methodology scope and governing principles**

* Энэхүү v2 Enhanced аргачлал нь Бүдүүн хад / XV-023222 / L23222 хайгуулын талбайн 78 raw input файлыг professional exploration workflow болгон үе шаттай хэрэгжүүлэх заавар юм.  
* Энэ баримт бичиг нь бодит processing result, нөөц/баялгийн тооцоо, эсвэл эцсийн өрөмдлөгийн баталсан target биш. Зөвхөн өгөгдөл боловсруулах, шалгах, талбайд баталгаажуулах, дараагийн шийдвэр гаргах аргачлал юм.  
* 78 input file register-ийг хадгалж, файл бүрийг spatial status, limitation, processing action, expected output-тэй холбож шинэчилсэн.  
* 29RawInputs аргачлалын input list-ийг ашиглаагүй; зөвхөн формат, QA/QC-ийн бичлэгийн түвшин, folder/output template-ийн бүтэц авсан.

| Core principle | Implementation rule |
| :---- | :---- |
| Raw preservation | 00\_Raw\_Files\_Archive дотор original file read-only хадгална. Rename хийх шаардлагатай бол standardized name register-д бичиж, raw file-г overwrite хийхгүй. |
| Processing copy | Бүх боловсруулалтыг 01-11 phase-ийн Input/Working/Processing хавтасны copy дээр хийнэ. |
| CRS control | Final deliverables EPSG:32647; native CRS/source CRS-г metadata-д хадгална. |
| Evidence hierarchy | Remote sensing/pXRF/drone \= support evidence; lab assay \+ field geology \+ structural control \= decision evidence. |
| Decision gates | Phase бүрийн төгсгөлд QA/QC болон go/no-go шалгуураар дараагийн шат руу шилжинэ. |

# **1\. Enhanced 78 raw input file register**

Доорх хүснэгт нь v1 баримт бичигт байгаа 78 input file-ийн жагсаалтыг хадгалж, хэрэгжүүлэхэд шаардлагатай spatial status, workflow phase, limitation, required processing action, expected output багануудыг нэмсэн register юм. Sidecar файлууд (.tfw, .aux.xml, .ovr, .rpc, .eph, .txt metadata) нь parent raster/image-ээс салгахгүй хадгалагдана.

| № | Evidence group | Raw input filename | File type | Spatial status / CRS status | Exploration use | Workflow phase | Confidence / limitation | Required processing action | Expected output |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | 01\_Tectonic\_Terrane\_KMZ | Geological and Tectonic Characteristics of the Lake Terrane, Mongolia.png | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Англи эх текст: Lake Terrane-ийн геологи, тектоникийн шинж | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 2 | 01\_Tectonic\_Terrane\_KMZ | Mongolia\_Tectonic\_Terrane\_Map\_Project\_Area\_Lake\_Island\_Arc\_Terrane.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Монголын террейний зураг: төслийн талбай Lake island arc terrane-тэй давхцах байдал | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 3 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Central\_Mongolian\_Massif\_and\_Daagandel\_Tectonic\_Zone\_Page11.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | МУГЗ-500 тайлбар, хуудас 11: Даагандэлийн бүс ба Төв Монголын массив | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 4 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part1\_Page08.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | МУГЗ-500 тайлбар, хуудас 8: Бодонч-Цээлийн бүс, Нуурын Атриат мегабүс | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 5 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part2\_Page09.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | МУГЗ-500 тайлбар, хуудас 9: Хурайн, Баатархайрханы, Улааншандын бүс | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 6 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part3\_Page10.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | МУГЗ-500 тайлбар, хуудас 10: Ханхөхийн ба Хантайширийн бүс | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 7 | 01\_Tectonic\_Terrane\_KMZ | Regional\_Tectonic\_Subdivision\_Map\_of\_Mongolia\_Tumurtogoo\_2017\_Buduunkhad\_Project\_in\_Ulaanshand\_Zone.jpg | Зураг/скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Монголын тектоник дүүрэгчлэлийн зураг: Бүдүүн хад төслийн талбай Улааншандын бүсэд | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Master inventory and confidence ranking entry |
| 8 | 01\_Tectonic\_Terrane\_KMZ | MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz | KMZ / KML polygon | Spatial polygon/vector; WGS84 байх магадлалтай. QGIS дээр EPSG:4326 \-\> EPSG:32647 хөрвүүлж баталгаажуулна. | L23222 / Buduunhhad тусгай зөвшөөрлийн хил, WGS84 координатын олон өнцөгт | 01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup | Medium/High after CRS, metadata, coordinate and content QA/QC. | Extract coordinates/attributes, clean register, link with GIS layers. | license\_boundary layer in Master\_GIS\_Database.gpkg |
| 9 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_DEM\_1arcsec\_WGS84\_v01\_raw.tif | Үндсэн raster өгөгдөл | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | Үндсэн raster өгөгдөл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 10 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_NumObservations\_1arcsec\_WGS84\_v01\_raw.tif | Үндсэн raster өгөгдөл | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | Үндсэн raster өгөгдөл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 11 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tfw | World file: pixel хэмжээ, байрлал, north-up georeference | Raster sidecar world file; parent raster-тай хамт хадгална, дангаар spatial layer биш. | World file: pixel хэмжээ, байрлал, north-up georeference | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 12 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif | Үндсэн raster өгөгдөл | GeoTIFF/raster; UTM47N/EPSG:32647 гэж нэрэнд дурдсан боловч CRS, pixel size, extent, NoData-г шалгана. | Үндсэн raster өгөгдөл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 13 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.aux.xml | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 14 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.ovr | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 15 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tfw | World file: pixel хэмжээ, байрлал, north-up georeference | Raster sidecar world file; parent raster-тай хамт хадгална, дангаар spatial layer биш. | World file: pixel хэмжээ, байрлал, north-up georeference | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 16 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif | Үндсэн raster өгөгдөл | GeoTIFF/raster; UTM47N/EPSG:32647 гэж нэрэнд дурдсан боловч CRS, pixel size, extent, NoData-г шалгана. | Үндсэн raster өгөгдөл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 17 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 18 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 19 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tfw | World file: pixel хэмжээ, байрлал, north-up georeference | Raster sidecar world file; parent raster-тай хамт хадгална, дангаар spatial layer биш. | World file: pixel хэмжээ, байрлал, north-up georeference | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 20 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif | Үндсэн raster өгөгдөл | GeoTIFF/raster; UTM47N/EPSG:32647 гэж нэрэнд дурдсан боловч CRS, pixel size, extent, NoData-г шалгана. | Үндсэн raster өгөгдөл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 21 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Auxiliary metadata: histogram/statistics ба GIS sidecar мэдээлэл | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 22 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | GIS sidecar/overview metadata; parent raster-ийн statistics, pyramid, display support. Parent file-тай хамт хадгална. | Overview/pyramid: хурдан харуулахад ашиглагдах багасгасан raster | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | DEM QC, projection check, hillshade/slope/aspect/drainage/terrain derivative. | Terrain derivatives: hillshade, slope, drainage, access/safety layers |
| 23 | 03\_KOMPSAT2\_MSC\_L1G | KOMPSAT EULA Form\_3.1.pdf | Лицензийн нөхцөл / End User License Agreement | Text/table scanned or office document; coordinate extraction, table cleaning, source confidence log шаардлагатай. | Data provenance, license compliance, тайлангийн хавсралт, хөрөнгө оруулагч/зөвлөх/төрийн байгууллагад эх үүсвэр тайлбарлахад хадгална. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Needs verification. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 24 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.tif | Panchromatic буюу PAN band raster зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Суурь зураг, lineament interpretation, зам/шурф/ухаш/эвдрэл/ил гарш ялгах, field route planning, pan-sharpening хийхэд хамгийн чухал үндсэн raster файл. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 25 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.txt | PAN metadata text file | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Тайлангийн Data Source хэсэг, GIS projection/GSD шалгалт, raw data register, QA/QC verification-д ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 26 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.rpc | PAN RPC файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Orthorectification, DEM ашигласан terrain correction, PAN 1 m зургийг газрын бодит байрлалд нарийвчлалтай тохируулахад ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 27 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.eph | PAN ephemeris/orbit файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Геометр боловсруулалтын туслах файл; энгийн GIS дээр шууд нээх шаардлагагүй боловч raw bundle-д хадгална. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 28 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.tif | Multispectral Green band raster | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | True color composite-ийн Green component, Red/Blue/NIR band-уудтай хамт RGB/false color composite, гадаргын өнгөний ялгаа, ус/ургамал/ил гаршийн ялгаралд ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 29 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.txt | Green band metadata | Spatial/metadata status тодруулах шаардлагатай; Data Audit phase-д шалгана. | Band stacking хийхэд band order шалгах, тайлангийн metadata, QA/QC register-д ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 30 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.rpc | Green band RPC файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Green band orthorectification, бусад MS band болон PAN band-тай spatial alignment хийхэд ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 31 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.eph | Green band ephemeris/orbit файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | RPC-based геометр засвар, processing audit-д хэрэгтэй; tif/txt/rpc/eph дөрвийг хамтад хадгална. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 32 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.tif | Multispectral Blue band raster | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | True color composite-ийн Blue component, ус/сүүдэр/atmospheric haze/цайвар гадаргын ялгаа, ил гарш ба хөрсний өнгөний ялгааг бусад band-тай харьцуулан тайлна. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 33 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.txt | Blue band metadata | Spatial/metadata status тодруулах шаардлагатай; Data Audit phase-д шалгана. | Blue band source verification, band stacking, тайлангийн хавсралт, data register-д ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 34 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.rpc | Blue band RPC файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Blue band orthorectification, DEM-тэй relief correction, band-to-band alignment хийхэд ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 35 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.eph | Blue band ephemeris/orbit файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Advanced geometric processing болон audit trail-д хадгална; шууд зураглал хийх файл биш. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 36 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.tif | Multispectral NIR band raster | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | False color composite, vegetation mask, Red band-тай NDVI, ил гарш/ургамлаар хучигдсан хэсэг, drainage pattern, аллювийн ялгаа харахад ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 37 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.txt | NIR band metadata | Spatial/metadata status тодруулах шаардлагатай; Data Audit phase-д шалгана. | NIR band-ийг зөв таних, NDVI/false color/vegetation mask workflow-д source verification хийхэд ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 38 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.rpc | NIR band RPC файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | NIR band orthorectification, бусад band-уудтай давхцуулах, pan-sharpening өмнөх geometry consistency шалгахад хэрэглэнэ. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 39 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.eph | NIR band ephemeris/orbit файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Advanced geometric processing, audit trail-д хадгална; шууд interpretation хийх файл биш. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 40 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.tif | Multispectral Red band raster | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | True color composite-ийн Red component, NIR-тэй NDVI, хөрс/ил гарш/ferric эсвэл iron-stained гадаргын өнгөний ялгааг ажиглахад ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 41 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.txt | Red band metadata | Spatial/metadata status тодруулах шаардлагатай; Data Audit phase-д шалгана. | Red band source verification, NDVI/true color/false color composite хийхэд band identity баталгаажуулах, QA/QC register-д ашиглана. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 42 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.rpc | Red band RPC файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Red band orthorectification, NIR/Green/Blue/PAN band-уудтай spatial alignment, DEM ашигласан terrain correction-д хэрэгтэй. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 43 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.eph | Red band ephemeris/orbit файл | Sensor/geometric/metadata sidecar; KOMPSAT PAN/MS orthorectification ба audit-д parent raster-тай хамт хадгална. | Геометр боловсруулалтын туслах өгөгдөл; raw data бүртгэлд хадгална. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Support file; parent data-гүй дангаар ашиглахгүй. Parent raster/image-тэй хамт хадгалах бол High support value. | KOMPSAT bundle-ийн parent PAN/MS file-тэй хамт archive; metadata/RPC audit-д холбох. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 44 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jpg | Browse image / preview зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Scene coverage зөв эсэхийг хурдан шалгах, data register/catalog thumbnail, тайлангийн internal preview-д ашиглана. Analysis хийх үндсэн зураг биш. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 45 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jgw | Browse image world file | Raster sidecar world file; parent raster-тай хамт хадгална, дангаар spatial layer биш. | br.jpg-г ArcGIS/QGIS дээр ойролцоогоор зөв байрлалтай нээх, lightweight preview overlay хийхэд ашиглана. Дангаараа зураг биш. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Needs verification. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 46 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_tn.jpg | Thumbnail image | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Data inventory, thumbnail preview, тайлангийн хавсралтад ашиглаж болно. Geospatial analysis, pixel value analysis хийхэд ашиглахгүй. | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | PAN/MS import, band identity check, RPC alignment, orthorectification, pan-sharpen/visual products. | KOMPSAT orthobasemap / NDVI / lineament-outcrop interpretation support |
| 47 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200000\_v01\_raw-scan.jpg | Зураг / шлихийн сорьцлолтын үр дүн | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Шлихийн сорьц, ёроолын сорьц, ашигт малтмалын/индикатор минералын тархалтын контур, элемент-минералын тэмдэглэгээ. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 48 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | Таних тэмдэг / шлихийн зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Шлих, ёроолын сорьцын тэмдэг, минералуудын нэршил, агуулгын ангилал, контурын тайлбар. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 49 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | Таних тэмдэг / ёроолын сорьц | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Ёроолын сорьцын агуулга, сарнилын урсгал, сав газрын контур, дээжлэлт хийсэн судлаачдын жагсаалт. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 50 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Polyelement\_1-200000\_v01\_raw-scan.jpg | Зураг / ёроолын сорьцын полиметалл үр дүн | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Cu, Pb, Zn, Ag, As, Bi, W, Sn, Mo, Mn, Ba, F зэрэг олон элементийн сарнилын хүрээ ба урсгалын зураглал. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 51 | 04\_HeavyMineral\_StreamSediment\_Field | 2011\_MN\_Namalzakh\_L47-74-A\_FieldRouteNotebook\_Routes14-15\_Obs1076-1090\_1-50000\_v01\_raw-scan.pdf | PDF / хээрийн маршрутын дэвтэр | Text/table scanned or office document; coordinate extraction, table cleaning, source confidence log шаардлагатай. | Маршрут 14, 15; ажиглалтын цэг 1076-1090; гар зураг, координат, чулуулгийн гарш, судал, структурын тэмдэглэл. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 52 | 04\_HeavyMineral\_StreamSediment\_Field | XV023222\_Buduunkhad\_Report7255\_FieldObservation\_StationDescription\_Table\_WGS84\_LegacyRaw\_v01.pdf | PDF / ажиглалтын цэгийн хүснэгт | Text/table scanned or office document; coordinate extraction, table cleaning, source confidence log шаардлагатай. | Ажиглалтын цэгүүдийн координат, чулуулаг, структур, эрдэсжилтийн товч тайлбар. | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | Needs verification. | Georeference/digitize anomaly contours, drainage catchment analysis, field follow-up planning. | stream\_sediment\_anomaly and heavy\_mineral\_anomaly GIS layers; follow-up plan |
| 53 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_1-200000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Региональ геологийн суурь зураг | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 54 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_Legend\_1-200000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Региональ геологийн зурагт ашигласан стратиграфи, интрузив, структур, литологийн тайлбар | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 55 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Нарийвчилсан геологи, литологи, хагарал, зүсэлт | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 56 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_Legend\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Нарийвчилсан стратиграфи, интрузив, судал, хувирлын тэмдэглэгээ | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 57 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_1-200000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Региональ ашигт малтмалын илрэл, геохимийн гажил, хүдрийн талбай | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 58 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_Legend\_1-200000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Ашигт малтмал, элемент, илрэл, гажлын тэмдэглэгээ | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 59 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralDistributionPatternMap\_1-100000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Металлогенийн бүс, хүдрийн дүүрэг, зангилаа, талбайн харилцан байрлал | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 60 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralOccurrenceMap\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Au-Cu, Cu, Mo, As, Zn зэрэг илрэл ба геологийн суурьтай давхцуулсан зураг | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 61 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MetallogenicSchemeAndMetallogenogram\_1-400000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Хүдрийн формац, нас, металлогенийн бүс ба элементүүдийн холбоо | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 62 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessment\_ReportExcerpt\_B3-TolKhar\_v01\_raw-photo.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Б-2, Б-3, Б-4 талбайн тайлбар, талбайн хэмжээ, илрэл, хэтийн төлөв | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 63 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessmentMap\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Б-3 Толь хяр, Г-1 зэрэг хэтийн төлөвтэй хэсгийг ялгасан зураг | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 64 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Маршрут, ажиглалтын цэг, сорьц, суваг, шурф, зүсэлтийн байрлал | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 65 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_Legend\_1-50000\_v01\_raw-scan.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Ажиглалтын цэг, маршрут, сорьц, шурф, суваг, тэмдэглэгээ | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 66 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_L47-XIX\_GoldOccurrenceDescriptions\_XIX-74-A\_4186\_v01\_raw.docx | DOCX текст | Text/table scanned or office document; coordinate extraction, table cleaning, source confidence log шаардлагатай. | XIX-74-A-1, A-2, A-3 алтны илрэлийн координат, агуулга, геологийн нөхцөл | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/High after CRS, metadata, coordinate and content QA/QC. | Extract coordinates/attributes, clean register, link with GIS layers. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 67 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralOccurrenceAndMineralizedPointRegister\_7255\_v01\_raw-scan.pdf | PDF скан, 14 хуудас | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Илрэл, эрдэсжсэн цэг, гар зураг, хүснэгт, P3 тайлбар | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 68 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralizedPointRegister\_7255\_v01\_raw-table.xlsx | XLSX хүснэгт | Text/table scanned or office document; coordinate extraction, table cleaning, source confidence log шаардлагатай. | Цэгийн дугаар, координат, чулуулаг, агуулга, эрдэсжилт, төрөл, дээж | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/High after CRS, metadata, coordinate and content QA/QC. | Extract coordinates/attributes, clean register, link with GIS layers. | Geology/mineral occurrence/prospectivity layers and occurrence database |
| 69 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_Legend\_RawScan\_2020\_v01.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Металлогений зургийн таних тэмдэг, ашигт малтмалын төрөл, орд-илрэлийн тэмдэглэгээ, судалгааны ажлын тэмдэглэгээ | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Metallogenic context map/report and deposit model screening table |
| 70 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_RawScan\_2020\_v01.jpg | JPG зураг | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Монгол улсын 1:500,000-ны металлогений зураг, L-47-B (Тал шанд) хавтгай | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Metallogenic context map/report and deposit model screening table |
| 71 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book01\_ProjectBook13\_1M500K\_RawScan\_2021\_v01.pdf | PDF скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Монгол орны 1:500,000-ны масштабын металлогений зураг, тайлбар бичиг. Ном-1, төслийн номын дугаар-13 | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Metallogenic context map/report and deposit model screening table |
| 72 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book04\_ProjectBook16\_1M500K\_RawScan\_2021\_v01.pdf | PDF скан | Scanned/non-native image; georeference status unknown. Map grid/GCP ашиглан QA/QC хийх шаардлагатай. | Монгол орны 1:500,000-ны масштабын металлогений зураг, тайлбар бичиг. Ном-4, төслийн номын дугаар-16 | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis | Medium/Low until georeferenced and source checked; scale/residual/confidence flag шаардлагатай. | Scan QA/QC, georeference if map, digitize key evidence, attribute coding, confidence flag. | Metallogenic context map/report and deposit model screening table |
| 73 | 07\_Basemap\_Sentinel2\_ASTER | 2005-09-05\_MN\_ASTER-L1B\_MultispectralImagery\_00409052005043503\_v01\_raw.hdf | HDF4 | ASTER HDF raw product; direct GIS layer биш. ASTER workflow v5 дагуу import/band extraction шаардлагатай. | error | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Needs verification; HDF import алдаа/compatibility шалгана. Raw product өөрчлөхгүй. | ASTER HDF import, band extraction, UTM47 grid, index/score/class/mask workflow. | ASTER raw score, class map, final binary support mask, QA/QC log |
| 74 | 07\_Basemap\_Sentinel2\_ASTER | 2025-05-28\_MN\_T46TGS\_GeoreferencedSatelliteRaster\_v01\_raw.tif | GTiff | GeoTIFF/raster; UTM46N/T46 tile байж болзошгүй. EPSG:32647 стандарт руу reproject хийх эсэхийг шалгана. | ok | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | Remote sensing QA/QC, subset/reproject, derive composites/indices, export EPSG:32647. | Sentinel/ASTER/basemap derivative GeoTIFF and remote sensing QA/QC report |
| 75 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_GoogleMaps\_BasemapImagery\_RGB\_2p4m\_WGS84\_Raw\_v01.tif | GTiff | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | ok | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | Remote sensing QA/QC, subset/reproject, derive composites/indices, export EPSG:32647. | Sentinel/ASTER/basemap derivative GeoTIFF and remote sensing QA/QC report |
| 76 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_EPSG3857\_0p15m\_Raw\_v01.tif | GTiff | GeoTIFF/raster; CRS/resolution/extent/NoData/band count шалгана. | ok | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | Remote sensing QA/QC, subset/reproject, derive composites/indices, export EPSG:32647. | Sentinel/ASTER/basemap derivative GeoTIFF and remote sensing QA/QC report |
| 77 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_GeologicalInterpretation\_RGB\_B12-B08-B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | GTiff | GeoTIFF/raster; UTM46N/T46 tile байж болзошгүй. EPSG:32647 стандарт руу reproject хийх эсэхийг шалгана. | ok | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | Remote sensing QA/QC, subset/reproject, derive composites/indices, export EPSG:32647. | Sentinel/ASTER/basemap derivative GeoTIFF and remote sensing QA/QC report |
| 78 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_B11B12\_B08B11\_B04B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | GTiff | GeoTIFF/raster; UTM46N/T46 tile байж болзошгүй. EPSG:32647 стандарт руу reproject хийх эсэхийг шалгана. | ok | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | Medium/High after CRS, metadata, coordinate and content QA/QC. | Remote sensing QA/QC, subset/reproject, derive composites/indices, export EPSG:32647. | Sentinel/ASTER/basemap derivative GeoTIFF and remote sensing QA/QC report |

| Evidence group | File count | Primary workflow use |
| :---- | :---- | :---- |
| 01\_Tectonic\_Terrane\_KMZ | 8 | Terrane, tectonic setting, license boundary and regional concept. |
| 02\_DEM\_ALOS\_ASTERGDEM | 14 | Terrain, slope, drainage, access, safety and lineament support. |
| 03\_KOMPSAT2\_MSC\_L1G | 24 | High-resolution visual basemap, PAN/MS, lineament/outcrop/access interpretation. |
| 04\_HeavyMineral\_StreamSediment\_Field | 6 | Historical geochemical anomaly, drainage follow-up and orientation sampling. |
| 05\_Geology\_Mineral\_Prospectivity | 16 | Detailed/regional geology, occurrences, prospectivity and occurrence database. |
| 06\_Regional\_Metallogenic\_L47B | 4 | 1:500,000 metallogenic context and deposit model screening. |
| 07\_Basemap\_Sentinel2\_ASTER | 6 | Sentinel/ASTER/basemap remote sensing support layers. |

# **1A. Explicit raw input assignment by workflow phase**

**Purpose:** Энэ хэсэг нь 78 raw input file бүрийг яг аль workflow phase-ийн input болохыг, filename-ээр нь, аргачлалын хэрэглээтэй нь холбож заана. Phase дотор “Input files” гэж ерөнхий бичихгүй; доорх № болон filename-ийг ашиглана. Raw data-г өөрчлөхгүй, зөвхөн working copy дээр боловсруулна.

## **1A.1 Phase-level input control summary**

| Workflow phase | Exact direct raw input № | How to apply | Handover note |
| :---- | :---- | :---- | :---- |
| 00 Raw Files Archive | №1-78 | Бүх raw file болон sidecar файлыг read-only archive-д бүртгэж checksum үүсгэнэ. | All later phases use working copies only. |
| 01 Data Audit and Master GIS Setup | №1-78 | Файл бүрийн metadata, CRS/spatial status, sidecar, scan quality, processing copy status, confidence-г шалгана. | Master inventory \+ Master GIS schema. |
| 02 Remote Sensing Preprocessing | №9-46, №73-78 | DEM, KOMPSAT, ASTER, Sentinel/basemaps-ийг QA/QC, orthorectify/reproject/subset/derive products болгоно. | Support evidence only; ore proof биш. |
| 03 Geological, Metallogenic and CMCS Synthesis | №1-8, №53-72 | Tectonic, geology, occurrence, prospectivity, source material, metallogenic context-ийг нэгтгэнэ. | Deposit model and geological evidence layers. |
| 03A Preliminary Deposit Model Preparation | №1-8, №47-78, №9-46 as support | Ордын candidate model бүрт exact source evidence ашиглан supporting/missing/validation хүснэгт гаргана. | Phase 4 scoring and Phase 10 final target model-fit. |
| 04 Preliminary Prospect Delineation and Ranking | Traceable basis №1-78 \+ Phase 1-3 outputs | Evidence overlay, 100-point score, A/B/C/D ranking; dominant\_deposit\_model талбар нэмнэ. | A/B prospects to drone/recon. |
| 05 Drone/LiDAR/Photogrammetry | №8, №9-22, №24-46, №75-78 \+ Phase 4 outputs | Flight block, terrain/access/safety/basemap/lineament support. | Drone outputs to Phase 6-10. |
| 06 Recon Mapping and pXRF | №8, №9-22, №55-56, №60, №63-68, №75-78 \+ Phase 4/5 outputs | Field validation, lithology/alteration/mineralization/pXRF forms and traverse planning. | Validated field evidence to Phase 7\. |
| 07 Rock Chip/Channel Sampling | №52, №55-56, №60, №63-68, №9-22, №75-78 \+ Phase 6 outputs | Sample candidate selection, lab submission, QA/QC insertion, assay import template. | Lab evidence to Phase 10\. |
| 08 Orientation Soil/Stream/Heavy Mineral | №47-52, №9-22, №53-56, №60, №63-64, №68 | Historical drainage/heavy mineral/geochemical evidence, orientation survey design. | Validated method to Phase 9\. |
| 09 Systematic Soil Grid | №8, №9-22, №47-52, №55, №60, №63-64, №68, №75-78 \+ Phase 8 outputs | Grid design, soil collection, lab QA/QC, soil anomaly map. | Assay anomalies to Phase 10\. |
| 10 Integrated Interpretation and Final Target Ranking | Full traceable source basis №1-78 \+ validated phase outputs | All evidence, field/lab QA/QC, model-fit re-score, final target sheets. | Final A/B targets to Phase 11\. |
| 11 Follow-up Trench/Geophysics/Scout Drill | №8, №9-22, №55, №60, №63-64, №68, №75-78 \+ Phase 10 outputs | Trench/IP/magnetic/scout drill collar planning, HSE/access/budget check. | Only if minimum criteria met. |
| 99 Final Deliverables | №1-78 traceability \+ all phase outputs | Final package, GIS, reports, QA/QC, limitations, source references. | Ready for technical/management review. |

## **1A.2 File-by-file input assignment matrix**

Энэ matrix-д raw input file бүрийг primary workflow phase-тэй холбов. Secondary phase-үүдэд ашиглах үед тухайн phase-ийн “Input files” мөр болон Phase-level summary-д заасан №-өөр татаж хэрэглэнэ.

| № | Evidence group | Exact raw input filename | Primary input phase | Methodology action |
| :---- | :---- | :---- | :---- | :---- |
| 1 | 01\_Tectonic\_Terrane\_KMZ | Geological and Tectonic Characteristics of the Lake Terrane, Mongolia.png | 03 | Lake Terrane tectonic/geological context; use as regional concept evidence only after source and scan QA/QC. |
| 2 | 01\_Tectonic\_Terrane\_KMZ | Mongolia\_Tectonic\_Terrane\_Map\_Project\_Area\_Lake\_Island\_Arc\_Terrane.jpg | 03 | Terrane overlay; supports Lake island arc terrane context and deposit model screening. |
| 3 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Central\_Mongolian\_Massif\_and\_Daagandel\_Tectonic\_Zone\_Page11.jpg | 03 | Regional tectonic explanation; extract narrative evidence and confidence/source note. |
| 4 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part1\_Page08.jpg | 03 | Nuur accretionary megazone context; use for regional geological setting. |
| 5 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part2\_Page09.jpg | 03 | Khurai/Baatarkhairkhan/Ulaanshand zone context; supports model screening. |
| 6 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part3\_Page10.jpg | 03 | Khankhukhi/Khantayshir regional context; source note and limitation flag required. |
| 7 | 01\_Tectonic\_Terrane\_KMZ | Regional\_Tectonic\_Subdivision\_Map\_of\_Mongolia\_Tumurtogoo\_2017\_Buduunkhad\_Project\_in\_Ulaanshand\_Zone.jpg | 03 | Ulaanshand Zone tectonic subdivision context for deposit model candidate screening. |
| 8 | 01\_Tectonic\_Terrane\_KMZ | MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz | 01 | Primary license boundary; import to GeoPackage, reproject EPSG:32647, use for all clipping/buffer/QA. |
| 9 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_DEM\_1arcsec\_WGS84\_v01\_raw.tif | 02 | DEM terrain base; derive hillshade/slope/aspect/drainage and use for access/safety/lineament support. |
| 10 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_NumObservations\_1arcsec\_WGS84\_v01\_raw.tif | 02 | ASTER GDEM observation-count QA layer; evaluate DEM reliability/artefacts. |
| 11 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tfw | 02 | World file sidecar for ALOS-PALSAR DEM; keep with parent raster, do not use alone. |
| 12 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif | 02 | High-resolution terrain DEM; produce DTM derivatives, drainage, slope and lineament support. |
| 13 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.aux.xml | 02 | Auxiliary metadata/statistics sidecar for ALOS DEM; preserve with parent raster. |
| 14 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.ovr | 02 | Overview/pyramid sidecar for ALOS DEM; preserve with parent raster. |
| 15 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tfw | 02 | World file sidecar for hillshade; keep with parent raster. |
| 16 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif | 02 | Hillshade support layer; use for structural/terrain interpretation and field/drone planning. |
| 17 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | 02 | Auxiliary metadata/statistics sidecar for hillshade; preserve with parent raster. |
| 18 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | 02 | Overview/pyramid sidecar for hillshade; preserve with parent raster. |
| 19 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tfw | 02 | World file sidecar for slope raster; keep with parent raster. |
| 20 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif | 02 | Slope degree raster; use for access, safety, drainage and drone/trench/drill workability. |
| 21 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | 02 | Auxiliary metadata/statistics sidecar for slope raster; preserve with parent raster. |
| 22 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | 02 | Overview/pyramid sidecar for slope raster; preserve with parent raster. |
| 23 | 03\_KOMPSAT2\_MSC\_L1G | KOMPSAT EULA Form\_3.1.pdf | 02 | License/provenance evidence; store in data source and compliance register. |
| 24 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.tif | 02 | KOMPSAT PAN raster; orthorectify/pansharpen, use for lineament, outcrop, access and basemap. |
| 25 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.txt | 02 | PAN metadata; use for source verification, GSD/projection audit, processing register. |
| 26 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.rpc | 02 | PAN RPC sidecar; required for orthorectification/terrain correction. |

| № | Evidence group | Exact raw input filename | Primary input phase | Methodology action |
| :---- | :---- | :---- | :---- | :---- |
| 27 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.eph | 02 | PAN ephemeris/orbit sidecar; preserve with PAN bundle for geometric audit. |
| 28 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.tif | 02 | KOMPSAT Green band; stack with MS bands for true/false color and pan-sharpened products. |
| 29 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.txt | 02 | Green band metadata; verify band identity and processing parameters. |
| 30 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.rpc | 02 | Green band RPC sidecar; use for MS orthorectification/alignment. |
| 31 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.eph | 02 | Green band ephemeris/orbit sidecar; preserve with MS bundle. |
| 32 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.tif | 02 | KOMPSAT Blue band; stack with MS bands for composites and basemap. |
| 33 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.txt | 02 | Blue band metadata; verify source and band identity. |
| 34 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.rpc | 02 | Blue band RPC sidecar; use for MS orthorectification/alignment. |
| 35 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.eph | 02 | Blue band ephemeris/orbit sidecar; preserve with MS bundle. |
| 36 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.tif | 02 | KOMPSAT NIR band; derive NDVI/vegetation mask and false color support. |
| 37 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.txt | 02 | NIR band metadata; verify source and band identity. |
| 38 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.rpc | 02 | NIR band RPC sidecar; use for MS orthorectification/alignment. |
| 39 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.eph | 02 | NIR band ephemeris/orbit sidecar; preserve with MS bundle. |
| 40 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.tif | 02 | KOMPSAT Red band; stack for RGB/NDVI/false color support. |
| 41 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.txt | 02 | Red band metadata; verify source and band identity. |
| 42 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.rpc | 02 | Red band RPC sidecar; use for MS orthorectification/alignment. |
| 43 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.eph | 02 | Red band ephemeris/orbit sidecar; preserve with MS bundle. |
| 44 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jpg | 02 | KOMPSAT browse image; use for scene coverage preview only, not analysis-grade raster. |
| 45 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jgw | 02 | Browse image world file; keep with br.jpg for lightweight overlay only. |
| 46 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_tn.jpg | 02 | Thumbnail preview; use for inventory/catalog only. |
| 47 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200000\_v01\_raw-scan.jpg | 08 | Heavy mineral sampling result map; georeference/digitize indicator minerals/anomaly polygons and drainage follow-up. |
| 48 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 08 | Heavy mineral legend; build symbol dictionary and indicator mineral domain values. |
| 49 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 08 | Stream sediment legend; build element/anomaly/contour domain values. |
| 50 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Polyelement\_1-200000\_v01\_raw-scan.jpg | 08 | Stream sediment polyelement map; digitize Cu-Pb-Zn-Ag-As-Bi-W-Sn-Mo-Mn-Ba-F anomaly layers. |
| 51 | 04\_HeavyMineral\_StreamSediment\_Field | 2011\_MN\_Namalzakh\_L47-74-A\_FieldRouteNotebook\_Routes14-15\_Obs1076-1090\_1-50000\_v01\_raw-scan.pdf | 08 | Field route notebook; extract observation routes/points, compare with geology and sampling plans. |
| 52 | 04\_HeavyMineral\_StreamSediment\_Field | XV023222\_Buduunkhad\_Report7255\_FieldObservation\_StationDescription\_Table\_WGS84\_LegacyRaw\_v01.pdf | 08 | Field observation station table; extract coordinates/lithology/mineralization into validation register. |

| № | Evidence group | Exact raw input filename | Primary input phase | Methodology action |
| :---- | :---- | :---- | :---- | :---- |
| 53 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_1-200000\_v01\_raw-scan.jpg | 03 | Regional geology map; georeference and digitize regional geology/structure for context. |
| 54 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 03 | Regional geology legend; build lithology/age/intrusion/structure lookup. |
| 55 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_1-50000\_v01\_raw-scan.jpg | 03 | Detailed geology map; primary local geology/structure/contact/section vectorization source. |
| 56 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 03 | Detailed geology legend; build stratigraphy, intrusive, vein and alteration domains. |
| 57 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_1-200000\_v01\_raw-scan.jpg | 03 | Regional mineral resources map; digitize occurrence/resource/anomaly context. |
| 58 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 03 | Mineral resources legend; build commodity/occurrence/anomaly symbol dictionary. |
| 59 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralDistributionPatternMap\_1-100000\_v01\_raw-scan.jpg | 03 | Mineral distribution pattern map; ore district/node/metallogenic area context. |
| 60 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralOccurrenceMap\_1-50000\_v01\_raw-scan.jpg | 03 | Detailed mineral occurrence map; primary Au-Cu/Cu/Mo/As/Zn occurrence vectorization source. |
| 61 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MetallogenicSchemeAndMetallogenogram\_1-400000\_v01\_raw-scan.jpg | 03 | Metallogenic scheme/metallogenogram; ore formation and regional metallogenic context. |
| 62 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessment\_ReportExcerpt\_B3-TolKhar\_v01\_raw-photo.jpg | 03 | Prospectivity report excerpt; extract B-2/B-3/B-4 narrative evidence and data gaps. |
| 63 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessmentMap\_1-50000\_v01\_raw-scan.jpg | 03 | Prospectivity assessment map; digitize B-3 Tol Khar/G-1 and priority areas. |
| 64 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_1-50000\_v01\_raw-scan.jpg | 03 | Source materials map; digitize routes, stations, samples, trenches, pits and sections. |
| 65 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 03 | Source materials legend; build route/observation/sample/work-type domains. |
| 66 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_L47-XIX\_GoldOccurrenceDescriptions\_XIX-74-A\_4186\_v01\_raw.docx | 03 | Gold occurrence descriptions; extract Au occurrence coordinates, grades and geological descriptions. |
| 67 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralOccurrenceAndMineralizedPointRegister\_7255\_v01\_raw-scan.pdf | 03 | Mineral occurrence/mineralized point register; extract/cross-check occurrence attributes and P3 notes. |
| 68 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralizedPointRegister\_7255\_v01\_raw-table.xlsx | 03 | Mineralized point table; import cleaned coordinates/attributes to occurrence database. |
| 69 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_Legend\_RawScan\_2020\_v01.jpg | 03 | Regional metallogenic legend; build belt/ore-formation/commodity domain values. |
| 70 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_RawScan\_2020\_v01.jpg | 03 | 1:500k metallogenic map; use as regional metallogenic context only. |
| 71 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book01\_ProjectBook13\_1M500K\_RawScan\_2021\_v01.pdf | 03 | Metallogenic report book 01; extract text evidence for ore formation and regional context. |
| 72 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book04\_ProjectBook16\_1M500K\_RawScan\_2021\_v01.pdf | 03 | Metallogenic report book 04; extract text evidence for ore formation and regional context. |
| 73 | 07\_Basemap\_Sentinel2\_ASTER | 2005-09-05\_MN\_ASTER-L1B\_MultispectralImagery\_00409052005043503\_v01\_raw.hdf | 02 | ASTER HDF raw product; import/extract bands and derive alteration/lithology indices. |
| 74 | 07\_Basemap\_Sentinel2\_ASTER | 2025-05-28\_MN\_T46TGS\_GeoreferencedSatelliteRaster\_v01\_raw.tif | 02 | Received satellite raster; QA/QC CRS/extent, subset/reproject and derive support products. |
| 75 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_GoogleMaps\_BasemapImagery\_RGB\_2p4m\_WGS84\_Raw\_v01.tif | 02 | Google Maps RGB basemap; QA/QC/reproject for field planning and visual reference. |
| 76 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_EPSG3857\_0p15m\_Raw\_v01.tif | 02 | High-resolution surface basemap; reproject/clip for access, outcrop and field planning support. |
| 77 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_GeologicalInterpretation\_RGB\_B12-B08-B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | 02 | Sentinel-2 geology composite; reproject to EPSG:32647 and use as lithology/alteration support. |
| 78 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_B11B12\_B08B11\_B04B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | 02 | Sentinel-2 lithology index product; reproject and use as support evidence only. |

## **1A.3 Mandatory rule for every phase**

* Phase бүрийн аргачлалд input-ийг “geology files” эсвэл “remote sensing files” гэж дангаар бичихгүй; Section 1A.2 дахь raw input № болон exact filename-ийг заавал ашиглана.  
* Output layer/report/table бүрт source\_input\_no, source\_raw\_filename, source\_group, source\_phase, processing\_version, confidence, limitation талбар/мөр хадгална.  
* Historical scanned map-derived evidence нь validation\_status \= Historical only байхаас field/lab confirmed evidence-тэй холигдохгүй.  
* Remote sensing, DEM, KOMPSAT, Sentinel, ASTER, drone/LiDAR, pXRF output нь хүдэржилтийн баталгаа биш; support evidence гэж тэмдэглэнэ.

# **1B. Phase-wise exact raw input file processing and output matrix — v6 update**

**Зорилго.** Энэ v6 нэмэлт нь 78 raw input file бүрийг аль phase-д ашиглах, яг ямар нэртэй input файл болох, ямар software/program-аар ямар боловсруулалт хийх, ямар нэртэй output file гаргахыг нэг бүрчлэн заана. Raw file-г overwrite хийхгүй; бүх ажил processing copy дээр хийгдэнэ. Output filename нь standard deliverable naming бөгөөд бодит боловсруулалтын үед version дугаарыг v01/v02... гэж өсгөнө.

## **1B.1 Phase тус бүрийн raw input file assignment summary**

| Workflow phase | Raw input file numbers | Main software/program | Main output package |
| :---- | :---- | :---- | :---- |
| 00\_Raw\_Files\_Archive | 1-78 | File system, checksum utility, Excel | Master inventory, checksum register, source data README |
| 01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup | 1-78 metadata; primary spatial boundary input №8; all raster/scan/doc sidecar QA | QGIS, GDAL/OGR, Excel | Master\_GIS\_Database.gpkg; Master\_QGIS\_Project.qgz; CRS/Georef QAQC Log; Data Confidence Ranking |
| 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | 9-46, 73-78 | SNAP 13.0.0, QGIS, GDAL, ILWIS 3.6.8, Global Mapper | Processed DEM/Sentinel/ASTER/KOMPSAT outputs, QAQC logs, remote sensing support layers |
| 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | 1-7, 53-72 plus outputs from Phase 1/2 and boundary №8 | QGIS, QGIS Georeferencer, Excel/Word evidence registers | Geological evidence layers, metallogenic context, occurrence database, Preliminary Deposit Model.docx |
| 04\_Phase\_4\_Preliminary\_Prospect\_Delineation\_and\_Ranking | Derived from raw №1-8, 47-78 and Phase 2/3 outputs | QGIS, Excel scoring matrix | Prospect polygons, ranking table, Go/No-Go desktop matrix |
| 05\_Phase\_5\_DJI\_Matrice\_400\_Drone\_LiDAR\_Photogrammetry\_Survey | Derived A/B prospect outputs from Phase 4; DEM/access from №9-22 and basemap №75-78 | DJI Matrice 400, Zenmuse P1/L2/L3, processing software, QGIS | Drone flight plan, orthomosaic, LiDAR point cloud, DTM/DSM, interpretation layers |
| 06\_Phase\_6\_Recon\_Mapping\_and\_Portable\_XRF\_Field\_Screening | Field planning from №51, №52, №60, №63, №64 and Phase 4/5 outputs | QField/QGIS, Olympus Vanta M, Bruker Titan S1 | Recon traverse, field observations, pXRF register and QAQC report |
| 07\_Phase\_7\_Rock\_Chip\_Channel\_and\_Verification\_Sampling | Field-confirmed targets derived from №55, №60, №63, №64, №66-68 and Phase 6 outputs | QField/QGIS, GPS/GNSS, lab submission templates | Rock chip/channel register, lab submission, assay import template |
| 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | 47-52 plus target/geology outputs from №55, №60, №63, №64 | QGIS, DEM drainage tools, pXRF, lab workflow | Orientation soil plan, stream/heavy mineral follow-up plan |
| 09\_Phase\_9\_Systematic\_Soil\_Grid\_and\_Laboratory\_QAQC | Derived from Phase 8; geologic/target controls from №55, №60, №63, №64 | QGIS grid design, pXRF, laboratory assay | Soil grid plan, sample points, QAQC report, soil assay results |
| 10\_Phase\_10\_Integrated\_Interpretation\_and\_Final\_Target\_Ranking | All validated raw-derived outputs from №1-78 plus lab/field/drone results | QGIS, Excel/statistical validation, Word report | Integrated interpretation report, final target polygons, target description sheets |
| 11\_Phase\_11\_Follow\_Up\_Trench\_Geophysics\_and\_Scout\_Drill\_Planning | Final A/B targets; DEM/access from №9-22; geology/structure from №53-68; RS from №73-78 | QGIS, trench/geophysics/drilling planning templates | Follow-up work plan, trench/geophysics lines, scout drilling proposal, collar table |

## **1B.2 Detailed 78 raw input file → software → processing → output matrix**

### **Phase 1 inputs: boundary, full metadata audit and Master GIS setup**

| № | Evidence group | Exact raw input filename | Primary workflow phase | Software / program | Processing action | Expected output filename(s) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 8 | 01\_Tectonic\_Terrane\_KMZ | MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz | 01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup | QGIS, GDAL/OGR, GeoPackage | KMZ/KML polygon import; CRS шалгах; EPSG:4326-аас EPSG:32647 руу export; topology/area/perimeter QA/QC; master project-ийн үндсэн boundary layer болгоно. | XV023222\_Buduunkhad\_L23222\_LicenseBoundary\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_LicenseBoundary\_QAQC\_Register.xlsx; XV023222\_Buduunkhad\_Project\_Buffer\_500m\_1km\_5km\_10km\_20km\_25km\_EPSG32647.gpkg |

### **Phase 2 inputs: DEM, ALOS-PALSAR, KOMPSAT-2, ASTER, Sentinel and basemap processing**

| № | Evidence group | Exact raw input filename | Primary workflow phase | Software / program | Processing action | Expected output filename(s) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 9 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_DEM\_1arcsec\_WGS84\_v01\_raw.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, Global Mapper | DEM CRS/resolution/NoData/extent шалгах; license+buffer subset; EPSG:32647 reproject; hillshade/slope/aspect/contour/drainage derivative гаргана. | XV023222\_Buduunkhad\_ASTERGDEM\_DEM\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ASTERGDEM\_Hillshade\_Slope\_Aspect\_Drainage\_EPSG32647\_v01.gpkg/tif; XV023222\_Buduunkhad\_DEM\_QAQC\_Log.xlsx |
| 10 | 02\_DEM\_ALOS\_ASTERGDEM | ASTER-GDEM-v3\_N45E096\_NumObservations\_1arcsec\_WGS84\_v01\_raw.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | ASTER GDEM observation-count raster-г DEM quality mask болгон шалгах; low reliability pixel flag; DEM QA/QC-д холбох. | XV023222\_Buduunkhad\_ASTERGDEM\_NumObservations\_QA\_Mask\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_DEM\_Quality\_Assessment.xlsx |
| 11 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tfw | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, Global Mapper | Parent DEM-тэй хамтад нь bundle болгон хадгална; CRS/pixel size/extent/NoData шалгаж EPSG:32647 DEM derivative-ийн үндсэн эх болгон ашиглана. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ALOS\_PALSAR\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg/tif; sidecar\_bundle\_QAQC entry (world file) |
| 12 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, Global Mapper | ALOS-PALSAR 12.5 m DEM-ийг CRS/pixel/extent шалгаж subset/reproject; terrain derivative, drainage, access/safety, drone/trench planning-д ашиглана. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ALOS\_PALSAR\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg/tif; sidecar\_bundle\_QAQC entry (12.5 m DEM raster) |
| 13 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.aux.xml | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, Global Mapper | Parent DEM-тэй хамтад нь bundle болгон хадгална; CRS/pixel size/extent/NoData шалгаж EPSG:32647 DEM derivative-ийн үндсэн эх болгон ашиглана. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ALOS\_PALSAR\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg/tif; sidecar\_bundle\_QAQC entry (aux/statistics sidecar) |
| 14 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_DEM\_12p5m\_UTM47N\_Raw\_v01.tif.ovr | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, Global Mapper | Parent DEM-тэй хамтад нь bundle болгон хадгална; CRS/pixel size/extent/NoData шалгаж EPSG:32647 DEM derivative-ийн үндсэн эх болгон ашиглана. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_DEM\_12p5m\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ALOS\_PALSAR\_Terrain\_Derivatives\_EPSG32647\_v01.gpkg/tif; sidecar\_bundle\_QAQC entry (overview pyramid sidecar) |
| 15 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tfw | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_hillshade\_world\_file\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 16 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_hillshade\_raster\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 17 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_hillshade\_aux\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 18 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_Hillshade\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_hillshade\_overview\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 19 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tfw | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_slope\_world\_file\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 20 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_slope\_raster\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 21 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.aux.xml | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_slope\_aux\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 22 | 02\_DEM\_ALOS\_ASTERGDEM | XV023222\_Buduunkhad\_ALOS-PALSAR\_SlopeDeg\_12p5m\_UTM47N\_Derived\_v01.tif.ovr | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | Derived raster/sidecar QA; parent raster-тэй хамт bundle audit; EPSG:32647 alignment шалгах; terrain/access/lineament interpretation-д reference layer болгоно. | XV023222\_Buduunkhad\_ALOS\_PALSAR\_slope\_overview\_QAQC\_EPSG32647\_v01.tif/register; XV023222\_Buduunkhad\_Terrain\_Derivatives\_Index.xlsx |
| 23 | 03\_KOMPSAT2\_MSC\_L1G | KOMPSAT EULA Form\_3.1.pdf | 00\_Raw\_Files\_Archive / 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | PDF reader, Word/Excel register | Data license/provenance бүртгэл; usage restriction, source note, acquisition info-г Source Data README-д оруулна. | XV023222\_Buduunkhad\_KOMPSAT2\_Data\_License\_Provenance\_Register.xlsx; XV023222\_Buduunkhad\_Source\_Data\_Readme.docx |
| 24 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | PAN raster: PAN orthorectification, terrain correction, pan-sharpen base, high-resolution lineament/outcrop/access interpretation; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 25 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.txt | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | PAN metadata: PAN metadata extraction: acquisition, GSD, projection/source details; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 26 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.rpc | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | PAN RPC: RPC terrain correction/orthorectification support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 27 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344PN00\_1G.eph | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | PAN ephemeris: orbit/geometry support archive; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 28 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Green band: MS band alignment and RGB composite component; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 29 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.txt | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Green metadata: band metadata extraction; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 30 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.rpc | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Green RPC: MS orthorectification support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 31 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M1N00G\_1G.eph | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Green ephemeris: orbit/geometry support archive; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 32 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Blue band: MS band alignment and RGB component; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 33 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.txt | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Blue metadata: band metadata extraction; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 34 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.rpc | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Blue RPC: MS orthorectification support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 35 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M2N00B\_1G.eph | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Blue ephemeris: orbit/geometry support archive; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 36 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | NIR band: false color/NDVI/vegetation mask component; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 37 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.txt | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | NIR metadata: band metadata extraction; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 38 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.rpc | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | NIR RPC: MS orthorectification support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 39 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M3N00N\_1G.eph | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | NIR ephemeris: orbit/geometry support archive; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 40 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Red band: RGB/NDVI component, iron-stained surface visual interpretation; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 41 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.txt | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Red metadata: band metadata extraction; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 42 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.rpc | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Red RPC: MS orthorectification support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 43 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344M4N00R\_1G.eph | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | Red ephemeris: orbit/geometry support archive; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 44 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jpg | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | browse image: coverage preview/catalog thumbnail only; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 45 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_br.jgw | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | browse world file: browse georeference sidecar support; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 46 | 03\_KOMPSAT2\_MSC\_L1G | MSC\_111127030410\_28454\_08621344N00\_1G\_tn.jpg | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, ILWIS 3.6.8, RPC/orthorectification workflow | thumbnail: inventory thumbnail only; PAN/MS bundle alignment, RPC/EPH/TXT metadata audit, orthorectification, band stack, true/false color and NDVI support products. | XV023222\_Buduunkhad\_KOMPSAT2\_PAN\_MS\_Orthorectified\_Bundle\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_KOMPSAT2\_NDVI\_Lineament\_Outcrop\_Interpretation\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_KOMPSAT2\_QAQC\_Register.xlsx |
| 73 | 07\_Basemap\_Sentinel2\_ASTER | 2005-09-05\_MN\_ASTER-L1B\_MultispectralImagery\_00409052005043503\_v01\_raw.hdf | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | SNAP 13.0.0, ILWIS/ASTER workflow v5, QGIS/GDAL | ASTER HDF import; VNIR/SWIR/TIR band extraction where available; projection to UTM47/EPSG32647; alteration/lithology indices; score/class/binary mask separation. | XV023222\_Buduunkhad\_ASTER\_BandStack\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_ASTER\_score\_porphyry\_alteration\_raw\_v01.tif; XV023222\_Buduunkhad\_ASTER\_porphyry\_potential\_class\_v01.tif; XV023222\_Buduunkhad\_ASTER\_porphyry\_final\_target\_binary\_mask\_v01.tif; ASTER\_QAQC\_Log.xlsx |
| 74 | 07\_Basemap\_Sentinel2\_ASTER | 2025-05-28\_MN\_T46TGS\_GeoreferencedSatelliteRaster\_v01\_raw.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL, SNAP if source L1C/L2A needed | CRS/extent/band check; subset/reproject to EPSG:32647; base satellite raster QA; derivative composite support. | XV023222\_Buduunkhad\_20250528\_T46TGS\_GeoreferencedSatelliteRaster\_EPSG32647\_v01.tif; RemoteSensing\_QAQC\_Register.xlsx |
| 75 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_GoogleMaps\_BasemapImagery\_RGB\_2p4m\_WGS84\_Raw\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | WGS84 basemap CRS check; reproject to EPSG:32647; visual reference layer for field route/access/outcrop interpretation. | XV023222\_Buduunkhad\_GoogleMaps\_Basemap\_RGB\_2p4m\_EPSG32647\_v01.tif; Basemap\_Overlay\_QAQC\_Log.xlsx |
| 76 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_EPSG3857\_0p15m\_Raw\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | QGIS, GDAL | EPSG:3857 high-resolution basemap reproject; tile/clip to license+buffer; use for detailed outcrop/disturbance/access interpretation. | XV023222\_Buduunkhad\_HighResolution\_RGB\_SurfaceBasemap\_GoogleMaps\_0p15m\_EPSG32647\_v01.tif; HighRes\_Basemap\_QAQC\_Log.xlsx |
| 77 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_GeologicalInterpretation\_RGB\_B12-B08-B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | SNAP 13.0.0, QGIS, GDAL | Sentinel-2 geology RGB B12-B08-B03 status check; UTM46N to EPSG32647 reproject; subset; lithology/structure visual interpretation support. | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_GeologicalInterpretation\_RGB\_B12-B08-B03\_10m\_EPSG32647\_v01.tif; Sentinel2\_Geology\_RGB\_QAQC\_Log.xlsx |
| 78 | 07\_Basemap\_Sentinel2\_ASTER | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_B11B12\_B08B11\_B04B03\_10m\_UTM46N\_ReceivedRaw\_v01.tif | 02\_Phase\_2\_Remote\_Sensing\_Preprocessing | SNAP 13.0.0, QGIS, GDAL | Sentinel-2 lithology index raster QA; UTM46N to EPSG32647; mask/noise check; geology/alteration support layer, ore proof биш. | XV023222\_Buduunkhad\_Sentinel2\_T46TGS\_20250528\_LithologyIndex\_B11B12\_B08B11\_B04B03\_10m\_EPSG32647\_v01.tif; Sentinel2\_LithologyIndex\_QAQC\_Log.xlsx |

### **Phase 3 / 03A inputs: tectonic, geology, mineral occurrence, prospectivity and metallogenic synthesis**

| № | Evidence group | Exact raw input filename | Primary workflow phase | Software / program | Processing action | Expected output filename(s) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | 01\_Tectonic\_Terrane\_KMZ | Geological and Tectonic Characteristics of the Lake Terrane, Mongolia.png | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Lake Terrane-ийн геологи/тектоникийн context зураг/эх мэдээлэл-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 2 | 01\_Tectonic\_Terrane\_KMZ | Mongolia\_Tectonic\_Terrane\_Map\_Project\_Area\_Lake\_Island\_Arc\_Terrane.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | төслийн талбай Lake island-arc terrane-тэй холбогдох regional context-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 3 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Central\_Mongolian\_Massif\_and\_Daagandel\_Tectonic\_Zone\_Page11.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Даагандэлийн бүс ба Төв Монголын массивын тайлбар-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 4 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part1\_Page08.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Нуурын аккрецийн мегабүсийн тайлбар-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 5 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part2\_Page09.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Хурайн/Баатархайрхан/Улааншандын бүсийн тайлбар-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 6 | 01\_Tectonic\_Terrane\_KMZ | MUGZ500\_Geomed2013\_Explanatory\_Text\_Nuur\_Accretionary\_Megazone\_Part3\_Page10.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Ханхөхий/Хантайширийн бүсийн тайлбар-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 7 | 01\_Tectonic\_Terrane\_KMZ | Regional\_Tectonic\_Subdivision\_Map\_of\_Mongolia\_Tumurtogoo\_2017\_Buduunkhad\_Project\_in\_Ulaanshand\_Zone.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS Layout, Excel/Word evidence register | Улааншандын бүсийн regional tectonic context-ийг source confidence-тэй бүртгэж, шаардлагатай бол georeference/overlay хийж terrane/metallogenic context болгон digitize/attribute coding хийнэ. | XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register.xlsx; XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Map\_EPSG32647.pdf; XV023222\_Buduunkhad\_Tectonic\_Context\_Layers.gpkg |
| 53 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_1-200000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; regional geology unit/fault/intrusive/contact vectorization; scale flag \= regional. | XV023222\_Buduunkhad\_1987\_L47-XIX\_GeologicalMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif; geology\_units\_200k\_polygons/structures\_faults\_lines\_EPSG32647\_v01.gpkg |
| 54 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS/Image viewer, Excel lookup | Regional geology legend dictionary; lithology/age/intrusive/structure domain values. | XV023222\_Buduunkhad\_1987\_GeologicalMap\_Legend\_Symbol\_Dictionary\_v01.xlsx |
| 55 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; detailed lithology, intrusive, contact, fault, vein, alteration/section digitizing; target-scale geology layer. | XV023222\_Buduunkhad\_2013\_L47-74-A\_GeologicalMap\_1-50K\_Georeferenced\_EPSG32647\_v01.tif; geology\_units\_50k\_polygons/structures\_faults\_lines/intrusive\_contacts\_lines/dyke\_vein\_lines\_EPSG32647\_v01.gpkg |
| 56 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS/Image viewer, Excel lookup | Detailed geology legend dictionary; stratigraphic\_unit, vein\_type, alteration, lithology domains. | XV023222\_Buduunkhad\_2013\_GeologicalMap\_Legend\_Symbol\_Dictionary\_v01.xlsx |
| 57 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_1-200000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; regional occurrence/resource/anomaly/ore field digitizing; commodity coding. | XV023222\_Buduunkhad\_1987\_L47-XIX\_MineralResourcesMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif; mineral\_occurrences\_points/mineralized\_zones\_polygons/ore\_field\_prospect\_polygons\_EPSG32647\_v01.gpkg |
| 58 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS/Image viewer, Excel lookup | Mineral resources legend dictionary; commodity, occurrence type, ore field type domains. | XV023222\_Buduunkhad\_1987\_MineralResources\_Legend\_Symbol\_Dictionary\_v01.xlsx |
| 59 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralDistributionPatternMap\_1-100000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; ore district/node/mineral distribution context digitizing; Phase 3 deposit model context. | XV023222\_Buduunkhad\_2013\_L47-73-74\_MineralDistributionPatternMap\_1-100K\_Georeferenced\_EPSG32647\_v01.tif; ore\_district\_node\_context\_EPSG32647\_v01.gpkg |
| 60 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralOccurrenceMap\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; Au-Cu/Cu/Mo/As/Zn occurrence points and target features digitizing; relation to geology/source materials. | XV023222\_Buduunkhad\_2013\_L47-74-A\_MineralOccurrenceMap\_1-50K\_Georeferenced\_EPSG32647\_v01.tif; mineral\_occurrences\_points\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_Mineral\_Occurrences\_Register.xlsx |
| 61 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MetallogenicSchemeAndMetallogenogram\_1-400000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Regional metallogenic scheme georeference/context digitizing; ore formation and age/element relation register. | XV023222\_Buduunkhad\_2013\_MetallogenicSchemeMetallogenogram\_1-400K\_Georeferenced\_EPSG32647\_v01.tif; metallogenic\_context\_layers\_EPSG32647\_v01.gpkg |
| 62 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessment\_ReportExcerpt\_B3-TolKhar\_v01\_raw-photo.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | Image/PDF viewer, Word/Excel evidence register | Report excerpt transcription/summary; B-2/B-3/B-4 area evidence, limitation, recommended follow-up coding. | XV023222\_Buduunkhad\_2013\_Prospectivity\_ReportExcerpt\_Evidence\_Register\_v01.xlsx; report\_evidence\_summary\_for\_Preliminary\_Deposit\_Model.docx |
| 63 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessmentMap\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; Б-3 Толь хяр, Г-1 and other prospectivity polygons digitizing; priority and evidence\_basis attributes. | XV023222\_Buduunkhad\_2013\_L47-74-A\_ProspectivityAssessmentMap\_1-50K\_Georeferenced\_EPSG32647\_v01.tif; prospectivity\_target\_zones\_polygons\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_Prospectivity\_Target\_Register.xlsx |
| 64 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference; route, observation, sample, trench/pit/shaft/channel, section line digitizing for QField/field validation. | XV023222\_Buduunkhad\_2013\_L47-74-A\_SourceMaterialsMap\_1-50K\_Georeferenced\_EPSG32647\_v01.tif; source\_material\_observation\_points/source\_material\_route\_lines/source\_material\_trench\_pit\_points\_EPSG32647\_v01.gpkg |
| 65 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS/Image viewer, Excel lookup | Source materials legend dictionary; observation\_type, sample\_type, work\_type domains; QField form lookup. | XV023222\_Buduunkhad\_SourceMaterials\_Legend\_Symbol\_Dictionary\_v01.xlsx; QField\_Lookups\_Domains.xlsx |
| 66 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_L47-XIX\_GoldOccurrenceDescriptions\_XIX-74-A\_4186\_v01\_raw.docx | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | Microsoft Word/LibreOffice, Excel, QGIS | Gold occurrence descriptions extraction; coordinates/grade/lithology/structure; occurrence register and model evidence coding. | XV023222\_Buduunkhad\_4186\_GoldOccurrence\_Descriptions\_Extracted\_Register\_v01.xlsx; XV023222\_Buduunkhad\_4186\_GoldOccurrence\_Points\_EPSG32647\_v01.gpkg; preliminary\_deposit\_model\_evidence\_table.xlsx |
| 67 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralOccurrenceAndMineralizedPointRegister\_7255\_v01\_raw-scan.pdf | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | PDF reader, Excel, QGIS | PDF register extraction; occurrence/mineralized point attributes; coordinate validation and cross-reference with map 60/68. | XV023222\_Buduunkhad\_7255\_MineralOccurrence\_MineralizedPoint\_Register\_Extracted\_v01.xlsx; XV023222\_Buduunkhad\_7255\_MineralizedPoint\_Layers\_EPSG32647\_v01.gpkg; extraction\_QAQC\_log.xlsx |
| 68 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralizedPointRegister\_7255\_v01\_raw-table.xlsx | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | Excel/LibreOffice Calc, QGIS | XLSX table cleaning; coordinate conversion; element/commodity standardization; GIS point layer and deposit model evidence. | XV023222\_Buduunkhad\_7255\_MineralizedPoint\_Clean\_Register\_v01.xlsx; XV023222\_Buduunkhad\_7255\_MineralizedPoint\_Points\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_Occurrence\_CrossReference\_7255\_4186.xlsx |
| 69 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_Legend\_RawScan\_2020\_v01.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS/Image viewer, Excel lookup | 1:500k metallogenic legend symbol dictionary; ore formation/commodity/metallogenic unit domains. | XV023222\_Buduunkhad\_L47B\_RegionalMetallogenic\_Legend\_Dictionary\_v01.xlsx |
| 70 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_RawScan\_2020\_v01.jpg | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | QGIS Georeferencer, QGIS digitizing | Georeference/context overlay; metallogenic belt/zone/ore district/node digitizing; context\_only flag. | XV023222\_Buduunkhad\_2020\_L47B\_Talshand\_RegionalMetallogenicMap\_1-500K\_Georeferenced\_EPSG32647\_v01.tif; metallogenic\_zones\_polygons\_EPSG32647\_v01.gpkg; regional\_metallogenic\_context\_map.pdf |
| 71 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book01\_ProjectBook13\_1M500K\_RawScan\_2021\_v01.pdf | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | PDF reader, Word/Excel evidence register | Regional report text/table extraction; ore formation/metallogenic context notes for deposit model. | XV023222\_Buduunkhad\_RegionalMetallogenic\_Report\_Book01\_Evidence\_Register\_v01.xlsx; metallogenic\_context\_summary.docx |
| 72 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book04\_ProjectBook16\_1M500K\_RawScan\_2021\_v01.pdf | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 03A | PDF reader, Word/Excel evidence register | Regional report text/table extraction; cross-reference with map 70/71; context evidence and limitations. | XV023222\_Buduunkhad\_RegionalMetallogenic\_Report\_Book04\_Evidence\_Register\_v01.xlsx; metallogenic\_context\_cross\_reference.xlsx |

### **Phase 6 and Phase 8 field/historical geochemistry inputs**

| № | Evidence group | Exact raw input filename | Primary workflow phase | Software / program | Processing action | Expected output filename(s) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 47 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200000\_v01\_raw-scan.jpg | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | QGIS Georeferencer, QGIS digitizing, DEM drainage analysis | Georeference; heavy mineral sample/anomaly/indicator contour digitizing; DEM drainage catchment overlay; upstream source check planning. | XV023222\_Buduunkhad\_1987\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_HeavyMineral\_Anomaly\_Layers\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_HeavyMineral\_FollowUp\_Plan.xlsx/pdf |
| 48 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | QGIS/Image viewer, Excel lookup table | Legend symbol dictionary үүсгэх; mineral\_indicator/anomaly\_class/sample\_symbol domain values; main map digitizing attribute control. | XV023222\_Buduunkhad\_HeavyMineral\_Symbol\_Dictionary\_v01.xlsx; QGIS lookup/domain table in gpkg |
| 49 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | QGIS/Image viewer, Excel lookup table | Stream sediment legend dictionary; element suite/anomaly level/contour type domain; map interpretation QA. | XV023222\_Buduunkhad\_StreamSediment\_Symbol\_Dictionary\_v01.xlsx; QGIS lookup/domain table in gpkg |
| 50 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Polyelement\_1-200000\_v01\_raw-scan.jpg | 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check | QGIS Georeferencer, QGIS digitizing, DEM drainage analysis | Georeference; Cu-Pb-Zn-Ag-As-Bi-W-Sn-Mo-Mn-Ba-F anomaly contour/vector digitizing; drainage source direction and orientation sampling plan. | XV023222\_Buduunkhad\_1987\_L47-XIX\_StreamSedimentPolyelementMap\_1-200K\_Georeferenced\_EPSG32647\_v01.tif; XV023222\_Buduunkhad\_StreamSediment\_Anomaly\_Layers\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_StreamSediment\_FollowUp\_Plan.xlsx/pdf |
| 51 | 04\_HeavyMineral\_StreamSediment\_Field | 2011\_MN\_Namalzakh\_L47-74-A\_FieldRouteNotebook\_Routes14-15\_Obs1076-1090\_1-50000\_v01\_raw-scan.pdf | 06\_Phase\_6\_Recon\_Mapping\_and\_Portable\_XRF\_Field\_Screening / 08\_Phase\_8 | PDF reader, QGIS, Excel register | Route 14-15 and observations 1076-1090 extraction; coordinates/route/sketch/observation attributes; QField recon and sampling planning. | XV023222\_Buduunkhad\_2011\_FieldRouteNotebook\_Routes14-15\_Observation\_Register\_v01.xlsx; XV023222\_Buduunkhad\_Field\_Route\_Observation\_Layers\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_QField\_Recon\_Input\_Package\_v01 |
| 52 | 04\_HeavyMineral\_StreamSediment\_Field | XV023222\_Buduunkhad\_Report7255\_FieldObservation\_StationDescription\_Table\_WGS84\_LegacyRaw\_v01.pdf | 06\_Phase\_6\_Recon\_Mapping\_and\_Portable\_XRF\_Field\_Screening / 03\_Phase\_3 | PDF reader, Excel, QGIS | Station description table extraction; WGS84 coordinates validation; lithology/structure/mineralization attribute coding; Master GIS observation layer. | XV023222\_Buduunkhad\_Report7255\_FieldObservation\_Station\_Register\_v01.xlsx; XV023222\_Buduunkhad\_Report7255\_FieldObservation\_Points\_EPSG32647\_v01.gpkg; XV023222\_Buduunkhad\_FieldObservation\_QAQC\_Log.xlsx |

**Тайлбар.** Phase 4-11 нь raw file-г шууд дахин боловсруулахаас илүүтэй Phase 1-3/03A болон Phase 8-аас гарсан QA/QC хийгдсэн derivative output-уудыг ашиглана. Гэсэн ч тэдгээр derivative output бүрийн эх raw input №-г дээрх matrix-д хадгалсан тул final target sheet, sample register, drill plan бүрт source\_raw\_input\_no/source\_file/source\_phase талбаруудыг заавал үлдээнэ.

## **1B.3 Required source-traceability fields for every output**

| Output field | Required value | Purpose |
| :---- | :---- | :---- |
| source\_raw\_input\_no | 1-78 дугаар | Output бүрийг аль raw input-оос үүссэнтэй audit trail-аар холбох |
| source\_raw\_filename | Exact raw filename | Файлын нэр өөрчлөгдөх/холилдох эрсдэлийг хаах |
| processing\_phase | 00/01/02/03/03A/04... | Аль workflow шатанд боловсруулсан болохыг тодруулах |
| processing\_software | QGIS / SNAP / GDAL / Excel / QField / etc. | Дахин боловсруулахад reproducibility хангах |
| processing\_action | Georeference / reproject / digitize / extract / score / QAQC | Юу хийснийг тодорхой бичих |
| output\_filename | Standardized output file name | Deliverable package-д нэг мөр нэршилтэй хадгалах |
| qaqc\_status | Draft / Checked / Approved / Rejected | Decision-grade биш output-г буруу ашиглахаас хамгаалах |
| validation\_status | Historical only / Field checked / Sampled / Lab confirmed | Historical evidence ба баталгаажсан evidence-г салгах |

# **v6 implementation note**

Энэ v6 хувилбар нь 78 raw input file бүрийг phase-wise байдлаар exact filename, software, processing action, expected output filename-тай холбосон тул цаашид QGIS/Excel/QField/Drone/Lab workflow-д source-traceability хадгалахад ашиглана. Бүх output нь preliminary/support evidence бөгөөд field validation, laboratory assay, QA/QC review хийгдэх хүртэл mineralization proof эсвэл resource/reserve estimate биш.

# **2\. Integrated 00-99 phase workflow**

00\_Raw\_Files\_Archive  
  \-\> 01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup  
  \-\> 02\_Phase\_2\_Remote\_Sensing\_Preprocessing  
  \-\> 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis  
  \-\> 04\_Phase\_4\_Preliminary\_Prospect\_Delineation\_and\_Ranking  
  \-\> 05\_Phase\_5\_DJI\_Matrice\_400\_Drone\_LiDAR\_Photogrammetry\_Survey  
  \-\> 06\_Phase\_6\_Recon\_Mapping\_and\_Portable\_XRF\_Field\_Screening  
  \-\> 07\_Phase\_7\_Rock\_Chip\_Channel\_and\_Verification\_Sampling  
  \-\> 08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check  
  \-\> 09\_Phase\_9\_Systematic\_Soil\_Grid\_and\_Laboratory\_QAQC  
  \-\> 10\_Phase\_10\_Integrated\_Interpretation\_and\_Final\_Target\_Ranking  
  \-\> 11\_Phase\_11\_Follow\_Up\_Trench\_Geophysics\_and\_Scout\_Drill\_Planning  
  \-\> 99\_Final\_Deliverables

# **00\. Raw Files Archive**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Raw data-г өөрчлөхгүй архивлах, integrity/metadata/source хяналт тогтоох. |
| Input files | Direct raw input files: №1-78 бүх raw input file. Яг filename, evidence group, primary phase, methodology action-ийг Section 1A-д бүрэн заасан. Sidecar files (.tfw, .aux.xml, .ovr, .rpc, .eph, .txt) parent raster/image-ээс салгахгүй. |
| Software / equipment | File system, checksum utility, inventory workbook. |

## **Processing folder structure**

00\_Raw\_Files\_Archive/  
├── 01\_Tectonic\_Terrane\_KMZ  
├── 02\_DEM\_ALOS\_ASTERGDEM  
├── 03\_KOMPSAT2\_MSC\_L1G  
├── 04\_HeavyMineral\_StreamSediment\_Field  
├── 05\_Geology\_Mineral\_Prospectivity  
├── 06\_Regional\_Metallogenic\_L47B  
└── 07\_Basemap\_Sentinel2\_ASTER

## **Step-by-step methodology**

1. 78 raw input файлыг evidence group-ийн дагуу raw archive хавтас руу байршуулна.  
2. Original filename, standardized filename, file type, source note, owner/responsible person, read status, processing copy status бүртгэнэ.  
3. SHA-256 checksum үүсгэж integrity log-д бичнэ.  
4. Sidecar файлуудыг parent file-аас салгахгүй: .tfw/.aux.xml/.ovr/.rpc/.eph/.txt metadata нь тухайн raster/image bundle-ийн хэсэг.  
5. Raw file дээр rename/overwrite/clip/reproject хийхгүй; working copy-г дараагийн phase-д хуулна.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Checksum match | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Raw overwrite хийгдээгүй | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Sidecar completeness | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Source note and owner registered | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_78Input\_Master\_Inventory.xlsx  
* XV-023222\_Buduunkhad\_Raw\_Data\_Integrity\_Log.xlsx  
* XV-023222\_Buduunkhad\_Source\_Data\_Readme.docx  
* SHA-256\_Checksum\_Register.csv

## **Decision gate / next phase condition**

* All files archived, checksum complete, processing copies available.

# **01\. Phase 1 — Data Audit and Master GIS Setup**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | 78 input file-ийг GIS-ready болгох, EPSG:32647 master database үүсгэх. |
| Input files | Direct raw input files: №1-78 бүх raw input file. Үүнээс №8 license boundary нь master boundary layer; №9-78 raster/scan/table/PDF/DOCX бүрийн metadata, CRS, sidecar, confidence, working-copy status шалгана. Section 1A-г primary input checklist болгон ашиглана. |
| Software / equipment | QGIS, GeoPackage, spreadsheet register. |

## **Processing folder structure**

01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup/  
├── 01\_File\_Inventory  
├── 02\_Metadata\_Check  
├── 03\_CRS\_Check  
├── 04\_Raster\_Scan\_Georeference\_QAQC  
├── 05\_KMZ\_KML\_to\_GPKG  
├── 06\_Master\_GeoPackage\_Schema  
├── 07\_Data\_Confidence\_Ranking  
└── 08\_Master\_QGIS\_Project\_Setup

## **Step-by-step methodology**

6. QGIS project үүсгэнэ: XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz.  
7. Project CRS-г WGS 84 / UTM Zone 47N, EPSG:32647 болгож тохируулна.  
8. MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz-г import хийж GeoPackage layer болгон хадгална.  
9. Raster бүрийн CRS, resolution, extent, NoData, band count, pixel alignment, sidecar availability-г шалгана.  
10. Scan map бүрт georeference QA/QC: GCP count, residual, map scale, grid/tick consistency, reviewer/date/decision бүртгэнэ.  
11. Master GeoPackage schema үүсгэнэ: license\_boundary, geology\_units\_polygon, faults\_structures\_line, intrusive\_contacts\_line, mineral\_occurrences\_point, stream\_sediment\_anomaly\_polygon, heavy\_mineral\_anomaly\_polygon, lineament\_interpretation\_line, preliminary\_prospect\_polygon, target\_polygon, field\_observation\_point, sample\_point, pXRF\_reading\_table.  
12. Data confidence ranking: High / Medium / Low / Needs verification өгнө.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| EPSG:32647 project CRS | Recorded in phase QA/QC log; reviewer/date/decision required. |
| KMZ boundary topology valid | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Raster CRS/resolution/extent/nodata/band count checked | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Scan georeference residual and confidence logged | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Master GPKG schema created | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Master\_GIS\_Database.gpkg  
* XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz  
* XV-023222\_Buduunkhad\_CRS\_Georeference\_QAQC\_Log.xlsx  
* XV-023222\_Buduunkhad\_Data\_Confidence\_Ranking.xlsx

## **Decision gate / next phase condition**

* Master GIS project opens without missing layers; critical data confidence recorded.

Нэмэлт дэд аргачлал: Historical scanned map файлуудыг QGIS дээр inventory \-\> georeference \-\> vector digitizing \-\> register \-\> QA/QC \-\> confidence ranking \-\> Master GIS handover дарааллаар боловсруулах нарийвчилсан SOP-ийг энэ баримт бичгийн Appendix E хэсэгт бүрэн оруулав. Энэ дэд аргачлал нь Phase 1 Data Audit, Phase 3 Geological/Metallogenic Synthesis, Phase 4 Prospect Ranking, Phase 6 Recon Mapping, Phase 7 Sampling, Phase 8/9 Soil/Stream/Heavy Mineral planning-д шууд handover хийх зориулалттай.

# **02\. Phase 2 — Remote Sensing Preprocessing**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Sentinel, ASTER, KOMPSAT, DEM өгөгдлийг QA/QC-тэй interpretation-ready support layer болгох. |
| Input files | Direct raw input files: №9-22 DEM/ALOS/ASTERGDEM; №23-46 KOMPSAT-2 PAN/MS/RPC/EPH/metadata/browse; №73 ASTER HDF; №74-78 Sentinel/Google/basemap rasters. Exact filename бүрийг Section 1A болон Section 1 register-ээс авна. |
| Software / equipment | SNAP 13.0.0, ASTER workflow v5/ILWIS, ILWIS 3.6.8 or QGIS, Global Mapper 24.0/QGIS. |

## **Processing folder structure**

02\_Phase\_2\_Remote\_Sensing\_Preprocessing/  
├── 01\_Sentinel2\_SNAP13  
├── 02\_ASTER\_Workflow\_v5  
├── 03\_KOMPSAT2\_ILWIS368\_QGIS  
├── 04\_ALOS\_ASTERGDEM\_GlobalMapper\_QGIS  
├── 05\_RemoteSensing\_QAQC  
└── 06\_Export\_EPSG32647

## **Step-by-step methodology**

13. Sentinel-2 raw/received raster status шалгана; L1C бол SNAP 13.0.0 Sen2Cor ашиглан L2A болгоно; received derivative бол metadata-г бүртгэнэ.  
14. Subset: license boundary \+ 500 m эсвэл 1 km buffer.  
15. Resample: all relevant bands to 10 m grid; pixel alignment шалгана.  
16. Cloud/shadow/snow/water/vegetation mask үүсгэж alteration/lithology interpretation-д noise орохоос сэргийлнэ.  
17. Sentinel RGB/index: Natural RGB, SWIR-NIR-Red, geology composite, lithology ratio/index, NDVI, NDWI, iron oxide, ferric, clay/SWIR, ferrous, brightness index.  
18. ASTER workflow v5: HDF import, band extraction, UTM47 project grid, b\*\_project band-аас index тооцох; haze/edge filter-ийг ratio calculation-д ашиглахгүй.  
19. ASTER outputs тусад нь хадгална: raw Float32 score, 1/2/3 class, 0/1 binary mask.  
20. KOMPSAT-2: PAN/MS, RPC, EPH, TXT metadata-г хамт хадгалж orthorectification/band alignment/pan-sharpen/NDVI/lineament-outcrop basemap гаргана.  
21. ALOS-PALSAR/ASTER GDEM: hillshade, slope, aspect, contour, drainage, watershed, terrain ruggedness, curvature, access/safety derivatives гаргана.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Cloud/shadow/vegetation mask applied where relevant | Recorded in phase QA/QC log; reviewer/date/decision required. |
| ASTER raw score/class/binary mask separated | Recorded in phase QA/QC log; reviewer/date/decision required. |
| KOMPSAT PAN/MS alignment checked | Recorded in phase QA/QC log; reviewer/date/decision required. |
| DEM derivatives visually and spatially checked | Recorded in phase QA/QC log; reviewer/date/decision required. |
| No remote sensing output treated as ore proof | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Sentinel2\_Processed\_Products.tif/gpkg  
* XV-023222\_Buduunkhad\_ASTER\_score\_porphyry\_alteration\_raw\_v1.tif  
* XV-023222\_Buduunkhad\_ASTER\_porphyry\_potential\_class\_v1.tif  
* XV-023222\_Buduunkhad\_ASTER\_porphyry\_final\_target\_binary\_mask\_v1.tif  
* XV-023222\_Buduunkhad\_KOMPSAT2\_Pansharpened\_Orthobasemap.tif  
* XV-023222\_Buduunkhad\_Terrain\_Derivatives.gpkg  
* XV-023222\_Buduunkhad\_RemoteSensing\_QAQC\_Report.docx

## **Decision gate / next phase condition**

* Remote sensing derivatives passed QA/QC and are ready as support evidence only.

# **03\. Phase 3 — Geological, Metallogenic and CMCS Synthesis**

### Purpose and scope

Энэ өргөтгөсөн Phase 3 аргачлал нь Бүдүүн хад / XV-023222 / L23222 талбайн tectonic, geology, mineral occurrence, prospectivity, source material, metallogenic context болон CMCS/MRPAM орд-илрэлийн мэдээллийг нэг Master GIS evidence base болгон нэгтгэх нарийвчилсан SOP юм.

*Phase 3 нь хүдэржилт батлах, нөөц/баялаг тогтоох шат биш. Энэ шатны бүх output нь Historical only / Contextual support / Preliminary interpretation статустай байна. Field validation, laboratory assay, structural/geological confirmation болон шаардлагатай бол trench/geophysics/scout drilling хийгдэх хүртэл decision-grade evidence гэж үзэхгүй.*

### 03.1 Phase 3 input control

Phase 3-д input-ийг “geology files” гэх мэт ерөнхий нэрээр бичихгүй. Доорх raw input № болон exact filename-ийг output бүрийн source traceability талбарт заавал хадгална.

| Raw input № | Exact input group / file use | Phase 3 use | Mandatory limitation flag |
| :---- | :---- | :---- | :---- |
| №1-7 | Tectonic / terrane context images and explanatory pages | Lake Terrane, Ulaanshand Zone, Nuur Accretionary Megazone and regional tectonic setting | Regional context only; not local target proof |
| №8 | MN\_BuduunKhad\_L23222\_LicenseBoundary\_WGS84\_v01\_raw.kmz | Overlay, clipping, 5 km / 10 km / 20 km / 25 km buffer and CMCS/MRPAM search boundary | Boundary topology and CRS must be checked |
| №53-56 | 1:200k and 1:50k geological map and legends | Lithology, stratigraphy, intrusive/contact, fault, vein, alteration and structural control | Scale limitation and georeference residual required |
| №57-58 | Mineral resources map and legend | Regional occurrence, ore field, anomaly and commodity context | Regional evidence only |
| №59-61 | Mineral distribution pattern, metallogenic scheme and metallogenogram | Ore district/node, ore formation, age and commodity association | Context layer; not target boundary |
| №62-65 | Prospectivity assessment, prospectivity map, source material map and legends | B-3 Tol Khar, G-1 and other prospectivity zones; routes, stations, samples, trenches/pits/sections | Historical only until field checked |
| №66-68 | Gold occurrence description, mineral occurrence/mineralized point register and XLSX table | Occurrence database, coordinate validation, commodity/lithology/structure attributes | Coordinate confidence and duplicate check required |
| №69-72 | Regional metallogenic map, legend and report books | 1:500k metallogenic belt, ore formation, regional commodity context | Cannot be used as local ore proof |
| Phase 2 outputs | Sentinel / ASTER / KOMPSAT / DEM derivative products | Alteration, lithology contrast, lineament, exposure, drainage and access support | Support evidence only; ore proof биш |

### 03.2 Working folder structure

03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis/

├── 01\_Input\_Working\_Copy

├── 02\_Tectonic\_Terrane\_Context

├── 03\_Regional\_Metallogenic\_1M500K

├── 04\_Regional\_Geology\_Mineral\_1M200K

├── 05\_Local\_Geology\_Occurrence\_1M50K

├── 06\_Source\_Materials\_and\_Prospectivity

├── 07\_Occurrence\_Register\_and\_Coordinate\_QAQC

├── 08\_CMCS\_MRPAM\_Buffer\_Check\_5km\_10km\_20km\_25km

├── 09\_Geological\_Evidence\_Layers\_GPKG

├── 10\_Preliminary\_Deposit\_Model\_03A

├── 11\_Evidence\_Scoring\_and\_DataGap

└── 12\_Phase3\_QAQC\_and\_Handover

### 03.3 Pre-start readiness check

| Readiness item | Acceptance requirement | Output / register to check |
| :---- | :---- | :---- |
| Master QGIS project | Project CRS \= WGS 84 / UTM Zone 47N, EPSG:32647; no critical missing layers | XV-023222\_Buduunkhad\_Master\_QGIS\_Project.qgz |
| License boundary | №8 boundary imported, topology checked, area/perimeter recorded, EPSG:32647 version available | LicenseBoundary\_EPSG32647.gpkg and QA/QC register |
| Scan georeference QA/QC | GCP count, residual, map scale, grid/tick consistency and reviewer/date/decision recorded | CRS\_Georeference\_QAQC\_Log.xlsx |
| Remote sensing support outputs | Sentinel/ASTER/KOMPSAT/DEM products are clipped/reprojected and marked support evidence only | RemoteSensing\_QAQC\_Report.docx |
| Data confidence ranking | Each raw and derived input has High / Medium / Low / Needs verification status | Data\_Confidence\_Ranking.xlsx |

### 03.4 Step-by-step methodology

#### Step 1 — Create Phase 3 working copy and source traceability register

1\. Copy Phase 3 raw inputs №1-7, №53-72 and boundary №8 from 00\_Raw\_Files\_Archive to 03/01\_Input\_Working\_Copy. Do not edit the raw archive.

2\. Create a Phase3\_Source\_Traceability\_Register with source\_raw\_input\_no, source\_raw\_filename, source\_group, processing\_phase, processing\_software, processing\_action, confidence, limitation, validation\_status and output\_filename.

3\. Set validation\_status \= Historical only for all scanned historical map-derived layers until field/lab confirmation is available.

#### Step 2 — Build tectonic and terrane context package from №1-7

1\. Register Lake Terrane, Lake island arc terrane, Ulaanshand Zone, Nuur Accretionary Megazone and related regional tectonic context.

2\. If a map has recognizable grid/ticks, georeference in QGIS; otherwise record as non-spatial narrative context.

3\. Digitize only defensible regional polygons/lines and mark them as context\_only \= Yes.

#### Step 3 — Process 1:500,000 regional metallogenic context from №69-72

1\. Create ore formation / commodity / metallogenic belt symbol dictionary from №69.

2\. Georeference №70 where possible; overlay with license boundary and 5 km / 10 km / 20 km buffers.

3\. Extract relevant ore formation and regional context notes from №71-72 and cross-reference them with the georeferenced map.

4\. Record source\_scale \= 1:500,000 and limitation \= Regional context only.

#### Step 4 — Process 1:200,000 regional geology and mineral resources from №53-58

1\. Georeference №53 geological map and digitize regional geology units, faults/structures, intrusive/contact lines and major lithological packages.

2\. Create lithology/age/intrusive/structure lookup tables from №54.

3\. Georeference №57 mineral resources map and digitize mineral occurrence, mineralized zone, ore field/prospect and anomaly features.

4\. Create commodity/occurrence/anomaly symbol dictionary from №58.

#### Step 5 — Process 1:50,000 local geology, occurrence and prospectivity from №55-65

1\. Georeference №55 and digitize local geology units, detailed structures, faults, contacts, veins/dykes, alteration and section lines.

2\. Use №56 to build stratigraphic\_unit, lithology, intrusive, alteration, vein\_type and structure domain values.

3\. Georeference №60 and digitize Au-Cu, Cu, Mo, As, Zn and related occurrence points/features.

4\. Georeference №63 and digitize B-3 Tol Khar, G-1 and other prospectivity target polygons with evidence\_basis and priority attributes.

5\. Georeference №64 and digitize route lines, observation points, sample points, trench/pit/shaft/channel and section features; use №65 as domain dictionary.

#### Step 6 — Extract and QA/QC occurrence registers from №66-68

1\. Extract coordinates, grades, commodities, lithology, structure, alteration and notes from №66.

2\. Extract and clean scanned PDF table/register content from №67; link occurrences to source pages where possible.

3\. Clean XLSX fields from №68; standardize element and commodity names; convert coordinates to EPSG:32647.

4\. Cross-check map-derived occurrence points from №60 against text/table-derived points from №66-68; flag duplicates and uncertain coordinates.

## **Step 7 — CMCS/MRPAM 5 km / 10 km / 20 km / 25 km contextual check**

1\. Create 5 km, 10 km, 20 km and 25 km buffers from the checked license boundary. Use 25 km as the all-near-occurrence coverage buffer when 20 km does not include the full BH\_near\_min\_occurrences dataset.

2\. Query or compile nearest deposits, occurrences, mineralized points, commodity, deposit type, direction and distance from CMCS/MRPAM or equivalent official register.

3\. Create CMCS\_Nearest\_Deposit\_Register and map. Add limitation: Context only — not proof of mineralization inside license.

## **Step 7A — 25 km near-occurrence coverage buffer for all nearby mineral occurrences**

Rationale. During the spatial check of the BH\_near\_min\_occurrences point layer, the 20 km buffer did not include all near-occurrence points, while the 25 km buffer included the full nearby occurrence dataset. Therefore, the 25 km buffer shall be retained as an additional coverage buffer for regional occurrence context analysis.

Important limitation. The 25 km buffer is not a mineralization proof boundary and must not be treated as evidence that mineralization occurs inside the XV-023222 / L23222 license. It is only a regional context and occurrence-coverage tool for screening analogue mineral systems, commodity associations, metallogenic setting, and follow-up prioritization.

### **QGIS method for 25 km buffer creation**

* Use the checked license boundary layer in EPSG:32647. Do not create a metric buffer from EPSG:4326 latitude/longitude geometry.  
* Run Vector \-\> Geoprocessing Tools \-\> Buffer.  
* Input layer: license\_boundary\_EPSG32647.  
* Distance: 25000 meters; Segments: 30; Dissolve result: checked.  
* Save output as XV023222\_Buduunkhad\_L23222\_Buffer\_25km\_EPSG32647.gpkg with layer name license\_boundary\_buffer\_25km.  
* Use Select by Location to confirm that BH\_near\_min\_occurrences points intersect or are within license\_boundary\_buffer\_25km.  
* Export selected points as BH\_near\_mineral\_occurrences\_within\_25km\_EPSG32647.gpkg and retain source\_raw\_input\_no/source\_raw\_filename or occurrence register references where available.

### **Recommended buffer interpretation hierarchy**

* 5 km buffer: immediate license-margin context and high-priority near-boundary check.  
* 10 km buffer: local exploration context and short-range analogue occurrence check.  
* 20 km buffer: standard regional context check used for CMCS/MRPAM nearest deposits and occurrences.  
* 25 km buffer: all-near-occurrence coverage buffer for this dataset because it captures all nearby mineral occurrence points that were not fully covered by the 20 km buffer.

### **Additional expected outputs from Step 7A**

* XV023222\_Buduunkhad\_L23222\_Buffer\_25km\_EPSG32647.gpkg  
* BH\_near\_mineral\_occurrences\_within\_25km\_EPSG32647.gpkg  
* XV023222\_Buduunkhad\_25km\_Near\_Occurrence\_Coverage\_Check\_Register\_v01.xlsx  
* XV023222\_Buduunkhad\_25km\_Near\_Occurrence\_Context\_Map\_v01.pdf

## Step 8 — Integrate all Phase 3 evidence into one GeoPackage

1\. Merge cleaned layers into XV023222\_Buduunkhad\_Geological\_Evidence\_Layers\_v01.gpkg.

2\. Every layer must carry source\_raw\_input\_no, source\_raw\_filename, source\_scale, evidence\_type, validation\_status, confidence and limitation.

3\. Apply consistent symbology and layer naming so Phase 4 and Phase 10 can use the package without re-processing raw scans.

#### Step 9 — Prepare Preliminary Deposit Model handover to 03A

1\. Summarize host geology, intrusive/contact, structure, occurrence, geochemistry, metallogenic context and remote sensing support by candidate model.

2\. Prepare supporting\_evidence / missing\_evidence / recommended\_validation\_work table for Au-Cu hydrothermal vein, intrusion-related Cu-Au-Mo, skarn/contact metasomatic, polymetallic vein, VMS possibility and heavy mineral/placer indicator.

3\. Calculate preliminary evidence score and data-gap priority using the 100-point model matrix in 03A.

#### Step 10 — Prepare Phase 3 QA/QC and handover package

1\. Review georeference residuals, scale limitations, coordinate confidence, duplicate occurrences, CMCS limitation and support-evidence flags.

2\. Export final Phase 3 maps, registers, GPKG and QA/QC log.

3\. Handover to Phase 4 only after source traceability and validation\_status fields are complete.

### 03.5 Expected output package

| Output file / layer | Purpose | Required source-traceability fields |
| :---- | :---- | :---- |
| XV023222\_Buduunkhad\_Tectonic\_Terrane\_Context\_Register\_v01.xlsx | Terrane / tectonic narrative and source confidence register | source\_raw\_input\_no, source\_raw\_filename, confidence, limitation |
| XV023222\_Buduunkhad\_Tectonic\_Context\_Layers\_v01.gpkg | Regional terrane and tectonic context layers | context\_only, source\_scale, validation\_status |
| XV023222\_Buduunkhad\_RegionalMetallogenic\_Context\_Map\_v01.pdf | 1:500k metallogenic context layout | source\_raw\_input\_no, source\_scale, limitation |
| XV023222\_Buduunkhad\_RegionalMetallogenic\_Evidence\_Register\_v01.xlsx | Metallogenic report/map extracted evidence | report\_book, page\_ref, evidence\_summary, limitation |
| geology\_units\_200k\_polygons\_EPSG32647\_v01.gpkg | Regional geology units | source\_scale, lithology\_code, confidence |
| geology\_units\_50k\_polygons\_EPSG32647\_v01.gpkg | Local target-scale geology units | source\_scale, stratigraphic\_unit, lithology, confidence |
| faults\_structures\_50k\_lines\_EPSG32647\_v01.gpkg | Local structural control layer | structure\_type, confidence, limitation |
| mineral\_occurrences\_points\_EPSG32647\_v01.gpkg | Historical occurrence and mineralized point layer | commodity, occurrence\_type, validation\_status |
| prospectivity\_target\_zones\_polygons\_EPSG32647\_v01.gpkg | B-3 Tol Khar / G-1 / other prospectivity zones | priority, evidence\_basis, limitation |
| source\_material\_observation\_points\_EPSG32647\_v01.gpkg | Routes, observations, samples, trenches/pits and source material features | work\_type, observation\_type, sample\_type |
| XV023222\_Buduunkhad\_CMCS\_Nearest\_Deposit\_Register\_v01.xlsx | Nearest deposit / occurrence contextual register | distance\_km, direction, context\_only |
| XV023222\_Buduunkhad\_Geological\_Evidence\_Layers\_v01.gpkg | Single integrated Phase 3 evidence package | all mandatory traceability fields |
| XV023222\_Buduunkhad\_Preliminary\_Deposit\_Model\_v01.docx | 03A conceptual deposit model document | source evidence references and data-gap table |
| XV023222\_Buduunkhad\_Phase3\_QAQC\_Log\_v01.xlsx | QA/QC decision record | reviewer, review\_date, qaqc\_status, decision |

### 03.6 Mandatory GeoPackage layer schema

| Field name | Required content | Why it is required |
| :---- | :---- | :---- |
| source\_raw\_input\_no | 1-78 input number | Links each output back to original raw data |
| source\_raw\_filename | Exact raw filename | Prevents loss of file provenance |
| source\_group | Evidence group name | Allows filtering by data family |
| processing\_phase | 03 or 03A | Shows where the layer/table was created |
| processing\_software | QGIS / Excel / Word / PDF reader / etc. | Reproducibility |
| source\_scale | 1:50k / 1:200k / 1:500k / text / table / unknown | Prevents overinterpretation of regional data |
| evidence\_type | geology / structure / occurrence / metallogenic / prospectivity / CMCS context | Supports scoring and filtering |
| validation\_status | Historical only / Field checked / Sampled / Lab confirmed | Separates historical evidence from confirmed evidence |
| confidence | High / Medium / Low / Needs verification | Controls decision confidence |
| limitation | Scale, scan, georef, coordinate or context limitation | Avoids misuse as direct proof |
| qaqc\_status | Draft / Checked / Approved / Rejected | Controls release status |
| processing\_version | v01 / v02 / ... | Version control |

### 03.7 QA/QC checklist

| QA/QC item | Acceptance criterion | Pass / fail consequence |
| :---- | :---- | :---- |
| Raw preservation | No raw file overwritten; all work done on processing copy | Fail \= stop and restore from archive |
| CRS control | All spatial deliverables exported or displayed in EPSG:32647; native CRS retained in metadata | Fail \= reproject/metadata correction |
| Georeference quality | GCP count, residual, scale and grid consistency recorded for each scanned map | Fail \= confidence lowered or map not used for spatial decision |
| Scale limitation | 1:500k / 1:200k / 1:50k evidence not mixed without source\_scale field | Fail \= scoring not allowed |
| Occurrence coordinate validation | №60, №66, №67 and №68 cross-checked; duplicate/uncertain points flagged | Fail \= occurrence layer remains Draft |
| CMCS/MRPAM limitation | Marked context\_only and not used as direct proof inside license | Fail \= report/map correction required |
| Remote sensing limitation | Sentinel/ASTER/KOMPSAT/DEM marked support evidence only | Fail \= interpretation note correction required |
| Historical evidence separation | Historical scanned map vectors use validation\_status \= Historical only | Fail \= Phase 4 handover blocked |
| Deposit model table | Supporting, missing and validation work fields completed for each candidate model | Fail \= 03A incomplete |
| Handover readiness | GPKG, registers, maps and QA/QC log complete | Fail \= no Phase 4 handover |

### 03.8 Decision gate and handover to Phase 4 / Phase 10

Phase 3 is complete only when the geological evidence package can be used by Phase 4 without returning to raw scans, and when every derived layer/table/report can be traced back to exact raw input numbers and filenames.

| Handover item | Used in Phase 4 | Updated in Phase 10 |
| :---- | :---- | :---- |
| Geological\_Evidence\_Layers.gpkg | Evidence overlay and prospect polygon delineation | Final integrated interpretation and target sheets |
| Occurrence and mineralized point database | Known occurrence score and field validation priority | Re-scored after field/lab confirmation |
| Metallogenic context register/map | Regional model-fit support | Context remains support unless validated locally |
| CMCS nearest deposit register | Context and analogue comparison | Not upgraded to proof unless local evidence confirms |
| Preliminary Deposit Model.docx and score matrix | dominant\_deposit\_model, model\_confidence and validation\_priority fields | Model-fit confidence updated with field/lab results |
| Phase3\_QAQC\_Log.xlsx | Go / Conditional Go / Hold control | Audit trail for final decision |

### 03.9 Phase 3 completion criteria

* №1-8 and №53-72 have been processed, registered or explicitly marked not usable with limitation.  
* All georeferenced scanned map outputs have GCP/residual/scale/confidence records.  
* Occurrence and mineralized point coordinates from map, table and text sources have been cross-checked.  
* CMCS/MRPAM 5 km, 10 km, 20 km and 25 km contextual/coverage register is complete and clearly marked context only. The 25 km buffer is specifically retained to capture all nearby occurrence points in the BH\_near\_min\_occurrences dataset.  
* Preliminary Deposit Model evidence table is ready for 03A and Phase 4 scoring.  
* Every output contains source\_raw\_input\_no, source\_raw\_filename, processing\_phase, confidence, limitation and validation\_status.  
* Phase 4 A/B/C/D preliminary ranking can start without reprocessing raw Phase 3 input files.

# **03A. Preliminary Deposit Model Preparation — Phase 3 доторх дэд workflow**

Энэ хэсэг нь XV-023222\_Buduunkhad\_Preliminary\_Deposit\_Model.docx файлыг бэлтгэх аргачлалыг үндсэн workflow-ийн Phase 3 дотор байрлуулсан болно. Энэ нь Appendix биш; Phase 3-ийн Geological, Metallogenic and CMCS Synthesis ажлын заавал хийх дэд ажил бөгөөд Phase 4 preliminary prospect ranking, Phase 10 final target ranking руу шууд handover хийнэ.

Энэхүү дэд workflow нь ордын төрлийн урьдчилсан концепцийн загвар гаргах аргачлал юм. Satellite, ASTER, KOMPSAT-2, DEM, Drone/LiDAR болон pXRF output нь хүдэржилтийн баталгаа биш; эдгээр нь target generation, field validation, sampling prioritization-д ашиглах support evidence. Эцсийн confidence нь хээрийн шалгалт, дээжлэлт, лабораторийн шинжилгээ, structural/geological evidence, шаардлагатай бол trench/geophysics/scout drilling-аар баталгаажна.

## **03A.1 Зорилго ба гарах баримт бичиг**

XV-023222\_Buduunkhad\_Preliminary\_Deposit\_Model.docx нь Бүдүүн хад талбайд боломжит ордын төрлүүдийг урьдчилсан байдлаар ялгаж, ямар evidence дээр үндэслэж байгаа, ямар evidence дутуу байгаа, дараагийн ямар field/lab validation хийх шаардлагатайг тодорхойлох концепцийн загварын баримт бичиг байна.

Энэ файлыг таамгаар бичихгүй. 78 input workflow-ийн Phase 3 — Geological, Metallogenic and CMCS Synthesis шатны үр дүнд, Phase 1-ийн Master GIS database болон historical scanned map vectorization output дээр тулгуурлан гаргана.

| Талбар | Утга |
| :---- | :---- |
| Project area | Buduunkhad / XV-023222 / L23222 |
| Standard CRS | WGS 84 / UTM Zone 47N, EPSG:32647 |
| Document to be prepared | XV-023222\_Buduunkhad\_Preliminary\_Deposit\_Model.docx |
| Document type | Preliminary conceptual deposit model methodology; final resource/reserve estimate биш |
| Source workflow basis | 78 Inputs v3/v4 Enhanced workflow \+ Historical Scanned Maps QGIS Vectorization v02 Detailed |
| Workflow location | 03\_Phase\_3\_Geological\_Metallogenic\_and\_CMCS\_Synthesis / 07\_Preliminary\_Deposit\_Model\_Preparation |

## **03A.2 Ашиглах input evidence**

| Input evidence | Ашиглах мэдээлэл | Deposit model-д өгөх үүрэг |
| :---- | :---- | :---- |
| Геологийн суурь зураг | 1:50,000, 1:200,000 geology map, legend, lithology, intrusive, structure, fault, vein, alteration. | Host rock, intrusive contact, structural control, local/regional geology. |
| Ашигт малтмалын илрэл, эрдэсжсэн цэг | Mineral occurrence map, mineral resources map, 7255 register, 4186 gold occurrence description, mineralized point table. | Au, Cu, Mo, As, Zn, Pb, W, Sn, Bi element association болон historical occurrence evidence. |
| Металлогений зураг, тайлан | 1:500,000 metallogenic map, L47B regional metallogenic report, metallogenic scheme/metallogenogram. | Metallogenic belt, ore formation, ore district/node context. Local target boundary биш. |
| Historical scanned map vector output | Georeferenced raster, geology, structure, occurrence, stream sediment, heavy mineral, prospectivity target vector layers. | Historical evidence database. validation\_status \= Historical only гэж хадгална. |
| Remote sensing support | Sentinel, ASTER, KOMPSAT, DEM, ALOS-PALSAR derivative layers. | Alteration, lithology, lineament, terrain, drainage, exposure support. Ore proof биш. |

## **03A.3 Ажлын үндсэн дараалал**

### **Алхам 1 — Evidence layer-үүдийг Master GIS дээр нэгтгэх**

QGIS дээр license\_boundary, geology\_units\_50k/200k, structures\_faults\_lines, intrusive\_contacts\_lines, mineral\_occurrences\_points, mineralized\_zones, stream\_sediment\_anomaly, heavy\_mineral\_anomaly, prospectivity\_target\_zones, metallogenic\_zones, Sentinel/ASTER/KOMPSAT/DEM support layer-үүдийг EPSG:32647 CRS-тэй нэг project-д давхарлана.

### **Алхам 2 — Historical map-уудаас ордын төрлийн evidence ялгах**

Historical scanned map vectorization workflow-ийн дагуу map type бүрээс host geology, structure, occurrence, geochemical anomaly, heavy mineral, prospectivity zone, metallogenic context ялгана. Historical vector data-г field/lab confirmed data-тай холихгүй.

### **Алхам 3 — Deposit model candidate-уудыг тодорхойлох**

Au-Cu hydrothermal vein, intrusion-related Cu-Au-Mo, skarn/contact metasomatic, polymetallic vein, VMS-type sulphide possibility, heavy mineral/placer indicator гэсэн candidate model бүрийг тусад нь шалгана.

### **Алхам 4 — Supporting evidence / missing evidence / validation work хүснэгт гаргах**

Ордын төрөл бүр дээр одоо байгаа evidence, дутуу evidence, баталгаажуулах ажлыг хүснэгтээр үнэлнэ.

### **Алхам 5 — Evidence weight ашиглаж preliminary ranking хийх**

Deposit model тус бүрт 100 онооны matrix-ээр оноо өгч High priority model / Moderate priority model / Low conceptual model / Insufficient evidence гэж ангилна.

| Map type | Deposit model-д авах мэдээлэл |
| :---- | :---- |
| Geological map | Host rock, intrusive contact, volcanic/intrusive package, structure. |
| Mineral occurrence map | Au-Cu, Cu, Mo, As, Zn зэрэг илрэл. |
| Mineral resources map | Regional occurrence, ore field, anomaly. |
| Stream sediment map | Cu-Pb-Zn-Ag-As-Bi-W-Sn-Mo-Mn-Ba-F anomaly. |
| Heavy mineral map | Au, W, Sn, Ti, Cr, magnetite зэрэг indicator. |
| Prospectivity map | Б-3 Толь хяр, Г-1 зэрэг хэтийн төлөвтэй хэсэг. |
| Metallogenic map | Ore formation, metallogenic belt, ore district context. |

## **03A.4 Deposit model candidate screening**

| Candidate deposit model | Юуг шалгах вэ? | Дутуу evidence / эрсдэл | Recommended validation work |
| :---- | :---- | :---- | :---- |
| Au-Cu hydrothermal vein | Quartz vein, pyrite, chalcopyrite, malachite, Au-Cu-Ag-As-Bi, shear/fault corridor, lineament intersection. | Au pXRF unreliable; судлын continuity, width, grade тодорхойгүй байж болно. | Recon mapping, rock chip/channel, lab Au fire assay \+ multi-element, LiDAR/structural mapping. |
| Intrusion-related Cu-Au-Mo | Diorite/granodiorite/gabbrodiorite contact, Cu-Mo-Bi-As, stockwork/quartz veinlets, ASTER/Sentinel alteration support. | Porphyry-style alteration zoning and sulphide system not confirmed. | ASTER validation, intrusive phase mapping, soil grid, IP/magnetic, trench/channel. |
| Skarn/contact metasomatic Cu-Au-W-Bi | Intrusive-carbonate contact, epidote/garnet/magnetite/skarn minerals, W-Bi-Cu-Au association. | Carbonate host and skarn mineral assemblage unclear. | Detailed contact mapping, pXRF W/Bi/Cu screening, petrography, magnetic/IP support. |
| Polymetallic vein | Pb-Zn-Cu-Ag-As association, vein/shear structures, gossan/iron oxide, historical occurrence overlap. | Depth continuity and grade continuity unknown. | Rock chip/channel, soil grid, structural mapping, lab Pb-Zn-Ag multi-element. |
| VMS-type sulphide possibility | Volcanic-sedimentary package, Cu-Zn-Pb-Ba-Fe-Mn, stratiform sulphide or gossan, regional arc/oceanic context. | Stratigraphic control and massive sulphide textures not confirmed. | Detailed stratigraphic mapping, geochemistry, IP, magnetic, targeted trenching. |
| Heavy mineral / placer indicator | Historical shlich/heavy mineral anomaly, drainage concentration, Au/W/Sn/Ti/Cr indicators. | Source may be transported/secondary; bedrock source not proven. | Drainage follow-up, upstream sampling, heavy mineral panning, geomorphology and bedrock checking. |

## **03A.5 Evidence weight ба preliminary ranking**

| Шалгуур | Оноо | Тайлбар |
| :---- | :---- | :---- |
| Favorable geology / host lithology | 20 | Host rock, intrusive/contact, volcanic-sedimentary or carbonate contact setting. |
| Intrusive/contact/structure control | 15 | Fault, shear, vein trend, lineament intersection, intrusive contact. |
| Known mineral occurrence | 15 | Historical Au-Cu/Cu/Mo/Pb-Zn/W-Sn occurrence or mineralized point. |
| Historical geochemistry / shlich / stream sediment | 15 | Cu-Au-Ag-Mo-Bi-As-Pb-Zn-W-Sn anomaly overlap, drainage source consistency. |
| Metallogenic context | 10 | Relevant metallogenic belt, ore formation, ore district/node context. |
| ASTER/Sentinel alteration support | 10 | Clay/sericite/silica/ferric/chlorite/carbonate indicators and lithology contrast. |
| Field mapping / pXRF support | 10 | Malachite, pyrite, epidote, quartz vein, elevated Cu/Pb/Zn/As/Mo/W/Sn; Au pXRF not decision-grade. |
| Access / workability | 5 | Field access, slope, drone/sampling/trenching feasibility. |
| Нийт | 100 | Deposit model тус бүрээр оноо өгнө. |

| Confidence class | Score range | Meaning |
| :---- | :---- | :---- |
| High priority model | \>=70 | Олон evidence давхцаж байгаа, field/lab follow-up priority. |
| Moderate priority model | 50-69 | Боломжтой боловч нэмэлт field/lab validation шаардлагатай. |
| Low / conceptual model | 30-49 | Contextual эсвэл дутуу evidence ихтэй. |
| Insufficient evidence | \<30 | Одоогийн өгөгдлөөр deposit model гэж дэмжихэд хангалтгүй. |

| Rank | Deposit model | Preliminary confidence | Why |
| :---- | :---- | :---- | :---- |
| 1 | Au-Cu hydrothermal vein | High / Moderate | Quartz vein, Au-Cu occurrence, structure support байвал өндөр оноо авна. |
| 2 | Intrusion-related Cu-Au-Mo | Moderate | Intrusive contact \+ Cu-Mo-Bi-As possibility \+ alteration support шалгана. |
| 3 | Skarn/contact metasomatic | Moderate / Low | Contact evidence байгаа ч carbonate/skarn mineral баталгаажуулах шаардлагатай. |
| 4 | Polymetallic vein | Moderate / Low | Pb-Zn-Cu-Ag-As association байгаа эсэхийг field/lab-аар шалгана. |
| 5 | VMS possibility | Conceptual | Regional volcanic context байж болох ч direct stratiform sulphide evidence дутуу. |
| 6 | Heavy mineral / placer | Contextual | Drainage/shlich evidence байж болох ч bedrock source тодорхойгүй. |

## **03A.6 XV-023222\_Buduunkhad\_Preliminary\_Deposit\_Model.docx санал болгох бүтэц**

* Title page: XV-023222 / L23222 Buduunkhad Preliminary Deposit Model; subtitle: Geological, Metallogenic, Historical Geochemistry, Remote Sensing and Occurrence Evidence-Based Conceptual Deposit Model.  
* Methodology note: Final resource model биш, preliminary conceptual model гэдгийг тайлбарлана.  
* Input data basis: 78 raw input-ийн аль evidence group-ээс ямар мэдээлэл авсныг хүснэгтээр оруулна.  
* Regional geological setting: Ulaanshand Zone, Nuur Accretionary Megazone, Lake island-arc terrane context.  
* Local geology and structural control: 1:50k, 1:200k geology, intrusive, fault, contact, vein, alteration.  
* Mineral occurrence and geochemical evidence: Au-Cu, Cu, Mo, As, Zn, Pb, W, Sn, Bi, stream sediment, heavy mineral evidence.  
* Remote sensing and terrain support: Sentinel, ASTER, KOMPSAT, ALOS/DEM support; ore proof биш гэдгийг заавал тэмдэглэнэ.  
* Deposit model candidate screening: 6 candidate model-ийг supporting evidence / missing evidence / recommended validation work хүснэгтээр үнэлнэ.  
* Preliminary model ranking: Хамгийн боломжтой ордын төрлийг evidence score-оор эрэмбэлнэ.  
* Recommended validation work: Historical map QA/QC, recon mapping, pXRF, sampling, orientation soil, drainage follow-up, lab assay, IP/magnetic/trench/scout drilling.

## **03A.7 Богино ажлын checklist**

* 78 input-ийн геологи, илрэл, геохими, металлогени, remote sensing evidence-г Master GIS-д нэгтгэнэ.  
* Historical scanned map-уудыг georeference \+ vectorize хийж confidence ranking өгнө.  
* Ордын боломжит төрлүүдийг Au-Cu vein, intrusion-related Cu-Au-Mo, skarn, polymetallic vein, VMS, placer/heavy mineral гэж ангилна.  
* Төрөл бүрээр байгаа evidence, дутуу evidence, баталгаажуулах ажлыг хүснэгтээр үнэлнэ.  
* Хамгийн боломжтой ордын төрлийг preliminary ranking-ээр гаргана.  
* Энэ нь final дүгнэлт биш, field validation \+ lab assay дараа шинэчлэгдэх conceptual model гэж тэмдэглэнэ.

## **03A.8 Phase 3 QA/QC notes for deposit model preparation**

* Raw data-г засварлахгүй; processing copy дээр ажиллана.  
* Final deliverables-ийн CRS нь EPSG:32647; native/raw CRS-г metadata-д хадгална.  
* Historical scanned map-derived vector data нь validation\_status \= Historical only гэж хадгалагдана.  
* Regional 1:400k/1:500k metallogenic layer-ийг local target boundary мэт ашиглахгүй.  
* ASTER final binary mask, Sentinel alteration ratio, KOMPSAT visual lineament, drone interpretation нь хүдэржилтийн баталгаа биш.  
* pXRF нь lab assay-г орлохгүй; Au-ийн pXRF response-ийг decision-grade гэж үзэхгүй.  
* CMCS/MRPAM nearest deposit нь contextual evidence бөгөөд тухайн license дотор хүдэржилт байгаа эсэхийг шууд батлахгүй.  
* Final target confidence нь хээрийн шалгалт, дээжлэлт, laboratory assay, structural/geological evidence, шаардлагатай бол trench/geophysics/scout drilling-аар баталгаажна.

Methodology guide only — not mineralization proof or resource estimate

## **03A.9 Handover from Phase 3 to Phase 4 and Phase 10**

03A дэд workflow-ийн үр дүн нь Phase 4-ийн Preliminary Prospect Delineation and Ranking-д deposit model evidence score, missing evidence, validation priority хэлбэрээр орно. Мөн Phase 10-д final target ranking хийх үед field/lab result-аар шинэчлэгдсэн conceptual model болгон дахин шалгана.

| Handover item | Phase 4-д ашиглах байдал | Phase 10-д ашиглах байдал |
| :---- | :---- | :---- |
| Deposit model candidate table | Prospect polygon бүрийн model-fit шалгуур болно. | Final target sheet-д model-fit confidence болгон шинэчилнэ. |
| Evidence weight score | Preliminary A/B/C/D ranking-ийн geology/model component болно. | Assay/field validation-аар re-score хийнэ. |
| Missing evidence / risk | Field validation, drone, recon, sampling priority гаргана. | Go/Conditional Go/No-Go decision-д data gap/risk болно. |
| Recommended validation work | Phase 5-9 ажлын дараалал, sample plan, orientation survey-г чиглүүлнэ. | Trench/geophysics/scout drilling criteria-д шилжинэ. |

# **04\. Phase 4 — Preliminary Prospect Delineation and Ranking**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Desktop evidence-үүдийг 100 онооны scoring matrix-аар preliminary prospect болгох. |
| Input files | Input files: Phase 1-3 processed outputs \+ source raw inputs №1-78 as traceable evidence basis. Key direct evidence sources: №47-52 geochemistry/field observations, №53-68 geology/occurrence/prospectivity/source materials, №69-72 metallogenic context, №9-46 and №73-78 terrain/remote sensing support, №8 license boundary. |
| Software / equipment | QGIS, scoring spreadsheet, prospect register. |

## **Processing folder structure**

04\_Phase\_4\_Preliminary\_Prospect\_Delineation\_and\_Ranking/  
├── 01\_Evidence\_Overlay  
├── 02\_Prospect\_Polygon\_Delineation  
├── 03\_Scoring\_Matrix  
├── 04\_Confidence\_DataGap\_NextAction  
└── 05\_A\_B\_C\_D\_Field\_Priority

## **Step-by-step methodology**

22. Evidence overlay үүсгэнэ: geology \+ occurrence \+ stream/heavy mineral \+ ASTER/Sentinel \+ KOMPSAT lineament/outcrop \+ DEM terrain \+ CMCS context.  
23. Prospect polygon бүрт evidence score, confidence flag, limitation/data gap, field access, safety risk, next action бүртгэнэ.  
24. A/B/C/D preliminary target class олгоно: A \>=75, B=55-74, C=35-54, D\<35.  
25. Field-ready A/B prospect-уудыг drone survey болон recon mapping-д шилжүүлнэ.

Phase 3-ийн 03A Preliminary Deposit Model Preparation-аас гарсан deposit model score, missing evidence, recommended validation work-ийг prospect scoring matrix-д заавал холбож оруулна. Prospect polygon бүрт dominant\_deposit\_model, model\_confidence, missing\_model\_evidence, validation\_priority талбар нэмнэ.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| 100-point matrix calculated | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Confidence/data gap/next action fields filled | Recorded in phase QA/QC log; reviewer/date/decision required. |
| A/B/C/D class reviewed | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Field access and safety checked | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Preliminary\_Prospect\_Ranking\_Map.pdf  
* XV-023222\_Buduunkhad\_Prospect\_Polygons.gpkg  
* XV-023222\_Buduunkhad\_Prospect\_Ranking\_Table.xlsx  
* XV-023222\_Buduunkhad\_Go\_NoGo\_Desktop\_Decision\_Matrix.xlsx

## **Decision gate / next phase condition**

* A/B prospects selected for drone and recon; C/D retained with data gaps.

# **05\. Phase 5 — DJI Matrice 400 Drone LiDAR Photogrammetry Survey**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Priority prospect дээр orthomosaic/LiDAR/terrain/structure field planning base авах. |
| Input files | Input files: Phase 4 A/B prospect polygons plus direct planning support raw inputs №8 license boundary, №9-22 DEM/slope/hillshade, №24-46 KOMPSAT basemap/lineament support, №75-78 high-resolution/Sentinel/basemap rasters. Exact filename list is in Section 1A. |
| Software / equipment | 4 x DJI Matrice 400, Zenmuse P1, Zenmuse L2, Zenmuse L3, GNSS/RTK/PPK, processing software. |

## **Processing folder structure**

05\_Phase\_5\_DJI\_Matrice\_400\_Drone\_LiDAR\_Photogrammetry\_Survey/  
├── 01\_Flight\_Block\_Design  
├── 02\_GCP\_Checkpoint\_RTK\_PPK  
├── 03\_Zenmuse\_P1\_Photogrammetry  
├── 04\_Zenmuse\_L2\_LiDAR  
├── 05\_Zenmuse\_L3\_Detailed\_LiDAR  
├── 06\_Raw\_Backup\_Flight\_Log  
├── 07\_Processing\_Orthomosaic\_PointCloud\_DTM\_DSM  
└── 08\_Drone\_QAQC\_Interpretation

## **Step-by-step methodology**

26. 4 ширхэг DJI Matrice 400-г parallel survey team болгон ашиглана: P1 orthomosaic, L2 terrain/structure, L3 detailed LiDAR, 4-р дрон backup/parallel block.  
27. Flight block design: target boundary \+ buffer, terrain/slope/access, take-off/landing/emergency area, no-fly/safety restriction.  
28. GCP/checkpoint, RTK/PPK, overlap, flight altitude, wind/weather/sun angle, battery rotation, raw backup, flight log бүртгэнэ.  
29. Zenmuse P1: high-resolution orthomosaic, oblique photo, outcrop mapping base.  
30. Zenmuse L2: DTM/DSM, terrain, drainage, slope, structural lineament.  
31. Zenmuse L3: detailed LiDAR, micro-topography, fault/contact/vein corridor.  
32. Output-уудыг field traverse, sample point, trench/drill pad planning-д ашиглана.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| GCP/checkpoint accuracy reviewed | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Flight log complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Overlap/altitude/weather recorded | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Raw photo/LiDAR backed up | Recorded in phase QA/QC log; reviewer/date/decision required. |
| DTM/DSM/orthomosaic checked | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Drone\_Flight\_Plan.pdf  
* XV-023222\_Buduunkhad\_Drone\_Orthomosaic\_P1.tif  
* XV-023222\_Buduunkhad\_Drone\_LiDAR\_PointCloud.laz  
* XV-023222\_Buduunkhad\_Drone\_DTM\_DSM.tif  
* XV-023222\_Buduunkhad\_Drone\_Structure\_Outcrop\_Interpretation.gpkg

## **Decision gate / next phase condition**

* Orthomosaic/LiDAR products meet mapping scale and field planning requirements.

# **06\. Phase 6 — Recon Mapping and Portable XRF Field Screening**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Priority target-ийг газар дээр шалгаж pXRF vectoring хийх. |
| Input files | Input files: Phase 4 target polygons \+ Phase 5 drone outputs \+ direct validation support raw inputs №55-56 detailed geology/legend, №60 mineral occurrence map, №63 prospectivity map, №64-65 source materials map/legend, №66-68 occurrence/register files, №9-22 terrain, №75-78 basemaps, №8 boundary. |
| Software / equipment | QField/QGIS forms, Olympus Vanta M, Bruker Titan S1, GPS/GNSS, camera. |

## **Processing folder structure**

06\_Phase\_6\_Recon\_Mapping\_and\_Portable\_XRF\_Field\_Screening/  
├── 01\_Traverse\_Planning  
├── 02\_Field\_Mapping\_Forms  
├── 03\_pXRF\_VantaM\_Primary  
├── 04\_pXRF\_TitanS1\_Duplicate\_Check  
├── 05\_pXRF\_QAQC\_CRM\_Blank\_Duplicate  
├── 06\_Field\_Database  
└── 07\_Recon\_Report

## **Step-by-step methodology**

33. A/B targets дээр traverse төлөвлөж lithology, alteration, mineralization, vein, structure, weathering, exposure, access, safety бүртгэнэ.  
34. Olympus Vanta M-г primary screening, Bruker Titan S1-г duplicate/cross-check байдлаар ашиглана.  
35. Өдөр бүр warm-up, calibration check, CRM, blank, duplicate, check sample уншуулна.  
36. pXRF бүртгэлд sample ID, GPS coordinate, lithology, alteration, mineralization, instrument model/serial, operator, mode, reading time, moisture/surface condition, Cu/Pb/Zn/As/Mo/W/Sn/Mn/Fe/S зэрэг element орно.  
37. Au-ийн pXRF response-ийг decision-grade evidence гэж үзэхгүй; lab assay шаардлагатай.  
38. pXRF-lab correlation sheet-д element бүрээр reliability flag өгнө.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| CRM/blank/duplicate/check sample daily | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Vanta M vs Titan S1 duplicate comparison | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Au not used as pXRF decision-grade | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Moisture/surface condition recorded | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Recon\_Traverse\_Lines.gpkg  
* XV-023222\_Buduunkhad\_Field\_Observation\_Points.gpkg  
* XV-023222\_Buduunkhad\_pXRF\_Field\_Screening\_Register.xlsx  
* XV-023222\_Buduunkhad\_pXRF\_QAQC\_Report.docx  
* XV-023222\_Buduunkhad\_Recon\_Mapping\_Report.docx

## **Decision gate / next phase condition**

* Field evidence and pXRF vectoring justify sampling or downgrade target.

# **07\. Phase 7 — Rock Chip, Channel and Verification Sampling**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Field-confirmed mineralization/alteration/structure дээр лабораторийн дээж авах. |
| Input files | Input files: Phase 6 recon/pXRF outputs \+ direct historical evidence raw inputs №52 field observation table, №55-56 detailed geology/legend, №60 mineral occurrence map, №63 prospectivity map, №64-65 source materials map/legend, №66-68 occurrence/register files, №9-22 terrain and №75-78 basemaps. |
| Software / equipment | Field sampling kit, GPS/GNSS, pXRF support, sample bags/tags, chain-of-custody forms. |

## **Processing folder structure**

07\_Phase\_7\_Rock\_Chip\_Channel\_and\_Verification\_Sampling/  
├── 01\_Sample\_Planning  
├── 02\_RockChip\_Channel\_Float\_Registers  
├── 03\_QAQC\_Insertion  
├── 04\_Chain\_of\_Custody  
├── 05\_Lab\_Submission  
└── 06\_Assay\_Import\_Preparation

## **Step-by-step methodology**

39. Recon/pXRF-ээр баталгаажсан quartz vein, gossan, malachite/sulphide, intrusive contact, shear/fault, altered lithology дээр дээж авна.  
40. Sample type: representative rock chip, selective rock chip, float, channel, verification sample.  
41. Sample ID convention: BUD-RC-001, BUD-CH-001, BUD-SOIL-001, BUD-STR-001, BUD-HM-001, BUD-QC-STD-001, BUD-QC-BLK-001, BUD-QC-DUP-001.  
42. Sample register: coordinate, photo, drone tile, pXRF reading, lithology, alteration, mineralization, structure, width/strike/dip, sample mass, collector, date/time.  
43. QA/QC: CRM/standard, blank, duplicate, field duplicate, lab duplicate, pulp duplicate; chain-of-custody ба lab submission template заавал бүрдүүлнэ.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Sample ID unique | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Coordinates/photo/chain-of-custody complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| QA/QC insertion complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Lab submission consistent with register | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Rock\_Chip\_Sampling\_Plan.pdf  
* XV-023222\_Buduunkhad\_Rock\_Chip\_Sample\_Register.xlsx  
* XV-023222\_Buduunkhad\_Rock\_Chip\_QAQC\_Plan.xlsx  
* XV-023222\_Buduunkhad\_Lab\_Submission\_RockChip.xlsx  
* XV-023222\_Buduunkhad\_Assay\_Import\_Template.xlsx

## **Decision gate / next phase condition**

* Lab submission complete and QA/QC inserted; assay import template ready.

# **08\. Phase 8 — Orientation Soil, Stream Sediment and Heavy Mineral Check**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Systematic grid өмнө soil/drainage response аргачлал баталгаажуулах. |
| Input files | Direct raw input files: №47 HeavyMineralSamplingResultsMap, №48 HeavyMineral legend, №49 StreamSediment legend, №50 StreamSediment Polyelement map, №51 field route notebook, №52 field observation table; support inputs №9-22 DEM/drainage, №53-56 geology, №60 occurrence map, №63-64 prospectivity/source materials, №68 mineralized point table. |
| Software / equipment | Soil auger/shovel/sieve, GPS, pXRF, lab submission workflow. |

## **Processing folder structure**

08\_Phase\_8\_Orientation\_Soil\_StreamSediment\_and\_HeavyMineral\_Check/  
├── 01\_Orientation\_Line\_Design  
├── 02\_Depth\_Horizon\_Mesh\_Test  
├── 03\_pXRF\_Lab\_Comparison  
├── 04\_StreamSediment\_FollowUp  
├── 05\_HeavyMineral\_FollowUp  
└── 06\_Recommended\_Systematic\_Method

## **Step-by-step methodology**

44. Systematic grid шууд эхлүүлэхгүй; эхлээд orientation survey хийж horizon/depth/mesh/spacing response баталгаажуулна.  
45. Depth test: 20 cm, 40 cm, 60-80 cm. Horizon: A/B/C/residual/transported.  
46. Mesh/fraction test, soil texture, carbonate, clay, slope position, drainage/alluvial influence тэмдэглэнэ.  
47. pXRF \+ lab comparison-аар ямар element suite, horizon, depth, spacing илүү anomaly өгч байгааг тодорхойлно.  
48. Historical stream sediment/heavy mineral map-тай drainage catchment analysis хийж upstream source direction болон follow-up point төлөвлөнө.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Depth/horizon/mesh comparison complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Transported vs residual flag | Recorded in phase QA/QC log; reviewer/date/decision required. |
| pXRF-lab comparison done | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Drainage source logic documented | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Orientation\_Soil\_Survey\_Plan.pdf  
* XV-023222\_Buduunkhad\_Orientation\_Soil\_Sample\_Register.xlsx  
* XV-023222\_Buduunkhad\_Orientation\_Soil\_pXRF\_Lab\_Comparison.xlsx  
* XV-023222\_Buduunkhad\_StreamSediment\_FollowUp\_Plan.pdf  
* XV-023222\_Buduunkhad\_HeavyMineral\_FollowUp\_Plan.pdf

## **Decision gate / next phase condition**

* Best horizon/depth/mesh/spacing confirmed before systematic grid.

# **09\. Phase 9 — Systematic Soil Grid and Laboratory QA/QC**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Validated method-оор systematic soil geochemical coverage хийх. |
| Input files | Input files: Phase 8 orientation results \+ direct planning support raw inputs №8 boundary, №9-22 DEM/slope/drainage, №47-52 historical drainage/heavy mineral/field evidence, №55/60/63/64/68 local geology-occurrence-source evidence, №75-78 basemaps/Sentinel support. Exact filenames in Section 1A. |
| Software / equipment | QGIS grid design, field collection tools, pXRF, laboratory assay. |

## **Processing folder structure**

09\_Phase\_9\_Systematic\_Soil\_Grid\_and\_Laboratory\_QAQC/  
├── 01\_Grid\_Design\_200x50\_100x25\_50x25\_25x10  
├── 02\_Field\_Collection  
├── 03\_pXRF\_Screening  
├── 04\_Lab\_Submission\_QAQC  
├── 05\_Assay\_Validation  
└── 06\_Soil\_Anomaly\_Map

## **Step-by-step methodology**

49. Orientation result-оор grid spacing сонгоно: Recon 200 m x 50 m, Target 100 m x 25 m, Infill 50 m x 25 m, Vein detail 25 m x 10 m.  
50. Grid orientation нь geological strike, structural trend, drainage/slope-д нийцсэн байна.  
51. pXRF realtime screening ашиглаж field vectoring хийж болох боловч final map lab assay дээр үндэслэнэ.  
52. QA/QC insertion schedule: CRM, blank, duplicate, field duplicate, lab repeat, pulp duplicate.  
53. Assay validation: unit conversion, detection limit, duplicate/CRM/blank performance, outlier check.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Grid spacing justified by orientation results | Recorded in phase QA/QC log; reviewer/date/decision required. |
| QA/QC performance acceptable | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Assay unit/detection limit validated | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Anomaly continuity checked | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Systematic\_Soil\_Grid\_Plan.pdf  
* XV-023222\_Buduunkhad\_Soil\_Sample\_Points.gpkg  
* XV-023222\_Buduunkhad\_Soil\_Sample\_Register.xlsx  
* XV-023222\_Buduunkhad\_Soil\_QAQC\_Report.docx  
* XV-023222\_Buduunkhad\_Soil\_Assay\_Results.xlsx

## **Decision gate / next phase condition**

* Validated geochemical anomaly supports final target ranking.

# **10\. Phase 10 — Integrated Interpretation and Final Target Ranking**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Бүх evidence, assay QA/QC, remote/drone/field data-г final target decision болгон нэгтгэх. |
| Input files | Input files: All validated phase outputs \+ full traceable raw evidence basis №1-78. Final target sheets must reference exact source raw input filenames from Section 1A/Section 1, not only generic evidence group names. |
| Software / equipment | QGIS, spreadsheet/statistical validation, report templates. |

## **Processing folder structure**

10\_Phase\_10\_Integrated\_Interpretation\_and\_Final\_Target\_Ranking/  
├── 01\_Assay\_Validation  
├── 02\_Evidence\_Integration  
├── 03\_Target\_Scoring  
├── 04\_Target\_Description\_Sheets  
├── 05\_Go\_NoGo\_Decision  
└── 06\_Final\_Target\_GIS\_Map\_Report

## **Step-by-step methodology**

54. Geology, metallogeny, mineral occurrence, stream sediment, heavy mineral, Sentinel, ASTER, KOMPSAT, ALOS DEM, drone, LiDAR, field mapping, pXRF, rock chip/channel assay, soil assay, CMCS context-ийг нэгтгэнэ.  
55. Assay validation: unit conversion, detection limits, duplicate check, CRM/blank performance, pXRF-lab correlation, outlier check.  
56. ASTER/Sentinel support layers-ийг field/lab evidence-тэй давхарлаж зөвхөн validation-supported target polygon болгон засварлана.  
57. Final target description sheet бүрт target ID, location, evidence summary, geology, structure, alteration, geochemistry, remote sensing, drone/LiDAR, sampling result, confidence, risk/data gap, recommended follow-up, Go/No-Go decision бичнэ.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| All evidence layers version-controlled | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Assay QA/QC passed | Recorded in phase QA/QC log; reviewer/date/decision required. |
| pXRF-lab correlation documented | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Target sheets complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Go/No-Go decision recorded | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Integrated\_Interpretation\_Report.docx  
* XV-023222\_Buduunkhad\_Integrated\_Geology\_Geochemistry\_Alteration\_Map.pdf  
* XV-023222\_Buduunkhad\_Final\_Target\_Polygons.gpkg  
* XV-023222\_Buduunkhad\_Final\_Target\_Ranking\_Table.xlsx  
* XV-023222\_Buduunkhad\_Target\_Description\_Sheets.docx

## **Decision gate / next phase condition**

* Final A/B targets have sufficient evidence for trench/geophysics/scout drill planning.

# **11\. Phase 11 — Follow-up Trench, Geophysics and Scout Drill Planning**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Final A/B target дээр trench, geophysics, scout drilling төлөвлөх. |
| Input files | Input files: Phase 10 final A/B targets \+ direct planning support raw inputs №8 boundary, №9-22 DEM/slope/hillshade, №55 detailed geology, №60 occurrence map, №63 prospectivity map, №64 source materials map, №68 mineralized point table, №75-78 basemap/Sentinel rasters. |
| Software / equipment | QGIS, trench/geophysics planning tools, drilling design spreadsheet, HSE/budget templates. |

## **Processing folder structure**

11\_Phase\_11\_Follow\_Up\_Trench\_Geophysics\_and\_Scout\_Drill\_Planning/  
├── 01\_Trench\_Channel\_Planning  
├── 02\_IP\_Resistivity\_Planning  
├── 03\_Magnetic\_Survey\_Planning  
├── 04\_Infill\_Soil\_Planning  
├── 05\_Scout\_Drill\_Collar\_Design  
├── 06\_HSE\_Environment\_Rehabilitation  
└── 07\_Budget\_Permit\_Schedule

## **Step-by-step methodology**

58. Trench/channel хийх нөхцөл: surface mineralization \+ lab/pXRF response \+ accessible slope \+ geometry trace.  
59. IP/resistivity хийх нөхцөл: disseminated sulphide/chargeability target эсвэл covered anomaly; line orientation нь structure/geology-г огтлох.  
60. Magnetic survey хийх нөхцөл: intrusive/mafic/contact/structure ялгах шаардлагатай үед.  
61. Infill soil хийх нөхцөл: open-ended soil anomaly, low spacing confidence, transported cover uncertainty.  
62. Scout drilling minimum criteria: confirmed surface mineralization, lab assay support, structure confirmed, favorable geology/contact, target geometry estimated, access/HSE possible, trench/geophysics recommended or completed.  
63. Drill collar table: collar ID, Easting/Northing, RL, azimuth, dip, depth, target, section line, access, pad, water, HSE, rehabilitation, budget.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Minimum scout drill criteria met | Recorded in phase QA/QC log; reviewer/date/decision required. |
| HSE/access/rehabilitation reviewed | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Drill collar geometry justified | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Budget/permit/schedule template completed | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* XV-023222\_Buduunkhad\_Follow\_Up\_Work\_Plan.pdf  
* XV-023222\_Buduunkhad\_Proposed\_Trench\_Locations.gpkg  
* XV-023222\_Buduunkhad\_Proposed\_IP\_Magnetic\_Lines.gpkg  
* XV-023222\_Buduunkhad\_Scout\_Drilling\_Proposal.docx  
* XV-023222\_Buduunkhad\_Drill\_Collar\_Table.xlsx

## **Decision gate / next phase condition**

* Scout drilling proceeds only if minimum criteria and HSE/access/permit conditions are met.

# **99\. Final Deliverables**

| Subsection | Methodology detail |
| :---- | :---- |
| Зорилго | Бүх output-ийг стандарт folder package болгон бүрдүүлэх. |
| Input files | Input files: All phase outputs and QA/QC logs, with source traceability back to raw input files №1-78. Final package must include the exact raw input filename reference from Section 1A for every evidence layer/report/table/map. |
| Software / equipment | QGIS, Office, PDF export, archive/checksum tools. |

## **Processing folder structure**

99\_Final\_Deliverables/  
├── 01\_Reports  
├── 02\_GIS\_GPKG\_QGIS\_QField  
├── 03\_Remote\_Sensing\_Products  
├── 04\_Drone\_LiDAR\_Orthomosaic\_PointCloud  
├── 05\_Field\_Forms\_and\_pXRF\_Registers  
├── 06\_Assay\_and\_QAQC\_Tables  
├── 07\_Target\_Ranking\_and\_Decision\_Matrix  
├── 08\_Follow\_Up\_Work\_Plans  
└── 09\_Final\_Report\_Package

## **Step-by-step methodology**

64. All reports, GIS, remote sensing, drone/LiDAR, field forms, assay/QAQC, target ranking, follow-up work plans and final report package-г зохион байгуулж өгнө.  
65. Final deliverables EPSG:32647 standard CRS-тэй байна; raw/native CRS болон metadata-г хадгална.  
66. Deliverable бүрт source, processing date, operator/reviewer, QA/QC status, limitation note бичнэ.

## **QA/QC check**

| QA/QC item | Acceptance note |
| :---- | :---- |
| Folder structure complete | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Files named consistently | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Metadata and limitations included | Recorded in phase QA/QC log; reviewer/date/decision required. |
| Final QA/QC notes included | Recorded in phase QA/QC log; reviewer/date/decision required. |

## **Expected outputs**

* Final report package, GIS package, remote sensing products, drone/LiDAR products, field forms, assay/QAQC tables, target ranking and follow-up plans.

## **Decision gate / next phase condition**

* Final package is internally consistent, QA/QC reviewed and ready for management/technical review.

# **3\. Remote sensing special subworkflows**

| Subworkflow | Key method | Important limitation |
| :---- | :---- | :---- |
| Sentinel-2 SNAP 13.0.0 | Raw/received status check; L1C \-\> Sen2Cor L2A; subset boundary \+ 500 m/1 km; 10 m resample; cloud/shadow/vegetation mask; Natural RGB, SWIR-NIR-Red, geology composite, lithology ratio/index, NDVI, NDWI, iron oxide, ferric, clay/SWIR, ferrous, brightness index; export GeoTIFF EPSG:32647. | Sentinel output нь field validation support бөгөөд хүдэржилтийн баталгаа биш. |
| ASTER workflow v5 | HDF import/band extraction; UTM47 project grid; b\*\_project band-аас alteration/lithology index тооцох; haze/edge filter зөвхөн visual; lithology composite \-\> favorable polygon \-\> raster \-\> normalized score; save score\_porphyry\_alteration\_raw\_v1.tif, porphyry\_potential\_class\_v1.tif, porphyry\_final\_target\_binary\_mask\_v1.tif. | Raw score=Float32 continuous; class=1/2/3; mask=0/1. Binary mask нь хүдэржилтийн баталгаа биш. |
| KOMPSAT-2 | PAN/MS band, RPC, EPH, TXT metadata bundle; PAN/MS alignment; orthorectification; true color, false color, NDVI, pan-sharpened basemap, lineament/outcrop/access interpretation. | SWIR байхгүй тул clay/sericite/carbonate alteration-ийг дангаар батлахгүй. |
| ALOS-PALSAR / ASTER GDEM / DEM | Hillshade, slope, aspect, contour, drainage, watershed, ruggedness, curvature; drone flight, access, trench/drill pad, safety, lineament support. | DEM derivative нь structural support; field confirmation шаардлагатай. |

# **4\. Deposit model candidate screening table**

| Deposit model candidate | Supporting evidence to look for | Missing evidence / risk | Recommended validation work |
| :---- | :---- | :---- | :---- |
| Au-Cu hydrothermal vein | Quartz vein, pyrite/chalcopyrite/malachite, Au-Cu-Ag-As-Bi, shear/fault corridor, lineament intersection. | Au pXRF unreliable; vein continuity/width/grade may be unknown. | Recon mapping, rock chip/channel, lab Au fire assay \+ multi-element, LiDAR/structural mapping. |
| Intrusion-related Cu-Au-Mo | Diorite/granodiorite/gabbrodiorite contact, Cu-Mo-Bi-As, stockwork/quartz veinlets, ASTER/Sentinel alteration support. | Porphyry-style alteration zoning and sulphide system not confirmed. | ASTER validation, mapping of intrusive phases, soil grid, IP/magnetic, trench/channel. |
| Skarn/contact metasomatic Cu-Au-W-Bi | Intrusive-carbonate contact, garnet/epidote/magnetite/skarn minerals, W-Bi-Cu-Au association. | Carbonate/contact continuity and skarn mineral assemblage may be unclear. | Detailed contact mapping, pXRF W/Bi/Cu screening, petrography, magnetic/IP support. |
| Polymetallic vein | Pb-Zn-Cu-Ag-As association, vein/shear structures, gossan/iron oxide, historical occurrence overlap. | Depth continuity and grade continuity unknown. | Rock chip/channel, soil grid, structure mapping, lab Pb-Zn-Ag multi-element. |
| VMS-type sulphide possibility | Volcanic-sedimentary package, Cu-Zn-Pb-Ba-Fe-Mn, stratiform sulphide or gossan, regional arc/oceanic context. | Stratigraphic control and massive sulphide textures not confirmed. | Detailed stratigraphic mapping, geochemistry, IP, magnetic, targeted trenching. |
| Heavy mineral / placer indicator | Historical shlich/heavy mineral anomaly, drainage concentration, Au/W/Sn/Ti/Cr indicators. | Source may be transported/secondary; bedrock source not proven. | Drainage follow-up, upstream sampling, heavy mineral panning, geomorphology and bedrock checking. |

# **5\. Preliminary and final target ranking matrix**

| Evidence | Weight | High score criterion | Required attribute fields |
| :---- | :---- | :---- | :---- |
| Geology / lithology / intrusive contact | 20 | Favorable host, intrusive contact, skarn/contact, volcanic/intrusive package, mapped mineralized zone. | score\_geology, confidence, data\_gap, next\_action |
| Historical geochemistry / shlich / stream sediment | 15 | Cu-Au-Ag-Mo-Bi-As-Pb-Zn-W-Sn anomaly overlap and drainage source consistency. | score\_historical\_geochem, source\_scale, limitation |
| ASTER / Sentinel alteration and lithology | 15 | Clay/sericite/silica/ferric/chlorite/carbonate indicators and lithology index overlap. | score\_rs, rs\_product, mask\_flag |
| Structure / lineament / intersection | 15 | Fault/shear/vein trend, lineament intersection, contact-parallel structures. | score\_structure, trend, intersection\_type |
| Field mapping and pXRF response | 15 | Malachite, pyrite, epidote, quartz vein, gossan, elevated Cu/Pb/Zn/As/Mo/W/Sn. | score\_field\_pxrf, instrument, qa\_status |
| Drone LiDAR / photogrammetry evidence | 8 | Outcrop exposure, vein trace, trench/pit evidence, micro-topography, access confirmation. | score\_drone, orthomosaic\_id, lidar\_id |
| CMCS nearest deposit / metallogenic context | 7 | Relevant Au-Cu/Cu-polymetallic/skarn/VMS occurrence within 5/10/20 km context. | score\_cmcs, buffer\_km, context\_only\_flag |
| Access / safety / workability | 5 | Field access possible, slope moderate, drone/sampling/trenching feasible. | score\_access, hse\_risk, route\_status |

| Target class | Score range | Meaning | Action |
| :---- | :---- | :---- | :---- |
| A | \>=75 | Field/lab follow-up priority with multiple evidence types. | Drone/recon/sampling/trench/geophysics planning. |
| B | 55-74 | Promising but additional mapping/sampling needed. | Drone/recon \+ targeted sampling; update confidence. |
| C | 35-54 | Data gap or low confidence. | Limited check, additional desktop/field validation. |
| D | \<35 | Archive/monitor unless new evidence emerges. | No immediate field cost except opportunistic check. |

# **6\. Portable XRF QA/QC and register schema**

| Daily pXRF step | Olympus Vanta M / Bruker Titan S1 procedure | Record field |
| :---- | :---- | :---- |
| Warm-up | Instrument manufacturer recommended warm-up; battery/mode/profile check. | instrument\_model, serial\_no, operator, date\_time |
| Calibration/check sample | Daily start/end check; known reference material comparison. | crm\_id, expected\_value, measured\_value, pass\_fail |
| Blank | Contamination check between high-grade or dusty samples. | blank\_id, measured\_elements, pass\_fail |
| Duplicate/cross-check | 10-15% duplicate reading or critical station repeat; Vanta M vs Titan S1 comparison. | duplicate\_id, parent\_sample\_id, instrument\_pair |
| Reading conditions | Surface prep, moisture, grain size, weathering, measurement window and time. | moisture, surface\_condition, reading\_time\_sec, mode |
| Element suite | Cu, Pb, Zn, As, Mo, W, Sn, Mn, Fe, S and relevant pathfinders. Au not decision-grade. | element\_ppm\_pct fields, reliability\_flag |

# **7\. Sampling methodology and QA/QC insertion**

| Sample type | When to use | Sample ID convention | Critical note |
| :---- | :---- | :---- | :---- |
| Representative rock chip | Alteration zone/host rock characterization. | BUD-RC-001 | Avoid only high-grade visible pieces unless coded as selective. |
| Selective rock chip | Visible sulphide/malachite/quartz vein/mineralized float. | BUD-RC-001 | Clearly flag selective bias. |
| Float sample | Mineralized float where outcrop is limited. | BUD-RC-001 / BUD-FLT-001 optional | Do not use as in-situ proof unless source traced. |
| Channel sample | Vein/zone width measurable and safe to cut across. | BUD-CH-001 | Record width, orientation, recovery, continuity. |
| Orientation soil | Before systematic grid to test response. | BUD-SOIL-001 | Depth/horizon/mesh/fraction required. |
| Stream sediment follow-up | Historical drainage anomaly source checking. | BUD-STR-001 | Use catchment logic and upstream/downstream control. |
| Heavy mineral follow-up | Shlich/heavy mineral anomaly verification. | BUD-HM-001 | Record panning/concentrate method and geomorphic setting. |
| QA/QC standard | Certified reference material insertion. | BUD-QC-STD-001 | CRM suitable for expected element suite. |
| QA/QC blank | Contamination monitoring. | BUD-QC-BLK-001 | Insert after high-grade or regular interval. |
| QA/QC duplicate | Field/lab precision check. | BUD-QC-DUP-001 | Blind duplicate preferred. |

# **8\. Final target description sheet schema**

| Field | Required content |
| :---- | :---- |
| target\_id | Unique ID, e.g., BUD-TGT-A01. |
| location | Easting/Northing EPSG:32647, license relation, access route. |
| evidence\_summary | Concise multi-evidence summary with source layers. |
| geology | Host lithology, intrusive/contact relation, map confidence. |
| structure | Fault/shear/vein trend, intersection, LiDAR/field confirmation. |
| alteration | ASTER/Sentinel support, field alteration, confidence. |
| geochemistry | pXRF/lab/soil/stream/heavy mineral values and QA/QC status. |
| remote\_sensing\_support | Sentinel/ASTER/KOMPSAT/DEM product IDs and limitation. |
| drone\_lidar\_support | Orthomosaic tile, LiDAR DTM/DSM/lineament/outcrop evidence. |
| sampling\_result | Rock chip/channel/soil assay summary and QA/QC performance. |
| confidence | High/Medium/Low with reason. |
| risk\_data\_gap | Missing evidence and uncertainty. |
| recommended\_follow\_up | Mapping, sampling, trench, IP, magnetic, scout drilling. |
| go\_no\_go\_decision | Go / Conditional Go / No-Go with reviewer/date. |

# **Appendix E — Historical Scanned Maps QGIS Vectorization Workflow v02 Detailed**

Энэ appendix нь XV023222\_Buduunkhad\_HistoricalScannedMaps\_QGIS\_Vectorization\_Workflow\_MN\_v02\_Detailed.docx баримт бичгийн аргачлалыг үндсэн 78Inputs v2 Enhanced workflow-д нэмсэн хэсэг юм. Historical scan-derived vector evidence нь field/lab confirmed evidence биш бөгөөд confidence flag, data gap, scale-use limitation-тайгаар ашиглагдана.

**XV-023222 / Buduunkhad / L23222**

**Historical Scanned Maps to Georeferenced Raster and Vector GIS Evidence Database Workflow**

*QGIS / GeoPackage / QA-QC / Confidence Ranking аргачлал \- v02 Detailed*

Энэ хувилбар нь v01 аргачлалыг илүү дэлгэрүүлж, QGIS дээр хийх бодит алхам, layer schema, Excel register sheet, QA/QC шалгуур, confidence scoring, data gap, handover acceptance criteria-г нэг бүрчлэн оруулсан audit-ready ажлын заавар юм.

| Талбар | Утга |
| :---- | :---- |
| Project | XV-023222 / Buduunkhad / L23222 |
| Workflow title | Historical Scanned Map to Georeferenced Raster and Vector GIS Evidence Database Workflow |
| Scope | 1987-2021 historical scanned geology, geochemistry, heavy mineral, stream sediment, mineral resources, metallogenic, prospectivity and source material maps |
| Standard CRS | WGS 84 / UTM Zone 47N, EPSG:32647 |
| Software | QGIS, GeoPackage, Excel register, QA/QC workbook |
| Workflow status | Raw Scan \-\> Inventory \-\> Georeference \-\> Vector Digitizing \-\> Register \-\> QA/QC \-\> Confidence Ranking \-\> Master GIS Handover |
| Version | v02 Detailed |
| Prepared date | 2026-05-26 |

# **Агуулгын товч жагсаалт**

67. 1\. Зорилго ба хамрах хүрээ  
68. 2\. Reference document-тэй нийцүүлэх зарчим  
69. 3\. Ажил гүйцэтгэх ерөнхий sequence  
70. 4\. Input scanned map inventory  
71. 5\. Map-to-legend linkage ба symbol dictionary  
72. 6\. Folder structure ба file governance  
73. 7\. QGIS project setup  
74. 8\. Georeferencing workflow  
75. 9\. Raster QA/QC ба confidence  
76. 10\. Vectorization strategy by map type  
77. 11\. Master GeoPackage design  
78. 12\. Field schema ба domain/lookup  
79. 13\. QGIS digitizing SOP  
80. 14\. Layer бүрийн нарийвчилсан SOP  
81. 15\. Excel register workbook  
82. 16\. QA/QC checklist  
83. 17\. Confidence ranking logic  
84. 18\. Data gap register  
85. 19\. Cross-map integration  
86. 20\. Handover package ба acceptance criteria  
87. 21\. Final workflow diagram  
88. 22\. Appendices

# **1\. Зорилго ба хамрах хүрээ**

Энэхүү аргачлал нь Бүдүүн хад / XV-023222 / L23222 төслийн бүх historical scanned map файлыг QGIS дээр бүртгэх, georeference хийх, vector GIS layer болгон боловсруулах, Excel/GeoPackage register үүсгэх, QA/QC болон confidence ranking хийж Master GIS database-д audit-ready байдлаар нэгтгэх зорилготой.

Энэ нь ганц ашигт малтмалын зураг боловсруулах workflow биш. 1987 оны 1:200,000 шлих, ёроолын сорьц, геологи, ашигт малтмалын зураг; 2013 оны 1:50,000 геологи, ашигт малтмал, хэтийн төлөв, эх материалын зураг; 1:100,000-1:500,000 металлогени болон regional metallogenic report scan/pdf файлуудыг нэгэн зэрэг хамарна.

Raw scan-derived vector data нь historical interpretation evidence бөгөөд field/lab confirmed evidence биш. Field validation, pXRF screening, rock chip/soil sampling, laboratory assay-аар баталгаажихаас өмнө decision-grade evidence гэж ашиглахгүй.

1:50,000 зураг нь target-scale interpretation болон QField field validation-д илүү өндөр ач холбогдолтой. 1:100,000-1:500,000 зураг нь regional context, drainage/geochemical dispersion, metallogenic framework, structural trend, target screening-д ашиглагдана.

Бүх final spatial output EPSG:32647-д хадгалагдана. Native/raw CRS, source scale, GCP, georeference confidence, digitizing confidence-г metadata/register-д заавал хадгална. Raw archive файлыг засварлахгүй. Processing зөвхөн working copy дээр хийгдэнэ.

| Хамрах зүйл | Энэ workflow-д хийх ажил | Хязгаарлалт |
| :---- | :---- | :---- |
| Raw scan JPG/PDF | Inventory, working copy, map type classification, legend linkage | Raw file дээр overwrite хийхгүй |
| Main map | Georeference, GeoTIFF, vector digitizing | Map scale-ийн хязгаарыг хадгална |
| Legend scan | Symbol dictionary, domain/lookup table, interpretation rule | Ихэвчлэн georeference хийхгүй |
| Vector evidence | Point/line/polygon layer, source traceability, QA/QC | Historical only гэсэн validation\_status хадгална |
| Register/QAQC | Excel workbook, confidence ranking, data gap register | Хоосон field-тэй output handover хийхгүй |

# **2\. Reference document-тэй нийцүүлэх зарчим**

| Reference | Энэ workflow-д тусгах шаардлага | v02-д нэмсэн дэлгэрүүлэлт |
| :---- | :---- | :---- |
| Overall 78-input exploration workflow | 78 raw input evidence group-ийг Phase 1 Data Audit and Master GIS Setup-тэй уялдуулах; EPSG:32647 CRS; raw data-г өөрчлөхгүй; Master GIS database; Phase 3/4/6/7/8/9 handover. | 21 scan map-ыг evidence group, map family, priority, handover use-ээр ангилсан. |
| Phase 1 \- Data Audit and Master GIS Setup | File inventory, metadata register, sidecar check, CRS check, georeference audit, GCP table, residual report, Master GeoPackage, Master QGIS project, QA/QC log, confidence ranking, data gap register. | GCP table schema, residual acceptance, raster/vector confidence score, data gap fields, acceptance criteria-г дэлгэрүүлсэн. |
| 2013 MineralOccurrenceMap QGIS workflow | Raw scan \-\> GeoTIFF \-\> vector digitizing \-\> register \-\> QA/QC гэсэн логикийг бүх scanned map family-д өргөтгөх. | Ганц occurrence point биш: geology, structure, geochemistry anomaly, heavy mineral, source material, prospectivity, metallogenic context layer-үүдийг нэмсэн. |

# **3\. Ажил гүйцэтгэх ерөнхий sequence**

89. Raw archive-г read-only гэж үзэж, бүх scan map-ыг evidence group-ээр шалгана.  
90. 01\_Input\_Working\_Copy руу файлуудыг хуулж, filename, size, extension, checksum, source note бүртгэнэ.  
91. Map Inventory болон Map-to-Legend Linkage register үүсгэнэ.  
92. QGIS project-ийг EPSG:32647 CRS-тэй үүсгэж, license boundary болон buffer layer-уудыг reference болгон load хийнэ.  
93. Main map бүрийн georeference priority тогтоож, GCP сонголтын төлөвлөгөө гаргана.  
94. QGIS Georeferencer дээр map бүрийг GeoTIFF болгож, GCP table, residual report, screenshot/check map хадгална.  
95. Georeferenced raster бүрт CRS, extent, RMSE/residual, grid alignment, license/basemap/DEM overlay шалгаж raster confidence өгнө.  
96. Map type бүрийн digitizing rule болон legend-based symbol dictionary-г баталгаажуулна.  
97. GeoPackage layer-үүдийг үүсгэж, common source traceability fields \+ layer-specific fields нэмнэ.  
98. Vector digitizing хийж, QGIS form tab, domain/lookup, required field constraints тохируулна.  
99. Topology, geometry validity, duplicate, NULL, ID uniqueness, scale-use flag, historical/confirmed separation QA/QC шалгана.  
100. Excel register workbook export хийж, confidence ranking болон data gap register бөглөнө.  
101. Cross-map integration хийж, evidence давхцал/зөрүү/шийдвэрийн нөлөөллийг бүртгэнэ.  
102. Master QGIS project, Master GeoPackage, QA/QC workbook, README, handover checklist багцалж дараагийн phase-д шилжүүлнэ.

| Stage | Input | Main action | Output | QA gate |
| :---- | :---- | :---- | :---- | :---- |
| S1 Inventory | Raw scan files | Register \+ checksum \+ working copy | Map Inventory | All files accounted |
| S2 Legend linkage | Main map \+ legend | Symbol/domain mapping | Legend linkage register | Legend status assigned |
| S3 Georeference | Working raster | GCP \+ transformation \+ GeoTIFF | GeoTIFF EPSG:32647 | Residual \+ overlay checked |
| S4 Vectorization | GeoTIFF \+ legend | Digitize by map type | GeoPackage layers | Geometry/attribute QA passed |
| S5 Register | Vector layers | Export and enrich attributes | Excel workbook | Required sheets complete |
| S6 Integration | All evidence layers | Cross-map overlay | Confidence/data gap/handover | Acceptance criteria passed |

# **4\. Input scanned map inventory**

Доорх 21 файлыг нэг Map Inventory-д бүртгэж, main map, legend, report excerpt, regional context гэсэн холбоосоор удирдана. Файл бүрийн raw path, working copy path, checksum, open status, georeference status, output status-г workbook-д нэмэлт баганаар хадгална.

| Map\_ID | Evidence group | Raw filename | Year | Sheet | Scale | Map type | Legend | Expected output | Priority | Main use |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| BK-SCAN-001 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Heavy mineral sampling results map | BK-SCAN-002 | GeoTIFF \+ heavy mineral sample/anomaly layers | P2 | Шлихийн сорьц, indicator mineral, тархалтын contour |
| BK-SCAN-002 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_HeavyMineralSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Heavy mineral legend | BK-SCAN-001 | Symbol dictionary / lookup | P2 | Шлих/индикатор минералын таних тэмдэг |
| BK-SCAN-003 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Stream sediment legend | BK-SCAN-004 | Symbol dictionary / lookup | P2 | Ёроолын сорьц, сарнилын урсгал, contour |
| BK-SCAN-004 | 04\_HeavyMineral\_StreamSediment\_Field | 1987\_MN\_L47-XIX\_StreamSedimentSamplingResultsMap\_Polyelement\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Stream sediment polyelement map | BK-SCAN-003 | GeoTIFF \+ anomaly polygon/contour layers | P2 | Cu Pb Zn Ag As Bi W Sn Mo Mn Ba F anomaly |
| BK-SCAN-005 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Regional geological map | BK-SCAN-006 | GeoTIFF \+ regional geology/structure layers | P2 | Региональ геологи, lithology, structure |
| BK-SCAN-006 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_GeologicalMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Regional geological legend | BK-SCAN-005 | Symbol dictionary / lookup | P2 | Stratigraphy, intrusion, structure, lithology |
| BK-SCAN-007 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Mineral resources map | BK-SCAN-008 | GeoTIFF \+ occurrence/resource layers | P2 | Региональ илрэл, гажил, хүдрийн талбай |
| BK-SCAN-008 | 05\_Geology\_Mineral\_Prospectivity | 1987\_MN\_L47-XIX\_MineralResourcesMap\_Legend\_1-200000\_v01\_raw-scan.jpg | 1987 | L47-XIX | 1:200,000 | Mineral resources legend | BK-SCAN-007 | Symbol dictionary / lookup | P2 | Ашигт малтмал, элемент, илрэл, гажлын тэмдэглэгээ |
| BK-SCAN-009 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Detailed geological map | BK-SCAN-010 | GeoTIFF \+ detailed geology/structure layers | P1 | Нарийвчилсан геологи, lithology, fault, section |
| BK-SCAN-010 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_GeologicalMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Detailed geological legend | BK-SCAN-009 | Symbol dictionary / lookup | P1 | Stratigraphy, intrusive, vein, alteration |
| BK-SCAN-011 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_MineralOccurrenceMap\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Mineral occurrence map | BK-SCAN-010/BK-SCAN-015 | GeoTIFF \+ mineral occurrence/target layers | P1 | Au-Cu Cu Mo As Zn илрэл \+ геологийн суурь |
| BK-SCAN-012 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessment\_ReportExcerpt\_B3-TolKhar\_v01\_raw-photo.jpg | 2013 | L47-74-A | Report/photo | Prospectivity report excerpt | BK-SCAN-013 | Text evidence register | P1 | Б-2/B-3/B-4 талбайн тайлбар |
| BK-SCAN-013 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_ProspectivityAssessmentMap\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Prospectivity assessment map | BK-SCAN-012 | GeoTIFF \+ prospectivity polygons | P1 | Б-3 Толь хяр, Г-1 хэтийн төлөвтэй хэсэг |
| BK-SCAN-014 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Source materials map | BK-SCAN-015 | GeoTIFF \+ routes/obs/sample/trench layers | P1 | Маршрут, ажиглалт, сорьц, суваг, шурф, зүсэлт |
| BK-SCAN-015 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-74-A\_SourceMaterialsMap\_Legend\_1-50000\_v01\_raw-scan.jpg | 2013 | L47-74-A | 1:50,000 | Source materials legend | BK-SCAN-014 | Symbol dictionary / lookup | P1 | Ажиглалтын цэг, маршрут, сорьц, шурф, суваг |
| BK-SCAN-016 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MineralDistributionPatternMap\_1-100000\_v01\_raw-scan.jpg | 2013 | L47-73-74 | 1:100,000 | Mineral distribution pattern map | None | GeoTIFF \+ ore district/node context | P3 | Металлогенийн бүс, хүдрийн дүүрэг, зангилаа |
| BK-SCAN-017 | 05\_Geology\_Mineral\_Prospectivity | 2013\_MN\_Namalzakh\_L47-73-74\_MetallogenicSchemeAndMetallogenogram\_1-400000\_v01\_raw-scan.jpg | 2013 | L47-73-74 | 1:400,000 | Metallogenic scheme/metallogenogram | None | GeoTIFF \+ metallogenic context | P3 | Хүдрийн формац, нас, металлогенийн бүс |
| BK-SCAN-018 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_Legend\_RawScan\_2020\_v01.jpg | 2020 | L47B Talshand | 1:500,000 | Regional metallogenic legend | BK-SCAN-019 | Symbol dictionary / lookup | P4 | Металлогений таних тэмдэг |
| BK-SCAN-019 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_L47B\_Talshand\_1M500K\_RawScan\_2020\_v01.jpg | 2020 | L47B Talshand | 1:500,000 | Regional metallogenic map | BK-SCAN-018 | GeoTIFF \+ regional metallogenic zones | P4 | Монгол улсын 1:500k металлогени |
| BK-SCAN-020 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book01\_ProjectBook13\_1M500K\_RawScan\_2021\_v01.pdf | 2021 | Regional | 1:500,000 | Metallogenic report book 01 | BK-SCAN-019 | Report evidence register | P4 | Тайлангийн текст, тайлбар |
| BK-SCAN-021 | 06\_Regional\_Metallogenic\_L47B | Regional\_MetallogenicMap\_Report\_Book04\_ProjectBook16\_1M500K\_RawScan\_2021\_v01.pdf | 2021 | Regional | 1:500,000 | Metallogenic report book 04 | BK-SCAN-019 | Report evidence register | P4 | Тайлангийн текст, тайлбар |

## **4.1 Inventory-д заавал нэмэх metadata баганууд**

| Багана | Төрөл | Заавал эсэх | Тайлбар / domain |
| :---- | :---- | :---- | :---- |
| raw\_path | Text | Yes | 00\_Raw\_Files\_Archive доторх эх файл |
| working\_copy\_path | Text | Yes | 01\_Input\_Working\_Copy доторх боловсруулалтын хуулбар |
| file\_size\_mb | Decimal | Yes | Хэмжээг audit-д хадгална |
| checksum\_sha256 | Text | Recommended | Raw vs working copy integrity шалгах |
| open\_status | Text | Yes | Opens / Error / Needs conversion |
| scan\_quality | Text | Yes | Good / Fair / Poor |
| has\_coordinate\_grid | Text | Yes | Yes / No / Partial / Unknown |
| georef\_required | Text | Yes | Yes / No / Context only |
| georef\_status | Text | Yes | Not started / In progress / Completed / Failed / Needs verification |
| vectorization\_status | Text | Yes | Not started / Draft / Checked / Approved / Not applicable |
| handover\_status | Text | Yes | Ready / Use with caution / Hold / Exclude |

# **5\. Map-to-legend linkage ба symbol dictionary**

Main map болон legend файлыг салгаж хадгалах боловч digitizing rule, attribute domain, symbol dictionary үүсгэхэд хооронд нь заавал холбож бүртгэнэ. Legend файлыг тусад нь georeference хийх шаардлагагүй, харин map symbol тайлах evidence болгон бүртгэнэ.

| Main map | Legend / report support | Digitizing rule | Domain / lookup үүсгэх зүйл |
| :---- | :---- | :---- | :---- |
| 1987 HeavyMineralSamplingResultsMap | 1987 HeavyMineralSamplingResultsMap\_Legend | Шлих, indicator mineral, contour, sample symbol domain үүсгэнэ. | mineral\_indicator, anomaly\_class, sample\_symbol |
| 1987 StreamSedimentSamplingResultsMap\_Polyelement | 1987 StreamSedimentSamplingResultsMap\_Legend | Element suite, anomaly contour, drainage dispersion symbol domain үүсгэнэ. | element\_suite, anomaly\_level, contour\_type |
| 1987 GeologicalMap | 1987 GeologicalMap\_Legend | Geological unit, age, lithology, intrusive, structure symbol domain үүсгэнэ. | map\_symbol, lithology, age, intrusive\_type |
| 1987 MineralResourcesMap | 1987 MineralResourcesMap\_Legend | Commodity, occurrence type, anomaly, ore field symbol domain үүсгэнэ. | commodity, occurrence\_type, ore\_field\_type |
| 2013 GeologicalMap | 2013 GeologicalMap\_Legend | Detailed lithology, fault, vein, alteration, section symbol domain үүсгэнэ. | stratigraphic\_unit, vein\_type, alteration |
| 2013 MineralOccurrenceMap | 2013 GeologicalMap/SourceMaterials legend болон map label | Au-Cu, Cu, Mo, As, Zn occurrence point and target zone digitizing rule үүсгэнэ. | commodity\_group, target\_style |
| 2013 SourceMaterialsMap | 2013 SourceMaterialsMap\_Legend | Route, station, sample, trench/pit/shaft/channel/section symbol domain үүсгэнэ. | observation\_type, sample\_type, work\_type |
| Regional MetallogenicMap L47B | Regional MetallogenicMap\_L47B\_Legend \+ Book01/Book04 | Metallogenic belt, ore district, commodity group, regional occurrence context rule үүсгэнэ. | metallogenic\_unit, ore\_formation, scale\_context |

## **5.1 Symbol dictionary үүсгэх алхам**

103. Legend scan-ыг QGIS эсвэл image viewer дээр нээгээд symbol бүрийг screenshot/zoom түвшинд шалгана.  
104. Symbol\_Code, Symbol\_Image\_Ref, Mongolian\_Name, English\_Name, Geometry\_Type, Default\_Layer, Attribute\_Field, Domain\_Value, Notes гэсэн баганатай dictionary sheet үүсгэнэ.  
105. Main map дээрх тэмдэглэгээ legend-тэй тохирч байгаа эсэхийг 10-20 жишээ feature дээр туршиж баталгаажуулна.  
106. Тодорхойгүй тэмдэглэгээ бүрт attribute\_confidence \= Low/Unknown, data\_gap\_type \= Unclear legend гэж тэмдэглэнэ.  
107. QGIS layer form дээр dropdown domain болгон ашиглах lookup list үүсгэнэ.

| Symbol dictionary багана | Жишээ | Тайлбар |
| :---- | :---- | :---- |
| symbol\_code | HM-MAG-01 | Дотоод код |
| symbol\_name\_mn | Магнетит агуулсан шлих | Legend-ээс уншсан нэр |
| symbol\_name\_en | Magnetite heavy mineral indicator | Тайлан/олон улсын нэршил |
| geometry\_type | Point / Line / Polygon | Digitize хийх геометр |
| target\_layer | heavy\_mineral\_sample\_points | QGIS layer |
| domain\_field | mineral\_indicator | Атрибут талбар |
| domain\_value | Magnetite | Нэг мөр стандарт утга |
| confidence\_default | Medium | Тэмдэглэгээний тод байдал |
| notes | Legend scan unclear | Тайлбар |

# **6\. Folder structure ба file governance**

Дараах бүтэц нь Phase 1 Data Audit and Master GIS Setup дотор ажиллахад тохиромжтой. Raw archive-г өөрчлөхгүй; энэ бүтэц нь working copy болон output-д зориулагдана.

01\_Phase\_1\_Data\_Audit\_and\_Master\_GIS\_Setup/  
  00\_Admin\_and\_Method/  
  01\_Input\_Working\_Copy/  
    01\_HeavyMineral\_StreamSediment\_1987/  
    02\_Geology\_MineralResources\_1987/  
    03\_Geology\_MineralOccurrence\_Prospectivity\_2013/  
    04\_Metallogenic\_Regional\_2013\_2021/  
  02\_Inventory\_and\_Metadata/  
  03\_CRS\_Check/  
  04\_Georeference\_Check/  
    01\_GCP\_Tables/  
    02\_Georeferenced\_Rasters/  
    03\_Residual\_Reports/  
    04\_Georeference\_Screenshots/  
    05\_Low\_Confidence\_Georef/  
  05\_Vector\_Digitized/  
    01\_Geology\_Polygons/  
    02\_Structures\_Faults\_Lines/  
    03\_Mineral\_Occurrences\_Points/  
    04\_Geochemistry\_Anomaly\_Polygons/  
    05\_HeavyMineral\_StreamSediment\_Layers/  
    06\_Source\_Materials\_Points\_Lines/  
    07\_Prospectivity\_Target\_Zones/  
    08\_Metallogenic\_Context/  
  06\_Register\_Metadata/  
  07\_QGIS\_Project/  
  08\_QAQC\_and\_Confidence/  
  09\_Handover\_Package/

| Governance rule | Зорилго | Хэрэгжүүлэх арга |
| :---- | :---- | :---- |
| Raw read-only | Эх өгөгдөл эвдрэхээс хамгаалах | Raw archive дээр бичих эрхгүй, processing зөвхөн copy дээр |
| Checksum | Файл солигдсон эсэхийг хянах | SHA-256 raw ба working copy-д хадгалах |
| Versioning | Дахин боловсруулалтыг ялгах | v01, v02, v03; draft файлыг \_DRAFT гэж тэмдэглэх |
| Sidecar grouping | Raster metadata алдагдахаас сэргийлэх | .aux.xml, .ovr, .tfw, .jgw, .rpc, .eph файлыг хамт хадгалах |
| Change log | Audit trail үүсгэх | Action\_Log.xlsx: date/operator/action/input/output/status |

# **7\. QGIS project setup**

108. QGIS \-\> Project \-\> New сонгоно.  
109. Project \-\> Properties \-\> CRS хэсгээс WGS 84 / UTM Zone 47N, EPSG:32647 сонгоно.  
110. Distance unit \= meters; Area unit \= square kilometers/hectares; Ellipsoid \= WGS84 тохируулна.  
111. Project-г 07\_QGIS\_Project хавтаст XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorization\_QGIS\_EPSG32647\_v02.qgz нэрээр хадгална.  
112. GeoPackage connection үүсгэж Master GeoPackage-г Browser Panel-д холбоно.  
113. Layer group structure-г доорх байдлаар үүсгэнэ.  
114. Project Properties \-\> General дээр project title, author/team, path relative тохиргоог шалгана.  
115. Project Properties \-\> Data Sources дээр Automatically create transaction groups шаардлагатай бол идэвхжүүлнэ.  
116. QGIS snapping болон topology editing тохиргоог vector digitizing эхлэхээс өмнө тохируулна.

Layer group structure:  
01\_Source\_Raw\_and\_Georef\_Raster  
02\_Admin\_Boundary\_and\_Buffer  
03\_Geology  
04\_Mineral\_Occurrence  
05\_HeavyMineral\_StreamSediment  
06\_Source\_Materials  
07\_Prospectivity\_Targets  
08\_Metallogenic\_Context  
09\_QAQC\_Confidence  
10\_Handover

| QGIS setting | Recommended value | Тайлбар |
| :---- | :---- | :---- |
| Project CRS | EPSG:32647 | Final output CRS |
| On-the-fly reprojection | Enabled | Native layer display хийхэд |
| Snapping type | Vertex and segment | Line/polygon digitizing-д |
| Snapping tolerance | 5-10 pixels / scale dependent | Scale-аас хамааруулж тохируулна |
| Topological editing | Enabled for line/polygon | Overlap/sliver багасгана |
| Avoid overlap | Enabled for same polygon layers | Geology/target zone polygon-д |
| Default encoding | UTF-8 | Монгол/кирилл attribute алдагдахгүй |
| Project paths | Relative | Handover package зөөвөрлөхөд |

# **8\. Georeferencing workflow**

Legend scan файлыг гол төлөв georeference хийхгүй. Main map scan-уудыг georeference хийж GeoTIFF болгосны дараа legend scan-ыг symbol dictionary, lookup/domain, attribute coding хийхэд ашиглана.

## **8.1 GCP сонгох эх сурвалжийн эрэмбэ**

| Эрэмбэ | Control source | Ашиглах нөхцөл | Confidence impact |
| :---- | :---- | :---- | :---- |
| 1 | Coordinate grid intersection | Зураг дээр coordinate grid тод, огтлолцол сайн харагдаж байвал хамгийн түрүүнд сонгоно. | High |
| 2 | Map frame corner coordinate / labelled tick | Булан/захын coordinate тодорхой үед. | High |
| 3 | Map sheet boundary | L47-XIX, L47-74-A sheet boundary coordinates баталгаатай үед. | Medium-High |
| 4 | License boundary corner / known control point | Тусгай зөвшөөрлийн хил эсвэл баталгаатай vector boundary давхцаж байвал. | Medium |
| 5 | Stable topographic feature | Голын уулзвар, замын огтлолцол, ridge/valley гэх мэт. | Medium-Low |
| 6 | Visual matching only | Grid/coordinate байхгүй үед зөвхөн context map-д. | Low / Needs verification |

## **8.2 QGIS Georeferencer дээр хийх алхам**

117. Raster \-\> Georeferencer нээнэ.  
118. Open Raster сонгож working copy JPG/PDF raster-г нээнэ. PDF бол шаардлагатай бол өмнө нь 300-600 dpi TIFF/PNG болгон хөрвүүлнэ.  
119. Settings \-\> Transformation Settings нээгээд Target CRS \= EPSG:32647 сонгоно.  
120. Output raster нэрийг 04\_Georeference\_Check/02\_Georeferenced\_Rasters хавтаст naming standard-аар өгнө.  
121. Load in QGIS when done сонголтыг идэвхжүүлнэ.  
122. Compression \= LZW; creation options-д TILED=YES, COMPRESS=LZW гэж боломжтой бол өгнө.  
123. GCP цэгүүдийг бүх талбайд жигд тархааж оруулна. Зөвхөн 4 булангаар хязгаарлахгүй.  
124. Coordinate оруулахдаа эх coordinate нь longitude/latitude бол decimal degree болгож оруулаад QGIS transform ашиглана эсвэл UTM координатаар шууд оруулна.  
125. Transformation-г эхлээд Polynomial 1 ашиглаж туршина. Residual их, scan distortion local байвал Thin Plate Spline туршиж, confidence note бичнэ.  
126. Georeferencing ажиллуулсны дараа GeoTIFF layer properties \-\> Source дээр CRS, extent, pixel size, path шалгана.  
127. GeoTIFF-г license boundary, DEM hillshade, basemap, өмнө georeferenced raster-тай давхарлаж overlay QA хийнэ.  
128. GCP table-г CSV/XLSX болгон хадгалж, residual report screenshot болон QGIS map screenshot хадгална.

| Scale | Minimum / preferred GCP | Transformation | Use rule | Confidence анхааруулга |
| :---- | :---- | :---- | :---- | :---- |
| 1:50,000 | Minimum 6; preferred 8-12 | Polynomial 1 / Helmert / TPS only if needed | Target-scale digitizing-д ашиглана | GCP муу бол occurrence/target vector confidence буурна |
| 1:100,000 | 6-10 | Polynomial 1 | Ore district / mineral distribution context | Local target geometry гэж хэтрүүлж ашиглахгүй |
| 1:200,000 | 6-10 | Polynomial 1 | Regional geology/geochemistry/drainage evidence | Field validation before decision-grade use |
| 1:400,000-1:500,000 | 4-8 | Polynomial 1 | Metallogenic context only | Context evidence; local target boundary биш |

## **8.3 DMS coordinate-г decimal degree болгох дүрэм**

Зарим scan map дээр coordinate нь 96°30′E, 46°00′N гэх мэт DMS хэлбэртэй байдаг. Decimal degree \= degree \+ minute/60 \+ second/3600. East/North эерэг, West/South сөрөг тэмдэгтэй байна.

| DMS | Decimal degree | Тайлбар |
| :---- | :---- | :---- |
| 96°30′00″E | 96.500000 | 96 \+ 30/60 |
| 45°50′00″N | 45.833333 | 45 \+ 50/60 |
| 96°45′00″E | 96.750000 | 96 \+ 45/60 |
| 46°00′00″N | 46.000000 | 46 \+ 0/60 |

# **9\. Raster QA/QC ба confidence**

| QA/QC item | QGIS дээр шалгах арга | Pass criteria | Fail / action |
| :---- | :---- | :---- | :---- |
| CRS | Layer Properties \-\> Source | EPSG:32647 | Wrong CRS бол reproject/georef дахин |
| Extent | Layer Properties \-\> Information \+ map canvas | License/buffer/map sheet-тэй logical overlap | Outside extent бол GCP/check coordinate |
| GCP count | Georeferencer GCP table | Scale-specific minimum хангагдсан | GCP нэмэх |
| Residual/RMSE | GCP residual table | Outlier багатай, grid alignment зөв | Outlier GCP-г шалгах/хасах |
| Grid alignment | Coordinate grid/tick давхцал | Булан болон дунд grid сайн таарсан | Transformation/GCP дахин |
| Visual distortion | Raster rotation/stretch | Уншигдахуйц, суналт хэтрээгүй | TPS/scan crop дахин |
| Raster completeness | Canvas display / overview | Зураг тасалдаагүй, эргээгүй | Export/render setting шалгах |
| Metadata | Inventory \+ properties | Source file, scale, year, map sheet бүртгэгдсэн | Metadata register бөглөх |
| **Raster confidence** | **Шалгуур** | **Use status** |  |
| High | 8+ well-distributed GCP; grid/coordinate сайн; residual acceptable; license/topographic overlay сайн; scan quality good | Target-scale digitizing болон Phase 4 ranking-д ашиглаж болно |  |
| Medium | 4-8 GCP; minor distortion; overlay logical; зарим grid/scan issue байна | Overlay/interpretation-д болгоомжтой ашиглана |  |
| Low | GCP цөөн; grid тодорхойгүй; regional scale; visual match давамгайлсан | Context evidence; local target boundary болгохгүй |  |
| Needs verification | CRS/georef эргэлзээтэй; residual өндөр; feature location conflict | Vector digitizing хийхээс өмнө дахин шалгана |  |

## **9.1 Georeferenced raster output naming**

| Raster theme | Output filename |
| :---- | :---- |
| 1987 Heavy mineral | XV023222\_Buduunkhad\_1987\_L47-XIX\_HeavyMineralSamplingResultsMap\_1-200K\_Georeferenced\_EPSG32647\_v02.tif |
| 1987 Stream sediment | XV023222\_Buduunkhad\_1987\_L47-XIX\_StreamSedimentPolyelementMap\_1-200K\_Georeferenced\_EPSG32647\_v02.tif |
| 1987 Geology | XV023222\_Buduunkhad\_1987\_L47-XIX\_GeologicalMap\_1-200K\_Georeferenced\_EPSG32647\_v02.tif |
| 1987 Mineral resources | XV023222\_Buduunkhad\_1987\_L47-XIX\_MineralResourcesMap\_1-200K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Detailed geology | XV023222\_Buduunkhad\_2013\_L47-74-A\_GeologicalMap\_1-50K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Mineral occurrence | XV023222\_Buduunkhad\_2013\_L47-74-A\_MineralOccurrenceMap\_1-50K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Prospectivity | XV023222\_Buduunkhad\_2013\_L47-74-A\_ProspectivityAssessmentMap\_1-50K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Source materials | XV023222\_Buduunkhad\_2013\_L47-74-A\_SourceMaterialsMap\_1-50K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Mineral distribution | XV023222\_Buduunkhad\_2013\_L47-73-74\_MineralDistributionPatternMap\_1-100K\_Georeferenced\_EPSG32647\_v02.tif |
| 2013 Metallogenic scheme | XV023222\_Buduunkhad\_2013\_L47-73-74\_MetallogenicSchemeMetallogenogram\_1-400K\_Georeferenced\_EPSG32647\_v02.tif |
| 2020 Regional metallogenic | XV023222\_Buduunkhad\_2020\_L47B\_Talshand\_RegionalMetallogenicMap\_1-500K\_Georeferenced\_EPSG32647\_v02.tif |

# **10\. Vectorization strategy by map type**

| Map type | Vector output | Use limit | Primary QA/QC |
| :---- | :---- | :---- | :---- |
| Geological maps | geology\_units\_50k\_polygons, geology\_units\_200k\_polygons, structures\_faults\_lines, intrusive\_contacts\_lines, dyke\_vein\_lines, alteration\_zones\_polygons | 1:50k \= local evidence; 1:200k \= regional evidence | Polygon topology, boundary match, symbol domain |
| Mineral occurrence / mineral resources maps | mineral\_occurrences\_points, mineralized\_zones\_polygons, ore\_field\_prospect\_polygons, occurrence\_labels, commodity groups | Historical map-derived evidence; field/lab confirmed гэж нэрлэхгүй | Point placement, commodity spelling, duplicate/cross-ref |
| Heavy mineral sampling maps | heavy\_mineral\_sample\_points, heavy\_mineral\_anomaly\_polygons, indicator\_mineral\_distribution\_polygons, drainage\_interpretation\_lines | Drainage/source direction interpretation requires DEM/drainage check | Contour closure, drainage relation, indicator mineral domain |
| Stream sediment polyelement maps | stream\_sediment\_sample\_points, stream\_sediment\_anomaly\_polygons, geochemical\_anomaly\_contours\_lines, drainage\_anomaly\_trend\_lines | Multi-element suite field заавал бөглөнө | Element suite, anomaly class, drainage consistency |
| Prospectivity assessment maps | prospectivity\_target\_zones\_polygons, priority\_areas, named\_prospects, recommended\_followup\_zones | Prospect polygon \= historical interpretation; ranking-д confidence-тэй хэрэглэнэ | Target ID, evidence basis, priority consistency |
| Source materials maps | source\_material\_observation\_points, source\_material\_route\_lines, sample\_points, trench\_pit\_shaft\_channel\_points, section\_lines | QField validation, field route planning-д шууд хэрэгтэй | Route connectivity, station/sample ID, source symbol |
| Metallogenic maps | metallogenic\_zones\_polygons, ore\_district\_node\_polygons, regional\_structure\_lines, regional\_occurrence\_context\_points | Context only; local target boundary биш | Scale flag, use\_limit, regional label |

# **11\. Master GeoPackage design**

Нэг Master GeoPackage үүсгэнэ: XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorized\_MasterGIS\_EPSG32647\_v02.gpkg. Layer бүрийн CRS EPSG:32647 байна. Layer name lowercase\_snake\_case байна.

| No | Layer name | Geometry | Purpose |
| :---- | :---- | :---- | :---- |
| 01 | scan\_map\_index\_polygons | Polygon | Georeferenced map extent, map ID, raster confidence |
| 02 | georeference\_gcp\_points | Point | GCP coordinate, residual, control source |
| 03 | geology\_units\_50k\_polygons | Polygon | 2013 detailed geology units |
| 04 | geology\_units\_200k\_polygons | Polygon | 1987 regional geology units |
| 05 | structures\_faults\_lines | LineString | Faults, inferred faults, lineaments |
| 06 | intrusive\_contacts\_lines | LineString | Intrusive/contact boundaries |
| 07 | dyke\_vein\_lines | LineString | Dyke, vein, quartz vein, section lines |
| 08 | alteration\_zones\_polygons | Polygon | Alteration zones if shown |
| 09 | mineral\_occurrences\_points | Point | Mineral occurrence/resource points |
| 10 | mineralized\_zones\_polygons | Polygon | Mineralized zones / ore fields |
| 11 | ore\_field\_prospect\_polygons | Polygon | Ore field/prospect areas |
| 12 | heavy\_mineral\_sample\_points | Point | Heavy mineral sample points if shown |
| 13 | heavy\_mineral\_anomaly\_polygons | Polygon | Indicator mineral/anomaly polygons |
| 14 | stream\_sediment\_sample\_points | Point | Stream sediment sample points if shown |
| 15 | stream\_sediment\_anomaly\_polygons | Polygon | Polyelement anomaly polygons |
| 16 | geochemical\_anomaly\_contours\_lines | LineString | Anomaly contour/dispersion lines |
| 17 | prospectivity\_target\_zones\_polygons | Polygon | Prospectivity / priority target zones |
| 18 | source\_material\_observation\_points | Point | Observation stations |
| 19 | source\_material\_route\_lines | LineString | Field route lines |
| 20 | source\_material\_trench\_pit\_points | Point | Trench/pit/shaft/channel points |
| 21 | metallogenic\_zones\_polygons | Polygon | Regional metallogenic belt/zone polygons |
| 22 | regional\_occurrence\_context\_points | Point | Regional occurrence points if shown |
| 23 | source\_cross\_reference | No geometry / table | Feature relationships across maps |
| 24 | data\_confidence\_ranking\_spatial | Point/Polygon/Table | Spatial confidence features |
| 25 | data\_gap\_register\_spatial | Point/Polygon/Table | Spatial data gaps |

## **11.1 GeoPackage үүсгэх QGIS алхам**

129. Browser Panel \-\> GeoPackage \-\> Create Database эсвэл Layer \-\> Create Layer \-\> New GeoPackage Layer сонгоно.  
130. Database path: 05\_Vector\_Digitized/XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorized\_MasterGIS\_EPSG32647\_v02.gpkg гэж өгнө.  
131. Эхний layer-ийг үүсгэсний дараа дараагийн layer-үүдийг ижил database-д Add layer to existing database байдлаар нэмнэ.  
132. Geometry type, CRS EPSG:32647, attribute fields-ийг schema-ийн дагуу үүсгэнэ.  
133. Layer бүрт fid/geometry auto field-г user form дээр нууж, feature\_id, source\_map\_id, confidence fields-ийг required болгоно.  
134. Layer style QML файлыг 05\_Master\_GIS\_Database/Styles\_QML хавтаст хадгалж version-той нэрлэнэ.

# **12\. Field schema ба domain/lookup**

## **12.1 Common source traceability fields**

| Field | Type | Required | Purpose / domain |
| :---- | :---- | :---- | :---- |
| feature\_id | Text | Yes | Unique feature ID, e.g. BUD-MIN-0001 |
| source\_map\_id | Text | Yes | BK-SCAN-xxx |
| source\_file | Text | Yes | Raw filename |
| source\_year | Integer | Yes | 1987/2013/2020/2021 |
| map\_sheet | Text | Yes | L47-XIX / L47-74-A / L47B |
| map\_scale | Text | Yes | 1:50,000 etc. |
| map\_type | Text | Yes | Geology / mineral / heavy mineral / stream sediment |
| digitized\_from\_raster | Text | Yes | Georeferenced GeoTIFF filename |
| legend\_file | Text | Recommended | Related legend file |
| original\_symbol | Text | Recommended | Symbol as shown on map |
| original\_label | Text | Recommended | Label/number on map |
| digitized\_by | Text | Yes | Operator name |
| digitized\_date | Date | Yes | Date of digitizing |
| geometry\_source | Text | Yes | Domain: digitized/interpreted/approximate |
| geom\_confidence | Text | Yes | High/Medium/Low/Needs verification |
| attribute\_confidence | Text | Yes | High/Medium/Low/Unknown |
| overall\_confidence | Text | Yes | High/Medium/Low/Needs verification |
| qaqc\_status | Text | Yes | Draft/Checked/Approved/Rejected |
| validation\_status | Text | Yes | Historical only/Field checked/Sampled/Lab confirmed/Not found/Not applicable |
| recommended\_followup | Text | Recommended | Field check/Rock chip/Soil grid/No action/Data gap |
| comment | Text | No | Free text |

## **12.2 Standard domain values**

| Field | Allowed values | Тайлбар |
| :---- | :---- | :---- |
| geom\_confidence | High; Medium; Low; Needs verification | Geometry/source position confidence |
| attribute\_confidence | High; Medium; Low; Unknown | Legend/label/attribute confidence |
| overall\_confidence | High; Medium; Low; Needs verification | Combined confidence |
| qaqc\_status | Draft; Checked; Approved; Rejected | QA/QC workflow status |
| validation\_status | Historical only; Field checked; Sampled; Lab confirmed; Not found; Not applicable | Field/lab verification status |
| geometry\_source | Digitized from georeferenced historical scan; Derived from map symbol; Interpreted from contour; Approximate from regional map | Source geometry origin |
| scale\_context | Local target-scale; Regional evidence; Metallogenic context; Report context | Map scale use limitation |
| use\_limit | Can support target ranking; Use with caution; Context only; Do not use until verified | Use status |

# **13\. Layer-specific schema**

## **13.x Layer: geology\_units\_polygons**

| Field name | Type | Required |
| :---- | :---- | :---- |
| unit\_id | Text | Yes |
| map\_symbol | Text | Yes |
| lithology | Text | Yes |
| age | Text | Recommended |
| stratigraphic\_unit | Text | Recommended |
| intrusive\_type | Text | Optional |
| alteration | Text | Optional |
| description | Text | Optional |
| source\_scale | Text | Yes |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: structures\_faults\_lines**

| Field name | Type | Required |
| :---- | :---- | :---- |
| struct\_id | Text | Yes |
| struct\_type | Text | Yes |
| certainty | Text | Yes |
| trend | Text | Recommended |
| relation\_to\_mineralization | Text | Recommended |
| relation\_to\_intrusion | Text | Recommended |
| relation\_to\_geochemistry | Text | Recommended |
| source\_symbol | Text | Recommended |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: mineral\_occurrences\_points**

| Field name | Type | Required |
| :---- | :---- | :---- |
| occ\_id | Text | Yes |
| map\_no | Text | Recommended |
| occ\_name | Text | Optional |
| commodity\_raw | Text | Yes |
| commodity\_1 | Text | Recommended |
| commodity\_2 | Text | Optional |
| commodity\_group | Text | Recommended |
| occurrence\_type | Text | Recommended |
| mineralization | Text | Optional |
| lithology | Text | Optional |
| structure\_relation | Text | Optional |
| target\_style | Text | Optional |
| recommended\_followup | Text | Recommended |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: heavy\_mineral\_anomaly\_polygons**

| Field name | Type | Required |
| :---- | :---- | :---- |
| anomaly\_id | Text | Yes |
| mineral\_indicator | Text | Yes |
| anomaly\_class | Text | Recommended |
| source\_material | Text | Recommended |
| drainage\_relation | Text | Recommended |
| interpreted\_source\_direction | Text | Optional |
| confidence | Text | Yes |
| recommended\_followup | Text | Recommended |
| comment | Text | No |

## **13.x Layer: stream\_sediment\_anomaly\_polygons**

| Field name | Type | Required |
| :---- | :---- | :---- |
| anomaly\_id | Text | Yes |
| element\_suite | Text | Yes |
| dominant\_element | Text | Recommended |
| associated\_elements | Text | Recommended |
| anomaly\_level | Text | Recommended |
| drainage\_basin | Text | Optional |
| possible\_source\_area | Text | Optional |
| confidence | Text | Yes |
| recommended\_followup | Text | Recommended |
| comment | Text | No |

## **13.x Layer: prospectivity\_target\_zones\_polygons**

| Field name | Type | Required |
| :---- | :---- | :---- |
| target\_id | Text | Yes |
| target\_name | Text | Recommended |
| prospect\_class | Text | Recommended |
| evidence\_basis | Text | Yes |
| dominant\_commodity | Text | Recommended |
| associated\_commodities | Text | Optional |
| geology\_control | Text | Recommended |
| structure\_control | Text | Recommended |
| geochem\_support | Text | Recommended |
| historical\_work\_support | Text | Recommended |
| priority | Text | Yes |
| data\_gap | Text | Optional |
| recommended\_next\_work | Text | Recommended |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: source\_material\_observation\_points**

| Field name | Type | Required |
| :---- | :---- | :---- |
| obs\_id | Text | Yes |
| route\_id | Text | Recommended |
| station\_no | Text | Recommended |
| observation\_type | Text | Yes |
| lithology | Text | Optional |
| mineralization | Text | Optional |
| sample\_reference | Text | Optional |
| trench\_pit\_reference | Text | Optional |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: source\_material\_route\_lines**

| Field name | Type | Required |
| :---- | :---- | :---- |
| route\_id | Text | Yes |
| route\_no | Text | Recommended |
| source\_year | Integer | Yes |
| observer | Text | Optional |
| route\_type | Text | Recommended |
| related\_observations | Text | Optional |
| confidence | Text | Yes |
| comment | Text | No |

## **13.x Layer: metallogenic\_zones\_polygons**

| Field name | Type | Required |
| :---- | :---- | :---- |
| zone\_id | Text | Yes |
| zone\_name | Text | Recommended |
| metallogenic\_unit | Text | Recommended |
| ore\_formation | Text | Recommended |
| commodity\_group | Text | Recommended |
| scale\_context | Text | Yes |
| relation\_to\_license | Text | Recommended |
| confidence | Text | Yes |
| use\_limit | Text | Yes |
| comment | Text | No |

# **14\. QGIS digitizing SOP**

135. GeoTIFF raster layer-ийг 40-60% opacity-тэй болгож, contrast/stretch-ийг уншигдах хэмжээнд тохируулна. Raster-г засварлахгүй.  
136. Legend dictionary sheet-ийг нээлттэй байлгаж, symbol бүрийг стандарт domain value-тай тулгана.  
137. Зөв layer сонгосон эсэхээ шалгаж Toggle Editing асаана.  
138. Feature digitize хийхдээ map symbol-ийн төв, line-ийн гол, polygon boundary-ийн зураг дээрх бодит хүрээг баримтална.  
139. Feature бүрт feature\_id болон source\_map\_id-г шууд өгнө. Feature ID давхцахгүй байх ёстой.  
140. original\_symbol, original\_label талбаруудыг map дээрх байдлаар бичнэ. Тодорхойгүй бол Unknown гэж бичээд data gap үүсгэнэ.  
141. Confidence-г геометр болон attribute тус бүрээр өгнө. Ерөнхий confidence нь хамгийн сул confidence-оос өндөр байж болохгүй.  
142. Editing дуусах бүрт Save Layer Edits хийнэ. Өдөр бүрийн төгсгөлд GeoPackage backup үүсгэнэ.  
143. QA/QC reviewer шалгасны дараа qaqc\_status \= Checked эсвэл Approved болгож өөрчилнө.

| Scale flag | Digitizing нарийвчлалын зарчим | Prohibited use |
| :---- | :---- | :---- |
| 1:50,000 | Local / target-scale evidence. Илрэл, маршрут, target polygon, geology contact-д ашиглаж болно. | Field/lab баталгаагүй байхад reserve/resource conclusion хийхгүй. |
| 1:100,000 | Ore district / mineral distribution context. Polygon boundary-г ойролцоогоор авна. | Local target boundary мэт ашиглахгүй. |
| 1:200,000 | Regional geology/geochemistry/drainage evidence. Anomaly/structure-г regional support гэж хэрэглэнэ. | Detailed trench/soil grid location-ийг дангаар тогтоохгүй. |
| 1:400,000-1:500,000 | Metallogenic context only. Deposit model, regional belt, report figure-д хэрэглэнэ. | License доторх local target geometry гэж ашиглахгүй. |

# **15\. Layer бүрийн нарийвчилсан SOP**

## **15.1 Geological unit polygons**

2013 1:50k болон 1987 1:200k geological map-аас lithology/stratigraphy нэгжүүдийг digitize хийнэ. Эхлээд major unit boundary, дараа нь intrusive body, alteration zone, dyke/vein separate layer болгон оруулна. Polygon closure, overlap, sliver шалгана. 1:50k layer-ийг geology\_units\_50k\_polygons, 1:200k layer-ийг geology\_units\_200k\_polygons гэж тусгаарлана.

## **15.2 Structures/faults/lineaments**

Fault, inferred fault, contact, lineament, shear, fold axis, vein trend зэрэг line feature-ийг structures\_faults\_lines layer-д оруулна. certainty \= Observed/Inferred/Interpreted; trend \= NE-SW/NW-SE/N-S/E-W гэх мэт. Илрэл, геохими, intrusive contact-тай хамаарал байвал relation\_to\_mineralization талбарт тэмдэглэнэ.

## **15.3 Mineral occurrence points**

Mineral occurrence symbol-ийн төвд point тавина. commodity\_raw-д map дээрх тэмдэглэгээг яг бичнэ; commodity\_1/2-д standardized element оруулна. Au-Cu, Cu, Mo, As, Zn зэрэг spelling-ийг lookup-тай тулгана. Map no, label тодорхойгүй бол attribute\_confidence \= Low/Unknown.

## **15.4 Heavy mineral layers**

Individual sample point харагдаж байвал sample point digitize хийнэ. Anomaly/indicator mineral contour харагдаж байвал polygon эсвэл line contour болгон оруулна. DEM/drainage layer-тай давхарлаж interpreted\_source\_direction-г зөвхөн тайлбарлагдсан үед бөглөнө.

## **15.5 Stream sediment polyelement layers**

Polyelement anomaly contour, drainage dispersion, sample point-уудыг тусад нь digitize хийнэ. element\_suite field-д Cu Pb Zn Ag As Bi W Sn Mo Mn Ba F зэрэг багцуудыг нэг мөр стандарт бичнэ. Anomaly level тодорхойгүй бол data gap үүсгэнэ.

## **15.6 Source materials layers**

Route lines, observation station, sample point, trench/pit/shaft/channel, section line-уудыг тусдаа layer-д оруулна. Field route planning болон QField validation-д хамгийн ашигтай тул route\_id, station\_no, sample\_reference талбарыг аль болох бүрэн бөглөнө.

## **15.7 Prospectivity target zones**

Prospectivity map дээрх Б-3 Толь хяр, Г-1 зэрэг target/prospect zone-уудыг polygon хэлбэрээр оруулна. evidence\_basis-д occurrence, geology, geochem, historical work support-ыг бичнэ. priority \= P1/P2/P3/P4 гэж өгч, regional map-аас авсан polygon бол use\_limit \= Context only гэж тэмдэглэнэ.

## **15.8 Metallogenic context**

1:400k-1:500k regional metallogenic map-аас belt, ore district, node, ore formation polygon/point-ийг context layer болгон оруулна. Энэ layer-ийг Phase 3 concept model болон Phase 4 scoring support-д ашиглах боловч local field target boundary биш.

# **16\. Excel register workbook**

Нэг QA/QC workbook гаргана: XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorization\_Register\_QAQC\_v02.xlsx. Workbook нь GIS layer бүрийн attribute export, GCP, QA/QC, confidence, data gap, handover checklist-ийг нэг дор хадгална.

| Sheet | Purpose |
| :---- | :---- |
| 00\_README | Workbook purpose, version, owner, CRS, definitions |
| 01\_Map\_Inventory | 21 scan map/report file metadata |
| 02\_Map\_Legend\_Linkage | Main map \+ legend \+ symbol dictionary status |
| 03\_Georeference\_GCP\_Table | GCP coordinates, source, residual |
| 04\_Georeference\_QAQC | Raster QA/QC results and raster confidence |
| 05\_Geology\_Units\_Register | Geology polygon export |
| 06\_Structures\_Register | Fault/structure/line export |
| 07\_Mineral\_Occurrences\_Register | Occurrence point export |
| 08\_HeavyMineral\_Register | Heavy mineral point/polygon export |
| 09\_StreamSediment\_Register | Stream sediment anomaly/sample export |
| 10\_Prospectivity\_Target\_Register | Prospect/target zone export |
| 11\_Source\_Materials\_Register | Route/obs/sample/trench export |
| 12\_Metallogenic\_Context\_Register | Regional metallogenic context export |
| 13\_Topology\_QAQC | Geometry/topology check log |
| 14\_Attribute\_QAQC | NULL/domain/ID/spelling check log |
| 15\_Confidence\_Ranking | Raster/vector confidence scoring |
| 16\_Data\_Gap\_Register | Gap type, impact, action, owner |
| 17\_Change\_Log | Date/operator/action/input/output/status |
| 18\_Handover\_Checklist | Final acceptance and phase handover status |
| 19\_Source\_Cross\_Reference | Cross-map evidence relationship table |
| 20\_Lookups\_Domains | Domain values for QGIS forms |

## **16.1 GCP table sheet schema**

| Column | Type | Description |
| :---- | :---- | :---- |
| gcp\_id | Text | Map\_ID \+ sequence, e.g. BK-SCAN-009-GCP-001 |
| source\_map\_id | Text | BK-SCAN-xxx |
| pixel\_x | Decimal | Georeferencer pixel x |
| pixel\_y | Decimal | Georeferencer pixel y |
| map\_x | Decimal | Target CRS Easting or longitude |
| map\_y | Decimal | Target CRS Northing or latitude |
| coord\_source | Text | Grid intersection / tick / boundary / topographic feature |
| residual\_x | Decimal | Residual x |
| residual\_y | Decimal | Residual y |
| residual\_total | Decimal | Total residual |
| used\_in\_transform | Text | Yes / No |
| review\_note | Text | Outlier or accepted note |

# **17\. QA/QC checklist**

| QA/QC group | Check item | Pass criteria |
| :---- | :---- | :---- |
| File inventory | Бүх raw file бүртгэгдсэн эсэх | 21 scanned map/report file Map Inventory-д орсон |
| File inventory | Main map ба legend холбоотой эсэх | Map-to-legend linkage register бөглөгдсөн |
| File inventory | Raw file өөрчлөгдөөгүй эсэх | Raw archive checksum / working copy path бүртгэгдсэн |
| CRS / georeference | CRS EPSG:32647 эсэх | Final GeoTIFF/vector layer EPSG:32647 |
| CRS / georeference | GCP хангалттай эсэх | Scale-specific GCP minimum хангагдсан |
| CRS / georeference | Residual error acceptable эсэх | GCP residual report хадгалагдсан, outlier note бичигдсэн |
| CRS / georeference | Overlay check | License boundary / basemap / DEM / other map-тэй logical overlap |
| Geometry | Invalid / empty geometry | QGIS Check validity OK |
| Geometry | Duplicate feature | Duplicate geometry / duplicate ID шалгасан |
| Geometry | Polygon overlap/sliver | Topology check хийсэн |
| Geometry | Point outside map extent/license/buffer | Flag or data gap created |
| Geometry | Line dangle/overshoot/undershoot | Structure/route/contact line-д reviewer check хийсэн |
| Attribute | Required NULL | Required fields бүрэн бөглөгдсөн |
| Attribute | ID uniqueness | feature\_id, occ\_id, anomaly\_id, target\_id unique |
| Attribute | Commodity/element spelling | Domain list-тэй нийцсэн |
| Attribute | Source traceability | source\_map\_id/source\_file/digitized\_from\_raster бүрэн |
| Interpretation | Scale-use flag | Regional map-derived feature local target мэт хэтрүүлээгүй |
| Interpretation | Historical vs confirmed | Historical map-derived data field/lab confirmed data-тай холигдоогүй |
| Handover | Workbook complete | Required sheets бөглөгдсөн |
| Handover | README and change log | Handover note complete |

# **18\. Confidence ranking logic**

Бүх raster болон vector output-д source quality, scan quality, legend clarity, GCP quality, georeference accuracy, map scale suitability, digitizing clarity, attribute completeness, cross-map consistency, field validation status гэсэн шалгуураар confidence үнэлгээ өгнө. Ерөнхий confidence нь хамгийн сул critical criterion-оос өндөр байж болохгүй.

| Criterion | Score 0 | Score 1 | Score 2 | Weight |
| :---- | :---- | :---- | :---- | :---- |
| Source quality | Unknown source | Known file but partial metadata | Known source \+ year \+ scale \+ map sheet | 10% |
| Scan quality | Unreadable/poor | Usable with unclear areas | Clear symbols/labels | 10% |
| Legend clarity | Missing | Partial/unclear | Clear linked legend | 10% |
| GCP quality | Insufficient/weak | Minimum met | Well-distributed preferred count | 15% |
| Georeference accuracy | High residual/conflict | Acceptable regional | Good overlay/grid | 15% |
| Map scale suitability | Too regional | Regional/context | Target-scale/local | 10% |
| Digitizing clarity | Approximate | Mostly clear | Clear symbol/boundary | 10% |
| Attribute completeness | Many NULL/unknown | Minor gaps | Complete required fields | 10% |
| Cross-map consistency | Conflict | Not checked/neutral | Supports other evidence | 5% |
| Validation status | Historical only | Field checked/sample pending | Sampled/lab confirmed | 5% |
| **Total score** | **Confidence class** | **Use status** |  |  |
| \>=80 | High | Target ranking-д ашиглаж болно; field validation шаардлагатай хэвээр |  |  |
| 60-79 | Medium | Overlay/interpretation-д болгоомжтой ашиглана |  |  |
| 40-59 | Low | Context evidence; decision-grade ашиглахгүй |  |  |
| \<40 or critical fail | Needs verification | Ашиглахаас өмнө дахин шалгах, field/lab/report validation шаардлагатай |  |  |

# **19\. Data gap register**

| Gap type | Impact | Required action | Owner / status field |
| :---- | :---- | :---- | :---- |
| Missing legend | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Unclear legend | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Poor scan quality | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Weak coordinate grid | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Insufficient GCP | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| High residual error | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| CRS uncertainty | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Symbol unreadable | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Attribute uncertain | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Feature duplicated across maps | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Conflicting feature location | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Scale too regional for local use | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Field validation required | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Lab confirmation required | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| Report text needed to interpret map | Confidence бууруулна / handover-д анхааруулга болно | Review, re-georeference, validate with field/lab/report, or use as context only | gap\_owner, due\_date, status |
| **Data gap register column** | **Description** |  |  |
| gap\_id | Unique ID, e.g. BUD-GAP-001 |  |  |
| source\_map\_id | Related BK-SCAN ID |  |  |
| feature\_id | Related feature if spatial |  |  |
| gap\_type | Controlled gap type |  |  |
| gap\_description | Detailed issue |  |  |
| impact\_on\_use | How it affects use |  |  |
| confidence\_impact | Decrease / hold / exclude |  |  |
| required\_action | What to do |  |  |
| responsible\_person | Owner |  |  |
| due\_date | Target date |  |  |
| status | Open / In progress / Closed / Deferred |  |  |
| closure\_note | How it was resolved |  |  |

# **20\. Cross-map integration**

Vector evidence-үүдийг нэг map-аас авсан дан мэдээлэл гэж үзэхгүй. Дараах overlay / consistency check-ийг хийж confidence-д нөлөөлүүлнэ.

| Overlay pair | Шалгах зүйл | Confidence impact | QGIS tool / method |
| :---- | :---- | :---- | :---- |
| 2013 mineral occurrence points vs 2013 geology | Occurrence нь favorable lithology/contact/structure дээр байгаа эсэх | Match бол confidence өснө; mismatch бол data gap | Join attributes by location, Select by location |
| 2013 prospectivity zones vs mineral occurrence points | Target zone дотор occurrence cluster байгаа эсэх | Давхцалтай бол P1/P2 ranking support | Count points in polygon |
| 2013 source materials routes/observations vs occurrence points | Historic observation/sample/trench point давхцах эсэх | Field validation planning-д шууд ашиглана | Distance to nearest hub / buffer |
| 1987 stream sediment anomalies vs geology | Anomaly drainage favorable lithology/structure-аас эхтэй эсэх | Drainage source confidence нэмэгдэнэ | Overlay \+ DEM drainage analysis |
| 1987 heavy mineral anomalies vs DEM/drainage/geology | Indicator mineral source direction logical эсэх | Orientation soil/stream sediment planning support | Drainage catchment overlay |
| 1987 mineral resources vs 2013 mineral occurrence | Historical occurrence continuity байгаа эсэх | Cross-source support нэмэгдэнэ | Spatial join \+ attribute compare |
| 2013 metallogenic scheme vs 2020/2021 regional metallogenic map | Ore formation / belt consistency | Deposit model support | Overlay and narrative register |
| All evidence vs license boundary and buffers | License дотор/гадна/буферийн байрлал | Field work priority болон use limit тогтооно | Clip, intersection, distance |
| **Cross-map consistency field** | **Description** |  |  |
| evidence\_id | Feature/evidence ID |  |  |
| related\_map\_1 | First map ID |  |  |
| related\_map\_2 | Second map ID |  |  |
| match\_type | Overlap / Near / Conflict / Supports / No relation |  |  |
| spatial\_relationship | Within / intersects / adjacent / upstream / downstream |  |  |
| geological\_relationship | Contact / same unit / structure controlled / no relation |  |  |
| confidence\_impact | Increase / Neutral / Decrease / Needs verification |  |  |
| required\_action | Field check / review legend / re-georef / report check |  |  |

# **21\. Handover package ба acceptance criteria**

| Deliverable | File / folder | Use | Acceptance criteria |
| :---- | :---- | :---- | :---- |
| Master QGIS Project | XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorization\_QGIS\_EPSG32647\_v02.qgz | Layer overlay, review, map production, QField package preparation | Opens without missing layers; relative paths OK |
| Master GeoPackage | XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorized\_MasterGIS\_EPSG32647\_v02.gpkg | All vector evidence layers in EPSG:32647 | All mandatory layers created or documented as N/A |
| Georeferenced GeoTIFF folder | 04\_Georeference\_Check/02\_Georeferenced\_Rasters | Base raster for audit and future redigitizing | Priority map GeoTIFF complete \+ QAQC |
| Excel QA/QC workbook | XV023222\_Buduunkhad\_HistoricalScannedMaps\_Vectorization\_Register\_QAQC\_v02.xlsx | Register, QA/QC, confidence, data gap, change log | Required sheets complete; no missing required fields |
| PDF index maps | Phase1\_Master\_GIS\_Index\_Maps.pdf | Review / reporting | License \+ evidence layers shown |
| README \+ Change log | README.txt, Change\_Log.xlsx | Audit trail and handover note | Version, CRS, source note, limitations documented |
| **Handover phase** | **Required layers** | **Decision use** |  |
| Phase 3 Geological / Metallogenic Synthesis | Geology, structures, metallogenic zones, occurrence context | Concept model, deposit style, regional context |  |
| Phase 4 Preliminary Prospect Ranking | Occurrence, target zones, geology, geochem anomalies, confidence layers | Evidence scoring, A/B/C/D ranking |  |
| Phase 6 Recon Mapping and pXRF | QField-ready observation/source materials/target points | Field validation and pXRF route planning |  |
| Phase 7 Rock Chip Sampling | Mineral occurrences, structures, target zones, source observations | Rock chip candidate locations |  |
| Phase 8/9 Soil / Stream Sediment Planning | Drainage, heavy mineral, stream sediment anomaly, geology/structure | Orientation survey and systematic grid planning |  |
| QField field validation package | Approved subset of points/targets/routes \+ forms | Mobile field verification |  |

# **22\. Final workflow diagram**

Raw Scanned Maps \+ Legends  
  \-\> Working Copy \+ File Inventory  
  \-\> Map-Legend Linkage Register  
  \-\> CRS / Georeference Status Audit  
  \-\> QGIS Georeferencing \+ GCP Table  
  \-\> Georeferenced GeoTIFF EPSG:32647  
  \-\> Georeference QA/QC \+ Raster Confidence Ranking  
  \-\> Vector Digitizing by Map Type  
  \-\> GeoPackage Layers \+ Source Traceability  
  \-\> Attribute Domain Validation  
  \-\> Topology / Geometry / Attribute QA/QC  
  \-\> Excel Registers \+ QA/QC Workbook  
  \-\> Cross-Map Evidence Integration  
  \-\> Confidence Ranking \+ Data Gap Register  
  \-\> Master GIS / QField / Prospect Ranking Handover

# **23\. Appendices**

## **Appendix A \- Feature ID naming standard**

| Layer | ID prefix | Example |
| :---- | :---- | :---- |
| geology\_units\_50k\_polygons | BUD-GEO50 | BUD-GEO50-0001 |
| geology\_units\_200k\_polygons | BUD-GEO200 | BUD-GEO200-0001 |
| structures\_faults\_lines | BUD-STR | BUD-STR-0001 |
| mineral\_occurrences\_points | BUD-MIN | BUD-MIN-0001 |
| heavy\_mineral\_anomaly\_polygons | BUD-HM-AN | BUD-HM-AN-0001 |
| stream\_sediment\_anomaly\_polygons | BUD-SS-AN | BUD-SS-AN-0001 |
| prospectivity\_target\_zones\_polygons | BUD-TGT | BUD-TGT-0001 |
| source\_material\_observation\_points | BUD-OBS | BUD-OBS-0001 |
| source\_material\_route\_lines | BUD-RTE | BUD-RTE-0001 |
| metallogenic\_zones\_polygons | BUD-MET | BUD-MET-0001 |
| data\_gap\_register\_spatial | BUD-GAP | BUD-GAP-0001 |

## **Appendix B \- QGIS Field Calculator expressions**

| Purpose | Expression | Тайлбар |
| :---- | :---- | :---- |
| UTM Easting | x($geometry) | Point layer-д x\_utm |
| UTM Northing | y($geometry) | Point layer-д y\_utm |
| Longitude WGS84 | x(transform($geometry, @layer\_crs, 'EPSG:4326')) | Point geometry longitude |
| Latitude WGS84 | y(transform($geometry, @layer\_crs, 'EPSG:4326')) | Point geometry latitude |
| Polygon area km2 | area($geometry) / 1000000 | Target/geology polygon талбай |
| Line length km | length($geometry) / 1000 | Route/fault/structure length |
| Feature ID example | concat('BUD-MIN-', lpad(@row\_number,4,'0')) | Draft ID үүсгэх |

## **Appendix C \- QField package preparation note**

* QField-д зөвхөн Approved эсвэл Checked status-тэй local target-scale layers оруулна.  
* Context-only 1:400k/1:500k metallogenic layer-ийг field package-д заавал оруулах шаардлагагүй; шаардлагатай бол non-editable reference layer болгоно.  
* Field editable layer-үүд: source\_material\_observation\_points, mineral\_occurrences\_points\_validation\_copy, prospectivity\_target\_zones\_polygons\_reference, source\_material\_route\_lines\_reference.  
* Form tab: Source / Geometry / Observation / Mineralization / Confidence / Photo / QAQC.  
* fid, system fields, geometry fields-ийг user form дээр hide хийнэ. Required fields-д constraint тавина.

## **Appendix D \- Чанарын хяналтын анхааруулга**

* Historical scanned map-derived vector data нь хүдэржилтийг батлах decision-grade evidence биш.  
* Field validation, rock chip sampling, pXRF screening, laboratory assay шаардлагатай.  
* Georeferenced scan map-ийн positional accuracy-г confidence flag-гүй ашиглаж болохгүй.  
* Regional scale map-аас гарсан polygon/line-г local target boundary мэт ашиглаж болохгүй.  
* Raster дээрх map symbol-ийг vector болгохдоо source\_file, source\_map\_id, original\_symbol, original\_label талбаруудыг заавал бөглөнө.  
* Raw scan file-г overwrite хийхгүй. Version update бүрт v02, v03 гэх мэтээр нэмэгдүүлнэ.

# **Critical QA/QC Notes**

* Raw data-г засварлахгүй; processing copy дээр ажиллана.  
* Final deliverables-ийн CRS нь EPSG:32647; native/raw CRS-г metadata-д хадгална.  
* .tfw, .aux.xml, .ovr, .rpc, .eph, .txt зэрэг sidecar файлуудыг parent raster/image-тэй хамт хадгална.  
* Scan map/georeferenced map-ийн positional accuracy-г residual болон confidence flag-тай хэрэглэнэ.  
* ASTER final binary mask, Sentinel alteration ratio, KOMPSAT visual lineament, drone interpretation нь хүдэржилтийн баталгаа биш.  
* pXRF нь lab assay-г орлохгүй; Au-ийн pXRF response-ийг decision-grade гэж үзэхгүй.  
* CMCS/MRPAM nearest deposit нь contextual evidence бөгөөд тухайн license дотор хүдэржилт байгаа эсэхийг шууд батлахгүй.  
* Final target confidence нь хээрийн шалгалт, дээжлэлт, лабораторийн assay, structural/geological evidence, шаардлагатай бол trench/geophysics/scout drilling-аар баталгаажна.

# **Methodology Limitation**

* Энэ баримт бичиг нь methodology / workflow guide бөгөөд бодит raster processing, vector digitizing, assay interpretation, target grade estimation хийгээгүй.  
* 78 raw input file-ийн агуулга, spatial correctness, coordinate accuracy, file integrity нь Phase 1 Data Audit-ээр баталгаажсаны дараа л analysis-ready гэж үзнэ.  
* Remote sensing index болон alteration proxy нь surface condition, vegetation, shadow, weathering, sensor limitations, CRS/pixel alignment-аас хамаарч буруу response өгөх боломжтой.  
* Historical map scale (1:500,000, 1:200,000, 1:50,000) нь target-scale field decision-д шууд хангалтгүй; field verification шаардлагатай.  
* Эцсийн follow-up болон scout drilling decision нь энэ document-ийн workflow-оос гадна permit, land access, HSE, budget, environmental and legal requirements-тай нийцэх ёстой.