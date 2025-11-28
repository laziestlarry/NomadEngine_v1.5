# scripts/make_products_from_yaml.py
import os, yaml, csv, random
from pathlib import Path
from scripts.visual_gen import save_art
from scripts.mockup_frame import make_mockup
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
IMDIR = BASE/"shopify/images"
CSV_OUT = BASE/"shopify/products_real.csv"

def build():
    conf = yaml.safe_load((BASE/"catalog.yaml").read_text())
    vendor = conf.get("vendor","ProPulse Group")
    product_type = conf.get("product_type","Digital Art")
    tags = conf.get("default_tags",["zen","calm","printable","minimal","abstract"])
    sizes = conf.get("sizes", ["8x10 in","11x14 in","16x20 in"])

    # global visual defaults
    g = {
        "style": conf.get("style","PosterZen"),
        "palette": conf.get("palette","boho"),
        "long_edge_px": int(conf.get("long_edge_px", 5200)),
        "title": conf.get("title_fallback","Modern Harmony"),
        "subtitle": conf.get("subtitle_fallback","Abstract Boho Print")
    }

    rows = []
    for item in conf.get("products", []):
        slug   = item["slug"]
        title  = item.get("title_text", g["title"])
        subtitle = item.get("subtitle_text", g["subtitle"])
        style  = item.get("style", g["style"])
        palette= item.get("palette", g["palette"])
        prices = item.get("price", [9.90, 12.90, 14.90])
        seed   = int(item.get("seed", random.randint(100,999)))
        longpx = int(item.get("long_edge_px", g["long_edge_px"]))
        product_title = item["title"]  # Shopify product title
        body_html = item.get("body_html","<p>Premium printable wall art with studio-grade mockups.</p>")

        for idx, size in enumerate(sizes):
            art_name = f"{slug}_{size.replace(' ','').replace('in','')}.jpg"
            art_path = IMDIR/art_name

            save_art(str(art_path),
                     size_label=size, long_edge_px=longpx,
                     style=style, palette=palette,
                     title=title, subtitle=subtitle, seed=seed+idx)

            # mockup (hero)
            mock_name = f"{slug}_mockup_{idx+1}.jpg"
            make_mockup(str(art_path), str(IMDIR/mock_name))

            sku = f"LL-{slug.upper()}-{size.replace(' ','').replace('in','')}"
            price = prices[idx] if idx < len(prices) else prices[-1]

            # Primary = mockup, Shopify will still upload art file on this row.
            rows.append({
                "title": product_title,
                "body_html": body_html,
                "vendor": vendor,
                "product_type": product_type,
                "tags": ",".join(tags),
                "price": f"{price:.2f}",
                "sku": sku,
                "image_file": f"shopify/images/{mock_name}",
                "option1_name": "Size",
                "option1_value": size
            })
            # Extra image rows (flat art) — same SKU with extra image lines if your sync supports it.
            rows.append({
                "title": "", "body_html": "", "vendor":"", "product_type":"",
                "tags":"", "price":"", "sku": sku,
                "image_file": f"shopify/images/{art_name}",
                "option1_name":"", "option1_value":""
            })

    # Optional bundle hero
    b = conf.get("bundle", {})
    if b.get("enabled"):
        bundle_img = b.get("image","zen_bundle.jpg")
        imgs = list(IMDIR.glob("zen1_*.jpg"))[:1] + list(IMDIR.glob("zen2_*.jpg"))[:1] + list(IMDIR.glob("zen3_*.jpg"))[:1] + list(IMDIR.glob("zen4_*.jpg"))[:1]
        if imgs:
            W,H = 2600,1700
            canv = Image.new("RGB",(W,H),(246,246,246))
            step = (W-220)//2
            for i, p in enumerate(imgs[:4]):
                im = Image.open(p).convert("RGB").resize((step-60, int((step-60)*0.75)))
                cx = 110 + (i%2)*step
                cy = 120 + (i//2)*int(H/2-140)
                canv.paste(im, (cx, cy))
            canv.save(IMDIR/bundle_img, quality=95, subsampling=0)
        rows.append({
            "title": b.get("title"),
            "body_html": "<p>Bundle of four premium posters. Includes multiple printable sizes.</p>",
            "vendor": vendor,
            "product_type": "Digital Bundle",
            "tags": ",".join(tags+["bundle"]),
            "price": f"{b.get('price',39.0):.2f}",
            "sku": b.get("sku","LL-ZEN-BUNDLE-001"),
            "image_file": f"shopify/images/{bundle_img}",
            "option1_name": "Format",
            "option1_value": "All-in-one Pack"
        })

    fields = ["title","body_html","vendor","product_type","tags","price","sku","image_file","option1_name","option1_value"]
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    print("Generated:", CSV_OUT, f"({len(rows)} rows)")
    print("Images at:", IMDIR)

if __name__ == "__main__":
    build()