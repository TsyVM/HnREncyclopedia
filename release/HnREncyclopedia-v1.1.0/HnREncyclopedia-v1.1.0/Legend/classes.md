# Legend — Runtime Classes

**1055 RTTI-confirmed classes** (1,207 incl. base-only), **965 with verified vtable addresses**. ✅ from the executable's own RTTI. The full table with inheritance and vtables is `DonutsSDK/data/shar_dumps.csv` + `class_vtables.csv`; the family breakdown is C23.3. This is the namespace summary.

| Namespace / prefix | Classes |
|---|---:|
| `global` | 843 |
| `choreo` | 46 |
| `sim` | 39 |
| `ActionButton` | 36 |
| `GuiSFX` | 22 |
| `Scenegraph` | 14 |
| `Sound` | 12 |
| `Scrooby` | 11 |
| `CharacterAi` | 6 |
| `FeResourceManager` | 5 |
| `radmusic` | 5 |
| `poser` | 3 |
| `std` | 3 |
| `tCompositeDrawable` | 3 |
| `AnimatedIcon` | 1 |
| `LoadVehicleObjective` | 1 |
| `p3d` | 1 |
| `radLoadFileStream` | 1 |
| `radLoadManager` | 1 |
| `tExpressionGroupLoader` | 1 |
| `tLoadRequest` | 1 |

> For any class's bases and vtable, query `shar_dumps.csv`/`class_vtables.csv` or `shar::db::find_class()` (C23.6).
