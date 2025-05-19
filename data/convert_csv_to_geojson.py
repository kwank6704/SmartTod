import pandas as pd
import geojson

df = pd.read_csv("data/bts_station.csv")

# กรองแถวที่ไม่มีพิกัด
df = df.dropna(subset=["lat", "lng"])

# เติมค่าว่างให้ทุกคอลัมน์ที่อาจเป็น NaN
df["idstation"] = df["idstation"].fillna("")
df["name"] = df["name"].fillna("")
df["id_btsline"] = df["id_btsline"].fillna(0)
df["btsline"] = df["btsline"].fillna("")
df["dcode"] = df["dcode"].fillna("")
df["dname"] = df["dname"].fillna("")
df["station_co"] = df["station_co"].fillna("")

features = []
for _, row in df.iterrows():
    try:
        lat = float(row["lat"])
        lng = float(row["lng"])
        point = geojson.Point((lng, lat))

        properties = {
            "idstation": row["idstation"],
            "name": row["name"],
            "id_btsline": int(row["id_btsline"]),
            "btsline": row["btsline"],
            "dcode": str(row["dcode"]),
            "dname": row["dname"],
            "station_co": row["station_co"]
        }

        features.append(geojson.Feature(geometry=point, properties=properties))
    except Exception as e:
        print(f"❌ ข้ามสถานี: {row.get('name', 'unknown')} | Error: {e}")

feature_collection = geojson.FeatureCollection(features)

with open("data/bts_stations.geojson", "w", encoding="utf-8") as f:
    geojson.dump(feature_collection, f, ensure_ascii=False, indent=2)

print("✅ แปลงและบันทึก GeoJSON สำเร็จแล้ว")
