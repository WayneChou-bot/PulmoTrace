# CXR-Seg — browser demo (static site)

Runs TorchXRayVision lung/heart segmentation **entirely in the browser** via ONNX Runtime Web.
The uploaded X-ray never leaves the device. **Non-diagnostic research/teaching demo.**

## Files
```
web/
├── index.html         single-page app (UI + inference logic)
├── vercel.json        headers (COOP/COEP for wasm threads) + caching
├── model/
│   └── pspnet_lunghearts_int8.onnx   (66 MB; 3-channel sigmoid: L lung, R lung, heart)
├── assets/failure_gallery.png
├── samples/           (add 2 public JSRT PNGs: sample1.png, sample2.png)  ← optional
├── MODEL_CARD.md · CLAIM_checklist.md · evaluation_report.md
```

## Test locally
A local **server** is required (not `file://`, because the model is fetched and wasm needs proper MIME):
```bash
cd web
python -m http.server 8000
# open http://localhost:8000
```
Upload a chest X-ray → **執行分割**. First run downloads the 66 MB model (then cached).
Note: locally you won't be cross-origin-isolated, so wasm runs single-threaded (slower). On Vercel the
headers in `vercel.json` enable multithreading → faster.

## Deploy to Vercel
1. Push the repo to GitHub. (The 66 MB `.onnx` is under GitHub's 100 MB limit but over 50 MB → GitHub shows a warning; fine. Or use Git LFS.)
2. On vercel.com → **Add New Project** → import the repo.
3. **Root Directory = `web`**, Framework Preset = **Other** (no build step). Deploy.
4. `vercel.json` sets COOP/COEP + cache headers automatically.

Public or private URL is your choice — public is fine (public data, nothing stored, clearly non-diagnostic).

## Add sample images (optional, nice UX)
Drop two public JSRT frontal CXRs into `web/samples/` named `sample1.png`, `sample2.png`
(the "範例" buttons load these). If absent, the buttons just show a load-error status — uploads still work.

## If INT8 fails to run in a browser
Some browsers/ORT builds may lack an int8 op. Fallback: use the **FP16** model (131 MB) hosted on a CDN /
Hugging Face model repo (GitHub can't hold >100 MB without LFS), and change one line in `index.html`:
```js
const MODEL_URL = "https://<your-hf-repo>/resolve/main/pspnet_lunghearts_fp16.onnx";
```
FP16 needs the WebGPU backend; set `executionProviders:['webgpu','wasm']` in `InferenceSession.create`.

## Credits / license
NIH ChestX-ray14 (images) · CheXmask v0.4 CC BY 4.0 (Gaggion et al. 2024) · JSRT+SCR (external gold).
See `CREDITS.md` in the repo root. **NOT a medical device. NOT for clinical use.**
