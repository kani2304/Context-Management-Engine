# Context Management Engine — Frontend

React 19 + TypeScript + Tailwind CSS v4 + Motion Primitives (`AnimatedBackground`, `TransitionPanel`) + Lucide.

```bash
cd frontend
npm install
cp .env.example .env     # leave VITE_API_BASE_URL empty for demo data
npm run dev              # http://localhost:5173
npm run typecheck
npm run build
```

- **Demo mode** (no `VITE_API_BASE_URL`): uses `src/api/adapters/mock.ts`. A "Demo data" badge is always visible; answers are excerpts, not model output. Create any account on the register page.
- **Live mode**: `VITE_API_BASE_URL=http://localhost:8000` uses `src/api/adapters/live.ts`. See `../FRONTEND_API.md`.
- Only frontend-safe values belong in `.env`. The Gemini key must stay on the backend.

```
src/
  api/        types.ts · client.ts · auth.ts · documents.ts · research.ts · adapters/{mock,live}.ts · mock/fixtures.ts
  state/      auth · documents (upload queue) · selection · theme · history
  pages/      Login · Register · Dashboard · Documents · DocumentDetail · Research
  features/   upload/ · documents/ · research/ (DocPicker, Composer, ResearchEntry, RetrievalPanel, SourceDrawer)
  components/ ui/ (Button, Field, Overlay, Tabs, AnimatedBackground, TransitionPanel, …) · layout/
```
